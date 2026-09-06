"""保留來源行號的 Markdown 分段；不將程式碼註解當成章節。"""
from __future__ import annotations

import re
from .models import Chunk, Document

HEADING = re.compile(r"^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")


class MarkdownChunker:
    """以字元預算切割，來源行號指向索引當時的原文。"""

    def __init__(self, target_chars: int = 1400, max_chars: int = 2600):
        if target_chars <= 0 or max_chars < target_chars:
            raise ValueError("target_chars 與 max_chars 設定不合理")
        self.target_chars, self.max_chars = target_chars, max_chars

    def _split_if_needed(self, text: str) -> list[str]:
        """優先在換行或句尾切開；拼接後必須等於輸入原文。"""
        parts = []
        while len(text) > self.max_chars:
            window = text[:self.max_chars]
            boundaries = list(re.finditer(r"\n|[。！？!?；;.]\s+", window))
            end = boundaries[-1].end() if boundaries else self.max_chars
            if end < self.target_chars:
                end = self.max_chars
            parts.append(text[:end])
            text = text[end:]
        if text:
            parts.append(text)
        return parts

    def chunk_document(self, document: Document) -> list[Chunk]:
        chunks = []
        heading = document.title
        fence_char, fence_length = "", 0
        section: list[tuple[int, str]] = []
        section_length = 0

        def flush() -> None:
            """使用原始字串切割，再依字元偏移回推行號。"""
            nonlocal section_length
            if not section:
                return
            text = "".join(value for _, value in section)
            offset = 0
            for part in self._split_if_needed(text):
                if part.strip():
                    start = section[0][0] + text[:offset].count("\n")
                    end = start + part.rstrip("\r\n").count("\n")
                    index = len(chunks)
                    chunks.append(Chunk(
                        f"{document.filepath}::chunk-{index}", document.filename,
                        document.filepath, document.title, heading, index, part,
                        start, end, document.source_sha256,
                    ))
                offset += len(part)
            section.clear()
            section_length = 0

        for number, line in enumerate(document.content.splitlines(keepends=True), 1):
            fence = FENCE.match(line)
            if fence_char:
                section.append((number, line))
                section_length += len(line)
                if (fence and fence.group(1)[0] == fence_char
                        and len(fence.group(1)) >= fence_length and not fence.group(2).strip()):
                    fence_char = ""
                continue
            if fence:
                fence_char, fence_length = fence.group(1)[0], len(fence.group(1))
                section.append((number, line))
                section_length += len(line)
                continue
            match = HEADING.match(line)
            if match:
                flush()
                heading = match.group(1)
                continue
            section.append((number, line))
            section_length += len(line)
            if not line.strip() and section_length >= self.target_chars:
                flush()
        flush()
        return chunks

    def chunk_documents(self, documents: list[Document]) -> list[Chunk]:
        """各文件獨立建立連續 chunk index。"""
        return [chunk for document in documents for chunk in self.chunk_document(document)]
