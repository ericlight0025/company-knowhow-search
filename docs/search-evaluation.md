# Search Evaluation

> 這份報告由 `python evaluate.py` 實際執行產生。Relevant file 是 POC 的人工標註，排名以主要案例第一次出現在 Top 5 的位置衡量。

## Summary

> 三種模式使用相同候選上限，按完整檔案路徑去重後比較 Top 5。平均排名僅限命中題；判斷品質請同時看 Hit@5 與 MRR。這是合成資料的開發集，不是獨立測試集。

| Metric | Value |
|---|---:|
| Query count | 10 |
| Keyword best or tied | 8 |
| Vector best or tied | 9 |
| Hybrid best or tied | 8 |
| Keyword unique winner | 1 |
| Vector unique winner | 1 |
| Hybrid unique winner | 0 |
| Keyword Top 1 relevant | 7 |
| Vector Top 1 relevant | 9 |
| Hybrid Top 1 relevant | 8 |
| Keyword average first relevant rank | 1.50 |
| Vector average first relevant rank | 1.30 |
| Hybrid average first relevant rank | 1.30 |
| No relevant result in Top 5 | 0 |

### First relevant rank

| ID | Category | Query | Keyword | Vector | Hybrid | Best |
|---|---|---|---:|---:|---:|---|
| A1 | 精準 keyword | POLICY_LOAN_AMT 在哪裡使用？ | 1 | 1 | 1 | Keyword / Vector / Hybrid（並列） |
| A2 | 精準 keyword | AML screening batch risk level | 1 | 1 | 1 | Keyword / Vector / Hybrid（並列） |
| A3 | 精準 keyword | POLICY_CONTRACT_CHANGE API callback | 1 | 1 | 1 | Keyword / Vector / Hybrid（並列） |
| A4 | 精準 keyword | PAYMENT_RECONCILIATION settlement amount mismatch | 1 | 1 | 1 | Keyword / Vector / Hybrid（並列） |
| B1 | 半模糊 | 保價金批次重新計算 | 1 | 1 | 1 | Keyword / Vector / Hybrid（並列） |
| B2 | 半模糊 | 保單借款金額欄位查詢 | 1 | 1 | 1 | Keyword / Vector / Hybrid（並列） |
| B3 | 半模糊 | 外部檔案傳輸失敗重送 | 1 | 1 | 1 | Keyword / Vector / Hybrid（並列） |
| C1 | 高度模糊 semantic | 客戶說改完保單後前台還是之前的數字，可能排程晚了 | 4 | 1 | 2 | Vector |
| C2 | 高度模糊 semantic | 有人說資料修正後，部分保單的金額被重複計算，應該怎麼查？ | 2 | 1 | 1 | Vector / Hybrid（並列） |
| C3 | 高度模糊 semantic | 新規則上線後 API 與資料庫寫入順序造成保單資料不一致 | 2 | 4 | 3 | Keyword |

## Detailed Results

### A1 — 精準 keyword

**Query:** POLICY_LOAN_AMT 在哪裡使用？

**Expected files:** `policy_loan.md`, `oracle_table_reference.md`

**Keyword first relevant rank:** 1

**Vector first relevant rank:** 1

**Hybrid first relevant rank:** 1

**Best:** Keyword / Vector / Hybrid（並列）

#### Keyword Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/policy_loan.md` | Field usage | 1.0000 | POLICY_LOAN_AMT 是保單借款目前未清償的本金欄位，主要使用於 loan quotation、利息計算、解約金試算與 customer portal summary。查詢時通常需要搭配 POLICY_ID、LOAN_STATUS 與 AS_OF_DATE。 |
| 2 | `knowhow/oracle_table_reference.md` | Useful columns | 0.5000 | 查詢金額問題時，常用 POLICY_ID、POLICY_VERSION、EFFECTIVE_DATE、CASH_VALUE、SURRENDER_VALUE、POLICY_LOAN_AMT、CALCULATION_VERSION 與 LAST_CALCULATED_AT。欄位名稱可能在 Java DTO 使用 camelCase，但 database 使用… |
| 3 | `knowhow/customer_portal_cache.md` | Cache behavior | 0.1667 | 前台 portal 會快取 policy summary、cash value 與 loan balance，以降低查詢主系統的頻率。cache key 必須包含 policy id 與 policy version，不能只使用 policy id。 |
| 4 | `knowhow/aml_screening.md` | Troubleshooting | 0.1429 | 查詢 AML screening 結果時，確認 batch run id、watchlist version、risk level、match score 與 exception reason。若重跑，必須使用相同的 business date 並保留原始結果與 audit trail。 |
| 5 | `knowhow/api_contract_change.md` | Callback and event | 0.1250 | 完成後會送出 POLICY_CONTRACT_CHANGE event；部分整合客戶仍使用 callback。若 callback timeout，producer 應保留 delivery status 並進入 retry，而不是重建一筆新的契約變更。 |

#### Vector Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/policy_loan.md` | Field usage | 0.6281 | POLICY_LOAN_AMT 是保單借款目前未清償的本金欄位，主要使用於 loan quotation、利息計算、解約金試算與 customer portal summary。查詢時通常需要搭配 POLICY_ID、LOAN_STATUS 與 AS_OF_DATE。 |
| 2 | `knowhow/oracle_table_reference.md` | Useful columns | 0.6277 | 查詢金額問題時，常用 POLICY_ID、POLICY_VERSION、EFFECTIVE_DATE、CASH_VALUE、SURRENDER_VALUE、POLICY_LOAN_AMT、CALCULATION_VERSION 與 LAST_CALCULATED_AT。欄位名稱可能在 Java DTO 使用 camelCase，但 database 使用… |
| 3 | `knowhow/customer_portal_cache.md` | Cache behavior | 0.6016 | 前台 portal 會快取 policy summary、cash value 與 loan balance，以降低查詢主系統的頻率。cache key 必須包含 policy id 與 policy version，不能只使用 policy id。 |
| 4 | `knowhow/java_service_layer.md` | Common bug | 0.5995 | 如果 service 在 transaction commit 前就 publish event，consumer 可能查不到新的 policy version，造成 calculation 使用舊資料。另一種常見問題是 API 回傳 success 後才非同步執行 batch，前台因此短時間顯示 previous value。 |
| 5 | `knowhow/external_file_transfer.md` | Failure and resend | 0.5743 | 若外部檔案傳輸失敗，先區分 authentication error、network timeout、remote disk full 與檔案格式錯誤。可重送的項目要使用相同 file id 與 idempotency key，避免合作方收到兩份相同檔案。 |

