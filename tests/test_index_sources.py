import tempfile
import unittest
from pathlib import Path

from index import collect_markdown_files
from src.index_config import SourceSpec


class IndexSourceSelectionTest(unittest.TestCase):
    """驗證 YAML 對應的資料匣、遞迴與排除規則。"""

    def test_source_spec_filters_recursive_markdown_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "top.md").write_text("# top", encoding="utf-8")
            (root / "nested").mkdir()
            (root / "nested" / "keep.md").write_text("# keep", encoding="utf-8")
            (root / "nested" / "notes.txt").write_text("notes", encoding="utf-8")
            (root / "archive").mkdir()
            (root / "archive" / "old.md").write_text("# old", encoding="utf-8")

            paths = collect_markdown_files(
                source_specs=(
                    SourceSpec(
                        path=root,
                        recursive=True,
                        include=("*.md",),
                        exclude=("archive/**",),
                    ),
                ),
            )

            self.assertEqual(
                [path.name for path in paths],
                ["keep.md", "top.md"],
            )

    def test_exact_files_can_be_used_without_a_default_source(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            selected = root / "selected.md"
            ignored = root / "ignored.md"
            selected.write_text("# selected", encoding="utf-8")
            ignored.write_text("# ignored", encoding="utf-8")

            paths = collect_markdown_files(
                files=[selected],
                source_specs=(),
            )

            self.assertEqual(paths, [selected.resolve()])


if __name__ == "__main__":
    unittest.main()
