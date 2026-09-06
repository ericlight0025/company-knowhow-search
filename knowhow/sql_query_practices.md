# SQL 查詢與除錯慣例

## Query rules

除錯正式資料時，SQL 必須帶有適當的 where 條件與 row limit，先使用 explain plan 確認 index，再逐步放大範圍。不要在 production 直接執行沒有條件的 update 或 delete。

## Insurance example

查保價金時，常用 POLICY_ID、POLICY_VERSION、AS_OF_DATE 與 CALCULATION_STATUS。查契約變更時，應依 CHANGE_ID、EFFECTIVE_DATE 排序，並將 event status 與 batch execution 一起比對。

## Evidence

Incident 記錄應保存 SQL template、查詢時間、database schema、row count 與遮罩後的 sample id。敏感欄位不得貼到公開 issue 或未授權的聊天工具。

