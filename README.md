# Company Know-how Search

這是一個可直接在 Windows 本機執行的 Markdown Know-how 搜尋 POC，主線是：

`模糊自然語言查詢 → keyword BM25 + local vector → RRF hybrid ranking → Top K 案例`

限制符合第一版需求：沒有 Web UI、沒有 Docker、沒有 PostgreSQL、沒有 Elasticsearch、沒有外部 Vector DB、沒有 Cloud DB，也不需要 Windows Administrator 權限。

## 目前實作

- `knowhow/**/*.md`：24 份企業資訊系統測試文件，含中文、英文、欄位名與刻意製造的同義描述。
- SQLite FTS5：索引 `filename`、`filepath`、`title`、`heading`、原文 `content` 與中文 n-gram／英文欄位 token。
- BM25：由 SQLite FTS5 排名，避免自己重寫全文索引。
- Markdown chunking：依 heading／paragraph 切割，每個 chunk 保存 source file、heading、chunk index。
- Local vector search：NumPy normalized dot product，預設使用 `HashingEmbeddingProvider`。
- Hybrid ranking：以 Reciprocal Rank Fusion（RRF）合併 keyword 與 vector rank；預設 vector 60%、keyword 40%。
- CLI：`search.py` 支援 hybrid、keyword、vector 與 JSON 輸出。
- Evaluation：10 組查詢比較三種結果，報告寫入 `docs/search-evaluation.md`。
- 演算法與 SA 文件使用說明：`docs/algorithm-tuning.md`。
- Copilot 與公司導入操作文件：`docs/copilot-operations.md`。

## 為什麼第一版不用 FAISS

目前環境沒有 FAISS，而且文件數量很小。NumPy brute-force cosine search 已足夠驗證「模糊查詢是否找到正確案例」，不需要為 POC 增加編譯、安裝或權限風險。`VectorIndex` 已隔離索引介面，未來資料量變大時可以換成 FAISS，不需要改 CLI 或 hybrid ranking。

預設 hashing vector 是可重現的本機 baseline，不等同於 transformer embedding。它使用中文單字／雙字 n-gram、英文詞元與 `config.py` 的領域同義詞概念特徵，例如「契變／契約變更／contract adjustment」、「保價金／cash value／CV」會共享概念特徵。這讓 POC 可以無模型下載直接驗證主線，但正式上線前應用同一份 evaluation query 比較 sentence-transformers 或公司內部 embedding API。

## 專案結構

```text
company-knowhow-search/
├── README.md
├── .gitignore
├── requirements.txt
├── config.py
├── index_config.yaml
├── index.py
├── menu.py
├── search.py
├── evaluate.py
├── src/
│   ├── markdown_loader.py
│   ├── chunker.py
│   ├── fts_index.py
│   ├── vector_index.py
│   ├── embedding_provider.py
│   ├── hybrid_search.py
│   ├── evaluation.py
│   ├── index_config.py
│   ├── models.py
│   └── text_utils.py
├── knowhow/
│   └── *.md
├── data/
│   ├── knowledge.db
│   ├── vectors.index
│   └── metadata.json
├── tests/
└── docs/
    ├── architecture.md
    ├── algorithm-tuning.md
    ├── copilot-operations.md
    └── search-evaluation.md
```

## 執行方式

以下指令在專案根目錄執行。第一版只需要 Python 3.10+、NumPy 與 PyYAML。

```bash
python -m pip install -r requirements.txt
python menu.py
python index.py
python search.py "契變完成後保價金沒有更新"
python search.py "以前是不是有批次重跑造成金額異常" --top 10
```

一般使用者可以直接執行 `python menu.py`，從選單選擇搜尋、重建索引、查看來源設定或查看索引狀態。Copilot 與自動化流程請繼續使用非互動式的 `search.py` 與 `index.py`。

如果目前 Python 環境已經有 NumPy 與 PyYAML，可以直接跳過安裝。`index.py` 每次都依 `index_config.yaml` 的選擇完整重建 SQLite 與 vector index；Markdown 是唯一來源，`data/` 下的檔案都可以重新產生。

## 用 YAML 選擇要索引的資料匣與 Markdown

預設設定檔是專案根目錄的 [`index_config.yaml`](index_config.yaml)。每次執行 `python index.py` 時，會讀取這份設定，將指定來源全部合併後完整重建 `data/` 下的 index。

資料匣可以是專案相對路徑，也可以是 `C:/`、`D:/`、`U:/` 或 UNC 路徑。Windows 路徑建議使用 `/`，避免 YAML 雙引號中的反斜線跳脫問題。

```yaml
sources:
  - path: "C:/Company/SA"
    recursive: true
    include:
      - "*.md"
    exclude:
      - "archive/**"

  - path: "U:/CompanyKnowhow/Batch"
    recursive: true
    include:
      - "*.md"

files:
  - "D:/Runbook/batch_retry.md"
  - "C:/Company/SA/api_design.md"
```

設定欄位的意思：

- `sources`：要掃描的資料匣清單，可以放多個資料匣。
- `path`：資料匣路徑；相對路徑以專案根目錄為基準。
- `recursive`：是否包含子資料匣；`false` 只掃描第一層。
- `include`：資料匣內要包含的 glob pattern，預設是 `*.md`。
- `exclude`：要排除的相對路徑或檔名 pattern，例如 `archive/**`。
- `files`：指定個別 `.md` 檔案；可以和 `sources` 同時使用。

常見用法：

```bash
# 使用 index_config.yaml
python index.py

# 使用另一份 YAML 設定
python index.py --config C:/Company/index_config.yaml

# 臨時覆蓋 YAML，只索引某個資料匣
python index.py --source "U:/CompanyKnowhow/SA"

# 臨時指定幾份文件
python index.py --file "C:/Company/SA/api_design.md" --file "D:/Runbook/batch_retry.md"
```

