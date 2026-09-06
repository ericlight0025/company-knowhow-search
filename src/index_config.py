"""index_config.yaml 的讀取與驗證。"""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
from typing import Any

from config import KNOWHOW_DIR, ROOT_DIR


@dataclass(frozen=True)
class SourceSpec:
    """一個資料匣來源與其篩選規則。"""

    path: Path
    recursive: bool = True
    include: tuple[str, ...] = ("*.md",)
    exclude: tuple[str, ...] = ()


@dataclass(frozen=True)
class IndexConfig:
    """YAML 內的來源設定。"""

    sources: tuple[SourceSpec, ...]
    files: tuple[Path, ...]


def load_index_config(config_path: Path) -> IndexConfig:
    """讀取 YAML，路徑相對於專案根目錄解析。"""

    if not config_path.exists():
        return IndexConfig(sources=(SourceSpec(KNOWHOW_DIR),), files=())

    try:
        import yaml
    except ImportError as exc:
        raise RuntimeError(
            "index_config.yaml 需要 PyYAML，請先執行：python -m pip install -r requirements.txt"
        ) from exc

    raw = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    if not isinstance(raw, dict):
        raise ValueError("index_config.yaml 的最外層必須是 mapping")

    source_values = raw.get("sources", [])
    if not isinstance(source_values, list):
        raise ValueError("index_config.yaml 的 sources 必須是 list")
    sources: list[SourceSpec] = []
    for item in source_values:
        if isinstance(item, str):
            sources.append(SourceSpec(path=_resolve_path(item)))
            continue
        if not isinstance(item, dict):
            raise ValueError("每個 sources 項目必須是字串或 mapping")
        if "path" not in item:
            raise ValueError("sources 項目缺少 path")
        include = _string_tuple(item.get("include", ["*.md"]), "include")
        exclude = _string_tuple(item.get("exclude", []), "exclude")
        sources.append(
            SourceSpec(
                path=_resolve_path(str(item["path"])),
                recursive=bool(item.get("recursive", True)),
                include=include or ("*.md",),
                exclude=exclude,
            )
        )

    file_values = raw.get("files", [])
    files = tuple(_resolve_path(value) for value in _string_tuple(file_values, "files"))
    if not sources and not files:
        sources.append(SourceSpec(KNOWHOW_DIR))
    return IndexConfig(sources=tuple(sources), files=files)


def _resolve_path(value: str) -> Path:
    expanded = os.path.expandvars(os.path.expanduser(value))
    path = Path(expanded)
    if not path.is_absolute():
        path = ROOT_DIR / path
    return path


def _string_tuple(value: Any, field_name: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,)
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"index_config.yaml 的 {field_name} 必須是字串或字串 list")
    return tuple(value)

