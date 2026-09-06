"""BM25 + vector 的 RRF hybrid ranking。"""

from __future__ import annotations

from dataclasses import replace
import json

from config import DATA_DIR, SearchConfig
from pathlib import Path
from .index_store import resolve_generation
from .text_utils import validate_query

from .embedding_provider import EmbeddingProvider, create_embedding_provider
from .fts_index import FTSIndex
from .models import Chunk, SearchResult
from .vector_index import VectorIndex


class HybridSearcher:
    """同時提供 keyword、vector、hybrid 三種模式。"""

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

    def keyword_search(self, query: str, top_k: int) -> list[SearchResult]:
        return self.fts_index.search(query, top_k)

    def vector_search(self, query: str, top_k: int) -> list[SearchResult]:
        return self.vector_index.search(query, self.provider, top_k, self.config.vector_min_similarity)

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
        # 一份文件可能切成多個 chunk；Hybrid 預設先保留每份文件最高分的 chunk，
        # 避免單一長文件佔滿 Top K，讓使用者看到更多可追查的來源。
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
        # 若文件種類少於 top_k，再用剩餘 chunk 補足結果數。
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

    def search(self, query: str, top_k: int, mode: str = "hybrid") -> list[SearchResult]:
        if mode == "keyword":
            return self.keyword_search(query, top_k)
        if mode == "vector":
            return self.vector_search(query, top_k)
        if mode == "hybrid":
            return self.hybrid_search(query, top_k)
        raise ValueError("mode 必須是 keyword、vector 或 hybrid")
