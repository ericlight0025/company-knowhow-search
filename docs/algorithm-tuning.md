# 搜尋演算法與 SA 文件使用說明

## 1. 這套架構能不能用在 SA 文件

可以。若 SA 指的是 System Analysis、Software Architecture、系統分析或系統設計文件，這套流程適合先做「相關段落召回」：

```text
SA Markdown
  ↓
Heading／Paragraph Chunking
  ↓
SQLite FTS5 + BM25
  ↓
Local Vector Search
  ↓
RRF Hybrid Ranking
  ↓
File + Heading + Chunk
```

特別適合搜尋：

- API contract、request／response 欄位
- Java service 與非同步事件流程
- Batch、retry、scheduler、timeout
- Oracle table、欄位與 SQL
- Incident、root cause、recovery procedure
- 系統間的 upstream／downstream 關係
- 同一概念但不同文件寫法的內容

目前最適合的輸入格式是 Markdown。SA 文件如果是 Word、PDF 或圖片，應先轉成可搜尋文字；PDF 需要額外保存頁碼，圖片中的架構圖則需要 OCR 或人工補充 metadata。

## 2. 目前可以定位到哪裡

目前搜尋結果會保存：

- filepath
- filename
- title
- heading
- chunk index
- chunk content

所以現在可以回答：

```text
File: knowhow/java_service_layer.md
Heading: Common bug
Chunk: 1
```

目前已保存 `start_line`、`end_line` 及來源檔案 `source_sha256`。

## 3. 精準行號定位

`search.py` 的文字與 JSON 輸出都包含 chunk 的原始行號範圍。行號是索引當時的版本；文件有修改時，請重建或驗證來源雜湊。程式碼圍欄內的註解不會被誤當成 heading。長段落按原文字串偏移切割，長行可能跨多個 chunk。

```bash
python index.py
python search.py "Java 非同步批次" --json
```

## 4. 不同文件格式的定位方式

| 文件格式 | 建議定位資訊 |
|---|---|
| Markdown／純文字 | 檔案＋行號＋heading |
| PDF | 檔案＋頁碼＋段落位置 |
| Word／DOCX | 檔案＋heading＋paragraph index；表格要加 row／column |
| Excel | 檔案＋sheet＋cell range |
| PowerPoint | 檔案＋slide number＋shape／text block |
| PNG／架構圖 | 檔案＋OCR 文字或人工標註區域 |

因此「第幾行」只適合 Markdown 和純文字。SA 文件若主要是 Word 或 PDF，建議使用 page／paragraph／table cell 作為引用位置。

## 5. 可調整的演算法

### Chunking

檔案：`src/chunker.py`

設定：`config.py`

```python
chunk_target_chars = 1400
chunk_max_chars = 2600
```

SA 文件的建議：

- API 規格：一個 endpoint 或一個 section 一個 chunk
- 流程設計：一個流程階段一個 chunk
- Table 定義：同一張表或同一個欄位群組不要拆散
- Incident：summary、root cause、recovery 可分開，但要保留同一份 source file

調整 chunking 後必須重建 index。

### BM25／全文搜尋

檔案：`src/fts_index.py`、`src/text_utils.py`

目前支援：

- 中文單字與雙字 n-gram
- 英文 token
- snake_case 欄位名
- heading、title、content

SA 文件若常查 API、錯誤碼、Table、欄位名，可以提高 BM25 的精準詞面比重。

### Vector Search

檔案：`src/embedding_provider.py`

目前是無模型下載的 hashing-local baseline，不等同於 transformer embedding。未來可以替換成 local model、sentence-transformers 或公司內部 embedding API，但替換後必須重建 vector index。

### Hybrid RRF

檔案：`src/hybrid_search.py`、`config.py`

目前公式：

```text
hybrid_score =
    0.4 / (60 + keyword_rank)
  + 0.6 / (60 + vector_rank)
```

可調整設定：

```text
KNOWHOW_VECTOR_WEIGHT
KNOWHOW_KEYWORD_WEIGHT
KNOWHOW_RRF_K
KNOWHOW_MAX_CHUNKS_PER_FILE
```

建議：

- API／欄位／錯誤碼查詢：Keyword 0.6、Vector 0.4
- 模糊描述／同義詞查詢：Keyword 0.3、Vector 0.7
- 一般 SA Know-how：Keyword 0.4、Vector 0.6

權重修改通常不需要重建 index；chunk、tokenizer、同義詞或 embedding 修改則需要重建。

## 6. 調整與驗證流程

不要一次修改所有演算法。建議：

1. 收集 20～50 個真實且脫敏的 SA 查詢。
2. 為每題標註預期文件與可接受文件。
3. 先調整 Hybrid 權重。
4. 再補充公司同義詞。
5. 再調整 chunking。
6. 最後才更換 embedding model。

每次修改後執行：

```bash
python index.py
python evaluate.py
python -m unittest discover -s tests -v
```

主要觀察：

- Top 1 relevant count
- Top 3／Top 5 recall
- average first relevant rank
- 是否能回到正確原始文件
- snippet 是否足夠讓使用者判斷

目前測試資料中有些句子刻意接近查詢，因此只能驗證 POC 流程。正式評估時應使用文件沒有出現過的 paraphrase query。

## 7. 安全與引用

SA 文件通常包含內部架構、API、資料表與權限資訊。預設應維持本機索引，不要把內容送到公開服務。

搜尋結果必須保留原始文件位置，讓使用者可以回到原文確認；不要只顯示模型摘要。未來加入權限控管時，權限過濾應在搜尋結果輸出前完成。

## 本次修正後的評估規則

三種模式按完整路徑去重後比較文件 Top 5。MRR@5 包含未命中題（計 0）；Hit@5 顯示召回率，平均首次命中排名只作輔助。開發用合成題不能作為獨立品質證明。

向量門檻由 `KNOWHOW_VECTOR_MIN_SIMILARITY` 設定，預設 0。調整門檻須同時觀察有答案與無答案題，避免為降低誤召回而漏掉正確文件。RRF 分數不適合作為機率門檻。
