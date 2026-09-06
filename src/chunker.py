"""依 Markdown heading／paragraph 進行 chunking。"""

from __future__ import annotations

from dataclasses import dataclass
import re

from .models import Chunk, Document


_HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$")
_SENTENCE_SPLIT_RE = re.compile(r"(?<=[。！？!?；;])\s+|(?<=\.)\s+(?=[A-Z0-9\u3400-\u9fff])")


@dataclass
class _Block:
    heading: str
    text: str


class MarkdownChunker:
    """以字元數近似 token 預算，讓中英文內容都能使用同一套規則。"""

    def __init__(self, target_chars: int = 1400, max_chars: int = 2600):
        if target_chars <= 0 or max_chars < target_chars:
            raise ValueError("target_chars 與 max_chars 設定不合理")
        self.target_chars = target_chars
        self.max_chars = max_chars

    def chunk_document(self, document: Document) -> list[Chunk]:
        blocks = self._parse_blocks(document)
        packed: list[tuple[str, str]] = []
        current_heading = document.title
        current_parts: list[str] = []
        current_length = 0

        def flush() -> None:
            nonlocal current_parts, current_length, current_heading
            if current_parts:
                packed.append((current_heading, "\n\n".join(current_parts).strip()))
                current_parts = []
                current_length = 0

        for block in blocks:
            if block.heading != current_heading and current_parts:
                # heading 改變時保留 section 邊界，避免不同主題被硬塞進同一 chunk。
                flush()
            current_heading = block.heading
            for part in self._split_if_needed(block.text):
                projected = current_length + len(part) + (2 if current_parts else 0)
                if current_parts and projected > self.max_chars:
                    flush()
                    current_heading = block.heading
                current_parts.append(part)
                current_length += len(part) + (2 if len(current_parts) > 1 else 0)
                if current_length >= self.target_chars:
                    flush()
                    current_heading = block.heading
        flush()

        chunks: list[Chunk] = []
        for index, (heading, content) in enumerate(packed):
            if not content.strip():
                continue
            chunks.append(
                Chunk(
                    chunk_id=f"{document.filepath}::chunk-{index}",
                    source_file=document.filename,
                    filepath=document.filepath,
                    title=document.title,
                    heading=heading,
                    chunk_index=index,
                    content=content,
                )
            )
        return chunks

    def chunk_documents(self, documents: list[Document]) -> list[Chunk]:
        chunks: list[Chunk] = []
        for document in documents:
            chunks.extend(self.chunk_document(document))
        return chunks

    def _parse_blocks(self, document: Document) -> list[_Block]:
        blocks: list[_Block] = []
        heading = document.title
        paragraph_lines: list[str] = []

        def flush_paragraph() -> None:
            nonlocal paragraph_lines
            text = "\n".join(paragraph_lines).strip()
            if text:
                blocks.append(_Block(heading=heading, text=text))
            paragraph_lines = []

        for line in document.content.splitlines():
            heading_match = _HEADING_RE.match(line)
            if heading_match:
                flush_paragraph()
                heading = heading_match.group(1).strip()
                continue
            if not line.strip():
                flush_paragraph()
                continue
            paragraph_lines.append(line.rstrip())
        flush_paragraph()
        return blocks

    def _split_if_needed(self, text: str) -> list[str]:
        if len(text) <= self.max_chars:
            return [text]
        sentences = [part.strip() for part in _SENTENCE_SPLIT_RE.split(text) if part.strip()]
        if not sentences:
            sentences = [text]
        parts: list[str] = []
        current = ""
        for sentence in sentences:
            if len(sentence) > self.max_chars:
                if current:
                    parts.append(current.strip())
                    current = ""
                parts.extend(
                    text[start : start + self.max_chars].strip()
                    for start in range(0, len(sentence), self.max_chars)
                )
                continue
            projected = len(current) + len(sentence) + (1 if current else 0)
            if current and projected > self.max_chars:
                parts.append(current.strip())
                current = sentence
            else:
                current = f"{current} {sentence}".strip()
        if current:
            parts.append(current.strip())
        return parts

