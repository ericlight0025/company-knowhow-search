import tempfile
import unittest
from pathlib import Path

from src.fts_index import FTSIndex
from src.models import Chunk


class FtsSearchTest(unittest.TestCase):
    def test_fts5_finds_chinese_and_english_terms(self):
        with tempfile.TemporaryDirectory() as directory:
            index = FTSIndex(Path(directory) / "knowledge.db")
            chunks = [
                Chunk("a::chunk-0", "a.md", "knowhow/a.md", "A", "保價金", 0, "契變完成後保價金需要重新計算。"),
                Chunk("b::chunk-0", "b.md", "knowhow/b.md", "B", "Loan", 0, "POLICY_LOAN_AMT is used by the loan service."),
            ]
            index.rebuild(chunks)
            cash_results = index.search("保價金", top_k=5)
            loan_results = index.search("POLICY_LOAN_AMT", top_k=5)
            self.assertTrue(cash_results)
            self.assertEqual(cash_results[0].chunk.source_file, "a.md")
            self.assertTrue(loan_results)
            self.assertEqual(loan_results[0].chunk.source_file, "b.md")


if __name__ == "__main__":
    unittest.main()