#### Hybrid Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/policy_loan.md` | Field usage | 1.0000 | POLICY_LOAN_AMT 是保單借款目前未清償的本金欄位，主要使用於 loan quotation、利息計算、解約金試算與 customer portal summary。查詢時通常需要搭配 POLICY_ID、LOAN_STATUS 與 AS_OF_DATE。 |
| 2 | `knowhow/oracle_table_reference.md` | Useful columns | 0.9839 | 查詢金額問題時，常用 POLICY_ID、POLICY_VERSION、EFFECTIVE_DATE、CASH_VALUE、SURRENDER_VALUE、POLICY_LOAN_AMT、CALCULATION_VERSION 與 LAST_CALCULATED_AT。欄位名稱可能在 Java DTO 使用 camelCase，但 database 使用… |
| 3 | `knowhow/customer_portal_cache.md` | Cache behavior | 0.9328 | 前台 portal 會快取 policy summary、cash value 與 loan balance，以降低查詢主系統的頻率。cache key 必須包含 policy id 與 policy version，不能只使用 policy id。 |
| 4 | `knowhow/aml_screening.md` | Troubleshooting | 0.8797 | 查詢 AML screening 結果時，確認 batch run id、watchlist version、risk level、match score 與 exception reason。若重跑，必須使用相同的 business date 並保留原始結果與 audit trail。 |
| 5 | `knowhow/external_file_transfer.md` | Failure and resend | 0.8760 | 若外部檔案傳輸失敗，先區分 authentication error、network timeout、remote disk full 與檔案格式錯誤。可重送的項目要使用相同 file id 與 idempotency key，避免合作方收到兩份相同檔案。 |

**原因：** 這些模式的第一份標註相關文件排名相同；單靠排名無法推論是哪項特徵造成命中。

### A2 — 精準 keyword

**Query:** AML screening batch risk level

**Expected files:** `aml_screening.md`

**Keyword first relevant rank:** 1

**Vector first relevant rank:** 1

**Hybrid first relevant rank:** 1

**Best:** Keyword / Vector / Hybrid（並列）

#### Keyword Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/aml_screening.md` | Troubleshooting | 1.0000 | 查詢 AML screening 結果時，確認 batch run id、watchlist version、risk level、match score 與 exception reason。若重跑，必須使用相同的 business date 並保留原始結果與 audit trail。 |
| 2 | `knowhow/batch_monitoring.md` | Key metrics | 0.2500 | 每個 batch dashboard 至少要顯示 run id、business date、queued、running、success、failed、retrying 與 stuck count。金額計算類批次還要顯示 input policy count、processed count 與 output amount total。 |
| 3 | `knowhow/batch_retry.md` | Incident handling | 0.1429 | 常見描述包括「以前有一個批次失敗後重跑造成金額不一致」、「batch retry 後同一筆資料被算兩次」或「補跑之後畫面才恢復」。完成 rerun 後要比對原始輸入、calculation version 與 audit log。 |
| 4 | `knowhow/payment_reconciliation.md` | Batch recovery | 0.1000 | 對帳 batch 失敗後要以 file id 與 business date 進行 controlled rerun，並確認已成功的 payment 不會再次入帳。所有差異要進 exception queue 供財務複核。 |
| 5 | `knowhow/batch_processing.md` | Monitoring | 0.0909 | 監控項目包含 queue depth、success rate、平均處理時間、retry count、stuck execution 與最後成功 business date。若 calculation batch 沒有完成，應先確認 upstream contract event 是否已送出。 |

#### Vector Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/aml_screening.md` | Scope | 0.7695 | AML（anti-money laundering）screening batch 每日依 customer、policy、payment 與 beneficiary data 執行風險篩檢。結果會產生 risk level、screening status 與 review queue，供合規人員人工複核。 |
| 2 | `knowhow/batch_monitoring.md` | Alert rules | 0.6372 | 當最後成功時間超過 SLA、failed ratio 超標、queue depth 持續增加或 calculation version 落後時告警。告警訊息要包含 execution id 與可直接查詢的 correlation id。 |
| 3 | `knowhow/customer_portal_cache.md` | Safe invalidation | 0.6129 | 只有在新 calculation version 已 commit 且 read model 已更新後才清除 cache。直接清 cache 可以暫時掩蓋問題，但不能取代 batch、event 或資料庫一致性檢查。 |
| 4 | `knowhow/audit_log.md` | Search example | 0.6101 | 排查契約變更與金額問題時，先以 policy id 和 correlation id 找到 API request，再沿著 transaction、event、batch execution、calculation version 查詢。 |
| 5 | `knowhow/api_contract_change.md` | Compatibility | 0.6046 | 新增欄位要維持 backward compatibility，enum 變更要先確認 Java client 與 batch consumer。Incident 排查可用 requestId、changeId、eventId 串起 API、database 與 downstream job。 |

#### Hybrid Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/aml_screening.md` | Scope | 1.0000 | AML（anti-money laundering）screening batch 每日依 customer、policy、payment 與 beneficiary data 執行風險篩檢。結果會產生 risk level、screening status 與 review queue，供合規人員人工複核。 |
| 2 | `knowhow/batch_monitoring.md` | Key metrics | 0.9505 | 每個 batch dashboard 至少要顯示 run id、business date、queued、running、success、failed、retrying 與 stuck count。金額計算類批次還要顯示 input policy count、processed count 與 output amount total。 |
| 3 | `knowhow/api_contract_change.md` | Compatibility | 0.8649 | 新增欄位要維持 backward compatibility，enum 變更要先確認 Java client 與 batch consumer。Incident 排查可用 requestId、changeId、eventId 串起 API、database 與 downstream job。 |
| 4 | `knowhow/audit_log.md` | Search example | 0.8647 | 排查契約變更與金額問題時，先以 policy id 和 correlation id 找到 API request，再沿著 transaction、event、batch execution、calculation version 查詢。 |
| 5 | `knowhow/customer_portal_cache.md` | Safe invalidation | 0.8576 | 只有在新 calculation version 已 commit 且 read model 已更新後才清除 cache。直接清 cache 可以暫時掩蓋問題，但不能取代 batch、event 或資料庫一致性檢查。 |

**原因：** 這些模式的第一份標註相關文件排名相同；單靠排名無法推論是哪項特徵造成命中。

### A3 — 精準 keyword

**Query:** POLICY_CONTRACT_CHANGE API callback

**Expected files:** `api_contract_change.md`, `contract_change.md`

**Keyword first relevant rank:** 1

**Vector first relevant rank:** 1

**Hybrid first relevant rank:** 1

**Best:** Keyword / Vector / Hybrid（並列）

