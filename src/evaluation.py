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
    EvaluationCase("A1", "精準 keyword", "POLICY_LOAN_AMT 在哪裡使用？", ("policy_loan.md", "oracle_table_reference.md")),
    EvaluationCase("A2", "精準 keyword", "AML screening batch risk level", ("aml_screening.md",)),
    EvaluationCase("A3", "精準 keyword", "POLICY_CONTRACT_CHANGE API callback", ("api_contract_change.md", "contract_change.md")),
    EvaluationCase("A4", "精準 keyword", "PAYMENT_RECONCILIATION settlement amount mismatch", ("payment_reconciliation.md",)),
    EvaluationCase("B1", "半模糊", "保價金批次重新計算", ("incident_cv_batch.md", "cash_value_recalculation.md", "batch_retry.md")),
    EvaluationCase("B2", "半模糊", "保單借款金額欄位查詢", ("policy_loan.md", "oracle_table_reference.md")),
    EvaluationCase("B3", "半模糊", "外部檔案傳輸失敗重送", ("external_file_transfer.md", "batch_retry.md")),
    EvaluationCase("C1", "高度模糊 semantic", "客戶說改完保單後前台還是之前的數字，可能排程晚了", ("incident_cv_batch.md", "cv_stale_after_endorsement.md", "customer_portal_cache.md")),
    EvaluationCase("C2", "高度模糊 semantic", "有人說資料修正後，部分保單的金額被重複計算，應該怎麼查？", ("batch_retry.md", "data_repair_runbook.md", "incident_cv_batch.md")),
    EvaluationCase("C3", "高度模糊 semantic", "新規則上線後 API 與資料庫寫入順序造成保單資料不一致", ("java_service_layer.md", "api_contract_change.md", "release_checklist.md")),
)


def first_relevant_rank(results: list[SearchResult], relevant_files: tuple[str, ...]) -> int | None:
    for rank, result in enumerate(results, start=1):
        if result.chunk.source_file in relevant_files:
            return rank
    return None


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
    for case in EVALUATION_CASES:
        results = {
            "keyword": searcher.keyword_search(case.query, top_k),
            "vector": searcher.vector_search(case.query, top_k),
            "hybrid": searcher.hybrid_search(case.query, top_k),
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
        hits = [rank for rank in ranks if rank is not None]
        rank_metrics[mode] = {
            "top1": sum(1 for rank in hits if rank == 1),
            "average": sum(hits) / len(hits) if hits else float("inf"),
        }

    lines = [
        "# Search Evaluation",
        "",
        "> 這份報告由 `python evaluate.py` 實際執行產生。Relevant file 是 POC 的人工標註，排名以主要案例第一次出現在 Top 5 的位置衡量。",
        "",
        "## Summary",
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
        "| Keyword average first relevant rank | " + f"{rank_metrics['keyword']['average']:.2f}" + " |",
        "| Vector average first relevant rank | " + f"{rank_metrics['vector']['average']:.2f}" + " |",
        "| Hybrid average first relevant rank | " + f"{rank_metrics['hybrid']['average']:.2f}" + " |",
        "| No relevant result in Top " + str(top_k) + " | " + str(wins["皆未命中"]) + " |",
        "",
        "### First relevant rank",
        "",
        "| ID | Category | Query | Keyword | Vector | Hybrid | Best |",
        "|---|---|---|---:|---:|---:|---|",
    ]
    for record in records:
        case = record["case"]
        ranks = record["ranks"]
        lines.append(
            f"| {case.case_id} | {case.category} | {case.query} | "
            f"{ranks['keyword'] or '—'} | {ranks['vector'] or '—'} | {ranks['hybrid'] or '—'} | {record['best']} |"
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
                f"**Expected files:** {', '.join(f'`{name}`' for name in case.relevant_files)}",
                "",
                f"**Keyword first relevant rank:** {ranks['keyword'] or '未命中'}  \n**Vector first relevant rank:** {ranks['vector'] or '未命中'}  \n**Hybrid first relevant rank:** {ranks['hybrid'] or '未命中'}  \n**Best:** {best}",
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
    output_path.write_text("\n".join(lines), encoding="utf-8")
    return {
        "records": records,
        "wins": wins,
        "unique_wins": unique_wins,
        "rank_metrics": rank_metrics,
        "output_path": str(output_path),
    }


def _reason_for_case(case: EvaluationCase, best: str, ranks: dict[str, int | None]) -> str:
    if best.startswith("Hybrid"):
        return "Hybrid 同時保留精準術語的 BM25 命中與同義／描述差異的向量召回，主要案例在三種結果中排名最前或並列最前。"
    if best == "Keyword":
        return "這題包含明確欄位名或系統術語，原文詞面本身就足以定位文件；BM25 的精準性勝過額外語意召回。"
    if best == "Vector":
        return "這題使用了與文件不同的描述方式，向量概念特徵比單純詞面更早召回標註的案例。"
    return "三種方法在 Top 5 都沒有命中人工標註的主要案例，需要補充資料、同義詞或更好的 embedding model。"
