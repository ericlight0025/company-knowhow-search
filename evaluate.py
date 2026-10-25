"""執行 10 組 keyword/vector/hybrid 搜尋並產生評估報告。"""

from __future__ import annotations

import sys

from config import ROOT_DIR, SearchConfig
from src.evaluation import generate_report
from src.hybrid_search import HybridSearcher


def main() -> int:
    searcher = HybridSearcher.load(SearchConfig())
    # 報告會寫進有版本控管的 docs/，只允許內建合成卡片，避免公司內容被 commit。
    sources = [str(item.get("file", "")) for item in searcher.index_metadata.get("sources", [])]
    if any(not name.startswith("knowhow/") for name in sources):
        print(
            "evaluate.py 只評估內建的 knowhow/ 合成卡片；目前索引含外部來源，"
            "為避免把公司內容寫進 docs/，已停止。",
            file=sys.stderr,
        )
        return 1
    report = generate_report(searcher, ROOT_DIR / "docs" / "search-evaluation.md", top_k=5)
    wins = report["wins"]
    unique_wins = report["unique_wins"]
    rank_metrics = report["rank_metrics"]
    print(f"Evaluation completed: {report['output_path']}")
    print(f"Keyword best or tied: {wins['Keyword']}; unique: {unique_wins['Keyword']}")
    print(f"Vector best or tied: {wins['Vector']}; unique: {unique_wins['Vector']}")
    print(f"Hybrid best or tied: {wins['Hybrid']}; unique: {unique_wins['Hybrid']}")
    print(
        "Average first relevant rank: "
        f"keyword={rank_metrics['keyword']['average']:.2f}, "
        f"vector={rank_metrics['vector']['average']:.2f}, "
        f"hybrid={rank_metrics['hybrid']['average']:.2f}"
    )
    print(f"No relevant Top 5 hit: {wins['皆未命中']}")
    for mode, metric in rank_metrics.items():
        print(f"{mode}: Hit@5={metric['hit_at_5']:.3f}, MRR@5={metric['mrr']:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
