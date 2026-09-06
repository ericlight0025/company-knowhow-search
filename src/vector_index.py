"""NumPy 向量 index；完全本機、無 server、無 FAISS 依賴。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np

from .embedding_provider import EmbeddingProvider
from .models import Chunk, SearchResult


class VectorIndex:
    """以 normalized dot product 實作 cosine semantic search。"""

    def __init__(self, index_path: Path, chunks: list[Chunk], vectors: np.ndarray, provider_metadata: dict[str, Any]):
        self.index_path = index_path
        self.chunks = chunks
        self.vectors = np.asarray(vectors, dtype=np.float32)
        self.provider_metadata = provider_metadata

    @classmethod
    def build(
        cls,
        index_path: Path,
        chunks: list[Chunk],
        provider: EmbeddingProvider,
    ) -> "VectorIndex":
        vectors = provider.embed_documents(chunk.embedding_text for chunk in chunks)
        vectors = cls._normalize_rows(vectors)
        return cls(index_path, chunks, vectors, provider.metadata())

    @classmethod
    def load(
        cls,
        index_path: Path,
        chunks: list[Chunk],
        provider: EmbeddingProvider,
        provider_metadata: dict[str, Any] | None = None,
    ) -> "VectorIndex":
        if not index_path.exists():
            raise FileNotFoundError(f"找不到向量 index：{index_path}")
        with index_path.open("rb") as handle:
            vectors = np.load(handle)
        current_metadata = provider.metadata()
        saved_metadata = provider_metadata or {}
        saved_dimension = int(saved_metadata.get("dimension", vectors.shape[1] if vectors.ndim == 2 else 0))
        if vectors.ndim != 2 or vectors.shape[0] != len(chunks):
            raise ValueError("向量 index 與 metadata 的 chunk 數量不一致，請重新執行 index.py")
        if vectors.shape[1] != saved_dimension or vectors.shape[1] != int(current_metadata["dimension"]):
            raise ValueError("embedding dimension 不一致，請刪除 data 後重新執行 index.py")
        return cls(index_path, chunks, cls._normalize_rows(vectors), saved_metadata or current_metadata)

    def save(self) -> None:
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        with self.index_path.open("wb") as handle:
            np.save(handle, self.vectors)

    def search(self, query: str, provider: EmbeddingProvider, top_k: int = 20) -> list[SearchResult]:
        if top_k <= 0 or not self.chunks:
            return []
        query_vector = provider.embed_query(query)
        query_vector = self._normalize_rows(np.asarray(query_vector, dtype=np.float32).reshape(1, -1))[0]
        scores = self.vectors @ query_vector
        ordered = np.argsort(-scores)[: min(top_k, len(self.chunks))]
        results: list[SearchResult] = []
        for rank, index in enumerate(ordered, start=1):
            chunk = self.chunks[int(index)]
            cosine_score = float(scores[int(index)])
            # cosine [-1, 1] 映射到較直觀的 [0, 1]，只是顯示用；hybrid 不直接相加。
            display_score = max(0.0, min(1.0, (cosine_score + 1.0) / 2.0))
            results.append(
                SearchResult(
                    chunk=chunk,
                    score=display_score,
                    source="vector",
                    rank=rank,
                    cosine_score=cosine_score,
                    vector_rank=rank,
                )
            )
        return results

    @staticmethod
    def _normalize_rows(matrix: np.ndarray) -> np.ndarray:
        if matrix.size == 0:
            return matrix.astype(np.float32)
        norms = np.linalg.norm(matrix, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        return (matrix / norms).astype(np.float32)

