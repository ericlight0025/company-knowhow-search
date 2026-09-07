"""公司 Know-how 搜尋 CLI。"""

from __future__ import annotations

import argparse
import json
import sys
import sqlite3

from src.hybrid_search import HybridSearcher
from src.models import SearchResult
from src.text_utils import compact_text, validate_query


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="搜尋本機 Markdown Know-how")
    parser.add_argument("query", help="自然語言或 keyword 查詢")
    parser.add_argument("--top", type=int, default=5, help="輸出結果數，預設 5")
    parser.add_argument(
        "--mode",
        choices=("auto", "hybrid", "keyword", "vector"),
        default="auto",
        help="搜尋模式，預設 auto（Keyword 優先，Hybrid 備援，低可信回 no match）",
    )
    parser.add_argument("--json", action="store_true", help="輸出 JSON，方便 Copilot CLI 讀取")
    return parser


def result_to_dict(result: SearchResult) -> dict[str, object]:
    return {
        "score": round(result.score, 6),
        "source": result.source,
        "file": result.chunk.filepath,
        "filename": result.chunk.source_file,
        "title": result.chunk.title,
        "heading": result.chunk.heading,
        "chunk_index": result.chunk.chunk_index,
        "start_line": result.chunk.start_line,
        "end_line": result.chunk.end_line,
        "source_sha256": result.chunk.source_sha256,
        "cosine_similarity": result.cosine_score,
        "snippet": compact_text(result.chunk.content),
        "keyword_rank": result.keyword_rank,
        "vector_rank": result.vector_rank,
    }


def print_text_results(query: str, mode: str, results: list[SearchResult]) -> None:
    print(f"Query:\n{query}\n")
    print(f"Mode: {mode}")
    print("\nTop Results:\n")
    print("分數僅表示候選排序，不是答案正確率；行號對應索引當時的原文。")
    if not results:
        print("No results. Evidence is insufficient; check the wording or rebuild the index if sources changed.")
        return
    for index, result in enumerate(results, start=1):
        print(f"{index}.")
        print(f"File: {result.chunk.filepath}")
        print(f"Heading: {result.chunk.heading}")
        print(f"Lines: {result.chunk.start_line}-{result.chunk.end_line}")
        print(f"Score: {result.score:.4f}")
        print("Snippet:")
        print(compact_text(result.chunk.content))
        if result.source == "hybrid":
            print(
                f"Ranks: keyword={result.keyword_rank or '-'}, "
                f"vector={result.vector_rank or '-'}"
            )
        print()


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.top <= 0:
        print("--top 必須大於 0", file=sys.stderr)
        return 2
    try:
        validate_query(args.query)
        searcher = HybridSearcher.load()
        results = searcher.search(args.query, args.top, args.mode)
    except (OSError, RuntimeError, ValueError, sqlite3.Error) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps({
            "query": args.query,
            "mode": args.mode,
            "status": "candidates" if results else "no_candidates",
            "score_note": "排序分數不是正確率；auto 模式會在證據不足時回傳 no_candidates。",
            "indexed_at": searcher.index_metadata["created_at"],
            "results": [result_to_dict(item) for item in results],
        }, ensure_ascii=False, indent=2))
    else:
        print_text_results(args.query, args.mode, results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
