import tempfile
import unittest
from pathlib import Path

from config import SearchConfig
from src.embedding_provider import HashingEmbeddingProvider
from src.fts_index import FTSIndex
from src.hybrid_search import HybridSearcher
from src.models import Chunk
from src.vector_index import VectorIndex


class HybridSearchTest(unittest.TestCase):
    def test_rrf_combines_keyword_and_vector_results(self):
        chunks = [
            Chunk(
                "incident::chunk-0",
                "incident.md",
                "knowhow/incident.md",
                "Incident",
                "Stale value",
                0,
                "契約變更完成後 cash value remains old because batch recalculation was delayed",
            ),
            Chunk(
                "generic::chunk-0",
                "generic.md",
                "knowhow/generic.md",
                "Generic",
                "Support",
                0,
                "一般客服查詢與登入問題處理方式",
            ),
        ]
        provider = HashingEmbeddingProvider(dimension=128)
        with tempfile.TemporaryDirectory() as directory:
            fts = FTSIndex(Path(directory) / "knowledge.db")
            fts.rebuild(chunks)
            vector = VectorIndex.build(Path(directory) / "vectors.index", chunks, provider)
            vector.save()
            searcher = HybridSearcher(fts, vector, provider, SearchConfig(embedding_dimension=128))
            results = searcher.hybrid_search("契變後保價金沒有更新，可能是重算批次延遲", top_k=2)
        self.assertEqual(results[0].chunk.source_file, "incident.md")
        self.assertEqual(results[0].source, "hybrid")
        self.assertIsNotNone(results[0].vector_rank)


if __name__ == "__main__":
    unittest.main()

