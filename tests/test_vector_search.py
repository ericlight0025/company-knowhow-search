import tempfile
import unittest
from pathlib import Path

from src.embedding_provider import HashingEmbeddingProvider
from src.models import Chunk
from src.vector_index import VectorIndex


class VectorSearchTest(unittest.TestCase):
    def test_vector_search_returns_semantically_related_chunk(self):
        chunks = [
            Chunk("cash::chunk-0", "cash.md", "knowhow/cash.md", "Cash Value", "Recalculation", 0, "cash value recalculation after contract adjustment"),
            Chunk("loan::chunk-0", "loan.md", "knowhow/loan.md", "Policy Loan", "Amount", 0, "policy loan amount and repayment"),
        ]
        provider = HashingEmbeddingProvider(dimension=128)
        with tempfile.TemporaryDirectory() as directory:
            index = VectorIndex.build(Path(directory) / "vectors.index", chunks, provider)
            index.save()
            results = index.search("contract change cash value recompute", provider, top_k=2, min_similarity=-1)
        self.assertEqual(results[0].chunk.source_file, "cash.md")
        self.assertGreaterEqual(results[0].cosine_score or 0.0, results[1].cosine_score or 0.0)


if __name__ == "__main__":
    unittest.main()