#### Keyword Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/api_contract_change.md` | Callback and event | 1.0000 | 完成後會送出 POLICY_CONTRACT_CHANGE event；部分整合客戶仍使用 callback。若 callback timeout，producer 應保留 delivery status 並進入 retry，而不是重建一筆新的契約變更。 |
| 2 | `knowhow/contract_change.md` | Important fields | 0.5000 | POLICY_CONTRACT_CHANGE.CHANGE_ID 是此次異動的識別碼，EFFECTIVE_DATE 決定生效日，CHANGE_STATUS 會經過 RECEIVED、VALIDATED、COMPLETED。若只看到 API 回應成功，不代表 downstream calculation 已完成。 |
| 3 | `knowhow/incident_cv_batch.md` | Root cause | 0.3333 | Contract adjustment service 只更新 POLICY_CONTRACT_CHANGE 與保單主檔，沒有同步等待 CV recalculation job。當 batch queue 堵塞或 job status 不是 SUCCESS 時，查詢 API 仍然可以回傳前一日的 cash value。 |
| 4 | `knowhow/oracle_table_reference.md` | Relationship | 0.2500 | POLICY_CONTRACT_CHANGE.CHANGE_ID 會關聯 calculation request。用 POLICY_ID 找資料時，不能忽略 POLICY_VERSION，否則可能把前一版契約與新一版現金價值混在一起。 |
| 5 | `knowhow/java_service_layer.md` | Transaction boundary | 0.2000 | ContractChangeService 負責驗證異動、寫入 POLICY_CONTRACT_CHANGE 並發布 domain event。CVCalculationService 負責消費事件與計算現金價值；兩者不應被誤認為同一個 transaction。 |

#### Vector Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/contract_change.md` | Important fields | 0.6882 | POLICY_CONTRACT_CHANGE.CHANGE_ID 是此次異動的識別碼，EFFECTIVE_DATE 決定生效日，CHANGE_STATUS 會經過 RECEIVED、VALIDATED、COMPLETED。若只看到 API 回應成功，不代表 downstream calculation 已完成。 |
| 2 | `knowhow/api_contract_change.md` | Callback and event | 0.6865 | 完成後會送出 POLICY_CONTRACT_CHANGE event；部分整合客戶仍使用 callback。若 callback timeout，producer 應保留 delivery status 並進入 retry，而不是重建一筆新的契約變更。 |
| 3 | `knowhow/release_checklist.md` | Before release | 0.6535 | 確認 database migration、Java service、API contract、batch schedule、feature flag 與 rollback package。若包含 calculation rule，準備代表性 policy 的 before／after expected value。 |
| 4 | `knowhow/policy_value_sync.md` | Repair | 0.6396 | repair job 應以 policy id 與 version 為範圍，先產生 dry-run 差異，再執行受控同步。完成後要確認 portal cache、API response 與下游 export 都讀到相同版本。 |
| 5 | `knowhow/data_repair_runbook.md` | Verification | 0.6317 | 修復完成後比對主檔、history、read model、portal API 與 export output。若是 batch retry 造成重複計算，要檢查 duplicate execution、ledger balance 與 audit log。 |

#### Hybrid Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/contract_change.md` | Important fields | 1.0000 | POLICY_CONTRACT_CHANGE.CHANGE_ID 是此次異動的識別碼，EFFECTIVE_DATE 決定生效日，CHANGE_STATUS 會經過 RECEIVED、VALIDATED、COMPLETED。若只看到 API 回應成功，不代表 downstream calculation 已完成。 |
| 2 | `knowhow/api_contract_change.md` | Callback and event | 0.9968 | 完成後會送出 POLICY_CONTRACT_CHANGE event；部分整合客戶仍使用 callback。若 callback timeout，producer 應保留 delivery status 並進入 retry，而不是重建一筆新的契約變更。 |
| 3 | `knowhow/release_checklist.md` | Before release | 0.9167 | 確認 database migration、Java service、API contract、batch schedule、feature flag 與 rollback package。若包含 calculation rule，準備代表性 policy 的 before／after expected value。 |
| 4 | `knowhow/incident_cv_batch.md` | Root cause | 0.8944 | Contract adjustment service 只更新 POLICY_CONTRACT_CHANGE 與保單主檔，沒有同步等待 CV recalculation job。當 batch queue 堵塞或 job status 不是 SUCCESS 時，查詢 API 仍然可以回傳前一日的 cash value。 |
| 5 | `knowhow/policy_value_sync.md` | Repair | 0.8776 | repair job 應以 policy id 與 version 為範圍，先產生 dry-run 差異，再執行受控同步。完成後要確認 portal cache、API response 與下游 export 都讀到相同版本。 |

**原因：** 這些模式的第一份標註相關文件排名相同；單靠排名無法推論是哪項特徵造成命中。

### A4 — 精準 keyword

**Query:** PAYMENT_RECONCILIATION settlement amount mismatch

**Expected files:** `payment_reconciliation.md`

**Keyword first relevant rank:** 1

**Vector first relevant rank:** 1

**Hybrid first relevant rank:** 1

**Best:** Keyword / Vector / Hybrid（並列）

#### Keyword Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/payment_reconciliation.md` | Mismatch | 1.0000 | 若 settlement amount mismatch，先檢查重複檔案、匯率、小數進位、partial payment 與 reversal。不要只用客戶姓名或保單號碼人工配對，需保留原始銀行 reference。 |
| 2 | `knowhow/release_checklist.md` | After release | 0.2500 | 觀察 error rate、latency、queue depth、batch success、retry count、cache stale rate 與金額 reconciliation。不要只看服務健康檢查為 green 就結束驗證。 |
| 3 | `knowhow/aml_screening.md` | Scope | 0.2000 | AML（anti-money laundering）screening batch 每日依 customer、policy、payment 與 beneficiary data 執行風險篩檢。結果會產生 risk level、screening status 與 review queue，供合規人員人工複核。 |
| 4 | `knowhow/cv_stale_after_endorsement.md` | Production symptom | 0.1667 | After an endorsement is accepted, the customer portal can still show the prior day's cash value. The user usually reports that the amount is old even though the policy change scre… |
| 5 | `knowhow/batch_monitoring.md` | Key metrics | 0.1429 | 每個 batch dashboard 至少要顯示 run id、business date、queued、running、success、failed、retrying 與 stuck count。金額計算類批次還要顯示 input policy count、processed count 與 output amount total。 |

