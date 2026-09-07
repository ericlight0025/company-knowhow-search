# Knowledge Map Search V2

本次調整維持原本的 Semantic Locator 定位，不擴充成大型 RAG。

## 主要變更

1. 預設搜尋模式改為 `auto`：Keyword 優先，證據不足時才使用 Hybrid fallback。
2. Auto 模式若 Keyword 與 Vector 證據都不足，回傳 `no_candidates`，不再固定硬塞 Top K。
3. 10～40 行左右的短 Knowledge Map 以整張 Markdown 作為單一搜尋文件；長文件仍沿用原本 chunking。
4. 搜尋載入時會比對 metadata 保存的來源 SHA256。Markdown 修改或刪除後，必須重新建立 index。
5. 英文 semantic alias 改成 boundary-aware matching，例如 `rapid` 不會再誤命中 `api`。
6. `keyword`、`vector`、`hybrid` 三種模式仍保留，方便 debug 與 evaluation。

## 升級後必須重建 index

Embedding feature matching 已更新 `algorithm_version`，因此舊 vector index 不應與新程式混用。

升級後請執行：

```bash
python index.py
```

再執行：

```bash
python search.py "契變完成但保價金還是昨天的資料" --top 3
```

JSON 模式：

```bash
python search.py "火星探測器如何校正軌道" --json
```

若證據不足，預期：

```json
{
  "status": "no_candidates",
  "results": []
}
```

## 可調參數

- `KNOWHOW_KEYWORD_MIN_COVERAGE`：Auto 模式接受 Keyword 結果的最低詞面覆蓋率。
- `KNOWHOW_NO_MATCH_VECTOR_SIMILARITY`：Hybrid fallback 的最低 cosine similarity。

RRF normalized score 仍只代表候選排序，不代表答案正確率，也不應直接作為 confidence probability。

## 評估原則

目前 repository 的 12 題仍屬 synthetic development set，部分問題與卡片「常見問法」非常接近，因此不能用來證明 Hybrid 一定優於 Keyword。

正式導入時建議使用 20～50 個脫敏、未直接出現在卡片中的 paraphrase query，重新比較 Keyword、Vector、Hybrid 與 Auto 的 Top 1、Top 3、Hit@5、MRR 與 no-match 誤判率。
