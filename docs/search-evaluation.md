# Search Evaluation

> 這份報告由 `python evaluate.py` 實際執行產生。Expected Card 是 POC 的人工標註，排名以主要卡片第一次出現在 Top 5 的位置衡量。

## Summary

> 三種模式使用相同候選上限，按完整檔案路徑去重後比較 Top 5。平均排名僅限命中題；判斷品質請同時看 Hit@5 與 MRR。這是合成資料的開發集，不是獨立測試集。

| Metric | Value |
|---|---:|
| Query count | 12 |
| Keyword best or tied | 12 |
| Vector best or tied | 11 |
| Hybrid best or tied | 12 |
| Keyword unique winner | 0 |
| Vector unique winner | 0 |
| Hybrid unique winner | 0 |
| Keyword Top 1 relevant | 12 |
| Vector Top 1 relevant | 11 |
| Hybrid Top 1 relevant | 12 |
| Keyword Top 3 relevant | 12 |
| Vector Top 3 relevant | 12 |
| Hybrid Top 3 relevant | 12 |
| Keyword average first relevant rank | 1.00 |
| Vector average first relevant rank | 1.08 |
| Hybrid average first relevant rank | 1.00 |
| No relevant result in Top 5 | 0 |

### Expected card rank

| ID | Category | Query | Expected Card | Keyword rank | Vector rank | Hybrid rank | Hybrid Top 1 | Hybrid Top 3 | Best |
|---|---|---|---|---:|---:|---:|---|---|---|
| L1 | Knowledge Map 定位 | 批次值日生每天要做什麼？ | batch_monitoring.md | 1 | 1 | 1 | 是 | 是 | Keyword / Vector / Hybrid（並列） |
| L2 | Knowledge Map 定位 | 每天晚上 Batch JOB 要看哪份 SOP？ | batch_monitoring.md | 1 | 1 | 1 | 是 | 是 | Keyword / Vector / Hybrid（並列） |
| L3 | Knowledge Map 定位 | 以前那張資料變更單在哪裡？ | data_repair_runbook.md | 1 | 1 | 1 | 是 | 是 | Keyword / Vector / Hybrid（並列） |
| L4 | Knowledge Map 定位 | 以前是不是改過某個 Table 欄位？ | data_repair_runbook.md | 1 | 1 | 1 | 是 | 是 | Keyword / Vector / Hybrid（並列） |
| L5 | Knowledge Map 定位 | 契變保額異動後沒有進電訪。 | api_contract_change.md | 1 | 1 | 1 | 是 | 是 | Keyword / Vector / Hybrid（並列） |
| L6 | Knowledge Map 定位 | 電訪案件沒產生要查哪裡？ | api_contract_change.md | 1 | 1 | 1 | 是 | 是 | Keyword / Vector / Hybrid（並列） |
| L7 | Knowledge Map 定位 | 契變完成但保價金還是昨天的資料。 | incident_cv_batch.md | 1 | 2 | 1 | 是 | 是 | Keyword / Hybrid（並列） |
| L8 | Knowledge Map 定位 | CV 沒重新計算以前是不是遇過？ | incident_cv_batch.md, cash_value_recalculation.md | 1 | 1 | 1 | 是 | 是 | Keyword / Vector / Hybrid（並列） |
| L9 | Knowledge Map 定位 | 外部檔案失敗後要找哪份重送 SOP？ | batch_processing.md | 1 | 1 | 1 | 是 | 是 | Keyword / Vector / Hybrid（並列） |
| L10 | Knowledge Map 定位 | 契變畫面的 JSP / JS 在哪？ | customer_portal_cache.md | 1 | 1 | 1 | 是 | 是 | Keyword / Vector / Hybrid（並列） |
| L11 | Knowledge Map 定位 | 契變相關 SQL 要去哪找？ | sql_query_practices.md, contract_change.md | 1 | 1 | 1 | 是 | 是 | Keyword / Vector / Hybrid（並列） |
| L12 | Knowledge Map 定位 | AML 相關系統文件在哪？ | aml_screening.md | 1 | 1 | 1 | 是 | 是 | Keyword / Vector / Hybrid（並列） |

## Detailed Results

### L1 — Knowledge Map 定位

**Query:** 批次值日生每天要做什麼？

**Expected card:** `batch_monitoring.md`

**Keyword rank:** 1

**Vector rank:** 1

**Hybrid rank:** 1

**Hybrid Top 1:** 是

**Hybrid Top 3:** 是

**Best:** Keyword / Vector / Hybrid（並列）

#### Keyword Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/batch_monitoring.md` | 常見問法 | 1.0000 | - 批次值日生每天要做什麼？ - 每天晚上 JOB 要檢查什麼？ - Batch 掛掉要看哪份 SOP？ - 值班人員交接文件在哪？ - Batch Monitoring 的 SOP 在哪？ |
| 2 | `knowhow/external_file_transfer.md` | 常見問法 | 0.1429 | - 外部檔案傳輸失敗要看哪裡？ - 檔案沒收到怎麼查？ - SFTP 傳輸規格在哪？ - 外部介接每日要檢查什麼？ |
| 3 | `knowhow/batch_retry.md` | 常見問法 | 0.1250 | - 批次失敗可以直接重跑嗎？ - Batch Retry 前要確認什麼？ - 重跑造成金額異常要看哪裡？ - 哪些 JOB 有前後相依？ |
| 4 | `knowhow/underwriting_rule.md` | 常見問法 | 0.1111 | - 核保規則文件在哪？ - 某個案件為什麼沒有通過？ - underwriting threshold 要去哪找？ |
| 5 | `knowhow/premium_adjustment.md` | 常見問法 | 0.1000 | - 保費調整規則在哪？ - 契變後保費為什麼不同？ - premium adjustment 的規格要看哪裡？ |

#### Vector Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/batch_monitoring.md` | 常見問法 | 0.7986 | - 批次值日生每天要做什麼？ - 每天晚上 JOB 要檢查什麼？ - Batch 掛掉要看哪份 SOP？ - 值班人員交接文件在哪？ - Batch Monitoring 的 SOP 在哪？ |
| 2 | `knowhow/batch_retry.md` | 用途 | 0.6694 | 定位批次失敗後的 retry 原則、相依工作與重跑前檢查。 |
| 3 | `knowhow/policy_loan.md` | 用途 | 0.6658 | 定位保單借款規格、金額欄位與相關批次或服務入口。 |
| 4 | `knowhow/cash_value_recalculation.md` | 常見問法 | 0.6594 | - 保價金批次重新計算要看哪裡？ - CV 沒重新計算以前是不是遇過？ - 現金價值重算 JOB 是哪一支？ - cash value recalculation 失敗如何檢查？ |
| 5 | `knowhow/audit_log.md` | 常見問法 | 0.6479 | - 誰改過這筆資料？ - 操作紀錄要去哪找？ - batch 執行歷程怎麼看？ |

