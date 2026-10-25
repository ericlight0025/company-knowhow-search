"""2026-10-26 review 修正的回歸測試。"""

import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import evaluate
import menu
from config import ROOT_DIR
from src.markdown_loader import MarkdownLoader


class SearchOutputEncodingTests(unittest.TestCase):
    def test_piped_json_is_utf8_without_python_utf8_mode(self):
        env = {key: value for key, value in os.environ.items()
               if key not in {"PYTHONUTF8", "PYTHONIOENCODING"}}
        query = "外部檔案失敗後要找哪份重送 SOP"
        completed = subprocess.run(
            [sys.executable, "-X", "utf8=0", "search.py", query, "--top", "1", "--json"],
            cwd=ROOT_DIR,
            env=env,
            capture_output=True,
            check=True,
        )
        payload = json.loads(completed.stdout.decode("utf-8"))
        self.assertEqual(payload["query"], query)


class MenuConfigTests(unittest.TestCase):
    def test_rebuild_uses_local_config_when_present(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "index_config.local.yaml").write_text("sources: []\n", encoding="utf-8")
            with patch.object(menu, "ROOT_DIR", root), \
                    patch.object(menu, "index_main", return_value=0) as index_main, \
                    patch("builtins.input", return_value="y"), \
                    patch.object(menu, "_pause"), \
                    contextlib.redirect_stdout(io.StringIO()):
                menu._rebuild_flow()
            index_main.assert_called_once_with(
                ["--config", str(root / "index_config.local.yaml")]
            )

    def test_default_config_without_local_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with patch.object(menu, "ROOT_DIR", root):
                self.assertEqual(menu.index_config_path(), root / "index_config.yaml")


class LoaderEncodingTests(unittest.TestCase):
    def test_non_utf8_card_error_names_the_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "big5_card.md"
            path.write_bytes("# 批次值日生\n內容\n".encode("cp950"))
            with self.assertRaisesRegex(ValueError, "big5_card.md.*UTF-8"):
                MarkdownLoader(Path(directory)).load(path)


class EvaluateGuardTests(unittest.TestCase):
    def test_external_sources_are_not_written_to_docs(self):
        searcher = type("Searcher", (), {})()
        searcher.index_metadata = {
            "sources": [{"file": "U:/Company/card.md", "sha256": "x"}],
        }
        with patch.object(evaluate.HybridSearcher, "load", return_value=searcher), \
                patch.object(evaluate, "generate_report") as generate_report, \
                contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(evaluate.main(), 1)
        generate_report.assert_not_called()


if __name__ == "__main__":
    unittest.main()