#### Vector Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/payment_reconciliation.md` | Matching | 0.6484 | Payment reconciliation 將銀行入帳檔、payment transaction 與保單應收資料配對。核心欄位包含 payment id、settlement date、amount、currency、policy id 與 matching status。 |
| 2 | `knowhow/cv_stale_after_endorsement.md` | Production symptom | 0.5629 | After an endorsement is accepted, the customer portal can still show the prior day's cash value. The user usually reports that the amount is old even though the policy change scre… |
| 3 | `knowhow/aml_screening.md` | Troubleshooting | 0.5562 | 查詢 AML screening 結果時，確認 batch run id、watchlist version、risk level、match score 與 exception reason。若重跑，必須使用相同的 business date 並保留原始結果與 audit trail。 |
| 4 | `knowhow/batch_monitoring.md` | Key metrics | 0.5527 | 每個 batch dashboard 至少要顯示 run id、business date、queued、running、success、failed、retrying 與 stuck count。金額計算類批次還要顯示 input policy count、processed count 與 output amount total。 |
| 5 | `knowhow/oracle_table_reference.md` | Useful columns | 0.5511 | 查詢金額問題時，常用 POLICY_ID、POLICY_VERSION、EFFECTIVE_DATE、CASH_VALUE、SURRENDER_VALUE、POLICY_LOAN_AMT、CALCULATION_VERSION 與 LAST_CALCULATED_AT。欄位名稱可能在 Java DTO 使用 camelCase，但 database 使用… |

#### Hybrid Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/payment_reconciliation.md` | Matching | 1.0000 | Payment reconciliation 將銀行入帳檔、payment transaction 與保單應收資料配對。核心欄位包含 payment id、settlement date、amount、currency、policy id 與 matching status。 |
| 2 | `knowhow/cv_stale_after_endorsement.md` | Production symptom | 0.9477 | After an endorsement is accepted, the customer portal can still show the prior day's cash value. The user usually reports that the amount is old even though the policy change scre… |
| 3 | `knowhow/batch_monitoring.md` | Key metrics | 0.9247 | 每個 batch dashboard 至少要顯示 run id、business date、queued、running、success、failed、retrying 與 stuck count。金額計算類批次還要顯示 input policy count、processed count 與 output amount total。 |
| 4 | `knowhow/aml_screening.md` | Scope | 0.8824 | AML（anti-money laundering）screening batch 每日依 customer、policy、payment 與 beneficiary data 執行風險篩檢。結果會產生 risk level、screening status 與 review queue，供合規人員人工複核。 |
| 5 | `knowhow/incident_2025_policy_amount.md` | Symptoms | 0.8171 | release 後少數客戶看到的保單金額與後台查詢不同，重新整理或等待下一次 job 後恢復。客服描述為「金額跳回去」或「今天看到的跟昨天不一樣」。 |

**原因：** 這些模式的第一份標註相關文件排名相同；單靠排名無法推論是哪項特徵造成命中。

### B1 — 半模糊

**Query:** 保價金批次重新計算

**Expected files:** `incident_cv_batch.md`, `cash_value_recalculation.md`, `batch_retry.md`

**Keyword first relevant rank:** 1

**Vector first relevant rank:** 1

**Hybrid first relevant rank:** 1

**Best:** Keyword / Vector / Hybrid（並列）

#### Keyword Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/cash_value_recalculation.md` | Common symptom | 1.0000 | 使用者可能說「保價金批次重新計算了嗎？」或「契變完成後金額還沒變」。技術上要看 CALCULATION_STATUS、CALCULATION_VERSION 及 LAST_CALCULATED_AT，而不是只看前台顯示值。 |
| 2 | `knowhow/incident_cv_batch.md` | Recovery | 0.5000 | 先確認 contract change transaction 已 commit，再查詢 CV calculation batch 的 execution id。必要時依 batch retry runbook 補跑重算，重新檢查 cash value、保價金與前台顯示時間。不要直接手動改畫面資料，因為下一次批次可能把人工值覆蓋。 |
| 3 | `knowhow/surrender_value.md` | Calculation dependency | 0.2500 | 解約金服務會讀取最新的 policy version、cash value、loan balance 與 surrender factor。契約變更完成後若保價金尚未重新計算，解約金也可能暫時沿用舊版資料。 |
| 4 | `knowhow/premium_adjustment.md` | Error pattern | 0.2000 | 若契變後保費正確而保價金未變，通常要看 calculation queue、rate version 與批次 execution，而不是重新送出相同的 contract change request。 |
| 5 | `knowhow/api_contract_change.md` | Endpoint | 0.1111 | POST `/api/policies/{policyId}/contract-changes` 接收契約變更請求，request 需要 changeType、effectiveDate、requestId 與 operator。成功回應代表請求已接受，不代表 cash value 或 surrender value 已完成重新計算。 |

#### Vector Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/cash_value_recalculation.md` | Common symptom | 0.7985 | 使用者可能說「保價金批次重新計算了嗎？」或「契變完成後金額還沒變」。技術上要看 CALCULATION_STATUS、CALCULATION_VERSION 及 LAST_CALCULATED_AT，而不是只看前台顯示值。 |
| 2 | `knowhow/incident_cv_batch.md` | Recovery | 0.7395 | 先確認 contract change transaction 已 commit，再查詢 CV calculation batch 的 execution id。必要時依 batch retry runbook 補跑重算，重新檢查 cash value、保價金與前台顯示時間。不要直接手動改畫面資料，因為下一次批次可能把人工值覆蓋。 |
| 3 | `knowhow/premium_adjustment.md` | Error pattern | 0.7250 | 若契變後保費正確而保價金未變，通常要看 calculation queue、rate version 與批次 execution，而不是重新送出相同的 contract change request。 |
| 4 | `knowhow/surrender_value.md` | Calculation dependency | 0.6718 | 解約金服務會讀取最新的 policy version、cash value、loan balance 與 surrender factor。契約變更完成後若保價金尚未重新計算，解約金也可能暫時沿用舊版資料。 |
| 5 | `knowhow/cv_stale_after_endorsement.md` | Why it happens | 0.6692 | The endorsement transaction publishes an event, while the scheduled recalculation job consumes that event later. If the consumer is delayed or a retry record remains pending, the… |

#### Hybrid Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/cash_value_recalculation.md` | Common symptom | 1.0000 | 使用者可能說「保價金批次重新計算了嗎？」或「契變完成後金額還沒變」。技術上要看 CALCULATION_STATUS、CALCULATION_VERSION 及 LAST_CALCULATED_AT，而不是只看前台顯示值。 |
| 2 | `knowhow/incident_cv_batch.md` | Recovery | 0.9745 | 先確認 contract change transaction 已 commit，再查詢 CV calculation batch 的 execution id。必要時依 batch retry runbook 補跑重算，重新檢查 cash value、保價金與前台顯示時間。不要直接手動改畫面資料，因為下一次批次可能把人工值覆蓋。 |
| 3 | `knowhow/premium_adjustment.md` | Error pattern | 0.9473 | 若契變後保費正確而保價金未變，通常要看 calculation queue、rate version 與批次 execution，而不是重新送出相同的 contract change request。 |
| 4 | `knowhow/surrender_value.md` | Calculation dependency | 0.9195 | 解約金服務會讀取最新的 policy version、cash value、loan balance 與 surrender factor。契約變更完成後若保價金尚未重新計算，解約金也可能暫時沿用舊版資料。 |
| 5 | `knowhow/batch_retry.md` | Rerun example | 0.8665 | 保單金額批次若在寫入 POLICY_VALUE_HISTORY 前中斷，重跑前要先查 execution id、processed count 與 idempotency key。補跑應使用相同的 business date，並避免把已成功的 policy 再計算一次。 |