#### Hybrid Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/batch_monitoring.md` | 常見問法 | 1.0000 | - 批次值日生每天要做什麼？ - 每天晚上 JOB 要檢查什麼？ - Batch 掛掉要看哪份 SOP？ - 值班人員交接文件在哪？ - Batch Monitoring 的 SOP 在哪？ |
| 2 | `knowhow/batch_retry.md` | 常見問法 | 0.8971 | - 批次失敗可以直接重跑嗎？ - Batch Retry 前要確認什麼？ - 重跑造成金額異常要看哪裡？ - 哪些 JOB 有前後相依？ |
| 3 | `knowhow/cash_value_recalculation.md` | 常見問法 | 0.8452 | - 保價金批次重新計算要看哪裡？ - CV 沒重新計算以前是不是遇過？ - 現金價值重算 JOB 是哪一支？ - cash value recalculation 失敗如何檢查？ |
| 4 | `knowhow/policy_loan.md` | 用途 | 0.8244 | 定位保單借款規格、金額欄位與相關批次或服務入口。 |
| 5 | `knowhow/incident_2025_policy_amount.md` | 常見問法 | 0.8096 | - 以前有沒有類似金額異常的 Incident？ - 歷史事故報告在哪？ - 批次或同步造成的問題怎麼回查？ - incident postmortem 要去哪找？ |

**原因：** 這些模式的第一份標註相關文件排名相同；單靠排名無法推論是哪項特徵造成命中。

### L2 — Knowledge Map 定位

**Query:** 每天晚上 Batch JOB 要看哪份 SOP？

**Expected card:** `batch_monitoring.md`

**Keyword rank:** 1

**Vector rank:** 1

**Hybrid rank:** 1

**Hybrid Top 1:** 是

**Hybrid Top 3:** 是

**Best:** Keyword / Vector / Hybrid（並列）

#### Keyword Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/batch_monitoring.md` | 常見問法 | 1.0000 | - 批次值日生每天要做什麼？ - 每天晚上 JOB 要檢查什麼？ - Batch 掛掉要看哪份 SOP？ - 值班人員交接文件在哪？ - Batch Monitoring 的 SOP 在哪？ |
| 2 | `knowhow/aml_screening.md` | 常見問法 | 0.5000 | - AML 相關系統文件在哪？ - AML 交易檢核規則要看哪份規格？ - screening batch 異常怎麼查？ - 可疑交易案件資料在哪？ |
| 3 | `knowhow/batch_retry.md` | 常見問法 | 0.2500 | - 批次失敗可以直接重跑嗎？ - Batch Retry 前要確認什麼？ - 重跑造成金額異常要看哪裡？ - 哪些 JOB 有前後相依？ |
| 4 | `knowhow/external_file_transfer.md` | 常見問法 | 0.2000 | - 外部檔案傳輸失敗要看哪裡？ - 檔案沒收到怎麼查？ - SFTP 傳輸規格在哪？ - 外部介接每日要檢查什麼？ |
| 5 | `knowhow/batch_processing.md` | 常見問法 | 0.1667 | - 外部檔案失敗後要找哪份重送 SOP？ - 檔案可以重送嗎？ - SFTP failed 要怎麼 resend？ - 重送後如何確認對方已收到？ |

#### Vector Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/batch_monitoring.md` | 常見問法 | 0.7542 | - 批次值日生每天要做什麼？ - 每天晚上 JOB 要檢查什麼？ - Batch 掛掉要看哪份 SOP？ - 值班人員交接文件在哪？ - Batch Monitoring 的 SOP 在哪？ |
| 2 | `knowhow/batch_retry.md` | 常見問法 | 0.6916 | - 批次失敗可以直接重跑嗎？ - Batch Retry 前要確認什麼？ - 重跑造成金額異常要看哪裡？ - 哪些 JOB 有前後相依？ |
| 3 | `knowhow/aml_screening.md` | 常見問法 | 0.6752 | - AML 相關系統文件在哪？ - AML 交易檢核規則要看哪份規格？ - screening batch 異常怎麼查？ - 可疑交易案件資料在哪？ |
| 4 | `knowhow/cash_value_recalculation.md` | 常見問法 | 0.6584 | - 保價金批次重新計算要看哪裡？ - CV 沒重新計算以前是不是遇過？ - 現金價值重算 JOB 是哪一支？ - cash value recalculation 失敗如何檢查？ |
| 5 | `knowhow/policy_value_sync.md` | 用途 | 0.6545 | 定位保單價值在服務、批次與查詢畫面間同步的規格。 |

#### Hybrid Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/batch_monitoring.md` | 常見問法 | 1.0000 | - 批次值日生每天要做什麼？ - 每天晚上 JOB 要檢查什麼？ - Batch 掛掉要看哪份 SOP？ - 值班人員交接文件在哪？ - Batch Monitoring 的 SOP 在哪？ |
| 2 | `knowhow/aml_screening.md` | 常見問法 | 0.9745 | - AML 相關系統文件在哪？ - AML 交易檢核規則要看哪份規格？ - screening batch 異常怎麼查？ - 可疑交易案件資料在哪？ |
| 3 | `knowhow/batch_retry.md` | 常見問法 | 0.9716 | - 批次失敗可以直接重跑嗎？ - Batch Retry 前要確認什麼？ - 重跑造成金額異常要看哪裡？ - 哪些 JOB 有前後相依？ |
| 4 | `knowhow/cash_value_recalculation.md` | 常見問法 | 0.9273 | - 保價金批次重新計算要看哪裡？ - CV 沒重新計算以前是不是遇過？ - 現金價值重算 JOB 是哪一支？ - cash value recalculation 失敗如何檢查？ |
| 5 | `knowhow/audit_log.md` | 常見問法 | 0.8819 | - 誰改過這筆資料？ - 操作紀錄要去哪找？ - batch 執行歷程怎麼看？ |

**原因：** 這些模式的第一份標註相關文件排名相同；單靠排名無法推論是哪項特徵造成命中。

### L3 — Knowledge Map 定位

**Query:** 以前那張資料變更單在哪裡？

**Expected card:** `data_repair_runbook.md`

**Keyword rank:** 1

**Vector rank:** 1

**Hybrid rank:** 1

**Hybrid Top 1:** 是

**Hybrid Top 3:** 是

**Best:** Keyword / Vector / Hybrid（並列）

#### Keyword Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/data_repair_runbook.md` | 常見問法 | 1.0000 | - 以前那張資料變更單在哪裡？ - 以前是不是改過某個 Table 欄位？ - 誰改過這筆資料？ - Data Change 或 CR 紀錄在哪？ - 資料修改單怎麼查？ |
| 2 | `knowhow/api_contract_change.md` | 常見問法 | 0.1429 | - 契變保額異動後沒有進電訪。 - 電訪案件沒產生要查哪裡？ - 契約變更需要電訪嗎？ - 金額異動卻沒有進 TeleCall。 - contract change telecall 規則在哪？ |
| 3 | `knowhow/policy_value_sync.md` | 常見問法 | 0.1250 | - 保單價值同步在哪裡做？ - Cash Value 更新後畫面何時會看到？ - value sync 異常怎麼查？ |
| 4 | `knowhow/cash_value_recalculation.md` | 常見問法 | 0.1111 | - 保價金批次重新計算要看哪裡？ - CV 沒重新計算以前是不是遇過？ - 現金價值重算 JOB 是哪一支？ - cash value recalculation 失敗如何檢查？ |
| 5 | `knowhow/policy_loan.md` | 常見問法 | 0.1000 | - 保單借款規則文件在哪？ - POLICY_LOAN_AMT 在哪裡使用？ - 保單借款金額欄位怎麼查？ - policy loan 的 Java module 在哪？ |

