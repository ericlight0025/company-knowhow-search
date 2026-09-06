"""內容完整性、版本發布與錯誤輸入的回歸測試。"""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
import index
import menu
from config import SearchConfig
from src.chunker import MarkdownChunker
from src.embedding_provider import HashingEmbeddingProvider
from src.evaluation import first_relevant_rank, rank_metrics_for, unique_documents
from src.fts_index import FTSIndex
from src.hybrid_search import HybridSearcher
from src.index_config import load_index_config
from src.index_store import resolve_generation
from src.markdown_loader import MarkdownLoader
from src.models import Chunk, Document, SearchResult
from src.vector_index import VectorIndex


class ContentTests(unittest.TestCase):
    def test_long_sentence_preserves_every_character(self):
        text = "Short. " + "Z" * 60 + "\n尾段。\n"
        parts = MarkdownChunker(10, 20)._split_if_needed(text)
        self.assertEqual("".join(parts), text)
        self.assertTrue(all(len(part) <= 20 for part in parts))

    def test_fences_and_line_ranges(self):
        for fence in ("```", "~~~~"):
            with self.subTest(fence=fence):
                text = f"# Title\n{fence}python\n# comment\n\nprint(1)\n{fence}\n## Next\n內容\n"
                chunks = MarkdownChunker(100, 200).chunk_document(Document("a.md", "a.md", "Title", text, "hash"))
                self.assertEqual([c.heading for c in chunks], ["Title", "Next"])
                self.assertIn("# comment", chunks[0].content)
                self.assertEqual((chunks[0].start_line, chunks[0].end_line), (2, 6))
                self.assertEqual((chunks[1].start_line, chunks[1].end_line), (8, 8))
                self.assertEqual(chunks[0].source_sha256, "hash")

    def test_long_line_ranges_match_original(self):
        text = "# T\n" + "Z" * 60 + "\nNext line\n"
        chunks = MarkdownChunker(10, 20).chunk_document(Document("a", "a", "T", text))
        self.assertEqual("".join(c.content for c in chunks), text.split("\n", 1)[1])
        for chunk in chunks:
            excerpt = "".join(text.splitlines(keepends=True)[chunk.start_line-1:chunk.end_line])
            self.assertIn(chunk.content, excerpt)

    def test_loader_ignores_code_title_and_hashes_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "a.md"
            path.write_text("```\n# fake\n```\n# Real\n", encoding="utf-8")
            loader = MarkdownLoader(path.parent)
            before = loader.load(path)
            self.assertEqual(before.title, "Real")
            path.write_text("# Updated\n", encoding="utf-8")
            self.assertNotEqual(before.source_sha256, loader.load(path).source_sha256)


