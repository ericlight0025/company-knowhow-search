"""Knowledge Map Search V2 的回歸測試。"""

import tempfile
import unittest
from pathlib import Path

from config import SearchConfig
from src.chunker import MarkdownChunker
from src.embedding_provider import HashingEmbeddingProvider
from src.fts_index import FTSIndex
from src.hybrid_search import HybridSearcher
from src.index_store import file_hash
from src.models import Chunk, Document
from src.vector_index import VectorIndex


class WholeCardIndexingTests(unittest.TestCase):
    def test_short_knowledge_map_is_one_chunk(self):
        document = Document(
            filename="card.md",
            filepath="knowhow/card.md",
            title="契變保價金",
            content=(
                "# 契變保價金\n\n"
                "## 用途\n定位契變後保價金沒有更新的問題。\n\n"
                "## 常見問法\n契變完成但保價金還是昨天的資料。\n\n"
                "## 原始資料位置\nU:/Company/SPEC/CV.docx\n"
            ),
            source_sha256="hash",
        )
        chunks = MarkdownChunker(
            target_chars=100,
            max_chars=1000,
            prefer_whole_document=True,
        ).chunk_document(document)
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0].filepath, "knowhow/card.md")
        self.assertEqual(chunks[0].content, document.content)
        self.assertEqual(chunks[0].source_sha256, "hash")

    def test_long_document_still_uses_normal_chunking(self):
        document = Document(
            filename="long.md",
            filepath="knowhow/long.md",
            title="Long",
            content="# Long\n\n## A\n" + ("A" * 120) + "\n\n## B\n" + ("B" * 120),
        )
        chunks = MarkdownChunker(
            target_chars=40,
            max_chars=80,
            prefer_whole_document=True,
        ).chunk_document(document)
        self.assertGreater(len(chunks), 1)
        self.assertEqual([chunk.chunk_index for chunk in chunks], list(range(len(chunks))))


class StaleIndexTests(unittest.TestCase):
    def test_modified_source_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "card.md"
            source.write_text("# Card\nold content\n", encoding="utf-8")
            payload = {
                "sources": [
                    {"file": str(source), "sha256": file_hash(source)},
                ]
            }
            HybridSearcher._validate_source_freshness(payload)

            source.write_text("# Card\nnew content\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "索引已過期"):
                HybridSearcher._validate_source_freshness(payload)

    def test_deleted_source_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "card.md"
            source.write_text("# Card\ncontent\n", encoding="utf-8")
            payload = {
                "sources": [
                    {"file": str(source), "sha256": file_hash(source)},
                ]
            }
            source.unlink()
            with self.assertRaisesRegex(ValueError, "已不存在"):
                HybridSearcher._validate_source_freshness(payload)


class SemanticAliasTests(unittest.TestCase):
    def test_rapid_does_not_match_api_concept(self):
        provider = HashingEmbeddingProvider(128)
        concepts = {name for name, _ in provider._matched_concepts("rapid deployment")}
        self.assertNotIn("api", concepts)

    def test_real_api_sql_and_aml_tokens_still_match(self):
        provider = HashingEmbeddingProvider(128)
        concepts = {
            name
            for name, _ in provider._matched_concepts(
                "API endpoint uses SQL for AML screening"
            )
        }
        self.assertIn("api", concepts)
        self.assertIn("database", concepts)
        self.assertIn("aml", concepts)


class AutoSearchTests(unittest.TestCase):
    def build_searcher(self) -> HybridSearcher:
        chunks = [
            Chunk(
                "cv::chunk-0",
                "cv.md",
                "knowhow/cv.md",
                "契變保價金",
                "契變保價金",
                0,
                "契變完成後保價金沒有更新時，先確認重算批次與 cash value 計算。",
            ),
            Chunk(
                "aml::chunk-0",
                "aml.md",
                "knowhow/aml.md",
                "AML",
                "AML",
                0,
                "AML screening batch 與可疑交易案件查核入口。",
            ),
        ]
        provider = HashingEmbeddingProvider(128)
        self.tempdir = tempfile.TemporaryDirectory()
        root = Path(self.tempdir.name)
        fts = FTSIndex(root / "knowledge.db")
        fts.rebuild(chunks)
        vector = VectorIndex.build(root / "vectors.index", chunks, provider)
        vector.save()
        config = SearchConfig(
            embedding_dimension=128,
            keyword_min_coverage=0.34,
            no_match_vector_similarity=0.90,
        )
        return HybridSearcher(fts, vector, provider, config)

    def tearDown(self):
        if hasattr(self, "tempdir"):
            self.tempdir.cleanup()

    def test_auto_finds_normal_knowledge_card(self):
        searcher = self.build_searcher()
        results = searcher.search("契變後保價金沒有更新", 3, "auto")
        self.assertTrue(results)
        self.assertEqual(results[0].chunk.filepath, "knowhow/cv.md")

    def test_auto_returns_no_match_when_evidence_is_insufficient(self):
        searcher = self.build_searcher()
        results = searcher.search("火星探測器如何校正軌道", 3, "auto")
        self.assertEqual(results, [])

    def test_legacy_search_modes_remain_available(self):
        searcher = self.build_searcher()
        for mode in ("keyword", "vector", "hybrid"):
            with self.subTest(mode=mode):
                self.assertTrue(searcher.search("AML screening", 2, mode))


if __name__ == "__main__":
    unittest.main()