#### Vector Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/data_repair_runbook.md` | 常見問法 | 0.7981 | - 以前那張資料變更單在哪裡？ - 以前是不是改過某個 Table 欄位？ - 誰改過這筆資料？ - Data Change 或 CR 紀錄在哪？ - 資料修改單怎麼查？ |
| 2 | `knowhow/oracle_table_reference.md` | 常見技術詞 | 0.6776 | Oracle、Table、Column、data dictionary、POLICY_LOAN_AMT、Cash Value、契變。 |
| 3 | `knowhow/premium_adjustment.md` | 用途 | 0.6774 | 定位保費調整規則、契變影響與相關資料查詢入口。 |
| 4 | `knowhow/customer_portal_cache.md` | 下一步 | 0.6685 | 請用 Copilot CLI 由 JSP/JS 找 API 與 Java controller，再追實際資料來源。 |
| 5 | `knowhow/java_service_layer.md` | 原始資料位置 | 0.6676 | - Java Folder：`D:/workspace/contract-change/` - Java：`D:/workspace/contract-change/src/ContractChangeService.java` - Word：`U:/Company/SPEC/ContractChange/` |

#### Hybrid Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/data_repair_runbook.md` | 常見問法 | 1.0000 | - 以前那張資料變更單在哪裡？ - 以前是不是改過某個 Table 欄位？ - 誰改過這筆資料？ - Data Change 或 CR 紀錄在哪？ - 資料修改單怎麼查？ |
| 2 | `knowhow/premium_adjustment.md` | 常見問法 | 0.8665 | - 保費調整規則在哪？ - 契變後保費為什麼不同？ - premium adjustment 的規格要看哪裡？ |
| 3 | `knowhow/oracle_table_reference.md` | 常見問法 | 0.8288 | - 契變資料 Table 在哪？ - POLICY_LOAN_AMT 屬於哪張表？ - 保價金欄位可能在哪？ |
| 4 | `knowhow/api_contract_change.md` | 常見問法 | 0.8275 | - 契變保額異動後沒有進電訪。 - 電訪案件沒產生要查哪裡？ - 契約變更需要電訪嗎？ - 金額異動卻沒有進 TeleCall。 - contract change telecall 規則在哪？ |
| 5 | `knowhow/customer_portal_cache.md` | 常見問法 | 0.7907 | - 契變畫面的 JSP / JS 在哪？ - contract change 前端頁面在哪個 module？ - 契變金額畫面由哪裡查出來？ - endorsement screen 欄位怎麼找？ |

**原因：** 這些模式的第一份標註相關文件排名相同；單靠排名無法推論是哪項特徵造成命中。

### L4 — Knowledge Map 定位

**Query:** 以前是不是改過某個 Table 欄位？

**Expected card:** `data_repair_runbook.md`

**Keyword rank:** 1

**Vector rank:** 1

**Hybrid rank:** 1

**Hybrid Top 1:** 是

**Hybrid Top 3:** 是

**Best:** Keyword / Vector / Hybrid（並列）

#### Keyword Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/data_repair_runbook.md` | 常見問法 | 1.0000 | - 以前那張資料變更單在哪裡？ - 以前是不是改過某個 Table 欄位？ - 誰改過這筆資料？ - Data Change 或 CR 紀錄在哪？ - 資料修改單怎麼查？ |
| 2 | `knowhow/cash_value_recalculation.md` | 常見問法 | 0.5000 | - 保價金批次重新計算要看哪裡？ - CV 沒重新計算以前是不是遇過？ - 現金價值重算 JOB 是哪一支？ - cash value recalculation 失敗如何檢查？ |
| 3 | `knowhow/underwriting_rule.md` | 常見問法 | 0.3333 | - 核保規則文件在哪？ - 某個案件為什麼沒有通過？ - underwriting threshold 要去哪找？ |
| 4 | `knowhow/audit_log.md` | 常見問法 | 0.2000 | - 誰改過這筆資料？ - 操作紀錄要去哪找？ - batch 執行歷程怎麼看？ |
| 5 | `knowhow/surrender_value.md` | 關鍵結論 | 0.1667 | - 解約金與保價金相關但不是同一個欄位概念。 - 查詢前應確認保單狀態與計算基準日。 |

#### Vector Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/data_repair_runbook.md` | 常見問法 | 0.7598 | - 以前那張資料變更單在哪裡？ - 以前是不是改過某個 Table 欄位？ - 誰改過這筆資料？ - Data Change 或 CR 紀錄在哪？ - 資料修改單怎麼查？ |
| 2 | `knowhow/oracle_table_reference.md` | 原始資料位置 | 0.6532 | - Excel：`U:/Company/DataDictionary/Oracle_Table_Column.xlsx` - SQL Folder：`U:/SQL/DataDictionary/` |
| 3 | `knowhow/underwriting_rule.md` | 原始資料位置 | 0.6404 | - Word：`U:/Company/SPEC/Underwriting/UNDERWRITING_RULE_SPEC.docx` - Java Folder：`D:/workspace/underwriting/` - SQL Folder：`U:/SQL/Underwriting/` |
| 4 | `knowhow/sql_query_practices.md` | 原始資料位置 | 0.6396 | - SQL Folder：`U:/SQL/ContractChange/` - SQL Folder：`U:/SQL/PolicyValue/` - Tool：既有 SQL Hit-rate Tool / DBeaver。 |
| 5 | `knowhow/premium_adjustment.md` | 原始資料位置 | 0.6280 | - Word：`U:/Company/SPEC/Premium/PREMIUM_ADJUSTMENT_SPEC.docx` - Java Folder：`D:/workspace/premium/` - SQL Folder：`U:/SQL/Premium/` |

#### Hybrid Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/data_repair_runbook.md` | 常見問法 | 1.0000 | - 以前那張資料變更單在哪裡？ - 以前是不是改過某個 Table 欄位？ - 誰改過這筆資料？ - Data Change 或 CR 紀錄在哪？ - 資料修改單怎麼查？ |
| 2 | `knowhow/oracle_table_reference.md` | 常見問法 | 0.9167 | - 契變資料 Table 在哪？ - POLICY_LOAN_AMT 屬於哪張表？ - 保價金欄位可能在哪？ |
| 3 | `knowhow/cash_value_recalculation.md` | 常見問法 | 0.7957 | - 保價金批次重新計算要看哪裡？ - CV 沒重新計算以前是不是遇過？ - 現金價值重算 JOB 是哪一支？ - cash value recalculation 失敗如何檢查？ |
| 4 | `knowhow/underwriting_rule.md` | 原始資料位置 | 0.7672 | - Word：`U:/Company/SPEC/Underwriting/UNDERWRITING_RULE_SPEC.docx` - Java Folder：`D:/workspace/underwriting/` - SQL Folder：`U:/SQL/Underwriting/` |
| 5 | `knowhow/sql_query_practices.md` | 原始資料位置 | 0.7625 | - SQL Folder：`U:/SQL/ContractChange/` - SQL Folder：`U:/SQL/PolicyValue/` - Tool：既有 SQL Hit-rate Tool / DBeaver。 |

