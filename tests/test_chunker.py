import unittest

from src.chunker import MarkdownChunker
from src.models import Document


class ChunkerTest(unittest.TestCase):
    def test_chunk_keeps_heading_and_source_metadata(self):
        document = Document(
            filename="sample.md",
            filepath="knowhow/sample.md",
            title="Sample",
            content=(
                "# Sample\n\n"
                "## First section\n\n"
                "這是一段中文內容，描述契約變更與批次處理。\n\n"
                "## Second section\n\n"
                "This section contains the cash value recalculation procedure."
            ),
        )
        chunks = MarkdownChunker(target_chars=40, max_chars=100).chunk_document(document)
        self.assertGreaterEqual(len(chunks), 2)
        self.assertEqual(chunks[0].source_file, "sample.md")
        self.assertEqual(chunks[0].filepath, "knowhow/sample.md")
        self.assertEqual(chunks[0].heading, "First section")
        self.assertEqual([chunk.chunk_index for chunk in chunks], list(range(len(chunks))))
        self.assertTrue(all(chunk.content.strip() for chunk in chunks))


if __name__ == "__main__":
    unittest.main()