只要執行 `index.py`，新的來源設定就會建立新的本機 index；不需要把外部 Markdown 複製到本專案。索引結果會保留來源檔案的完整路徑，之後搜尋結果可以知道答案來自哪個磁碟與哪一份文件。一次 rebuild 只保留本次 YAML 選出的來源，不會自動保留上一次來源。

## 搜尋模式

```bash
# 預設：Hybrid
python search.py "契變完成後保價金沒有更新" --top 5

# 單獨比較
python search.py "契變完成後保價金沒有更新" --mode keyword --top 5
python search.py "契變完成後保價金沒有更新" --mode vector --top 5

# 給 Copilot CLI 或其他本機腳本讀取
python search.py "幫我找契變後金額還是舊資料的案例" --top 5 --json
```

CLI 結果包含 file、heading、score、snippet；hybrid 另外顯示 keyword／vector rank，方便人工 debug。

## 測試與評估

```bash
python -m unittest discover -s tests -v
python evaluate.py
```

`evaluate.py` 會實際執行 10 組查詢，分為精準 keyword、半模糊與高度模糊 semantic，並把每題的 Keyword Top 5、Vector Top 5、Hybrid Top 5 寫入 `docs/search-evaluation.md`。報告的「最佳」是依人工標註 relevant file 第一次出現在 Top 5 的排名判斷，不是訓練模型得到的客觀真值。

若要把這套流程用在 SA 文件，或調整 chunking、BM25、Vector、RRF 權重與精準行號引用，請參考 [`docs/algorithm-tuning.md`](docs/algorithm-tuning.md)。

要交給公司人員或 Copilot 使用，請參考 [`docs/copilot-operations.md`](docs/copilot-operations.md)。

目前這 10 題的 baseline 結果：Hybrid 平均首次命中排名 1.30，優於 Vector 1.40 與 Keyword 1.50；但 Vector 的 Top 1 命中題數較多（9 題），Hybrid 為 8 題，Keyword 為 7 題。這表示 Hybrid 在整體排名穩定性上較好，但不是每個查詢都單獨勝出，正式導入前仍應用真實脫敏查詢擴充評估集。

## SA 文件與精準引用

這套流程可以用於 SA（System Analysis／Software Architecture）Markdown 文件，特別適合搜尋 API、Java Service、非同步事件、Batch、Oracle Table、SQL、Incident 與上下游流程。

目前搜尋結果可以定位到：

```text
File + Heading + Chunk index + Snippet
```

目前尚未保存 Markdown 的 `start_line`／`end_line`，因此還不能保證輸出精準行號。若要輸出：

```text
File: knowhow/java_service_layer.md
Lines: 9-9
Heading: Common bug
```

需要讓 chunk metadata 額外保存 `start_line` 與 `end_line`，再重新執行 `python index.py`。這只會增加文件 provenance，不會改變 BM25、Vector 或 Hybrid 演算法。

如果來源是 PDF，應保存頁碼；如果來源是 Word，應保存 heading、paragraph 或 table cell，而不是假設有穩定的行號。

完整調整方式請看 [`docs/algorithm-tuning.md`](docs/algorithm-tuning.md)。

## 調整 Hybrid 權重

預設設定在 `config.py`：

```text
vector_weight = 0.6
keyword_weight = 0.4
rrf_k = 60
```

也可以用環境變數做快速實驗：

```bash
set KNOWHOW_VECTOR_WEIGHT=0.7
set KNOWHOW_KEYWORD_WEIGHT=0.3
python search.py "保價金批次重新計算"
```

Hybrid 不會直接把 BM25 原始分數與 cosine 原始分數相加，而是先各自排名，再用 RRF 融合，避免兩種分數尺度不一致。

## 替換 EmbeddingProvider

目前 `src/embedding_provider.py` 定義 `EmbeddingProvider` 介面，`VectorIndex` 只依賴這個介面。未來可新增：

1. `LocalEmbeddingProvider`：使用公司允許的本地模型。
2. `SentenceTransformersEmbeddingProvider`：已放入可選 adapter，但沒有預設下載模型。
3. `OpenAIEmbeddingProvider` 或公司內部 API adapter：只應在資料治理與網路政策允許時啟用。

公司 Know-how 不會因為執行這個 POC 自動上傳到公開服務；預設程式只讀本機 Markdown 和本機 index。

## Copilot 整合的最小方案

目前不建立 MCP Server。最簡單的下一階段是讓 Copilot Chat／CLI 具備一個本機 command tool，執行：

```bash
python search.py "幫我找以前契變後保價金沒有更新的案例" --top 5 --json
```

Copilot 讀取 JSON 的 file、heading、snippet，再把結果整理成回答並要求使用者開啟原始 Markdown。這條路徑沒有新增 server、port、帳號或資料搬移，適合先驗證使用價值。等搜尋品質與權限模型穩定後，再評估 MCP wrapper。

## POC 風險與下一步

- hashing vector 是輕量 baseline，不是完整語意模型；同義詞表需要持續由實際查詢補強。
- NumPy brute-force 適合目前小資料量；若 chunk 達到數十萬，才考慮 FAISS 或其他本機索引。
- SQLite FTS5 的中文召回依賴 n-gram，不等同完整中文斷詞；正式導入前應用真實匿名查詢驗證。
- 目前 index 是 full rebuild，沒有 incremental indexing、權限過濾或文件版本治理。

第一個 must-have 是把真實但已脫敏的查詢加入 evaluation set，確認 Hybrid 是否穩定找到正確 Know-how，再考慮模型、MCP 或 UI 等擴充。