**原因：** 這些模式的第一份標註相關文件排名相同；單靠排名無法推論是哪項特徵造成命中。

### L5 — Knowledge Map 定位

**Query:** 契變保額異動後沒有進電訪。

**Expected card:** `api_contract_change.md`

**Keyword rank:** 1

**Vector rank:** 1

**Hybrid rank:** 1

**Hybrid Top 1:** 是

**Hybrid Top 3:** 是

**Best:** Keyword / Vector / Hybrid（並列）

#### Keyword Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/api_contract_change.md` | 常見問法 | 1.0000 | - 契變保額異動後沒有進電訪。 - 電訪案件沒產生要查哪裡？ - 契約變更需要電訪嗎？ - 金額異動卻沒有進 TeleCall。 - contract change telecall 規則在哪？ |
| 2 | `knowhow/incident_2025_policy_amount.md` | 常見問法 | 0.3333 | - 以前有沒有類似金額異常的 Incident？ - 歷史事故報告在哪？ - 批次或同步造成的問題怎麼回查？ - incident postmortem 要去哪找？ |
| 3 | `knowhow/audit_log.md` | 常見技術詞 | 0.1250 | audit log、操作紀錄、operator、trace id、資料異動、job log。 |
| 4 | `knowhow/data_repair_runbook.md` | 關鍵結論 | 0.1111 | - 卡片只定位變更紀錄，不保存實際修改內容。 - 欄位異動需以 Change Request 與核准附件為準。 |
| 5 | `knowhow/cv_stale_after_endorsement.md` | 常見問法 | 0.0909 | - 契變完成後畫面還是舊資料。 - CV 顯示前一天的值是快取嗎？ - 契變頁面沒有刷新怎麼查？ |

#### Vector Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/api_contract_change.md` | 常見問法 | 0.7947 | - 契變保額異動後沒有進電訪。 - 電訪案件沒產生要查哪裡？ - 契約變更需要電訪嗎？ - 金額異動卻沒有進 TeleCall。 - contract change telecall 規則在哪？ |
| 2 | `knowhow/customer_portal_cache.md` | 下一步 | 0.6783 | 請用 Copilot CLI 由 JSP/JS 找 API 與 Java controller，再追實際資料來源。 |
| 3 | `knowhow/premium_adjustment.md` | 常見技術詞 | 0.6717 | 保費、premium、adjustment、契變、endorsement、計費、effective date。 |
| 4 | `knowhow/contract_change.md` | 常見技術詞 | 0.6630 | 契變、契約變更、contract change、contract adjustment、endorsement、保價金、Cash Value、CV、現金價值。 |
| 5 | `knowhow/cv_stale_after_endorsement.md` | 下一步 | 0.6567 | 請先用 Copilot CLI 追畫面 API，再比對後端資料與快取時間。 |

#### Hybrid Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/api_contract_change.md` | 常見問法 | 1.0000 | - 契變保額異動後沒有進電訪。 - 電訪案件沒產生要查哪裡？ - 契約變更需要電訪嗎？ - 金額異動卻沒有進 TeleCall。 - contract change telecall 規則在哪？ |
| 2 | `knowhow/contract_change.md` | 常見技術詞 | 0.8591 | 契變、契約變更、contract change、contract adjustment、endorsement、保價金、Cash Value、CV、現金價值。 |
| 3 | `knowhow/premium_adjustment.md` | 常見技術詞 | 0.8460 | 保費、premium、adjustment、契變、endorsement、計費、effective date。 |
| 4 | `knowhow/cv_stale_after_endorsement.md` | 常見問法 | 0.8317 | - 契變完成後畫面還是舊資料。 - CV 顯示前一天的值是快取嗎？ - 契變頁面沒有刷新怎麼查？ |
| 5 | `knowhow/data_repair_runbook.md` | 關鍵結論 | 0.7893 | - 卡片只定位變更紀錄，不保存實際修改內容。 - 欄位異動需以 Change Request 與核准附件為準。 |

**原因：** 這些模式的第一份標註相關文件排名相同；單靠排名無法推論是哪項特徵造成命中。

### L6 — Knowledge Map 定位

**Query:** 電訪案件沒產生要查哪裡？

**Expected card:** `api_contract_change.md`

**Keyword rank:** 1

**Vector rank:** 1

**Hybrid rank:** 1

**Hybrid Top 1:** 是

**Hybrid Top 3:** 是

**Best:** Keyword / Vector / Hybrid（並列）

#### Keyword Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/api_contract_change.md` | 常見問法 | 1.0000 | - 契變保額異動後沒有進電訪。 - 電訪案件沒產生要查哪裡？ - 契約變更需要電訪嗎？ - 金額異動卻沒有進 TeleCall。 - contract change telecall 規則在哪？ |
| 2 | `knowhow/external_file_transfer.md` | 常見問法 | 0.2500 | - 外部檔案傳輸失敗要看哪裡？ - 檔案沒收到怎麼查？ - SFTP 傳輸規格在哪？ - 外部介接每日要檢查什麼？ |
| 3 | `knowhow/underwriting_rule.md` | 常見問法 | 0.2000 | - 核保規則文件在哪？ - 某個案件為什麼沒有通過？ - underwriting threshold 要去哪找？ |
| 4 | `knowhow/cash_value_recalculation.md` | 常見問法 | 0.1667 | - 保價金批次重新計算要看哪裡？ - CV 沒重新計算以前是不是遇過？ - 現金價值重算 JOB 是哪一支？ - cash value recalculation 失敗如何檢查？ |
| 5 | `knowhow/aml_screening.md` | 常見問法 | 0.1250 | - AML 相關系統文件在哪？ - AML 交易檢核規則要看哪份規格？ - screening batch 異常怎麼查？ - 可疑交易案件資料在哪？ |

#### Vector Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/api_contract_change.md` | 常見問法 | 0.7492 | - 契變保額異動後沒有進電訪。 - 電訪案件沒產生要查哪裡？ - 契約變更需要電訪嗎？ - 金額異動卻沒有進 TeleCall。 - contract change telecall 規則在哪？ |
| 2 | `knowhow/external_file_transfer.md` | 常見問法 | 0.6153 | - 外部檔案傳輸失敗要看哪裡？ - 檔案沒收到怎麼查？ - SFTP 傳輸規格在哪？ - 外部介接每日要檢查什麼？ |
| 3 | `knowhow/surrender_value.md` | 常見問法 | 0.5834 | - 解約金怎麼計算？ - surrender value 規格在哪？ - 解約後金額不對要看哪裡？ - 解約金和 Cash Value 有什麼關係？ |
| 4 | `knowhow/underwriting_rule.md` | 常見問法 | 0.5721 | - 核保規則文件在哪？ - 某個案件為什麼沒有通過？ - underwriting threshold 要去哪找？ |
| 5 | `knowhow/policy_loan.md` | 常見問法 | 0.5721 | - 保單借款規則文件在哪？ - POLICY_LOAN_AMT 在哪裡使用？ - 保單借款金額欄位怎麼查？ - policy loan 的 Java module 在哪？ |

