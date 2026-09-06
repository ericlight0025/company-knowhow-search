"""Markdown 文件掃描與基本 metadata 解析。"""

from __future__ import annotations

from pathlib import Path
import re

from .models import Document


_HEADING_RE = re.compile(r"^\s*#\s+(.+?)\s*$")


class MarkdownLoader:
    """從指定資料夾遞迴讀取 Markdown。"""

    def __init__(self, root_dir: Path):
        self.root_dir = root_dir

    def discover(self) -> list[Path]:
        return sorted(path for path in self.root_dir.rglob("*.md") if path.is_file())

    def load(self, path: Path, display_filepath: str | None = None) -> Document:
        content = path.read_text(encoding="utf-8-sig")
        title = self._extract_title(content, path)
        relative_path = display_filepath or path.relative_to(self.root_dir.parent).as_posix()
        return Document(
            filename=path.name,
            filepath=relative_path,
            title=title,
            content=content,
        )

    def load_all(self) -> list[Document]:
        return [self.load(path) for path in self.discover()]

    @staticmethod
    def _extract_title(content: str, path: Path) -> str:
        for line in content.splitlines():
            match = _HEADING_RE.match(line)
            if match:
                return match.group(1).strip()
        return path.stem.replace("_", " ").replace("-", " ").title()
