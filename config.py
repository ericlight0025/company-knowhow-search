"""專案設定。

第一版刻意把路徑、權重與 embedding 參數集中在這裡，讓 POC 可以在不改動
搜尋流程的情況下替換資料位置或調整排名策略。
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os
import math


ROOT_DIR = Path(__file__).resolve().parent
KNOWHOW_DIR = ROOT_DIR / "knowhow"
DATA_DIR = ROOT_DIR / "data"


# 領域同義詞只用來改善本機 POC 的向量召回，不會改寫原始 Markdown。
# 未來可把這段移到 JSON 或公司詞彙服務。
SEMANTIC_GROUPS: dict[str, tuple[str, ...]] = {
    "contract_change": (
        "契變",
        "契約變更",
        "契約異動",
        "保單變更",
        "contract change",
        "contract adjustment",
        "policy change",
        "endorsement",
        "變更作業",
        "改完保單",
        "改完",
        "異動完成",
        "變更",
    ),
    "cash_value": (
        "保價金",
        "現金價值",
        "現金值",
        "cash value",
        "cash-value",
        "cv calculation",
        "cv",
    ),
    "surrender_value": (
        "解約金",
        "解約價值",
        "surrender value",
        "cash surrender value",
    ),
    "policy_loan": (
        "保單借款",
        "保單貸款",
        "policy loan",
        "loan amount",
        "借款金額",
    ),
    "batch": (
        "批次",
        "批次處理",
        "批次工作",
        "batch",
        "batch job",
        "scheduled process",
        "排程",
        "夜間作業",
        "夜間批次",
        "批次延遲",
    ),
    "recalculation": (
        "重新計算",
        "重算",
        "再計算",
        "recalculate",
        "recalculation",
        "recompute",
        "refresh calculation",
        "重算批次",
        "夜間重算",
        "計算工作",
    ),
    "stale_value": (
        "舊資料",
        "舊金額",
        "前一天數值",
        "前一日",
        "沒有更新",
        "未更新",
        "stale value",
        "outdated amount",
        "previous day cash value",
        "old value",
        "之前的數字",
        "前一版數值",
        "變更前的數字",
        "舊數字",
        "落後",
        "prior amount",
        "previous amount",
        "stale",
    ),
    "retry_rerun": (
        "重跑",
        "重送",
        "重試",
        "補跑",
        "retry",
        "rerun",
        "reprocess",
        "replay",
    ),
    "data_repair": (
        "資料修正",
        "資料修復",
        "修復資料",
        "資料重建",
        "data repair",
        "repair data",
        "duplicate execution",
        "duplicate calculation",
        "重複計算",
        "重複處理",
        "算兩次",
    ),
    "external_transfer": (
        "外部檔案傳輸",
        "檔案交換",
        "檔案傳送",
        "sftp",
        "file transfer",
        "outbound file",
        "inbound file",
    ),
    "aml": (
        "洗錢防制",
        "防制洗錢",
        "aml",
        "anti-money laundering",
        "screening",
        "風險篩檢",
    ),
    "incident": (
        "事故",
        "事件",
        "incident",
        "production issue",
        "異常案例",
        "故障",
    ),
    "api": (
        "介面",
        "應用程式介面",
        "api",
        "rest api",
        "endpoint",
        "callback",
    ),
    "database": (
        "資料表",
        "資料庫",
        "oracle table",
        "table",
        "sql",
        "query",
    ),
}


@dataclass(frozen=True)
class SearchConfig:
    """可調整的搜尋設定。"""

    vector_weight: float = float(os.getenv("KNOWHOW_VECTOR_WEIGHT", "0.6"))
    keyword_weight: float = float(os.getenv("KNOWHOW_KEYWORD_WEIGHT", "0.4"))
    rrf_k: int = int(os.getenv("KNOWHOW_RRF_K", "60"))
    embedding_dimension: int = int(os.getenv("KNOWHOW_EMBEDDING_DIM", "512"))
    chunk_target_chars: int = int(os.getenv("KNOWHOW_CHUNK_TARGET_CHARS", "1400"))
    chunk_max_chars: int = int(os.getenv("KNOWHOW_CHUNK_MAX_CHARS", "2600"))
    default_top_k: int = int(os.getenv("KNOWHOW_DEFAULT_TOP_K", "5"))
    max_chunks_per_file: int = int(os.getenv("KNOWHOW_MAX_CHUNKS_PER_FILE", "1"))
    vector_min_similarity: float = float(os.getenv("KNOWHOW_VECTOR_MIN_SIMILARITY", "0.0"))
    keyword_min_coverage: float = float(os.getenv("KNOWHOW_KEYWORD_MIN_COVERAGE", "0.34"))
    no_match_vector_similarity: float = float(
        os.getenv("KNOWHOW_NO_MATCH_VECTOR_SIMILARITY", "0.15")
    )

    def validate(self) -> None:
        """驗證設定，避免索引建立到一半才發現權重錯誤。"""

        confidence_values = (
            self.vector_weight,
            self.keyword_weight,
            self.vector_min_similarity,
            self.keyword_min_coverage,
            self.no_match_vector_similarity,
        )
        if not all(math.isfinite(value) for value in confidence_values):
            raise ValueError("權重與相似度門檻必須是有限數值")
        if not -1 <= self.vector_min_similarity <= 1:
            raise ValueError("vector_min_similarity 必須介於 -1 與 1")
        if not 0 <= self.keyword_min_coverage <= 1:
            raise ValueError("keyword_min_coverage 必須介於 0 與 1")
        if not -1 <= self.no_match_vector_similarity <= 1:
            raise ValueError("no_match_vector_similarity 必須介於 -1 與 1")
        if self.default_top_k <= 0:
            raise ValueError("default_top_k 必須大於 0")
        if self.vector_weight < 0 or self.keyword_weight < 0:
            raise ValueError("vector_weight 與 keyword_weight 不可為負數")
        if self.vector_weight + self.keyword_weight <= 0:
            raise ValueError("至少要有一個搜尋權重大於 0")
        if self.rrf_k <= 0:
            raise ValueError("rrf_k 必須大於 0")
        if self.embedding_dimension < 64:
            raise ValueError("embedding_dimension 太小，至少需要 64")
        if self.chunk_target_chars <= 0 or self.chunk_max_chars < self.chunk_target_chars:
            raise ValueError("chunk size 設定不合理")
        if self.max_chunks_per_file <= 0:
            raise ValueError("max_chunks_per_file 必須大於 0")