**原因：** 這些模式的第一份標註相關文件排名相同；單靠排名無法推論是哪項特徵造成命中。

### B2 — 半模糊

**Query:** 保單借款金額欄位查詢

**Expected files:** `policy_loan.md`, `oracle_table_reference.md`

**Keyword first relevant rank:** 1

**Vector first relevant rank:** 1

**Hybrid first relevant rank:** 1

**Best:** Keyword / Vector / Hybrid（並列）

#### Keyword Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/policy_loan.md` | Field usage | 1.0000 | POLICY_LOAN_AMT 是保單借款目前未清償的本金欄位，主要使用於 loan quotation、利息計算、解約金試算與 customer portal summary。查詢時通常需要搭配 POLICY_ID、LOAN_STATUS 與 AS_OF_DATE。 |
| 2 | `knowhow/surrender_value.md` | Support check | 0.5000 | 遇到金額爭議，先記錄 policy id、effective date、calculation version，再確認是否有 pending batch、保單借款扣除或人工調整紀錄。 |
| 3 | `knowhow/oracle_table_reference.md` | Core tables | 0.2000 | POLICY_MASTER 保存保單主資料，POLICY_CONTRACT_CHANGE 保存契約異動，POLICY_VALUE_HISTORY 保存每次 cash value calculation 的結果，POLICY_LOAN_ACCOUNT 保存保單借款帳戶與 POLICY_LOAN_AMT。 |
| 4 | `knowhow/policy_value_sync.md` | Purpose | 0.1667 | Policy Value Sync 將主系統的保價金、解約金與貸款餘額同步到查詢 read model。同步可能由 event-driven consumer 或 daily batch 觸發，兩種路徑的 status 欄位不同。 |
| 5 | `knowhow/audit_log.md` | Search example | 0.1429 | 排查契約變更與金額問題時，先以 policy id 和 correlation id 找到 API request，再沿著 transaction、event、batch execution、calculation version 查詢。 |

#### Vector Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/policy_loan.md` | Field usage | 0.7078 | POLICY_LOAN_AMT 是保單借款目前未清償的本金欄位，主要使用於 loan quotation、利息計算、解約金試算與 customer portal summary。查詢時通常需要搭配 POLICY_ID、LOAN_STATUS 與 AS_OF_DATE。 |
| 2 | `knowhow/surrender_value.md` | Support check | 0.6708 | 遇到金額爭議，先記錄 policy id、effective date、calculation version，再確認是否有 pending batch、保單借款扣除或人工調整紀錄。 |
| 3 | `knowhow/oracle_table_reference.md` | Core tables | 0.6307 | POLICY_MASTER 保存保單主資料，POLICY_CONTRACT_CHANGE 保存契約異動，POLICY_VALUE_HISTORY 保存每次 cash value calculation 的結果，POLICY_LOAN_ACCOUNT 保存保單借款帳戶與 POLICY_LOAN_AMT。 |
| 4 | `knowhow/payment_reconciliation.md` | Matching | 0.6116 | Payment reconciliation 將銀行入帳檔、payment transaction 與保單應收資料配對。核心欄位包含 payment id、settlement date、amount、currency、policy id 與 matching status。 |
| 5 | `knowhow/policy_value_sync.md` | Purpose | 0.5963 | Policy Value Sync 將主系統的保價金、解約金與貸款餘額同步到查詢 read model。同步可能由 event-driven consumer 或 daily batch 觸發，兩種路徑的 status 欄位不同。 |

#### Hybrid Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/policy_loan.md` | Field usage | 1.0000 | POLICY_LOAN_AMT 是保單借款目前未清償的本金欄位，主要使用於 loan quotation、利息計算、解約金試算與 customer portal summary。查詢時通常需要搭配 POLICY_ID、LOAN_STATUS 與 AS_OF_DATE。 |
| 2 | `knowhow/surrender_value.md` | Support check | 0.9839 | 遇到金額爭議，先記錄 policy id、effective date、calculation version，再確認是否有 pending batch、保單借款扣除或人工調整紀錄。 |
| 3 | `knowhow/oracle_table_reference.md` | Core tables | 0.9385 | POLICY_MASTER 保存保單主資料，POLICY_CONTRACT_CHANGE 保存契約異動，POLICY_VALUE_HISTORY 保存每次 cash value calculation 的結果，POLICY_LOAN_ACCOUNT 保存保單借款帳戶與 POLICY_LOAN_AMT。 |
| 4 | `knowhow/policy_value_sync.md` | Purpose | 0.9079 | Policy Value Sync 將主系統的保價金、解約金與貸款餘額同步到查詢 read model。同步可能由 event-driven consumer 或 daily batch 觸發，兩種路徑的 status 欄位不同。 |
| 5 | `knowhow/payment_reconciliation.md` | Matching | 0.8999 | Payment reconciliation 將銀行入帳檔、payment transaction 與保單應收資料配對。核心欄位包含 payment id、settlement date、amount、currency、policy id 與 matching status。 |

**原因：** 這些模式的第一份標註相關文件排名相同；單靠排名無法推論是哪項特徵造成命中。

### B3 — 半模糊

**Query:** 外部檔案傳輸失敗重送

**Expected files:** `external_file_transfer.md`, `batch_retry.md`

**Keyword first relevant rank:** 1

**Vector first relevant rank:** 1

**Hybrid first relevant rank:** 1

**Best:** Keyword / Vector / Hybrid（並列）

