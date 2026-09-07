"""建立 Markdown、SQLite FTS5 與 NumPy vector index。"""

from __future__ import annotations

import argparse
from fnmatch import fnmatchcase
import json
import sys
import sqlite3
from datetime import datetime, timezone
from dataclasses import asdict
from pathlib import Path

from config import (
    DATA_DIR,
    KNOWHOW_DIR,
    ROOT_DIR,
    SearchConfig,
)
from src.chunker import MarkdownChunker
from src.embedding_provider import create_embedding_provider
from src.fts_index import FTSIndex
from src.index_config import SourceSpec, load_index_config
from src.markdown_loader import MarkdownLoader
from src.vector_index import VectorIndex
from src.index_store import new_generation, publish


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="掃描指定來源的 Markdown，完整重建本機 Know-how index。"
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=ROOT_DIR / "index_config.yaml",
        help="來源 YAML 設定檔，預設為專案根目錄的 index_config.yaml。",
    )
    parser.add_argument(
        "--source",
        action="append",
        type=Path,
        help="臨時覆蓋 YAML 的資料匣或單一來源路徑；可重複指定。",
    )
    parser.add_argument(
        "--file",
        action="append",
        type=Path,
        help="臨時加入指定的單一 Markdown 檔案；可重複指定。",
    )
    parser.add_argument(
        "--include",
        action="append",
        default=None,
        help="臨時覆蓋資料匣內的 glob pattern，例如 '*.md'；可重複指定。",
    )
    parser.add_argument(
        "--no-recursive",
        action="store_true",
        help="資料匣只掃描第一層，不遞迴子資料匣。",
    )
    return parser


def collect_markdown_files(
    sources: list[Path] | None = None,
    files: list[Path] | None = None,
    include_patterns: list[str] | None = None,
    recursive: bool = True,
    source_specs: tuple[SourceSpec, ...] | None = None,
) -> list[Path]:
    """解析來源選擇，回傳去重後的 Markdown 檔案清單。"""

    selected: dict[str, Path] = {}
    exact_files = files or []

    if source_specs is not None:
        configured_sources = list(source_specs)
    else:
        source_paths = sources if sources is not None else ([] if files else [KNOWHOW_DIR])
        patterns = tuple(include_patterns or ["*.md"])
        configured_sources = [
            SourceSpec(
                path=source,
                recursive=recursive,
                include=patterns,
            )
            for source in source_paths
        ]

    for file_path in exact_files:
        path = file_path.expanduser().resolve()
        if not path.exists() or not path.is_file():
            raise FileNotFoundError(f"找不到指定 Markdown：{file_path}")
        if path.suffix.casefold() != ".md":
            raise ValueError(f"指定檔案不是 .md：{file_path}")
        selected[str(path).casefold()] = path

    for source_spec in configured_sources:
        path = source_spec.path.expanduser().resolve()
        if not path.exists():
            raise FileNotFoundError(f"找不到來源路徑：{source_spec.path}")
        if path.is_file():
            if path.suffix.casefold() != ".md":
                raise ValueError(f"來源檔案不是 .md：{source_spec.path}")
            selected[str(path).casefold()] = path
            continue
        if not path.is_dir():
            raise ValueError(f"來源不是資料匣或檔案：{source_spec.path}")
        for pattern in source_spec.include:
            iterator = path.rglob(pattern) if source_spec.recursive else path.glob(pattern)
            for candidate in iterator:
                if candidate.is_file() and candidate.suffix.casefold() == ".md":
                    relative_text = candidate.relative_to(path).as_posix()
                    if any(
                        fnmatchcase(relative_text, exclude_pattern)
                        or fnmatchcase(candidate.name, exclude_pattern)
                        for exclude_pattern in source_spec.exclude
                    ):
                        continue
                    resolved = candidate.resolve()
                    selected[str(resolved).casefold()] = resolved

    return sorted(selected.values(), key=lambda item: str(item).casefold())


