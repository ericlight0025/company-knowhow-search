"""可抽換的本機 embedding provider。

預設 provider 不下載大型模型，使用 deterministic hashing vector：

* 中英文詞元與中文 bigram
* snake_case／hyphenated 欄位名稱拆分
* config.py 的領域同義詞概念特徵

這足以驗證 POC 的「模糊描述找案例」主線；未來只要替換 provider，不必改動
chunk、SQLite FTS 或 hybrid ranking。
"""

from __future__ import annotations

from abc import ABC, abstractmethod
import hashlib
import json
import re
from typing import Iterable

import numpy as np

from config import SEMANTIC_GROUPS

from .text_utils import normalize_text, tokenize_text


class EmbeddingProvider(ABC):
    """Embedding provider 的最小介面。"""

    @abstractmethod
    def embed_documents(self, texts: Iterable[str]) -> np.ndarray:
        """回傳 shape=(n, dimension) 的向量。"""

    @abstractmethod
    def embed_query(self, text: str) -> np.ndarray:
        """回傳 shape=(dimension,) 的 query vector。"""

    @abstractmethod
    def metadata(self) -> dict[str, object]:
        """提供 index 驗證所需 metadata。"""


class HashingEmbeddingProvider(EmbeddingProvider):
    """無外部模型的 deterministic local vector provider。"""

    def __init__(self, dimension: int = 512):
        if dimension < 64:
            raise ValueError("dimension 至少需要 64")
        self.dimension = dimension

    def embed_documents(self, texts: Iterable[str]) -> np.ndarray:
        rows = [self._embed_one(text) for text in texts]
        if not rows:
            return np.empty((0, self.dimension), dtype=np.float32)
        return np.vstack(rows).astype(np.float32)

    def embed_query(self, text: str) -> np.ndarray:
        return self._embed_one(text)

    def metadata(self) -> dict[str, object]:
        return {
            "name": "hashing-local",
            "dimension": self.dimension,
            "semantic_groups": len(SEMANTIC_GROUPS),
            # 英文 alias matching 改為 boundary-aware，舊 vector 必須重建。
            "algorithm_version": 2,
            "synonyms_sha256": hashlib.sha256(json.dumps(
                SEMANTIC_GROUPS, ensure_ascii=False, sort_keys=True
            ).encode("utf-8")).hexdigest(),
        }

    def _embed_one(self, text: str) -> np.ndarray:
        vector = np.zeros(self.dimension, dtype=np.float32)
        normalized = normalize_text(text)
        tokens = tokenize_text(normalized)

        for token in tokens:
            self._add_feature(vector, f"token:{token}", 1.0)

        for left, right in zip(tokens, tokens[1:]):
            self._add_feature(vector, f"pair:{left}:{right}", 0.35)

        for concept, weight in self._matched_concepts(normalized):
            self._add_feature(vector, f"concept:{concept}", weight)

        for word in re.findall(r"[a-z0-9_/-]{3,}", normalized):
            compact = word.replace("_", "").replace("-", "")
            for index in range(max(0, len(compact) - 2)):
                self._add_feature(vector, f"char3:{compact[index:index + 3]}", 0.12)

        norm = float(np.linalg.norm(vector))
        if norm == 0:
            return vector
        return vector / norm

    def _matched_concepts(self, normalized: str) -> list[tuple[str, float]]:
        """中文可 substring；英文 alias 必須完整 token/boundary 命中。"""

        normalized = normalize_text(normalized)
        matches: list[tuple[str, float]] = []
        for concept, aliases in SEMANTIC_GROUPS.items():
            matched = False
            for alias in aliases:
                alias_normalized = alias.casefold()
                if alias_normalized.isascii():
                    pattern = rf"(?<![a-z0-9]){re.escape(alias_normalized)}(?![a-z0-9])"
                    alias_matches = re.search(pattern, normalized) is not None
                else:
                    alias_matches = alias_normalized in normalized
                if alias_matches:
                    matched = True
                    break
            if matched:
                matches.append((concept, 3.0))
        return matches

    def _add_feature(self, vector: np.ndarray, feature: str, weight: float) -> None:
        digest = hashlib.sha256(feature.encode("utf-8")).digest()
        first = int.from_bytes(digest[:8], "big") % self.dimension
        second = int.from_bytes(digest[8:16], "big") % self.dimension
        sign = 1.0 if digest[16] % 2 == 0 else -1.0
        vector[first] += weight * sign
        vector[second] += weight * 0.5


class SentenceTransformersEmbeddingProvider(EmbeddingProvider):
    """可選的未來 adapter；未安裝套件時不影響預設 POC。"""

    def __init__(self, model_name: str):
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError(
                "未安裝 sentence-transformers；目前 POC 請使用 hashing-local provider。"
            ) from exc
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.dimension = int(self.model.get_sentence_embedding_dimension())

    def embed_documents(self, texts: Iterable[str]) -> np.ndarray:
        return np.asarray(self.model.encode(list(texts), normalize_embeddings=True), dtype=np.float32)

    def embed_query(self, text: str) -> np.ndarray:
        return np.asarray(self.model.encode(text, normalize_embeddings=True), dtype=np.float32)

    def metadata(self) -> dict[str, object]:
        return {"name": "sentence-transformers", "model": self.model_name, "dimension": self.dimension}


def create_embedding_provider(dimension: int = 512) -> EmbeddingProvider:
    """集中建立預設 provider，日後可由設定切換實作。"""

    return HashingEmbeddingProvider(dimension=dimension)