#### Hybrid Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/api_contract_change.md` | 常見問法 | 1.0000 | - 契變保額異動後沒有進電訪。 - 電訪案件沒產生要查哪裡？ - 契約變更需要電訪嗎？ - 金額異動卻沒有進 TeleCall。 - contract change telecall 規則在哪？ |
| 2 | `knowhow/external_file_transfer.md` | 常見問法 | 0.9622 | - 外部檔案傳輸失敗要看哪裡？ - 檔案沒收到怎麼查？ - SFTP 傳輸規格在哪？ - 外部介接每日要檢查什麼？ |
| 3 | `knowhow/underwriting_rule.md` | 常見問法 | 0.9299 | - 核保規則文件在哪？ - 某個案件為什麼沒有通過？ - underwriting threshold 要去哪找？ |
| 4 | `knowhow/surrender_value.md` | 常見問法 | 0.9020 | - 解約金怎麼計算？ - surrender value 規格在哪？ - 解約後金額不對要看哪裡？ - 解約金和 Cash Value 有什麼關係？ |
| 5 | `knowhow/policy_loan.md` | 常見問法 | 0.8948 | - 保單借款規則文件在哪？ - POLICY_LOAN_AMT 在哪裡使用？ - 保單借款金額欄位怎麼查？ - policy loan 的 Java module 在哪？ |

**原因：** 這些模式的第一份標註相關文件排名相同；單靠排名無法推論是哪項特徵造成命中。

### L7 — Knowledge Map 定位

**Query:** 契變完成但保價金還是昨天的資料。

**Expected card:** `incident_cv_batch.md`

**Keyword rank:** 1

**Vector rank:** 2

**Hybrid rank:** 1

**Hybrid Top 1:** 是

**Hybrid Top 3:** 是

**Best:** Keyword / Hybrid（並列）

#### Keyword Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/incident_cv_batch.md` | 常見問法 | 1.0000 | - 契變完成但保價金還是昨天的資料。 - 契變做完後畫面金額還是舊的。 - contract adjustment 成功但 cash value 沒更新。 - CV calculation batch 沒跑嗎？ - 契變畫面金額怪怪的怎麼查？ |
| 2 | `knowhow/cv_stale_after_endorsement.md` | 常見問法 | 0.5000 | - 契變完成後畫面還是舊資料。 - CV 顯示前一天的值是快取嗎？ - 契變頁面沒有刷新怎麼查？ |
| 3 | `knowhow/contract_change.md` | 關鍵結論 | 0.3333 | - 契變完成不等同保價金已重算完成。 - 保價金處理需同時確認契變狀態與後續 batch。 |
| 4 | `knowhow/cash_value_recalculation.md` | 關鍵結論 | 0.1667 | - CV 重算通常以批次與 valuation date 為準。 - 異常時先確認是否有符合重算條件，再看 JOB 是否完成。 |
| 5 | `knowhow/policy_value_sync.md` | 關鍵結論 | 0.1111 | - 同步完成時間可能不同於主交易完成時間。 - 要以資料基準日與同步批號共同判斷。 |

#### Vector Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/contract_change.md` | 原始資料位置 | 0.7880 | - Word：`U:/Company/SPEC/ContractChange/CashValue_Impact_SPEC.docx` - Folder：`U:/Company/SPEC/ContractChange/` - SQL Folder：`U:/SQL/ContractChange/` |
| 2 | `knowhow/incident_cv_batch.md` | 常見問法 | 0.7845 | - 契變完成但保價金還是昨天的資料。 - 契變做完後畫面金額還是舊的。 - contract adjustment 成功但 cash value 沒更新。 - CV calculation batch 沒跑嗎？ - 契變畫面金額怪怪的怎麼查？ |
| 3 | `knowhow/oracle_table_reference.md` | 常見問法 | 0.7594 | - 契變資料 Table 在哪？ - POLICY_LOAN_AMT 屬於哪張表？ - 保價金欄位可能在哪？ |
| 4 | `knowhow/sql_query_practices.md` | 常見技術詞 | 0.7487 | SQL、Table、Column、DBeaver、query、契變、保價金、Cash Value、CV。 |
| 5 | `knowhow/cv_stale_after_endorsement.md` | 常見問法 | 0.7375 | - 契變完成後畫面還是舊資料。 - CV 顯示前一天的值是快取嗎？ - 契變頁面沒有刷新怎麼查？ |

#### Hybrid Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/incident_cv_batch.md` | 常見問法 | 1.0000 | - 契變完成但保價金還是昨天的資料。 - 契變做完後畫面金額還是舊的。 - contract adjustment 成功但 cash value 沒更新。 - CV calculation batch 沒跑嗎？ - 契變畫面金額怪怪的怎麼查？ |
| 2 | `knowhow/contract_change.md` | 原始資料位置 | 0.9529 | - Word：`U:/Company/SPEC/ContractChange/CashValue_Impact_SPEC.docx` - Folder：`U:/Company/SPEC/ContractChange/` - SQL Folder：`U:/SQL/ContractChange/` |
| 3 | `knowhow/cv_stale_after_endorsement.md` | 常見問法 | 0.9409 | - 契變完成後畫面還是舊資料。 - CV 顯示前一天的值是快取嗎？ - 契變頁面沒有刷新怎麼查？ |
| 4 | `knowhow/oracle_table_reference.md` | 常見問法 | 0.9196 | - 契變資料 Table 在哪？ - POLICY_LOAN_AMT 屬於哪張表？ - 保價金欄位可能在哪？ |
| 5 | `knowhow/sql_query_practices.md` | 常見技術詞 | 0.8975 | SQL、Table、Column、DBeaver、query、契變、保價金、Cash Value、CV。 |

**原因：** 這些模式的第一份標註相關文件排名相同；單靠排名無法推論是哪項特徵造成命中。

### L8 — Knowledge Map 定位

**Query:** CV 沒重新計算以前是不是遇過？

**Expected card:** `incident_cv_batch.md`, `cash_value_recalculation.md`

**Keyword rank:** 1

**Vector rank:** 1

**Hybrid rank:** 1

**Hybrid Top 1:** 是

**Hybrid Top 3:** 是

**Best:** Keyword / Vector / Hybrid（並列）

