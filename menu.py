"""公司 Know-how Search 的互動式 Menu CLI。"""

from __future__ import annotations

import json

from config import DATABASE_PATH, METADATA_PATH, ROOT_DIR, VECTOR_INDEX_PATH
from index import main as index_main
from search import main as search_main
from src.index_config import load_index_config


SEARCH_MODES = ("hybrid", "keyword", "vector")


def parse_top(value: str, default: int = 5) -> int:
    """解析互動式輸入的 Top K，空白時使用預設值。"""

    text = value.strip()
    if not text:
        return default
    try:
        top = int(text)
    except ValueError as exc:
        raise ValueError("Top K 必須是正整數") from exc
    if top <= 0:
        raise ValueError("Top K 必須大於 0")
    return top


def normalise_mode(value: str, default: str = "hybrid") -> str:
    """解析搜尋模式；空白時使用 Hybrid。"""

    mode = value.strip().lower() or default
    if mode not in SEARCH_MODES:
        raise ValueError("模式只能是 hybrid、keyword 或 vector")
    return mode


def _pause() -> None:
    """讓使用者有時間閱讀輸出。"""

    try:
        input("\n按 Enter 返回主選單...")
    except (EOFError, KeyboardInterrupt):
        print()


def _search_flow() -> None:
    """執行一次互動式搜尋。"""

    query = input("\n請輸入查詢內容：").strip()
    if not query:
        print("查詢內容不可為空。")
        return

    try:
        top = parse_top(input("Top K（預設 5）："))
        mode = normalise_mode(input("模式 hybrid/keyword/vector（預設 hybrid）："))
    except ValueError as exc:
        print(f"輸入錯誤：{exc}")
        return

    exit_code = search_main([query, "--top", str(top), "--mode", mode])
    if exit_code != 0:
        print("搜尋未完成，請先確認索引狀態。")
    _pause()


def _rebuild_flow() -> None:
    """確認後完整重建索引。"""

    print("\n索引重建會依 index_config.yaml 完整重建 data/ 下的檔案。")
    print("原始 Markdown 不會被修改。")
    confirmation = input("確定要重建嗎？輸入 Y 繼續：").strip().lower()
    if confirmation not in {"y", "yes"}:
        print("已取消。")
        return

    try:
        index_main([])
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"索引重建失敗：{exc}")
    _pause()


def _show_source_config() -> None:
    """顯示目前 YAML 解析後的來源設定。"""

    config_path = ROOT_DIR / "index_config.yaml"
    try:
        index_config = load_index_config(config_path)
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"讀取來源設定失敗：{exc}")
        _pause()
        return

    print(f"\n設定檔：{config_path}")
    print("資料匣來源：")
    if not index_config.sources:
        print("- （無）")
    for source in index_config.sources:
        print(f"- Path: {source.path}")
        print(f"  Recursive: {source.recursive}")
        print(f"  Include: {', '.join(source.include)}")
        print(f"  Exclude: {', '.join(source.exclude) or '（無）'}")

    print("指定文件：")
    if not index_config.files:
        print("- （無）")
    for file_path in index_config.files:
        print(f"- {file_path}")
    _pause()


def _show_index_status() -> None:
    """顯示三個本機索引檔案與 metadata 狀態。"""

    print("\n本機索引狀態：")
    for label, path in (
        ("SQLite FTS5", DATABASE_PATH),
        ("Vector index", VECTOR_INDEX_PATH),
        ("Metadata", METADATA_PATH),
    ):
        if path.exists():
            size_kb = path.stat().st_size / 1024
            print(f"- {label}: OK ({size_kb:.1f} KB)")
        else:
            print(f"- {label}: 尚未建立 ({path})")

    if METADATA_PATH.exists():
        try:
            payload = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
            print(f"Documents: {payload.get('document_count', '?')}")
            print(f"Chunks: {payload.get('chunk_count', '?')}")
            provider = payload.get("embedding_provider", {})
            print(f"Embedding: {provider.get('name', '?')}")
        except (OSError, json.JSONDecodeError) as exc:
            print(f"Metadata 讀取失敗：{exc}")
    _pause()


def print_menu() -> None:
    """顯示主選單。"""

    print(
        "\n"
        "==============================\n"
        " Company Know-how Search\n"
        "==============================\n"
        "1. 搜尋 Know-how\n"
        "2. 重建索引\n"
        "3. 查看來源設定\n"
        "4. 查看索引狀態\n"
        "0. 離開\n"
    )


def run_menu() -> int:
    """執行互動式主選單。"""

    while True:
        print_menu()
        try:
            choice = input("請選擇功能：").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n已離開。")
            return 0

        if choice in {"0", "q", "quit", "exit"}:
            print("已離開。")
            return 0
        if choice == "1":
            _search_flow()
        elif choice == "2":
            _rebuild_flow()
        elif choice == "3":
            _show_source_config()
        elif choice == "4":
            _show_index_status()
        else:
            print("無效選項，請輸入 0～4。")


def main() -> int:
    """程式進入點。"""

    return run_menu()


if __name__ == "__main__":
    raise SystemExit(main())
