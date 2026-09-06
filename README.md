# Company Know-how Semantic Locator

這不是完整企業 RAG，也不是用來複製或向量化公司原始文件的知識庫。

它是一個可在 Windows 本機執行的小型 **Knowledge Map / Semantic Locator**：使用者用自然語言提問後，由 Hybrid Search 找出最相關的 Markdown 導航卡，再定位到真正的 Word、Excel、Java、SQL、JSP、JS 或資料夾，最後交給 Copilot Chat／Copilot CLI 讀取與分析實際內容。

```text
自然語言問題
  → Hybrid Search
  → Top 3 Knowledge Map Cards
  → Word / Excel / Java / SQL / JSP / JS 的原始位置
  → Copilot Chat / Copilot CLI
  → 分析真實內容
```

## 核心定位

- Markdown 卡片是 **地圖**：每張只描述一個問題、SOP、系統入口或歷史 Incident，保留常見問法、技術詞、原始資料位置與下一步。
- Word、Excel、Java、SQL、JSP、JS 才是 **Source of Truth**：不需要複製進 repository，也不會被這個 POC 預設索引。
- Hybrid Search 只負責 **找到正確卡片**：SQLite FTS5/BM25 與本機 vector 結果用 RRF 合併。
- Copilot 負責 **閱讀真實資料**：找到路徑後，再由已受公司權限控管的 Copilot Chat／CLI 分析規格、程式碼或 SQL。

這個設計避免把完整公司文件做成大型 KB、RAG 或第二套 SQL／Java 搜尋器；先驗證「模糊問題能否穩定導到正確資料位置」。

## 快速開始

在專案根目錄執行。需要 Python 3.10+、NumPy 與 PyYAML；不需要 Docker、Windows Administrator 權限、資料庫伺服器或雲端服務。

```bash
python -m pip install -r requirements.txt
python index.py
python search.py "批次值日生每天要做什麼" --top 3
python search.py "契變保額異動後沒有進電訪要查哪裡" --top 3
```

一般手動使用可啟動選單：

```bash
python menu.py
```

`index.py` 每次都完整重建本機 SQLite 與 vector index。Markdown 卡片才是版本控管的主要內容；repository 另附一份僅由合成範例卡片產生的 `data/` 索引，方便 clone 後立即試查。公司實際資料重建的索引仍應維持 Git 忽略。

## 卡片格式與範例

每張 `knowhow/*.md` 維持 10–40 行左右，格式固定：

```markdown
# 卡片名稱

## 用途
這張卡要把哪種問題帶到哪個正式資料來源。

## 常見問法
- 使用者會怎麼自然描述問題？

## 常見技術詞
中英文、同義詞、系統術語。

## 原始資料位置
- Word：`U:/Company/.../SPEC.docx`
- Java：`D:/workspace/.../Service.java`
- SQL Folder：`U:/SQL/.../`

## 下一步
請 Copilot Chat／CLI 讀取正式來源。

## 關鍵結論
- 可重複使用的排查起點。
```

範例卡片包括：批次值日生、批次重跑、契變電訪、契變保價金、保價金重算、契變後保價金未更新、契變畫面、資料變更單、SQL 查詢入口、AML 交易檢核、外部檔案傳輸／重送、保單借款、解約金與歷史 Incident。

卡片內的 `U:/Company/...`、`D:/workspace/...` 都是範例路徑；公司導入時請改成真實且不含敏感內容的定位資訊。

## 搜尋

```bash
# 預設 Hybrid：適合模糊提問
python search.py "契變完成但保價金還是昨天的資料" --top 3

# 比較單一路徑
python search.py "契變相關 SQL 要去哪找" --mode keyword --top 5
python search.py "契變相關 SQL 要去哪找" --mode vector --top 5

# 給 Copilot CLI 或自動化讀取
python search.py "外部檔案失敗後要找哪份重送 SOP" --top 3 --json
```

結果包含卡片檔名、heading、snippet、來源行號與分數。Hybrid 結果另含 keyword/vector rank，方便人工檢查為什麼命中。

### Copilot 最小整合

不需要 MCP Server。讓 Copilot Chat 或 Copilot CLI 先執行：

```bash
python search.py "幫我找以前契變後保價金沒有更新的案例" --top 3 --json
```

Copilot 讀取 Top 3 卡片的 `原始資料位置`，取得使用者授權後開啟公司內部原始檔或 repository。搜尋器不會自行上傳文件；是否將內容送到遠端模型，仍須依公司 Copilot 部署與資料治理政策決定。

## 來源設定

本 POC 預設只掃描 Markdown 卡片。`index_config.yaml` 可改成專案相對路徑，或任何可存取的 `C:/`、`D:/`、`U:/`、UNC 資料夾；不需要把原始資料複製進本專案。

```yaml
sources:
  - path: "knowhow"
    recursive: true
    include:
      - "*.md"

files: []
```

公司使用時，建議將個人或部門路徑放在 `.gitignore` 已排除的 `index_config.local.yaml`：

```bash
python index.py --config index_config.local.yaml
```

只要卡片散落在不同磁碟，也可以設定多個 Markdown 資料夾。原始 Word／Excel／Java／SQL 不必納入索引；卡片只保存其位置與如何追查。

## 評測

```bash
python -m unittest discover -s tests -v
python evaluate.py
```

`evaluate.py` 會執行 12 組 Knowledge Map 定位題，將每題的 Expected Card、Keyword rank、Vector rank、Hybrid rank、Hybrid Top 1／Top 3 與三種 Top 5 寫到 [`docs/search-evaluation.md`](docs/search-evaluation.md)。成功標準是正確卡片多數進入 Hybrid Top 3，而不是宣稱模型已理解所有公司知識。

## 架構與限制

```text
Markdown Knowledge Map
  → Markdown Loader / Chunking
  → SQLite FTS5 (BM25) + local Vector Index
  → RRF Hybrid Ranking
  → Top K cards
  → Copilot Chat / Copilot CLI 讀原始資料
```

- Markdown 是搜尋地圖的 Single Source of Truth；SQLite/vector index 都可由 `index.py` 重建。
- 預設 vector 是輕量本機 hashing baseline，介面可替換為公司允許的 local embedding 或內部 API。
- 目前不使用 Docker、PostgreSQL、Qdrant、Elasticsearch、FAISS、MCP、Web UI、AST／Method Index，也不做完整文件向量化。
- SQL 卡只指向可能 Table／Column、SQL 資料夾及既有 SQL Hit-rate Tool／DBeaver；不建立第二個 SQL 語意引擎。
- Java 卡只提供 repository、module、file、class；method/caller/callee/SQL 的實際追查交給 Copilot CLI。

更完整的索引可靠性與演算法調整請見 [`docs/architecture.md`](docs/architecture.md)、[`docs/algorithm-tuning.md`](docs/algorithm-tuning.md) 與 [`docs/copilot-operations.md`](docs/copilot-operations.md)。