#### Keyword Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/cash_value_recalculation.md` | 常見問法 | 1.0000 | - 保價金批次重新計算要看哪裡？ - CV 沒重新計算以前是不是遇過？ - 現金價值重算 JOB 是哪一支？ - cash value recalculation 失敗如何檢查？ |
| 2 | `knowhow/data_repair_runbook.md` | 常見問法 | 0.5000 | - 以前那張資料變更單在哪裡？ - 以前是不是改過某個 Table 欄位？ - 誰改過這筆資料？ - Data Change 或 CR 紀錄在哪？ - 資料修改單怎麼查？ |
| 3 | `knowhow/surrender_value.md` | 關鍵結論 | 0.3333 | - 解約金與保價金相關但不是同一個欄位概念。 - 查詢前應確認保單狀態與計算基準日。 |
| 4 | `knowhow/incident_2025_policy_amount.md` | 常見問法 | 0.1429 | - 以前有沒有類似金額異常的 Incident？ - 歷史事故報告在哪？ - 批次或同步造成的問題怎麼回查？ - incident postmortem 要去哪找？ |
| 5 | `knowhow/cv_stale_after_endorsement.md` | 常見問法 | 0.1111 | - 契變完成後畫面還是舊資料。 - CV 顯示前一天的值是快取嗎？ - 契變頁面沒有刷新怎麼查？ |

#### Vector Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/cash_value_recalculation.md` | 常見問法 | 0.8013 | - 保價金批次重新計算要看哪裡？ - CV 沒重新計算以前是不是遇過？ - 現金價值重算 JOB 是哪一支？ - cash value recalculation 失敗如何檢查？ |
| 2 | `knowhow/incident_cv_batch.md` | 常見技術詞 | 0.6895 | CV、cash value、保價金、現金價值、recalculation、previous day、batch、contract adjustment。 |
| 3 | `knowhow/contract_change.md` | 下一步 | 0.6704 | 請讓 Copilot Chat 讀完整規格，再依實際變更類型判斷是否需重算。 |
| 4 | `knowhow/cv_stale_after_endorsement.md` | 常見技術詞 | 0.6322 | 契變、endorsement、CV、舊值、cache、API、畫面刷新、資料同步。 |
| 5 | `knowhow/sql_query_practices.md` | 常見技術詞 | 0.6293 | SQL、Table、Column、DBeaver、query、契變、保價金、Cash Value、CV。 |

#### Hybrid Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/cash_value_recalculation.md` | 常見問法 | 1.0000 | - 保價金批次重新計算要看哪裡？ - CV 沒重新計算以前是不是遇過？ - 現金價值重算 JOB 是哪一支？ - cash value recalculation 失敗如何檢查？ |
| 2 | `knowhow/incident_cv_batch.md` | 常見技術詞 | 0.8847 | CV、cash value、保價金、現金價值、recalculation、previous day、batch、contract adjustment。 |
| 3 | `knowhow/surrender_value.md` | 用途 | 0.8446 | 定位解約金計算規格、保價金關聯與查詢入口。 |
| 4 | `knowhow/contract_change.md` | 下一步 | 0.8367 | 請讓 Copilot Chat 讀完整規格，再依實際變更類型判斷是否需重算。 |
| 5 | `knowhow/cv_stale_after_endorsement.md` | 常見技術詞 | 0.8252 | 契變、endorsement、CV、舊值、cache、API、畫面刷新、資料同步。 |

**原因：** 這些模式的第一份標註相關文件排名相同；單靠排名無法推論是哪項特徵造成命中。

### L9 — Knowledge Map 定位

**Query:** 外部檔案失敗後要找哪份重送 SOP？

**Expected card:** `batch_processing.md`

**Keyword rank:** 1

**Vector rank:** 1

**Hybrid rank:** 1

**Hybrid Top 1:** 是

**Hybrid Top 3:** 是

**Best:** Keyword / Vector / Hybrid（並列）

#### Keyword Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/batch_processing.md` | 常見問法 | 1.0000 | - 外部檔案失敗後要找哪份重送 SOP？ - 檔案可以重送嗎？ - SFTP failed 要怎麼 resend？ - 重送後如何確認對方已收到？ |
| 2 | `knowhow/external_file_transfer.md` | 關鍵結論 | 0.2500 | - 先分辨是來源未產檔、傳輸失敗或接收端驗證失敗。 - 不要在未確認重複風險前手動重送。 |
| 3 | `knowhow/batch_retry.md` | 用途 | 0.0769 | 定位批次失敗後的 retry 原則、相依工作與重跑前檢查。 |
| 4 | `knowhow/batch_monitoring.md` | 常見問法 | 0.0667 | - 批次值日生每天要做什麼？ - 每天晚上 JOB 要檢查什麼？ - Batch 掛掉要看哪份 SOP？ - 值班人員交接文件在哪？ - Batch Monitoring 的 SOP 在哪？ |
| 5 | `knowhow/cash_value_recalculation.md` | 常見問法 | 0.0625 | - 保價金批次重新計算要看哪裡？ - CV 沒重新計算以前是不是遇過？ - 現金價值重算 JOB 是哪一支？ - cash value recalculation 失敗如何檢查？ |

#### Vector Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/batch_processing.md` | 常見問法 | 0.8118 | - 外部檔案失敗後要找哪份重送 SOP？ - 檔案可以重送嗎？ - SFTP failed 要怎麼 resend？ - 重送後如何確認對方已收到？ |
| 2 | `knowhow/external_file_transfer.md` | 關鍵結論 | 0.6949 | - 先分辨是來源未產檔、傳輸失敗或接收端驗證失敗。 - 不要在未確認重複風險前手動重送。 |
| 3 | `knowhow/batch_retry.md` | 常見技術詞 | 0.6370 | Batch Retry、restart、rerun、job dependency、補跑、重跑、rollback。 |
| 4 | `knowhow/batch_monitoring.md` | 常見問法 | 0.5989 | - 批次值日生每天要做什麼？ - 每天晚上 JOB 要檢查什麼？ - Batch 掛掉要看哪份 SOP？ - 值班人員交接文件在哪？ - Batch Monitoring 的 SOP 在哪？ |
| 5 | `knowhow/audit_log.md` | 常見問法 | 0.5740 | - 誰改過這筆資料？ - 操作紀錄要去哪找？ - batch 執行歷程怎麼看？ |

#### Hybrid Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/batch_processing.md` | 常見問法 | 1.0000 | - 外部檔案失敗後要找哪份重送 SOP？ - 檔案可以重送嗎？ - SFTP failed 要怎麼 resend？ - 重送後如何確認對方已收到？ |
| 2 | `knowhow/external_file_transfer.md` | 關鍵結論 | 0.9443 | - 先分辨是來源未產檔、傳輸失敗或接收端驗證失敗。 - 不要在未確認重複風險前手動重送。 |
| 3 | `knowhow/batch_retry.md` | 常見問法 | 0.8526 | - 批次失敗可以直接重跑嗎？ - Batch Retry 前要確認什麼？ - 重跑造成金額異常要看哪裡？ - 哪些 JOB 有前後相依？ |
| 4 | `knowhow/batch_monitoring.md` | 常見問法 | 0.8069 | - 批次值日生每天要做什麼？ - 每天晚上 JOB 要檢查什麼？ - Batch 掛掉要看哪份 SOP？ - 值班人員交接文件在哪？ - Batch Monitoring 的 SOP 在哪？ |
| 5 | `knowhow/aml_screening.md` | 常見問法 | 0.7744 | - AML 相關系統文件在哪？ - AML 交易檢核規則要看哪份規格？ - screening batch 異常怎麼查？ - 可疑交易案件資料在哪？ |