#### Keyword Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/external_file_transfer.md` | Failure and resend | 1.0000 | 若外部檔案傳輸失敗，先區分 authentication error、network timeout、remote disk full 與檔案格式錯誤。可重送的項目要使用相同 file id 與 idempotency key，避免合作方收到兩份相同檔案。 |
| 2 | `knowhow/batch_retry.md` | Retry policy | 0.2500 | 批次失敗時不可直接整批重跑。先將 failed item 與 retryable error 分開，確認是否為 deadlock、temporary network error、外部檔案未到或 business validation failure。只有暫時性錯誤可以進入 retry queue。 |
| 3 | `knowhow/aml_screening.md` | Data flow | 0.2000 | 夜間 job 先匯入 watchlist，再處理 customer matching、transaction threshold 與 sanction hit。外部名單檔案沒有完成交換時，batch 不應把所有客戶標成 clean，而要維持 INPUT_PENDING。 |
| 4 | `knowhow/batch_processing.md` | Data consistency | 0.1429 | 長時間批次應採 chunked processing 與 checkpoint。每個 chunk 完成後寫入 progress，讓失敗時可以從 checkpoint 繼續，而不是重複處理全部保單。跨表更新要確認 transaction boundary。 |
| 5 | `knowhow/payment_reconciliation.md` | Mismatch | 0.1250 | 若 settlement amount mismatch，先檢查重複檔案、匯率、小數進位、partial payment 與 reversal。不要只用客戶姓名或保單號碼人工配對，需保留原始銀行 reference。 |

#### Vector Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/external_file_transfer.md` | Monitoring | 0.8109 | 監控 transfer status、remote acknowledgement、retry count、checksum 與最後成功時間。當使用者說「檔案沒有送出去」或「失敗後要重送」，先查 transfer execution 與 application log。 |
| 2 | `knowhow/batch_retry.md` | Retry policy | 0.6750 | 批次失敗時不可直接整批重跑。先將 failed item 與 retryable error 分開，確認是否為 deadlock、temporary network error、外部檔案未到或 business validation failure。只有暫時性錯誤可以進入 retry queue。 |
| 3 | `knowhow/java_service_layer.md` | Debugging | 0.6093 | 排查時記錄 correlation id、transaction id、event id、policy version、consumer lag 與 calculation execution id。Java exception stack trace 要連同 root cause、retry 次數與資料庫 timeout 一起保存。 |
| 4 | `knowhow/aml_screening.md` | Troubleshooting | 0.6051 | 查詢 AML screening 結果時，確認 batch run id、watchlist version、risk level、match score 與 exception reason。若重跑，必須使用相同的 business date 並保留原始結果與 audit trail。 |
| 5 | `knowhow/release_checklist.md` | After release | 0.5918 | 觀察 error rate、latency、queue depth、batch success、retry count、cache stale rate 與金額 reconciliation。不要只看服務健康檢查為 green 就結束驗證。 |

#### Hybrid Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/external_file_transfer.md` | Monitoring | 1.0000 | 監控 transfer status、remote acknowledgement、retry count、checksum 與最後成功時間。當使用者說「檔案沒有送出去」或「失敗後要重送」，先查 transfer execution 與 application log。 |
| 2 | `knowhow/batch_retry.md` | Retry policy | 0.9593 | 批次失敗時不可直接整批重跑。先將 failed item 與 retryable error 分開，確認是否為 deadlock、temporary network error、外部檔案未到或 business validation failure。只有暫時性錯誤可以進入 retry queue。 |
| 3 | `knowhow/aml_screening.md` | Data flow | 0.8690 | 夜間 job 先匯入 watchlist，再處理 customer matching、transaction threshold 與 sanction hit。外部名單檔案沒有完成交換時，batch 不應把所有客戶標成 clean，而要維持 INPUT_PENDING。 |
| 4 | `knowhow/payment_reconciliation.md` | Batch recovery | 0.8555 | 對帳 batch 失敗後要以 file id 與 business date 進行 controlled rerun，並確認已成功的 payment 不會再次入帳。所有差異要進 exception queue 供財務複核。 |
| 5 | `knowhow/batch_processing.md` | Monitoring | 0.8411 | 監控項目包含 queue depth、success rate、平均處理時間、retry count、stuck execution 與最後成功 business date。若 calculation batch 沒有完成，應先確認 upstream contract event 是否已送出。 |

**原因：** 這些模式的第一份標註相關文件排名相同；單靠排名無法推論是哪項特徵造成命中。

### C1 — 高度模糊 semantic

**Query:** 客戶說改完保單後前台還是之前的數字，可能排程晚了

**Expected files:** `incident_cv_batch.md`, `cv_stale_after_endorsement.md`, `customer_portal_cache.md`

**Keyword first relevant rank:** 4

**Vector first relevant rank:** 1

**Hybrid first relevant rank:** 2

**Best:** Vector

#### Keyword Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/cash_value_recalculation.md` | Common symptom | 1.0000 | 使用者可能說「保價金批次重新計算了嗎？」或「契變完成後金額還沒變」。技術上要看 CALCULATION_STATUS、CALCULATION_VERSION 及 LAST_CALCULATED_AT，而不是只看前台顯示值。 |
| 2 | `knowhow/incident_2025_policy_amount.md` | Symptoms | 0.5000 | release 後少數客戶看到的保單金額與後台查詢不同，重新整理或等待下一次 job 後恢復。客服描述為「金額跳回去」或「今天看到的跟昨天不一樣」。 |
| 3 | `knowhow/payment_reconciliation.md` | Mismatch | 0.3333 | 若 settlement amount mismatch，先檢查重複檔案、匯率、小數進位、partial payment 與 reversal。不要只用客戶姓名或保單號碼人工配對，需保留原始銀行 reference。 |
| 4 | `knowhow/incident_cv_batch.md` | Recovery | 0.2500 | 先確認 contract change transaction 已 commit，再查詢 CV calculation batch 的 execution id。必要時依 batch retry runbook 補跑重算，重新檢查 cash value、保價金與前台顯示時間。不要直接手動改畫面資料，因為下一次批次可能把人工值覆蓋。 |
| 5 | `knowhow/customer_portal_cache.md` | Stale display | 0.1667 | 使用者看到舊金額不一定是 calculation 失敗，也可能是 cache invalidation 晚於資料 commit。排查時比對 API response version、cache created time、origin query time 與最後一次同步時間。 |

#### Vector Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/incident_cv_batch.md` | Root cause | 0.6554 | Contract adjustment service 只更新 POLICY_CONTRACT_CHANGE 與保單主檔，沒有同步等待 CV recalculation job。當 batch queue 堵塞或 job status 不是 SUCCESS 時，查詢 API 仍然可以回傳前一日的 cash value。 |
| 2 | `knowhow/cash_value_recalculation.md` | Common symptom | 0.6487 | 使用者可能說「保價金批次重新計算了嗎？」或「契變完成後金額還沒變」。技術上要看 CALCULATION_STATUS、CALCULATION_VERSION 及 LAST_CALCULATED_AT，而不是只看前台顯示值。 |
| 3 | `knowhow/contract_change.md` | Troubleshooting | 0.6463 | 遇到異動後金額未更新，先比對 change transaction commit time、event status 與 calculation batch start time，再確認是否有 cache 或 retry queue 延遲。 |
| 4 | `knowhow/cv_stale_after_endorsement.md` | Why it happens | 0.6437 | The endorsement transaction publishes an event, while the scheduled recalculation job consumes that event later. If the consumer is delayed or a retry record remains pending, the… |
| 5 | `knowhow/underwriting_rule.md` | Release note | 0.6404 | 規則更新前要建立 regression cases、灰度範圍與 rollback plan。若同時變更 API schema 與 batch consumer，必須確認舊版 client 仍可運作。 |

