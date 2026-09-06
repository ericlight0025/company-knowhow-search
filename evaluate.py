"""執行 10 組 keyword/vector/hybrid 搜尋並產生評估報告。"""

from __future__ import annotations

from config import ROOT_DIR, SearchConfig
from src.evaluation import generate_report
from src.hybrid_search import HybridSearcher


def main() -> int:
    searcher = HybridSearcher.load(SearchConfig())
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