**原因：** 這些模式的第一份標註相關文件排名相同；單靠排名無法推論是哪項特徵造成命中。

### L10 — Knowledge Map 定位

**Query:** 契變畫面的 JSP / JS 在哪？

**Expected card:** `customer_portal_cache.md`

**Keyword rank:** 1

**Vector rank:** 1

**Hybrid rank:** 1

**Hybrid Top 1:** 是

**Hybrid Top 3:** 是

**Best:** Keyword / Vector / Hybrid（並列）

#### Keyword Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/customer_portal_cache.md` | 常見問法 | 1.0000 | - 契變畫面的 JSP / JS 在哪？ - contract change 前端頁面在哪個 module？ - 契變金額畫面由哪裡查出來？ - endorsement screen 欄位怎麼找？ |
| 2 | `knowhow/cv_stale_after_endorsement.md` | 原始資料位置 | 0.1667 | - Word：`U:/Company/Incident/INC_ENDORSEMENT_STALE_SCREEN.docx` - JSP：`D:/workspace/contract-change/web/contractChange.jsp` - JS：`D:/workspace/contract-change/web/contractChange.js` |
| 3 | `knowhow/policy_value_sync.md` | 常見問法 | 0.0769 | - 保單價值同步在哪裡做？ - Cash Value 更新後畫面何時會看到？ - value sync 異常怎麼查？ |
| 4 | `knowhow/incident_cv_batch.md` | 常見問法 | 0.0714 | - 契變完成但保價金還是昨天的資料。 - 契變做完後畫面金額還是舊的。 - contract adjustment 成功但 cash value 沒更新。 - CV calculation batch 沒跑嗎？ - 契變畫面金額怪怪的怎麼查？ |
| 5 | `knowhow/api_contract_change.md` | 原始資料位置 | 0.0667 | - Word：`U:/Company/SPEC/ContractChange/TeleCall_SPEC.docx` - Java：`D:/workspace/contract-change/src/TeleCallRuleService.java` - JSP：`D:/workspace/contract-change/web/teleCall.jsp`… |

#### Vector Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/customer_portal_cache.md` | 常見技術詞 | 0.8052 | 契變畫面、contract change、endorsement、JSP、JS、screen、controller、欄位。 |
| 2 | `knowhow/cv_stale_after_endorsement.md` | 原始資料位置 | 0.7279 | - Word：`U:/Company/Incident/INC_ENDORSEMENT_STALE_SCREEN.docx` - JSP：`D:/workspace/contract-change/web/contractChange.jsp` - JS：`D:/workspace/contract-change/web/contractChange.js` |
| 3 | `knowhow/premium_adjustment.md` | 常見技術詞 | 0.7143 | 保費、premium、adjustment、契變、endorsement、計費、effective date。 |
| 4 | `knowhow/api_contract_change.md` | 常見技術詞 | 0.7129 | 電訪、電話訪問、TeleCall、Interview、Outbound Call、threshold、amount、change_type。 |
| 5 | `knowhow/java_service_layer.md` | 常見問法 | 0.7096 | - 契變的 Java Service 在哪？ - contract change 後端 module 怎麼找？ - 想追 API 呼叫到哪個 service？ |

#### Hybrid Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/customer_portal_cache.md` | 常見問法 | 1.0000 | - 契變畫面的 JSP / JS 在哪？ - contract change 前端頁面在哪個 module？ - 契變金額畫面由哪裡查出來？ - endorsement screen 欄位怎麼找？ |
| 2 | `knowhow/cv_stale_after_endorsement.md` | 原始資料位置 | 0.9333 | - Word：`U:/Company/Incident/INC_ENDORSEMENT_STALE_SCREEN.docx` - JSP：`D:/workspace/contract-change/web/contractChange.jsp` - JS：`D:/workspace/contract-change/web/contractChange.js` |
| 3 | `knowhow/java_service_layer.md` | 常見問法 | 0.8252 | - 契變的 Java Service 在哪？ - contract change 後端 module 怎麼找？ - 想追 API 呼叫到哪個 service？ |
| 4 | `knowhow/api_contract_change.md` | 關鍵結論 | 0.8127 | - 是否產生電訪取決於 change_type 與金額門檻。 - 規格、Java 與前端欄位需一起比對，不能只看單一畫面。 |
| 5 | `knowhow/premium_adjustment.md` | 常見技術詞 | 0.7768 | 保費、premium、adjustment、契變、endorsement、計費、effective date。 |

**原因：** 這些模式的第一份標註相關文件排名相同；單靠排名無法推論是哪項特徵造成命中。

### L11 — Knowledge Map 定位

**Query:** 契變相關 SQL 要去哪找？

**Expected card:** `sql_query_practices.md`, `contract_change.md`

**Keyword rank:** 1

**Vector rank:** 1

**Hybrid rank:** 1

**Hybrid Top 1:** 是

**Hybrid Top 3:** 是

**Best:** Keyword / Vector / Hybrid（並列）

#### Keyword Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/sql_query_practices.md` | 常見問法 | 1.0000 | - 契變相關 SQL 要去哪找？ - 保價金的 Table 或 Column 可能在哪？ - SQL 查詢入口在哪？ - 想查歷史資料要看哪個資料夾？ |
| 2 | `knowhow/underwriting_rule.md` | 常見問法 | 0.5000 | - 核保規則文件在哪？ - 某個案件為什麼沒有通過？ - underwriting threshold 要去哪找？ |
| 3 | `knowhow/audit_log.md` | 常見問法 | 0.3333 | - 誰改過這筆資料？ - 操作紀錄要去哪找？ - batch 執行歷程怎麼看？ |
| 4 | `knowhow/release_checklist.md` | 常見問法 | 0.2500 | - 系統規格文件在哪？ - SA 文件要去哪找？ - 某功能的設計書或 API spec 在哪？ - 上線版本的規格怎麼追？ |
| 5 | `knowhow/incident_2025_policy_amount.md` | 常見問法 | 0.2000 | - 以前有沒有類似金額異常的 Incident？ - 歷史事故報告在哪？ - 批次或同步造成的問題怎麼回查？ - incident postmortem 要去哪找？ |

#### Vector Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/sql_query_practices.md` | 常見問法 | 0.7869 | - 契變相關 SQL 要去哪找？ - 保價金的 Table 或 Column 可能在哪？ - SQL 查詢入口在哪？ - 想查歷史資料要看哪個資料夾？ |
| 2 | `knowhow/java_service_layer.md` | 下一步 | 0.7688 | 請用 Copilot CLI 在既有 repository 搜尋 method、caller、callee 與 SQL。 |
| 3 | `knowhow/oracle_table_reference.md` | 常見技術詞 | 0.7304 | Oracle、Table、Column、data dictionary、POLICY_LOAN_AMT、Cash Value、契變。 |
| 4 | `knowhow/api_contract_change.md` | 下一步 | 0.7226 | 請用 Copilot CLI 從 TeleCallRuleService 追規則、呼叫端與 SQL；再以規格確認門檻。 |
| 5 | `knowhow/data_repair_runbook.md` | 下一步 | 0.7158 | 請用 Copilot Chat 讀 Excel/Word 原始紀錄，依 Table、Column、日期與申請單號追查。 |