#### Hybrid Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/cash_value_recalculation.md` | Common symptom | 1.0000 | 使用者可能說「保價金批次重新計算了嗎？」或「契變完成後金額還沒變」。技術上要看 CALCULATION_STATUS、CALCULATION_VERSION 及 LAST_CALCULATED_AT，而不是只看前台顯示值。 |
| 2 | `knowhow/incident_cv_batch.md` | Incident summary | 0.9307 | 某次契約變更（契變）完成後，保單畫面仍顯示前一日的保價金。表面看起來像 contract adjustment 沒有更新金額，實際檢查發現 CV calculation batch 在上游資料寫入後沒有完成，因此後續查詢沿用了 previous day cash value。 這個案例常被描述成「契變做完之後金額還是舊的」、「保價金沒有刷新」或「變更成功但… |
| 3 | `knowhow/java_service_layer.md` | Common bug | 0.8955 | 如果 service 在 transaction commit 前就 publish event，consumer 可能查不到新的 policy version，造成 calculation 使用舊資料。另一種常見問題是 API 回傳 success 後才非同步執行 batch，前台因此短時間顯示 previous value。 |
| 4 | `knowhow/aml_screening.md` | Data flow | 0.8903 | 夜間 job 先匯入 watchlist，再處理 customer matching、transaction threshold 與 sanction hit。外部名單檔案沒有完成交換時，batch 不應把所有客戶標成 clean，而要維持 INPUT_PENDING。 |
| 5 | `knowhow/incident_2025_policy_amount.md` | Symptoms | 0.8594 | release 後少數客戶看到的保單金額與後台查詢不同，重新整理或等待下一次 job 後恢復。客服描述為「金額跳回去」或「今天看到的跟昨天不一樣」。 |

**原因：** 這題使用了與文件不同的描述方式，向量概念特徵比單純詞面更早召回標註的案例。

### C2 — 高度模糊 semantic

**Query:** 有人說資料修正後，部分保單的金額被重複計算，應該怎麼查？

**Expected files:** `batch_retry.md`, `data_repair_runbook.md`, `incident_cv_batch.md`

**Keyword first relevant rank:** 2

**Vector first relevant rank:** 1

**Hybrid first relevant rank:** 1

**Best:** Vector / Hybrid（並列）

#### Keyword Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/surrender_value.md` | Business definition | 1.0000 | 解約金（surrender value）是保單終止或解約時依保單年度、累積保費、保價金與費用規則計算的金額。部分文件稱 cash surrender value，不要與一般 cash value 混用。 |
| 2 | `knowhow/data_repair_runbook.md` | Verification | 0.5000 | 修復完成後比對主檔、history、read model、portal API 與 export output。若是 batch retry 造成重複計算，要檢查 duplicate execution、ledger balance 與 audit log。 |
| 3 | `knowhow/cash_value_recalculation.md` | Recalculation procedure | 0.3333 | 若 calculation job failed，先確認是否有 lock、資料庫 timeout 或上游 contract change 尚未 commit。修正原因後執行 controlled rerun，並以同一個 policy id 比對舊版與新版 cash value。所有人工補算都要留下 audit record。 |
| 4 | `knowhow/batch_processing.md` | Data consistency | 0.2500 | 長時間批次應採 chunked processing 與 checkpoint。每個 chunk 完成後寫入 progress，讓失敗時可以從 checkpoint 繼續，而不是重複處理全部保單。跨表更新要確認 transaction boundary。 |
| 5 | `knowhow/incident_cv_batch.md` | Incident summary | 0.1667 | 某次契約變更（契變）完成後，保單畫面仍顯示前一日的保價金。表面看起來像 contract adjustment 沒有更新金額，實際檢查發現 CV calculation batch 在上游資料寫入後沒有完成，因此後續查詢沿用了 previous day cash value。 這個案例常被描述成「契變做完之後金額還是舊的」、「保價金沒有刷新」或「變更成功但… |

#### Vector Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/data_repair_runbook.md` | Verification | 0.6514 | 修復完成後比對主檔、history、read model、portal API 與 export output。若是 batch retry 造成重複計算，要檢查 duplicate execution、ledger balance 與 audit log。 |
| 2 | `knowhow/batch_processing.md` | Data consistency | 0.6477 | 長時間批次應採 chunked processing 與 checkpoint。每個 chunk 完成後寫入 progress，讓失敗時可以從 checkpoint 繼續，而不是重複處理全部保單。跨表更新要確認 transaction boundary。 |
| 3 | `knowhow/payment_reconciliation.md` | Matching | 0.6258 | Payment reconciliation 將銀行入帳檔、payment transaction 與保單應收資料配對。核心欄位包含 payment id、settlement date、amount、currency、policy id 與 matching status。 |
| 4 | `knowhow/release_checklist.md` | Incident readiness | 0.6118 | Release notes 必須列出 correlation id 查法、常見 log pattern、資料修復方式與聯絡人。若出現 API 成功但 downstream value 沒更新，優先確認 event、consumer、batch 與 cache 的順序。 |
| 5 | `knowhow/incident_cv_batch.md` | Recovery | 0.6104 | 先確認 contract change transaction 已 commit，再查詢 CV calculation batch 的 execution id。必要時依 batch retry runbook 補跑重算，重新檢查 cash value、保價金與前台顯示時間。不要直接手動改畫面資料，因為下一次批次可能把人工值覆蓋。 |

#### Hybrid Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/data_repair_runbook.md` | Verification | 1.0000 | 修復完成後比對主檔、history、read model、portal API 與 export output。若是 batch retry 造成重複計算，要檢查 duplicate execution、ledger balance 與 audit log。 |
| 2 | `knowhow/batch_processing.md` | Data consistency | 0.9685 | 長時間批次應採 chunked processing 與 checkpoint。每個 chunk 完成後寫入 progress，讓失敗時可以從 checkpoint 繼續，而不是重複處理全部保單。跨表更新要確認 transaction boundary。 |
| 3 | `knowhow/surrender_value.md` | Support check | 0.9117 | 遇到金額爭議，先記錄 policy id、effective date、calculation version，再確認是否有 pending batch、保單借款扣除或人工調整紀錄。 |
| 4 | `knowhow/release_checklist.md` | Incident readiness | 0.9040 | Release notes 必須列出 correlation id 查法、常見 log pattern、資料修復方式與聯絡人。若出現 API 成功但 downstream value 沒更新，優先確認 event、consumer、batch 與 cache 的順序。 |
| 5 | `knowhow/batch_retry.md` | Incident handling | 0.8736 | 常見描述包括「以前有一個批次失敗後重跑造成金額不一致」、「batch retry 後同一筆資料被算兩次」或「補跑之後畫面才恢復」。完成 rerun 後要比對原始輸入、calculation version 與 audit log。 |

