"""固定的 10 組 POC 評估查詢與 Markdown 報告產生器。"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .hybrid_search import HybridSearcher
from .models import SearchResult
from .text_utils import compact_text


@dataclass(frozen=True)
class EvaluationCase:
    case_id: str
    category: str
    query: str
    relevant_files: tuple[str, ...]


EVALUATION_CASES: tuple[EvaluationCase, ...] = (
    EvaluationCase("L1", "Knowledge Map 定位", "批次值日生每天要做什麼？", ("batch_monitoring.md",)),
    EvaluationCase("L2", "Knowledge Map 定位", "每天晚上 Batch JOB 要看哪份 SOP？", ("batch_monitoring.md",)),
    EvaluationCase("L3", "Knowledge Map 定位", "以前那張資料變更單在哪裡？", ("data_repair_runbook.md",)),
    EvaluationCase("L4", "Knowledge Map 定位", "以前是不是改過某個 Table 欄位？", ("data_repair_runbook.md",)),
    EvaluationCase("L5", "Knowledge Map 定位", "契變保額異動後沒有進電訪。", ("api_contract_change.md",)),
    EvaluationCase("L6", "Knowledge Map 定位", "電訪案件沒產生要查哪裡？", ("api_contract_change.md",)),
    EvaluationCase("L7", "Knowledge Map 定位", "契變完成但保價金還是昨天的資料。", ("incident_cv_batch.md",)),
    EvaluationCase("L8", "Knowledge Map 定位", "CV 沒重新計算以前是不是遇過？", ("incident_cv_batch.md", "cash_value_recalculation.md")),
    EvaluationCase("L9", "Knowledge Map 定位", "外部檔案失敗後要找哪份重送 SOP？", ("batch_processing.md",)),
    EvaluationCase("L10", "Knowledge Map 定位", "契變畫面的 JSP / JS 在哪？", ("customer_portal_cache.md",)),
    EvaluationCase("L11", "Knowledge Map 定位", "契變相關 SQL 要去哪找？", ("sql_query_practices.md", "contract_change.md")),
    EvaluationCase("L12", "Knowledge Map 定位", "AML 相關系統文件在哪？", ("aml_screening.md",)),
)


def first_relevant_rank(results: list[SearchResult], relevant_files: tuple[str, ...]) -> int | None:
    expected = {name if "/" in name else f"knowhow/{name}" for name in relevant_files}
    for rank, result in enumerate(results, start=1):
        if result.chunk.filepath in expected:
            return rank
    return None


def unique_documents(results: list[SearchResult], top_k: int) -> list[SearchResult]:
    """三種模式統一以完整來源路徑去重，避免同名檔案混淆。"""
    selected = {}
    for result in results:
        selected.setdefault(result.chunk.filepath, result)
    return list(selected.values())[:top_k]


def rank_metrics_for(ranks: list[int | None]) -> dict[str, float | int]:
    """所有題目都進入分母，未命中在 MRR 計為零。"""
    hits = [rank for rank in ranks if rank is not None]
    return {"top1": sum(rank == 1 for rank in ranks),
            "top3": sum(rank is not None and rank <= 3 for rank in ranks),
            "hit_at_5": len(hits) / len(ranks) if ranks else 0.0,
            "mrr": sum(1 / rank for rank in hits) / len(ranks) if ranks else 0.0,
            "average": sum(hits) / len(hits) if hits else float("inf")}


def _rank_quality(rank: int | None) -> float:
    return 0.0 if rank is None else 1.0 / rank


def _best_modes(ranks: dict[str, int | None]) -> tuple[str, ...]:
    qualities = {mode: _rank_quality(rank) for mode, rank in ranks.items()}
    max_quality = max(qualities.values())
    if max_quality == 0:
        return ()
    return tuple(mode for mode, value in qualities.items() if value == max_quality)


def _best_mode(ranks: dict[str, int | None]) -> str:
    labels = {"keyword": "Keyword", "vector": "Vector", "hybrid": "Hybrid"}
    modes = _best_modes(ranks)
    if not modes:
        return "皆未命中"
    rendered = [labels[mode] for mode in modes]
    return rendered[0] if len(rendered) == 1 else " / ".join(rendered) + "（並列）"


def _result_table(results: list[SearchResult]) -> str:
    lines = ["| Rank | File | Heading | Score | Snippet |", "|---:|---|---|---:|---|"]
    for index, result in enumerate(results, start=1):
        snippet = compact_text(result.chunk.content, 180).replace("|", "\\|")
        heading = result.chunk.heading.replace("|", "\\|")
        lines.append(
            f"| {index} | `{result.chunk.filepath}` | {heading} | {result.score:.4f} | {snippet} |"
        )
    return "\n".join(lines)


def generate_report(searcher: HybridSearcher, output_path: Path, top_k: int = 5) -> dict[str, object]:
    """執行所有評估查詢並輸出可讀的 Markdown 報告。"""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, object]] = []
    candidate_count = max(top_k, len(searcher.vector_index.chunks))
    for case in EVALUATION_CASES:
        results = {
            "keyword": unique_documents(searcher.keyword_search(case.query, candidate_count), top_k),
            "vector": unique_documents(searcher.vector_search(case.query, candidate_count), top_k),
            "hybrid": unique_documents(searcher.hybrid_search(case.query, candidate_count), top_k),
        }
        ranks = {mode: first_relevant_rank(value, case.relevant_files) for mode, value in results.items()}
        records.append(
            {
                "case": case,
                "results": results,
                "ranks": ranks,
                "best": _best_mode(ranks),
                "best_modes": _best_modes(ranks),
            }
        )

    wins = {"Keyword": 0, "Vector": 0, "Hybrid": 0, "皆未命中": 0}
    unique_wins = {"Keyword": 0, "Vector": 0, "Hybrid": 0}
    for record in records:
        best_modes = record["best_modes"]
        if not best_modes:
            wins["皆未命中"] += 1
            continue
        for mode in best_modes:
            wins[{"keyword": "Keyword", "vector": "Vector", "hybrid": "Hybrid"}[mode]] += 1
        if len(best_modes) == 1:
            unique_wins[{"keyword": "Keyword", "vector": "Vector", "hybrid": "Hybrid"}[best_modes[0]]] += 1

    rank_metrics: dict[str, dict[str, float | int]] = {}
    for mode, label in (("keyword", "Keyword"), ("vector", "Vector"), ("hybrid", "Hybrid")):
        ranks = [record["ranks"][mode] for record in records]
        rank_metrics[mode] = rank_metrics_for(ranks)

    lines = [
        "# Search Evaluation",
        "",
        "> 這份報告由 `python evaluate.py` 實際執行產生。Expected Card 是 POC 的人工標註，排名以主要卡片第一次出現在 Top 5 的位置衡量。",
        "",
        "## Summary",
        "",
        "> 三種模式使用相同候選上限，按完整檔案路徑去重後比較 Top 5。平均排名僅限命中題；判斷品質請同時看 Hit@5 與 MRR。這是合成資料的開發集，不是獨立測試集。",
        "",
        "| Metric | Value |",
        "|---|---:|",
        "| Query count | " + str(len(records)) + " |",
        "| Keyword best or tied | " + str(wins["Keyword"]) + " |",
        "| Vector best or tied | " + str(wins["Vector"]) + " |",
        "| Hybrid best or tied | " + str(wins["Hybrid"]) + " |",
        "| Keyword unique winner | " + str(unique_wins["Keyword"]) + " |",
        "| Vector unique winner | " + str(unique_wins["Vector"]) + " |",
        "| Hybrid unique winner | " + str(unique_wins["Hybrid"]) + " |",
        "| Keyword Top 1 relevant | " + str(rank_metrics["keyword"]["top1"]) + " |",
        "| Vector Top 1 relevant | " + str(rank_metrics["vector"]["top1"]) + " |",
        "| Hybrid Top 1 relevant | " + str(rank_metrics["hybrid"]["top1"]) + " |",
        "| Keyword Top 3 relevant | " + str(rank_metrics["keyword"]["top3"]) + " |",
        "| Vector Top 3 relevant | " + str(rank_metrics["vector"]["top3"]) + " |",
        "| Hybrid Top 3 relevant | " + str(rank_metrics["hybrid"]["top3"]) + " |",
        "| Keyword average first relevant rank | " + f"{rank_metrics['keyword']['average']:.2f}" + " |",
        "| Vector average first relevant rank | " + f"{rank_metrics['vector']['average']:.2f}" + " |",
        "| Hybrid average first relevant rank | " + f"{rank_metrics['hybrid']['average']:.2f}" + " |",
        "| No relevant result in Top " + str(top_k) + " | " + str(wins["皆未命中"]) + " |",
        "",
        "### Expected card rank",
        "",
        "| ID | Category | Query | Expected Card | Keyword rank | Vector rank | Hybrid rank | Hybrid Top 1 | Hybrid Top 3 | Best |",
        "|---|---|---|---|---:|---:|---:|---|---|---|",
    ]
    for record in records:
        case = record["case"]
        ranks = record["ranks"]
        lines.append(
            f"| {case.case_id} | {case.category} | {case.query} | "
            f"{', '.join(case.relevant_files)} | {ranks['keyword'] or '—'} | {ranks['vector'] or '—'} | "
            f"{ranks['hybrid'] or '—'} | {'是' if ranks['hybrid'] == 1 else '否'} | "
            f"{'是' if ranks['hybrid'] is not None and ranks['hybrid'] <= 3 else '否'} | {record['best']} |"
        )

    lines.extend(["", "## Detailed Results", ""])
    for record in records:
        case = record["case"]
        ranks = record["ranks"]
        best = record["best"]
        lines.extend(
            [
                f"### {case.case_id} — {case.category}",
                "",
                f"**Query:** {case.query}",
                "",
                f"**Expected card:** {', '.join(f'`{name}`' for name in case.relevant_files)}",
                "",
                f"**Keyword rank:** {ranks['keyword'] or '未命中'}  \n**Vector rank:** {ranks['vector'] or '未命中'}  \n**Hybrid rank:** {ranks['hybrid'] or '未命中'}  \n**Hybrid Top 1:** {'是' if ranks['hybrid'] == 1 else '否'}  \n**Hybrid Top 3:** {'是' if ranks['hybrid'] is not None and ranks['hybrid'] <= 3 else '否'}  \n**Best:** {best}",
                "",
                "#### Keyword Top 5",
                "",
                _result_table(record["results"]["keyword"]),
                "",
                "#### Vector Top 5",
                "",
                _result_table(record["results"]["vector"]),
                "",
                "#### Hybrid Top 5",
                "",
                _result_table(record["results"]["hybrid"]),
                "",
                f"**原因：** {_reason_for_case(case, best, ranks)}",
                "",
            ]
        )

    lines.extend(
        [
            "## Interpretation",
            "",
            "這是沒有使用大型語言模型或雲端 embedding API 的本機 baseline。Hybrid 使用 RRF 合併 BM25 與 vector rank，沒有直接相加兩種不可比的原始分數。",
            "若之後接入 sentence-transformers 或公司內部 embedding API，應保留同一份評估查詢重新比較；這份報告不能宣稱 hashing vector 等同於 transformer embedding。",
            "",
        ]
    )
    lines.extend(["", "## Document-level metrics", "",
                  "| Mode | Hit@5 | MRR@5 |", "|---|---:|---:|"])
    for mode, metric in rank_metrics.items():
        lines.append(f"| {mode} | {metric['hit_at_5']:.3f} | {metric['mrr']:.3f} |")
    # 負例揭露誤召回，不因為向量有回傳就聲稱存在答案。
    lines.extend(["", "## 無答案查詢檢查", "",
                  "下列問題在合成 Know-how 無對應答案；數字是回傳候選數，越多不代表越好。尚未用公司題庫校準門檻。", "",
                  "| Query | Keyword | Vector | Hybrid |", "|---|---:|---:|---:|"])
    for query in ("火星探測器如何校正軌道", "義大利麵食譜番茄醬比例", "蘭花葉片枯黃如何施肥"):
        counts = [len(searcher.search(query, top_k, mode)) for mode in ("keyword", "vector", "hybrid")]
        lines.append(f"| {query} | {counts[0]} | {counts[1]} | {counts[2]} |")
    output_path.write_text("\n".join(lines).replace("  \n", "\n\n"), encoding="utf-8")
    return {
        "records": records,
        "wins": wins,
        "unique_wins": unique_wins,
        "rank_metrics": rank_metrics,
        "output_path": str(output_path),
    }


def _reason_for_case(case: EvaluationCase, best: str, ranks: dict[str, int | None]) -> str:
    if "並列" in best:
        return "這些模式的第一份標註相關文件排名相同；單靠排名無法推論是哪項特徵造成命中。"
    if best.startswith("Hybrid"):
        return "Hybrid 同時保留精準術語的 BM25 命中與同義／描述差異的向量召回，主要案例在三種結果中排名最前或並列最前。"
    if best == "Keyword":
        return "這題包含明確欄位名或系統術語，原文詞面本身就足以定位文件；BM25 的精準性勝過額外語意召回。"
    if best == "Vector":
        return "這題使用了與文件不同的描述方式，向量概念特徵比單純詞面更早召回標註的案例。"
    return "三種方法在 Top 5 都沒有命中人工標註的主要案例，需要補充資料、同義詞或更好的 embedding model。"