class ConfigTests(unittest.TestCase):
    def parse(self, raw):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.yaml"
            path.write_text(raw, encoding="utf-8")
            return load_index_config(path)

    def test_strict_yaml(self):
        for raw in ('sources: [{path: knowhow, recursive: "false"}]',
                    'sources: []\nfiles: []', 'sources: [{path: ""}]',
                    'sources: [{path: knowhow, include: []}]', 'sources: [',
                    'soruces: [knowhow]', 'sources: [{path: knowhow, include: ["../*.md"]}]'):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                self.parse(raw)
        result = self.parse('sources: [{path: knowhow, recursive: false}]')
        self.assertFalse(result.sources[0].recursive)

    def test_missing_config_does_not_fall_back(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(FileNotFoundError):
                load_index_config(Path(directory) / "missing.yaml")


class SnapshotTests(unittest.TestCase):
    def test_failed_rebuild_preserves_published_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "a.md"
            source.write_text("# Cash\n保價金需要重新計算\n", encoding="utf-8")
            data = root / "data"
            with patch.object(index, "DATA_DIR", data), contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(index.main(["--file", str(source)]), 0)
                old = resolve_generation(data)
                loaded = HybridSearcher.load(data_dir=data)
                source.write_text("# New\n契變後重算\n", encoding="utf-8")
                with patch.object(index.VectorIndex, "save", side_effect=OSError("磁碟失敗")):
                    self.assertEqual(index.main(["--file", str(source)]), 1)
                self.assertEqual(resolve_generation(data), old)
                self.assertTrue(HybridSearcher.load(data_dir=data).search("保價金", 1))
                with patch("src.index_store.os.replace", side_effect=PermissionError("切換失敗")):
                    self.assertEqual(index.main(["--file", str(source)]), 1)
                self.assertEqual(resolve_generation(data), old)
                self.assertEqual(index.main(["--file", str(source)]), 0)
                self.assertNotEqual(resolve_generation(data), old)
                # 已載入的搜尋物件仍使用舊快照，不會混入新版。
                self.assertIn("保價金", loaded.search("保價金", 1)[0].chunk.content)
                self.assertTrue(old.exists())
                current = resolve_generation(data)
                (current / "vectors.index").write_bytes(b"broken")
                with self.assertRaises(ValueError):
                    HybridSearcher.load(data_dir=data)

    def test_provider_change_same_dimension_rejected(self):
        provider = HashingEmbeddingProvider(128)
        chunks = [Chunk("a::chunk-0", "a", "a", "A", "A", 0, "cash value")]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "vectors.index"
            vector = VectorIndex.build(path, chunks, provider)
            vector.save()
            changed = dict(provider.metadata(), synonyms_sha256="changed")
            with self.assertRaises(ValueError):
                VectorIndex.load(path, chunks, provider, changed)


class QueryTests(unittest.TestCase):
    def test_invalid_query_and_zero_vector(self):
        provider = HashingEmbeddingProvider(128)
        chunks = [Chunk("a::chunk-0", "a", "a", "A", "A", 0, "cash value")]
        with tempfile.TemporaryDirectory() as directory:
            vector = VectorIndex.build(Path(directory) / "vectors.index", chunks, provider)
            fts = FTSIndex(Path(directory) / "knowledge.db")
            fts.rebuild(chunks)
            searcher = HybridSearcher(fts, vector, provider, SearchConfig(embedding_dimension=128))
            for mode in ("keyword", "vector", "hybrid"):
                for query in ("", "   ", "!!!"):
                    with self.subTest(mode=mode, query=query), self.assertRaises(ValueError):
                        searcher.search(query, 5, mode)
            with patch.object(provider, "embed_query", return_value=np.zeros(128)):
                self.assertEqual(vector.search("cash", provider), [])
            self.assertEqual(vector.search("cash", provider, min_similarity=1.0), [])

    def test_fts_line_metadata_and_title_weight(self):
        with tempfile.TemporaryDirectory() as directory:
            fts = FTSIndex(Path(directory) / "knowledge.db")
            chunks = [Chunk("a::chunk-0", "a", "a", "needle", "other", 0, "other", 2, 3, "hash"),
                      Chunk("b::chunk-0", "b", "b", "other", "other", 0, "needle", 4, 5, "hash2")]
            fts.rebuild(chunks)
            results = fts.search("needle")
            self.assertEqual(results[0].chunk.filepath, "a")
            self.assertEqual((results[0].chunk.start_line, results[0].chunk.end_line), (2, 3))
            self.assertEqual(results[0].chunk.source_sha256, "hash")


class EvaluationTests(unittest.TestCase):
    def test_misses_count_in_metrics(self):
        metric = rank_metrics_for([1, None])
        self.assertEqual(metric["mrr"], .5)
        self.assertEqual(metric["hit_at_5"], .5)

    def test_same_filename_is_not_same_document(self):
        a = SearchResult(Chunk("a", "same.md", "a/same.md", "", "", 0, ""), 1, "keyword")
        b = SearchResult(Chunk("b", "same.md", "b/same.md", "", "", 0, ""), 1, "keyword")
        self.assertEqual(len(unique_documents([a, a, b], 5)), 2)
        self.assertEqual(first_relevant_rank([a, b], ("b/same.md",)), 2)


class MenuRecoveryTests(unittest.TestCase):
    def test_submenu_interrupt_and_io_error_return_to_menu(self):
        for error in (KeyboardInterrupt(), PermissionError("來源無權限"), ValueError("YAML 錯誤")):
            with patch("builtins.input", side_effect=["3", "0"]), patch.object(menu, "_show_source_config", side_effect=error), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(menu.run_menu(), 0)
