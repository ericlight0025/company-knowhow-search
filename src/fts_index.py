"""SQLite FTS5 index 與 BM25 搜尋。"""

from __future__ import annotations

from pathlib import Path
import sqlite3

from .models import Chunk, SearchResult
from .text_utils import build_fts_query, build_fts_search_text, validate_query


class FTSIndex:
    """使用單一 SQLite 檔案儲存可重建的 FTS5 index。"""

    # 對應 chunk_id、filename、filepath、title、heading、content、search_text。
    _BM25_WEIGHTS = (0.0, 2.0, 1.0, 4.0, 4.0, 1.0, 2.0, 0.0, 0.0, 0.0)

    def __init__(self, db_path: Path):
        self.db_path = db_path

    def rebuild(self, chunks: list[Chunk]) -> None:
        """完整重建，不做 incremental indexing。"""

        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.db_path)
        try:
            connection.execute("DROP TABLE IF EXISTS chunks_fts")
            connection.execute(
                """
                CREATE VIRTUAL TABLE chunks_fts USING fts5(
                    chunk_id UNINDEXED,
                    filename,
                    filepath,
                    title,
                    heading,
                    content,
                    search_text,
                    start_line UNINDEXED,
                    end_line UNINDEXED,
                    source_sha256 UNINDEXED,
                    tokenize = 'unicode61 remove_diacritics 0'
                )
                """
            )
            connection.executemany(
                """
                INSERT INTO chunks_fts
                    (chunk_id, filename, filepath, title, heading, content, search_text,
                     start_line, end_line, source_sha256)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        chunk.chunk_id,
                        chunk.source_file,
                        chunk.filepath,
                        chunk.title,
                        chunk.heading,
                        chunk.content,
                        build_fts_search_text(chunk.embedding_text),
                        chunk.start_line,
                        chunk.end_line,
                        chunk.source_sha256,
                    )
                    for chunk in chunks
                ],
            )
            connection.commit()
        finally:
            connection.close()

    def search(self, query: str, top_k: int = 20) -> list[SearchResult]:
        """以 BM25 排序，並把 rank 轉成 0 到 1 的相對分數。"""

        if top_k <= 0:
            return []
        validate_query(query)
        match_query = build_fts_query(query)
        weight_sql = ", ".join(str(weight) for weight in self._BM25_WEIGHTS)
        sql = f"""
            SELECT chunk_id, filename, filepath, title, heading, content,
                   bm25(chunks_fts, {weight_sql}) AS bm25_score,
                   start_line, end_line, source_sha256
            FROM chunks_fts
            WHERE chunks_fts MATCH ?
            ORDER BY bm25_score ASC
            LIMIT ?
        """
        connection = None
        cursor = None
        try:
            connection = sqlite3.connect(self.db_path.resolve().as_uri() + "?mode=ro", uri=True)
            cursor = connection.cursor()
            cursor.execute(sql, (match_query, top_k))
            rows = cursor.fetchall()
        except sqlite3.OperationalError as exc:
            raise RuntimeError(f"SQLite FTS5 查詢失敗：{exc}") from exc
        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close()

        results: list[SearchResult] = []
        for rank, row in enumerate(rows, start=1):
            chunk_id = str(row[0])
            chunk = Chunk(
                chunk_id=chunk_id,
                source_file=str(row[1]),
                filepath=str(row[2]),
                title=str(row[3]),
                heading=str(row[4]),
                chunk_index=self._chunk_index_from_id(chunk_id),
                content=str(row[5]),
                start_line=int(row[7]),
                end_line=int(row[8]),
                source_sha256=str(row[9]),
            )
            results.append(
                SearchResult(
                    chunk=chunk,
                    score=1.0 / rank,
                    source="keyword",
                    rank=rank,
                    bm25_score=float(row[6]),
                    keyword_rank=rank,
                )
            )
        return results

    def count(self) -> int:
        if not self.db_path.exists():
            return 0
        connection = sqlite3.connect(self.db_path)
        try:
            row = connection.execute("SELECT count(*) FROM chunks_fts").fetchone()
        finally:
            connection.close()
        return int(row[0]) if row else 0

    @staticmethod
    def _chunk_index_from_id(chunk_id: str) -> int:
        try:
            return int(chunk_id.rsplit("chunk-", 1)[1])
        except (IndexError, ValueError):
            return 0
