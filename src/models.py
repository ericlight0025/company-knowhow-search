"""搜尋流程使用的資料模型。"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class Document:
    """一份 Markdown 原始文件。"""

    filename: str
    filepath: str
    title: str
    content: str


@dataclass(frozen=True)
class Chunk:
    """可被全文與向量索引的 Markdown 區塊。"""

    chunk_id: str
    source_file: str
    filepath: str
    title: str
    heading: str
    chunk_index: int
    content: str

    @property
    def embedding_text(self) -> str:
        """Embedding 同時保留文件標題與 heading，避免只看段落正文。"""

        return f"{self.title}\n{self.heading}\n{self.content}"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "Chunk":
        return cls(
            chunk_id=str(value["chunk_id"]),
            source_file=str(value["source_file"]),
            filepath=str(value["filepath"]),
            title=str(value["title"]),
            heading=str(value["heading"]),
            chunk_index=int(value["chunk_index"]),
            content=str(value["content"]),
        )


@dataclass
class SearchResult:
    """單一搜尋結果；score 會依搜尋模式代表不同的 normalized 分數。"""

    chunk: Chunk
    score: float
    source: str
    rank: int = 0
    bm25_score: float | None = None
    cosine_score: float | None = None
    keyword_rank: int | None = None
    vector_rank: int | None = None