def display_filepath(path: Path) -> str:
    """專案內檔案用相對路徑，外部 C:/D:/U:/ 或 UNC 檔案保留完整路徑。"""

    resolved = path.resolve()
    try:
        return resolved.relative_to(ROOT_DIR).as_posix()
    except ValueError:
        return str(resolved)


def build_index(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    settings = SearchConfig()
    settings.validate()

    cli_source_override = (
        args.source is not None
        or args.file is not None
        or args.include is not None
        or args.no_recursive
    )
    config_path = args.config.expanduser().resolve()
    if cli_source_override:
        override_sources = args.source if args.source is not None else (
            [] if args.file is not None else [KNOWHOW_DIR]
        )
        source_specs = tuple(
            SourceSpec(
                path=source,
                recursive=not args.no_recursive,
                include=tuple(args.include or ["*.md"]),
            )
            for source in override_sources
        )
        configured_files = tuple(args.file or [])
    else:
        index_config = load_index_config(config_path)
        source_specs = index_config.sources
        configured_files = index_config.files

    paths = collect_markdown_files(
        files=list(configured_files),
        source_specs=source_specs,
    )
    if not paths:
        raise RuntimeError("沒有找到可索引的 .md 文件")

    loader_root = paths[0].parent
    loader = MarkdownLoader(loader_root)
    documents = [loader.load(path, display_filepath=display_filepath(path)) for path in paths]

    # Knowledge Map 卡通常短小；短卡以整張文件作為搜尋單位，避免 heading 過度切碎。
    # 超過 max_chars 的長文件仍沿用原本的 heading / 字元預算切割。
    chunker = MarkdownChunker(
        settings.chunk_target_chars,
        settings.chunk_max_chars,
        prefer_whole_document=True,
    )
    chunks = chunker.chunk_documents(documents)
    if not chunks:
        raise RuntimeError("Markdown 有文件但沒有可索引的內容")

    provider = create_embedding_provider(settings.embedding_dimension)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    generation = new_generation(DATA_DIR)
    database_path = generation / "knowledge.db"
    vector_path = generation / "vectors.index"
    metadata_path = generation / "metadata.json"
    fts_index = FTSIndex(database_path)
    fts_index.rebuild(chunks)
    vector_index = VectorIndex.build(vector_path, chunks, provider)
    vector_index.save()

    metadata = {
        "format_version": 2,
        "generation": generation.name,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "settings": asdict(settings),
        "sources": [{"file": doc.filepath, "sha256": doc.source_sha256} for doc in documents],
        "embedding_provider": provider.metadata(),
        "chunk_count": len(chunks),
        "document_count": len(documents),
        "source_files": [document.filepath for document in documents],
        "chunks": [chunk.to_dict() for chunk in chunks],
    }
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    VectorIndex.load(vector_path, chunks, provider, provider.metadata())
    if fts_index.count() != len(chunks):
        raise RuntimeError("FTS 筆數驗證失敗")
    publish(DATA_DIR, generation)

    print("Index completed")
    print(f"Config: {config_path}")
    print(f"Documents: {len(documents)}")
    print(f"Chunks: {len(chunks)}")
    print(f"SQLite FTS5: {database_path}")
    print(f"Vector index: {vector_path}")
    print(f"Metadata: {metadata_path}")
    print(f"Embedding provider: {provider.metadata()['name']} ({settings.embedding_dimension} dimensions)")
    print("Source files:")
    for document in documents:
        print(f"- {document.filepath}")
    return 0


def main(argv: list[str] | None = None) -> int:
    """統一顯示可處理的錯誤，索引中斷時保留已發布版本。"""
    try:
        return build_index(argv)
    except (OSError, RuntimeError, ValueError, sqlite3.Error) as exc:
        print(f"索引建立失敗：{exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("索引建立已中斷；已發布版本仍保留。", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
