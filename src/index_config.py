"""index_config.yaml 的讀取與驗證。"""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
from typing import Any

from config import ROOT_DIR


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
        raise FileNotFoundError(f"找不到來源設定檔：{config_path}")

    try:
        import yaml
    except ImportError as exc:
        raise RuntimeError(
            "index_config.yaml 需要 PyYAML，請先執行：python -m pip install -r requirements.txt"
        ) from exc

    try:
        raw = yaml.safe_load(config_path.read_text(encoding="utf-8-sig"))
    except yaml.YAMLError as exc:
        raise ValueError(f"YAML 格式錯誤：{exc}") from exc
    if not isinstance(raw, dict):
        raise ValueError("index_config.yaml 的最外層必須是 mapping")
    if set(raw) - {"sources", "files"}:
        raise ValueError("來源設定有未知欄位，只接受 sources、files")

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
        if set(item) - {"path", "recursive", "include", "exclude"}:
            raise ValueError("sources 項目有未知欄位")
        recursive = item.get("recursive", True)
        if not isinstance(recursive, bool):
            raise ValueError("recursive 必須是 true 或 false，不可加引號")
        include = _string_tuple(item.get("include", ["*.md"]), "include")
        exclude = _string_tuple(item.get("exclude", []), "exclude")
        if not include:
            raise ValueError("include 不可為空")
        for pattern in include + exclude:
            if Path(pattern).is_absolute() or ".." in Path(pattern).parts:
                raise ValueError("篩選 pattern 必須在來源資料匣內，不可包含 ..")
        sources.append(
            SourceSpec(
                path=_resolve_path(item["path"]),
                recursive=recursive,
                include=include,
                exclude=exclude,
            )
        )

    file_values = raw.get("files", [])
    files = tuple(_resolve_path(value) for value in _string_tuple(file_values, "files"))
    if not sources and not files:
        raise ValueError("sources 與 files 不可同時為空，請指定要索引的來源")
    return IndexConfig(sources=tuple(sources), files=files)


def _resolve_path(value: str) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("來源路徑必須是非空字串")
    expanded = os.path.expandvars(os.path.expanduser(value))
    path = Path(expanded)
    if not path.is_absolute():
        path = ROOT_DIR / path
    return path


def _string_tuple(value: Any, field_name: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        value = [value]
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"index_config.yaml 的 {field_name} 必須是字串或字串 list")
    if any(not item.strip() for item in value):
        raise ValueError(f"{field_name} 不可包含空白項目")
    return tuple(value)
