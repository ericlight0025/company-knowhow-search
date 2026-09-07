"""BM25 + vector 的 RRF hybrid ranking，以及 keyword-first Auto 搜尋。"""

from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path

from config import DATA_DIR, ROOT_DIR, SearchConfig
from .embedding_provider import EmbeddingProvider, create_embedding_provider
from .fts_index import FTSIndex
from .index_store import file_hash, resolve_generation
from .models import Chunk, SearchResult
from .text_utils import tokenize_text, validate_query
from .vector_index import VectorIndex


class HybridSearcher:
    """提供 keyword、vector、hybrid 與 keyword-first auto 四種搜尋模式。"""

    def __init__(
        self,
        fts_index: FTSIndex,
        vector_index: VectorIndex,
        provider: EmbeddingProvider,
        config: SearchConfig,
    ):
        self.fts_index = fts_index
        self.vector_index = vector_index
        self.provider = provider
        self.config = config
        self.config.validate()

    @classmethod
    def load(cls, config: SearchConfig | None = None, data_dir: Path = DATA_DIR) -> "HybridSearcher":
        config = config or SearchConfig()
        config.validate()
        generation = resolve_generation(data_dir)
        payload = json.loads((generation / "metadata.json").read_text(encoding="utf-8"))
        if payload.get("format_version") != 2 or payload.get("generation") != generation.name:
            raise ValueError("索引版本不一致，請重新建立索引")

        cls._validate_source_freshness(payload)

        chunks = [Chunk.from_dict(item) for item in payload.get("chunks", [])]
        provider = create_embedding_provider(config.embedding_dimension)
        vector_index = VectorIndex.load(
            generation / "vectors.index",
            chunks,
            provider,
            provider_metadata=payload.get("embedding_provider"),
        )
        fts = FTSIndex(generation / "knowledge.db")
        if fts.count() != len(chunks) or payload.get("chunk_count") != len(chunks):
            raise ValueError("索引筆數不一致，請重新建立索引")
        searcher = cls(fts, vector_index, provider, config)
        searcher.index_metadata = payload
        searcher.generation = generation
        return searcher

    @staticmethod
    def _validate_source_freshness(payload: dict[str, object]) -> None:
        """驗證被索引的 Markdown 來源仍存在且 SHA256 未改變。"""

        sources = payload.get("sources")
        if not isinstance(sources, list):
            raise ValueError("索引來源 metadata 格式錯誤，請重新建立索引")

        for source in sources:
            if not isinstance(source, dict):
                raise ValueError("索引來源 metadata 格式錯誤，請重新建立索引")
            source_name = str(source.get("file", ""))
            expected_sha256 = str(source.get("sha256", ""))
            if not source_name or not expected_sha256:
                raise ValueError("索引來源 metadata 不完整，請重新建立索引")

            source_path = Path(source_name)
            if not source_path.is_absolute():
                source_path = ROOT_DIR / source_path
            if not source_path.is_file():
                raise ValueError(f"索引來源已不存在：{source_name}；請重新建立索引")
            if file_hash(source_path) != expected_sha256:
                raise ValueError(f"索引已過期：{source_name} 已修改；請重新執行 index.py")

    @staticmethod
    def _keyword_coverage(query: str, result: SearchResult) -> float:
        """以英文 token 與中文 bigram 計算可解釋的詞面覆蓋率。"""

        query_tokens = set(tokenize_text(query, include_cjk_unigrams=False))
        if not query_tokens:
            return 0.0
        document_tokens = set(
            tokenize_text(result.chunk.embedding_text, include_cjk_unigrams=False)
        )
        return len(query_tokens & document_tokens) / len(query_tokens)

    def keyword_search(self, query: str, top_k: int) -> list[SearchResult]:
        return self.fts_index.search(query, top_k)

    def vector_search(self, query: str, top_k: int) -> list[SearchResult]:
        return self.vector_index.search(
            query,
            self.provider,
            top_k,
            self.config.vector_min_similarity,
        )

    def hybrid_search(self, query: str, top_k: int) -> list[SearchResult]:
        validate_query(query)
        if top_k <= 0:
            return []
        candidate_limit = max(top_k * 5, 20)
        keyword_results = self.keyword_search(query, candidate_limit) if self.config.keyword_weight else []
        vector_results = self.vector_search(query, candidate_limit) if self.config.vector_weight else []

        fused: dict[str, SearchResult] = {}
        for result in keyword_results:
            existing = fused.setdefault(result.chunk.chunk_id, replace(result, source="hybrid"))
            existing.keyword_rank = result.rank
            existing.bm25_score = result.bm25_score
        for result in vector_results:
            existing = fused.setdefault(result.chunk.chunk_id, replace(result, source="hybrid"))
            existing.vector_rank = result.rank
            existing.cosine_score = result.cosine_score

        for result in fused.values():
            keyword_part = (
                self.config.keyword_weight / (self.config.rrf_k + result.keyword_rank)
                if result.keyword_rank
                else 0.0
            )
            vector_part = (
                self.config.vector_weight / (self.config.rrf_k + result.vector_rank)
                if result.vector_rank
                else 0.0
            )
            result.score = keyword_part + vector_part

        ordered_all = sorted(fused.values(), key=lambda item: item.score, reverse=True)
        ordered: list[SearchResult] = []
        file_counts: dict[str, int] = {}
        for result in ordered_all:
            filepath = result.chunk.filepath
            if file_counts.get(filepath, 0) >= self.config.max_chunks_per_file:
                continue
            ordered.append(result)
            file_counts[filepath] = file_counts.get(filepath, 0) + 1
            if len(ordered) >= top_k:
                break
        if len(ordered) < top_k:
            selected_ids = {item.chunk.chunk_id for item in ordered}
            ordered.extend(item for item in ordered_all if item.chunk.chunk_id not in selected_ids)
            ordered = ordered[:top_k]

        max_score = ordered[0].score if ordered else 1.0
        normalized: list[SearchResult] = []
        for rank, result in enumerate(ordered, start=1):
            result.score = result.score / max_score if max_score else 0.0
            result.rank = rank
            normalized.append(result)
        return normalized

    def auto_search(self, query: str, top_k: int) -> list[SearchResult]:
        """Keyword 優先；證據不足才使用 Hybrid，仍不足則回空結果。"""

        validate_query(query)
        if top_k <= 0:
            return []

        candidate_limit = max(top_k * 5, 20)
        keyword_results = self.keyword_search(query, candidate_limit)
        accepted_keyword = [
            result
            for result in keyword_results
            if self._keyword_coverage(query, result) >= self.config.keyword_min_coverage
        ]
        if accepted_keyword:
            return accepted_keyword[:top_k]

        fallback = self.hybrid_search(query, candidate_limit)
        accepted_fallback = [
            result
            for result in fallback
            if result.cosine_score is not None
            and result.cosine_score >= self.config.no_match_vector_similarity
        ]
        return accepted_fallback[:top_k]

    def search(self, query: str, top_k: int, mode: str = "auto") -> list[SearchResult]:
        if mode == "auto":
            return self.auto_search(query, top_k)
        if mode == "keyword":
            return self.keyword_search(query, top_k)
        if mode == "vector":
            return self.vector_search(query, top_k)
        if mode == "hybrid":
            return self.hybrid_search(query, top_k)
        raise ValueError("mode 必須是 auto、keyword、vector 或 hybrid")
