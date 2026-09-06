"""中英文混合文字的輕量 tokenization 工具。

SQLite unicode61 對中文長句不適合直接拿來做高召回查詢，因此這裡額外產生
中文單字與雙字 n-gram，並保留英文欄位名稱、snake_case 與 hyphenated term。
"""

from __future__ import annotations

import re
from collections import OrderedDict


_TOKEN_RE = re.compile(r"[A-Za-z0-9]+(?:[_-][A-Za-z0-9]+)*|[\u3400-\u4dbf\u4e00-\u9fff]")
_ALNUM_RE = re.compile(r"[A-Za-z0-9]+(?:[_-][A-Za-z0-9]+)*")
_CJK_RUN_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]+")
_COMMON_CJK_STOPWORDS = {"的", "了", "在", "與", "和", "是", "有", "到", "後", "前", "一", "個"}


def normalize_text(text: str) -> str:
    """做不破壞中英文語意的基本正規化。"""

    return re.sub(r"\s+", " ", text.casefold()).strip()


def tokenize_text(text: str, include_cjk_unigrams: bool = True) -> list[str]:
    """產生穩定、可給 SQLite FTS 與本機 embedding 使用的 token。"""

    normalized = normalize_text(text)
    tokens: list[str] = []

    # 英文／數字欄位名稱保留完整形式與拆開後的 component。
    for match in _ALNUM_RE.finditer(normalized):
        value = match.group(0)
        tokens.append(value)
        for part in re.split(r"[_-]", value):
            if part and part != value:
                tokens.append(part)

    # 中文同時保留單字與雙字，讓「契變」可以匹配「契約變更」的一部分。
    for run_match in _CJK_RUN_RE.finditer(normalized):
        run = run_match.group(0)
        if include_cjk_unigrams:
            tokens.extend(char for char in run if char not in _COMMON_CJK_STOPWORDS)
        tokens.extend(run[index : index + 2] for index in range(len(run) - 1))

    # 有些文字中混有單一 CJK 字元或不在上述 pattern 的 Unicode，補一次通用掃描。
    if not tokens:
        tokens.extend(match.group(0) for match in _TOKEN_RE.finditer(normalized))

    unique: OrderedDict[str, None] = OrderedDict()
    for token in tokens:
        token = token.strip()
        if token:
            unique[token] = None
    return list(unique)


def build_fts_search_text(text: str) -> str:
    """建立只含原文詞元的 FTS 欄位；語意同義詞由向量層處理。"""

    return " ".join(tokenize_text(text))


def validate_query(query: str) -> None:
    """阻擋空字串與只有標點的查詢，供所有入口共用。"""

    if not query.strip() or not tokenize_text(query):
        raise ValueError("查詢必須包含可搜尋的中文、英文或數字")


def build_fts_query(query: str) -> str:
    """將查詢轉成安全的 FTS5 OR query。"""

    tokens = tokenize_text(query)
    if not tokens:
        return '""'
    # 用 OR 提高混合中英文及模糊查詢的召回率，再由 BM25 排序。
    quoted = [f'"{token.replace(chr(34), chr(34) + chr(34))}"' for token in tokens]
    return " OR ".join(quoted)


def compact_text(text: str, max_chars: int = 260) -> str:
    """供 CLI／報告使用的單行 snippet。"""

    value = re.sub(r"\s+", " ", text).strip()
    if len(value) <= max_chars:
        return value
    return value[: max_chars - 1].rstrip() + "…"
