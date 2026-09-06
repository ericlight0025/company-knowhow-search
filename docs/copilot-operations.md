# Company Know-how Search POC 操作文件

本文件提供給使用者、維運人員與 Copilot 參考，說明如何設定來源、建立索引、執行查詢，以及如何正確解讀結果。

## 1. 系統定位

```text
Markdown Know-how
       ↓
index_config.yaml 選擇來源
       ↓
python index.py
       ↓
SQLite FTS5 + local vector index
       ↓
python search.py "問題" --json
       ↓
Copilot 整理結果
```

這是一個 Windows 本機端 CLI 工具：

- 不建立 Web UI。
- 不使用 Docker、PostgreSQL、Elasticsearch 或外部 Vector DB。
- 不會自動把 Know-how 上傳到公開服務。
- Markdown 是原始資料；SQLite 與 vector index 都是可重建的衍生資料。

## 2. 目前版本支援範圍

目前 baseline 實際支援：

- `.md` Markdown 文件。
- 中文、英文、欄位名稱、API 名稱與一般程式術語。
- `keyword`、`vector`、`hybrid` 三種搜尋模式。
- 多資料匣、遞迴掃描、排除 pattern、指定單一 Markdown。

目前尚未直接支援：

- `.sql`
- `.java`
- `.doc`
- `.docx`

`.sql` 與 `.java` 是純文字格式，未來可由通用文字 Loader 擴充；`.docx` 可加入文件解析器；舊版 `.doc` 建議先轉成 `.docx`、`.txt` 或 `.md`。在程式尚未擴充前，不要只修改 YAML 就把這些副檔名加入 `include`。

## 3. 專案結構

```text
company-knowhow-search/
├── index.py                       # 建立或重建索引
├── menu.py                        # 一般使用者的互動式選單
├── search.py                      # 搜尋 CLI
├── index_config.yaml              # 來源資料匣與檔案設定
├── requirements.txt               # Python dependency
├── config.py                      # 搜尋與 chunk 設定
├── src/                           # 搜尋核心
├── tests/                         # 自動化測試
├── docs/                          # 架構、調校與操作文件
├── knowhow/                       # 合成測試 Know-how，可提交 Git
└── data/                          # 執行 index.py 後產生的本機索引
```

`data/` 會產生：

- `knowledge.db`：SQLite FTS5 keyword index。
- `vectors.index`：NumPy local vector index。
- `metadata.json`：chunk metadata、來源路徑與內容資料。

這些檔案不應人工編輯，也建議不要提交 Git；需要時由 `python index.py` 重新產生。

## 4. 第一次安裝

在專案根目錄執行：

```bash
python --version
python -m pip install -r requirements.txt
```

建議使用 Python 3.10 以上。安裝不需要 Windows Administrator 權限。

## 5. 設定來源文件

編輯根目錄的 `index_config.yaml`。

### 5.1 一個資料匣

```yaml
sources:
  - path: "U:/CompanyKnowhow"
    recursive: true
    include:
      - "*.md"
    exclude: []

files: []
```

### 5.2 多個資料匣與排除資料匣

```yaml
sources:
  - path: "U:/CompanyKnowhow/SA"
    recursive: true
    include:
      - "*.md"
    exclude:
      - "archive/**"

  - path: "D:/TeamRunbook"
    recursive: true
    include:
      - "*.md"
    exclude:
      - "draft/**"

files: []
```

### 5.3 指定個別文件

```yaml
sources: []

files:
  - "C:/Company/SA/api_design.md"
  - "D:/TeamRunbook/batch_retry.md"
  - "U:/CompanyKnowhow/incident_cv.md"
```

`sources` 與 `files` 可以同時使用。相對路徑以專案根目錄為基準；Windows 路徑建議使用 `/`。

不同電腦的磁碟代號不同時，可使用環境變數：

```yaml
sources:
  - path: "%COMPANY_KNOWHOW_ROOT%"
    recursive: true
    include:
      - "*.md"
```

## 6. 建立或更新索引

設定好來源後執行：

```bash
python index.py
```

這是 full rebuild，會：

1. 讀取 YAML。
2. 掃描符合條件的 `.md`。
3. 解析 heading 與段落。
4. 建立 chunks。
5. 重建 SQLite FTS5。
6. 重建 local vector index。

文件新增、修改、刪除，或 YAML 有變更時，都要重新執行 `python index.py`。

使用另一份 YAML：

```bash
python index.py --config C:/Company/knowhow-index-config.yaml
```

一次性的 CLI 覆蓋選項：

```bash
python index.py --source "U:/CompanyKnowhow/SA"
python index.py --file "C:/Company/SA/api_design.md"
python index.py --source "D:/Runbook" --no-recursive
```

## 7. 一般查詢

一般使用者也可以執行：

```bash
python menu.py
```

