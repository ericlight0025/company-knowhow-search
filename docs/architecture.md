# Architecture

## Scope

這個 POC 以本機 Markdown 作為公司 Know-how 的唯一來源，驗證模糊自然語言查詢能否找到正確案例。沒有 Web UI、沒有 Docker、沒有額外 Server；SQLite 與 NumPy index 都只是可以重新建立的衍生物。

## Pipeline

```text
Markdown files
      ↓
Markdown Loader
      ↓
Markdown Chunking
(Heading + Paragraph + Code fence；以字元預算近似，不保證 token 數)
      ↓
 ┌──────────────────────────┐
 │ SQLite FTS5              │  Vector Index
 │ BM25 keyword search      │  Local embedding + cosine
 └──────────────┬───────────┘
                ↓
          Hybrid Ranking
       (weighted RRF fusion)
                ↓
             Top K Results
                ↓
       Copilot Chat / Copilot CLI
```

## Components

### Markdown Loader

`index_config.yaml` 先決定要索引的資料匣與指定檔案，支援專案相對路徑、`C:/`、`D:/`、`U:/` 與 UNC 路徑，再由 Loader 讀取 UTF-8 Markdown、解析 title，並保存來源 filepath。Loader 不會修改來源文件。

### Chunker

Chunker 依 heading 與 paragraph 建立 chunk；長段落再依句子邊界切分。每個 chunk 都保存：

- source file / filename
- filepath
- document title
- heading
- chunk index
- chunk content

Embedding 的文字會包含 title、heading 與正文，避免只看一小段正文而遺失上下文。

### SQLite FTS5

`data/generations/<版本>/knowledge.db` 內的 `chunks_fts` 保存 filename、filepath、title、heading、content 與 search_text。`search_text` 是給 FTS 的中英文 token 化欄位：中文加入單字與雙字 n-gram，英文保留原詞及 snake_case／hyphenated components。

查詢使用 SQLite 的 `bm25()` 排序。BM25 分數只在 keyword layer 內使用；不會直接與 cosine 分數相加。

### Vector Index

第一版使用 `HashingEmbeddingProvider` 與 NumPy matrix。向量先正規化，搜尋時用 dot product 等價於 cosine similarity。版本資料匣內的 `vectors.index` 和 `metadata.json` 都是衍生檔，刪除後可由 `python index.py` 重建。

Embedding provider 由 `EmbeddingProvider` 介面隔離，未來可替換本地模型、sentence-transformers、OpenAI embedding API 或公司內部 embedding API；替換時要重新建立 vector index。

### Hybrid Ranking

先從 BM25 與 vector 各取得候選結果，再以 rank fusion 合併：

```text
hybrid_score = 0.4 / (rrf_k + keyword_rank)
             + 0.6 / (rrf_k + vector_rank)
```

缺少某一側結果的 chunk 只得到另一側的分數。最後將 fused score 正規化到第一名為 1.0，供 CLI 顯示。權重與 `rrf_k` 集中在 `config.py`。

## Single Source of Truth

Markdown 是 Single Source of Truth：

```text
index_config.yaml ─┐
                   ├─index.py─> knowledge.db
Markdown files ────┘          └─> vectors.index
                                └─> metadata.json
```

SQLite FTS5 與 vector index 都不應被人工編輯，也不應被當成主資料。YAML 只負責描述本次要納入的來源，Markdown 修改或 YAML 變更後直接重新執行 `python index.py` 即可產生一致的新 index；這個 POC 為了簡單與可回滾，第一版不做 incremental indexing。

## Copilot integration

目前最小整合方式是本機 command invocation：

```text
Copilot user question
        ↓
python search.py "..." --top 5 --json
        ↓
read file / heading / snippet
        ↓
回答並附上原始 Markdown 位置
```

這比一開始建立 MCP Server 少一層部署與權限風險。當 command 的輸出格式、權限過濾、審計與真實查詢評估穩定後，再把同一個 service layer 包成 MCP tool。

## 版本發布與引用

`index.py` 在獨立版本資料匣完成 SQLite、vectors、metadata；驗證成功後才以原子替換更新 `data/current.json`。搜尋一次讀取指標，固定使用該版本；舊版本不自動刪除。中途中斷會留下未發布資料匣，但不會切換現行索引。

載入時核對檔案 SHA-256、embedding metadata 與筆數；metadata 另保存 UTC 建立時間、來源雜湊、設定與 chunk 行號。行號不表示文件目前未改動，須以相同來源雜湊為準。

評估統一文件去重，包含 Hit@5、MRR@5 與無答案題。Hashing 與同義詞是基準實作，尚無通用的答案存在判斷器。