#### Hybrid Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/sql_query_practices.md` | 常見問法 | 1.0000 | - 契變相關 SQL 要去哪找？ - 保價金的 Table 或 Column 可能在哪？ - SQL 查詢入口在哪？ - 想查歷史資料要看哪個資料夾？ |
| 2 | `knowhow/java_service_layer.md` | 下一步 | 0.8843 | 請用 Copilot CLI 在既有 repository 搜尋 method、caller、callee 與 SQL。 |
| 3 | `knowhow/api_contract_change.md` | 下一步 | 0.8501 | 請用 Copilot CLI 從 TeleCallRuleService 追規則、呼叫端與 SQL；再以規格確認門檻。 |
| 4 | `knowhow/premium_adjustment.md` | 用途 | 0.8395 | 定位保費調整規則、契變影響與相關資料查詢入口。 |
| 5 | `knowhow/contract_change.md` | 原始資料位置 | 0.8133 | - Word：`U:/Company/SPEC/ContractChange/CashValue_Impact_SPEC.docx` - Folder：`U:/Company/SPEC/ContractChange/` - SQL Folder：`U:/SQL/ContractChange/` |

**原因：** 這些模式的第一份標註相關文件排名相同；單靠排名無法推論是哪項特徵造成命中。

### L12 — Knowledge Map 定位

**Query:** AML 相關系統文件在哪？

**Expected card:** `aml_screening.md`

**Keyword rank:** 1

**Vector rank:** 1

**Hybrid rank:** 1

**Hybrid Top 1:** 是

**Hybrid Top 3:** 是

**Best:** Keyword / Vector / Hybrid（並列）

#### Keyword Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/aml_screening.md` | 常見問法 | 1.0000 | - AML 相關系統文件在哪？ - AML 交易檢核規則要看哪份規格？ - screening batch 異常怎麼查？ - 可疑交易案件資料在哪？ |
| 2 | `knowhow/release_checklist.md` | 常見問法 | 0.5000 | - 系統規格文件在哪？ - SA 文件要去哪找？ - 某功能的設計書或 API spec 在哪？ - 上線版本的規格怎麼追？ |
| 3 | `knowhow/underwriting_rule.md` | 常見問法 | 0.1250 | - 核保規則文件在哪？ - 某個案件為什麼沒有通過？ - underwriting threshold 要去哪找？ |
| 4 | `knowhow/policy_loan.md` | 常見問法 | 0.1111 | - 保單借款規則文件在哪？ - POLICY_LOAN_AMT 在哪裡使用？ - 保單借款金額欄位怎麼查？ - policy loan 的 Java module 在哪？ |
| 5 | `knowhow/batch_monitoring.md` | 常見問法 | 0.1000 | - 批次值日生每天要做什麼？ - 每天晚上 JOB 要檢查什麼？ - Batch 掛掉要看哪份 SOP？ - 值班人員交接文件在哪？ - Batch Monitoring 的 SOP 在哪？ |

#### Vector Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/aml_screening.md` | 常見問法 | 0.7998 | - AML 相關系統文件在哪？ - AML 交易檢核規則要看哪份規格？ - screening batch 異常怎麼查？ - 可疑交易案件資料在哪？ |
| 2 | `knowhow/release_checklist.md` | 常見問法 | 0.6198 | - 系統規格文件在哪？ - SA 文件要去哪找？ - 某功能的設計書或 API spec 在哪？ - 上線版本的規格怎麼追？ |
| 3 | `knowhow/policy_loan.md` | 常見問法 | 0.5938 | - 保單借款規則文件在哪？ - POLICY_LOAN_AMT 在哪裡使用？ - 保單借款金額欄位怎麼查？ - policy loan 的 Java module 在哪？ |
| 4 | `knowhow/underwriting_rule.md` | 常見問法 | 0.5787 | - 核保規則文件在哪？ - 某個案件為什麼沒有通過？ - underwriting threshold 要去哪找？ |
| 5 | `knowhow/audit_log.md` | 關鍵結論 | 0.5696 | - 查核需保留時間範圍、操作人與 trace id。 - 正式稽核紀錄以原始系統為準。 |

#### Hybrid Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/aml_screening.md` | 常見問法 | 1.0000 | - AML 相關系統文件在哪？ - AML 交易檢核規則要看哪份規格？ - screening batch 異常怎麼查？ - 可疑交易案件資料在哪？ |
| 2 | `knowhow/release_checklist.md` | 常見問法 | 0.9481 | - 系統規格文件在哪？ - SA 文件要去哪找？ - 某功能的設計書或 API spec 在哪？ - 上線版本的規格怎麼追？ |
| 3 | `knowhow/policy_loan.md` | 常見問法 | 0.8691 | - 保單借款規則文件在哪？ - POLICY_LOAN_AMT 在哪裡使用？ - 保單借款金額欄位怎麼查？ - policy loan 的 Java module 在哪？ |
| 4 | `knowhow/underwriting_rule.md` | 常見問法 | 0.8534 | - 核保規則文件在哪？ - 某個案件為什麼沒有通過？ - underwriting threshold 要去哪找？ |
| 5 | `knowhow/payment_reconciliation.md` | 常見問法 | 0.8252 | - 銀行入帳時應收相關內容在哪？ - 收款與應收對不起來怎麼查？ - payment reconciliation SOP 在哪？ |

**原因：** 這些模式的第一份標註相關文件排名相同；單靠排名無法推論是哪項特徵造成命中。

## Interpretation

這是沒有使用大型語言模型或雲端 embedding API 的本機 baseline。Hybrid 使用 RRF 合併 BM25 與 vector rank，沒有直接相加兩種不可比的原始分數。
若之後接入 sentence-transformers 或公司內部 embedding API，應保留同一份評估查詢重新比較；這份報告不能宣稱 hashing vector 等同於 transformer embedding。


## Document-level metrics

| Mode | Hit@5 | MRR@5 |
|---|---:|---:|
| keyword | 1.000 | 1.000 |
| vector | 1.000 | 0.958 |
| hybrid | 1.000 | 1.000 |

## 無答案查詢檢查

下列問題在合成 Know-how 無對應答案；數字是回傳候選數，越多不代表越好。尚未用公司題庫校準門檻。

| Query | Keyword | Vector | Hybrid |
|---|---:|---:|---:|
| 火星探測器如何校正軌道 | 5 | 5 | 5 |
| 義大利麵食譜番茄醬比例 | 5 | 5 | 5 |
| 蘭花葉片枯黃如何施肥 | 5 | 5 | 5 |