Menu 提供搜尋、重建索引、查看來源設定與查看索引狀態；Copilot 和批次流程仍應使用後面的非互動式指令。

預設使用 Hybrid Search，輸出 Top 5：

```bash
python search.py "契變完成後保價金沒有更新"
```

指定結果數量：

```bash
python search.py "以前是不是有批次重跑造成金額異常" --top 10
```

比較三種搜尋模式：

```bash
python search.py "POLICY_LOAN_AMT 在哪裡使用" --mode keyword --top 5
python search.py "保價金批次重新計算" --mode vector --top 5
python search.py "契變完成後畫面金額還是舊的" --mode hybrid --top 5
```

模式用途：

- `keyword`：欄位名、API 名稱、錯誤代碼、表名與精準詞。
- `vector`：模糊描述、同義詞與不同說法。
- `hybrid`：預設模式，綜合 keyword 與 vector。

搜尋分數是排序用的 normalized score，不是答案正確率百分比。結果仍需回到原始文件確認。

## 8. Copilot 標準呼叫方式

Copilot 查詢本機 Know-how 時，預設執行：

```bash
python search.py "使用者的自然語言問題" --top 5 --json
```

例如：

```bash
python search.py "幫我找以前契變後保價金沒有更新的案例" --top 5 --json
```

### Copilot 執行規則

```text
1. 將使用者問題原文送給 search.py。
2. 預設使用 hybrid，不要先自行猜測文件名稱。
3. 讀取 JSON results。
4. 回答時列出 file、heading、snippet。
5. 不要把 score 當成答案正確率。
6. 結果不足時，改用較短查詢或比較 keyword/vector。
7. 仍然沒有結果時，明確說目前索引找不到，不要編造 Know-how。
8. 需要完整步驟時，要求使用者開啟原始文件確認。
```

### JSON 輸出欄位

```json
{
  "query": "契變完成後保價金沒有更新",
  "mode": "hybrid",
  "results": [
    {
      "score": 1.0,
      "source": "hybrid",
      "file": "knowhow/incident_cv_batch.md",
      "filename": "incident_cv_batch.md",
      "title": "Incident CV Batch",
      "heading": "Incident summary",
      "chunk_index": 0,
      "snippet": "契約變更完成後，畫面仍顯示前一日的保價金...",
      "keyword_rank": 1,
      "vector_rank": 3
    }
  ]
}
```

Copilot 最少應保留：`file`、`heading`、`snippet`、`score`。Hybrid 結果可另外顯示 `keyword_rank` 與 `vector_rank` 協助除錯。

Copilot 不應：

- 自行修改原始 Know-how。
- 修改 `data/knowledge.db` 或 `vectors.index`。
- 把搜尋結果當成正式事故處理指示而不要求確認。
- 補寫搜尋結果中不存在的欄位、流程、日期或責任人。
- 把公司 Know-how 貼到公開服務或外部網站。

## 9. Git 提交規則

合成測試資料可以提交 Git；不要提交你的個人環境資訊：

- 不提交含有使用者名稱的絕對路徑。
- 不提交 `.codex`、私人設定、token、API key 或 `.env`。
- 不提交 `__pycache__/`。
- 不提交 `data/knowledge.db`、`data/vectors.index`、`data/metadata.json`。
- 真實公司 Know-how 是否提交，依公司資料治理規範決定；預設建議放在受控的 `C:/`、`D:/` 或 `U:/` 來源路徑。

`metadata.json` 可能包含 chunk 內容與來源路徑，即使是索引檔，也要按照資料內容處理。

## 10. 常見問題

### 顯示 index 尚未建立

先執行：

```bash
python index.py
```

### 找不到來源路徑

確認資料碟已連線、YAML 路徑正確，且執行 Python 的 Windows 使用者有讀取權限。

### 修改文件後結果沒有變

目前不是即時索引，必須重新執行：

```bash
python index.py
```

### 結果太少或不準

先嘗試不同查詢模式：

```bash
python search.py "較短的關鍵描述" --top 10
python search.py "精準欄位或 API 名稱" --mode keyword --top 10
python search.py "模糊自然語言描述" --mode vector --top 10
```

請記錄原始問題、正確文件與實際排名，之後再調整同義詞、chunk 或 embedding provider。

## 11. 公司導入最小流程

```text
1. Clone Git repository。
2. 安裝 Python dependency。
3. 編輯 index_config.yaml。
4. 設定公司允許索引的資料匣與 .md。
5. 執行 python index.py。
6. 用 5～10 個真實脫敏問題驗證搜尋品質。
7. 將 python search.py ... --json 作為 Copilot 的本機 command tool。
8. 確認檔案權限與資料治理規範。
```

第一階段不需要 MCP Server。等搜尋品質、權限控管、稽核與查詢格式穩定後，再評估包成 Copilot tool 或 MCP tool。
