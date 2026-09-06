# 契約變更與契變流程

## Business flow

契約變更包含受益人、繳費方式、保額與保單狀態異動。Legacy 文件也會使用 endorsement、policy change、contract adjustment 等詞，搜尋時不能只依賴「契約變更」四個字。

契變交易先寫入 POLICY_CONTRACT_CHANGE，再由 Java service 產生待處理事件。事件完成後，保單查詢、保價金與解約金相關批次才會讀取新版本的契約資料。

## Important fields

POLICY_CONTRACT_CHANGE.CHANGE_ID 是此次異動的識別碼，EFFECTIVE_DATE 決定生效日，CHANGE_STATUS 會經過 RECEIVED、VALIDATED、COMPLETED。若只看到 API 回應成功，不代表 downstream calculation 已完成。

## Troubleshooting

遇到異動後金額未更新，先比對 change transaction commit time、event status 與 calculation batch start time，再確認是否有 cache 或 retry queue 延遲。

