"""以不可變版本資料匣與單一指標切換，避免混用新舊索引。"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import uuid

FILES = ("knowledge.db", "vectors.index", "metadata.json")


def file_hash(path: Path) -> str:
    """串流計算檔案雜湊。"""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def new_generation(data_dir: Path) -> Path:
    """每次重建使用獨立位置；失敗不會動到目前版本。"""
    path = data_dir / "generations" / uuid.uuid4().hex
    path.mkdir(parents=True)
    return path


def publish(data_dir: Path, generation: Path) -> None:
    """完成後原子替換指標；舊版本保留供回復。"""
    manifest = {"format_version": 2, "generation": generation.name,
                "sha256": {name: file_hash(generation / name) for name in FILES}}
    temporary = data_dir / f"current-{uuid.uuid4().hex}.tmp"
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, data_dir / "current.json")


def resolve_generation(data_dir: Path) -> Path:
    """固定讀取單一版本，驗證三個檔案都完整。"""
    pointer = data_dir / "current.json"
    if not pointer.is_file():
        raise FileNotFoundError("索引尚未建立或屬於舊版，請執行 python index.py")
    try:
        manifest = json.loads(pointer.read_text(encoding="utf-8"))
        identifier = manifest["generation"]
        if (manifest["format_version"] != 2 or not isinstance(identifier, str)
                or len(identifier) != 32 or any(c not in "0123456789abcdef" for c in identifier)):
            raise ValueError("索引指標格式錯誤")
        generation = data_dir / "generations" / identifier
        for name in FILES:
            if file_hash(generation / name) != manifest["sha256"][name]:
                raise ValueError(f"索引檔案校驗失敗：{name}")
        return generation
    except (KeyError, TypeError) as exc:
        raise ValueError("索引指標損壞，請重新建立索引") from exc