**原因：** 這些模式的第一份標註相關文件排名相同；單靠排名無法推論是哪項特徵造成命中。

### C3 — 高度模糊 semantic

**Query:** 新規則上線後 API 與資料庫寫入順序造成保單資料不一致

**Expected files:** `java_service_layer.md`, `api_contract_change.md`, `release_checklist.md`

**Keyword first relevant rank:** 2

**Vector first relevant rank:** 4

**Hybrid first relevant rank:** 3

**Best:** Keyword

#### Keyword Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/underwriting_rule.md` | Rule version | 1.0000 | 核保規則以 rule set version 管理，API request 會帶入產品、通路、客戶風險與生效日。規則上線不代表歷史保單會立即重新判定，需看 migration scope。 |
| 2 | `knowhow/release_checklist.md` | Incident readiness | 0.5000 | Release notes 必須列出 correlation id 查法、常見 log pattern、資料修復方式與聯絡人。若出現 API 成功但 downstream value 沒更新，優先確認 event、consumer、batch 與 cache 的順序。 |
| 3 | `knowhow/batch_retry.md` | Incident handling | 0.3333 | 常見描述包括「以前有一個批次失敗後重跑造成金額不一致」、「batch retry 後同一筆資料被算兩次」或「補跑之後畫面才恢復」。完成 rerun 後要比對原始輸入、calculation version 與 audit log。 |
| 4 | `knowhow/customer_portal_cache.md` | Safe invalidation | 0.2500 | 只有在新 calculation version 已 commit 且 read model 已更新後才清除 cache。直接清 cache 可以暫時掩蓋問題，但不能取代 batch、event 或資料庫一致性檢查。 |
| 5 | `knowhow/java_service_layer.md` | Debugging | 0.2000 | 排查時記錄 correlation id、transaction id、event id、policy version、consumer lag 與 calculation execution id。Java exception stack trace 要連同 root cause、retry 次數與資料庫 timeout 一起保存。 |

#### Vector Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/customer_portal_cache.md` | Safe invalidation | 0.6509 | 只有在新 calculation version 已 commit 且 read model 已更新後才清除 cache。直接清 cache 可以暫時掩蓋問題，但不能取代 batch、event 或資料庫一致性檢查。 |
| 2 | `knowhow/underwriting_rule.md` | Rule version | 0.6481 | 核保規則以 rule set version 管理，API request 會帶入產品、通路、客戶風險與生效日。規則上線不代表歷史保單會立即重新判定，需看 migration scope。 |
| 3 | `knowhow/incident_2025_policy_amount.md` | Investigation | 0.6279 | 比對 read model、policy master、calculation history 與 cache timestamp，確認是否存在 eventual consistency。此次事件不是資料遺失，而是 API 讀到尚未 publish 的舊版本。 |
| 4 | `knowhow/java_service_layer.md` | Debugging | 0.6241 | 排查時記錄 correlation id、transaction id、event id、policy version、consumer lag 與 calculation execution id。Java exception stack trace 要連同 root cause、retry 次數與資料庫 timeout 一起保存。 |
| 5 | `knowhow/release_checklist.md` | Incident readiness | 0.6202 | Release notes 必須列出 correlation id 查法、常見 log pattern、資料修復方式與聯絡人。若出現 API 成功但 downstream value 沒更新，優先確認 event、consumer、batch 與 cache 的順序。 |

#### Hybrid Top 5

| Rank | File | Heading | Score | Snippet |
|---:|---|---|---:|---|
| 1 | `knowhow/underwriting_rule.md` | Rule version | 1.0000 | 核保規則以 rule set version 管理，API request 會帶入產品、通路、客戶風險與生效日。規則上線不代表歷史保單會立即重新判定，需看 migration scope。 |
| 2 | `knowhow/customer_portal_cache.md` | Safe invalidation | 0.9908 | 只有在新 calculation version 已 commit 且 read model 已更新後才清除 cache。直接清 cache 可以暫時掩蓋問題，但不能取代 batch、event 或資料庫一致性檢查。 |
| 3 | `knowhow/release_checklist.md` | Incident readiness | 0.9574 | Release notes 必須列出 correlation id 查法、常見 log pattern、資料修復方式與聯絡人。若出現 API 成功但 downstream value 沒更新，優先確認 event、consumer、batch 與 cache 的順序。 |
| 4 | `knowhow/java_service_layer.md` | Debugging | 0.9476 | 排查時記錄 correlation id、transaction id、event id、policy version、consumer lag 與 calculation execution id。Java exception stack trace 要連同 root cause、retry 次數與資料庫 timeout 一起保存。 |
| 5 | `knowhow/incident_2025_policy_amount.md` | Investigation | 0.9197 | 比對 read model、policy master、calculation history 與 cache timestamp，確認是否存在 eventual consistency。此次事件不是資料遺失，而是 API 讀到尚未 publish 的舊版本。 |

**原因：** 這題包含明確欄位名或系統術語，原文詞面本身就足以定位文件；BM25 的精準性勝過額外語意召回。

## Interpretation

這是沒有使用大型語言模型或雲端 embedding API 的本機 baseline。Hybrid 使用 RRF 合併 BM25 與 vector rank，沒有直接相加兩種不可比的原始分數。
若之後接入 sentence-transformers 或公司內部 embedding API，應保留同一份評估查詢重新比較；這份報告不能宣稱 hashing vector 等同於 transformer embedding。


## Document-level metrics

| Mode | Hit@5 | MRR@5 |
|---|---:|---:|
| keyword | 1.000 | 0.825 |
| vector | 1.000 | 0.925 |
| hybrid | 1.000 | 0.883 |

## 無答案查詢檢查

下列問題在合成 Know-how 無對應答案；數字是回傳候選數，越多不代表越好。尚未用公司題庫校準門檻。

| Query | Keyword | Vector | Hybrid |
|---|---:|---:|---:|
| 火星探測器如何校正軌道 | 5 | 5 | 5 |
| 義大利麵食譜番茄醬比例 | 5 | 5 | 5 |
| 蘭花葉片枯黃如何施肥 | 1 | 5 | 5 |