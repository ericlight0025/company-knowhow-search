# Audit Log 與追蹤欄位

## Required fields

重要異動至少記錄 event id、request id、correlation id、operator、source system、before value、after value、timestamp 與 result。敏感資料需遮罩，但不能刪掉能串起 incident 的識別碼。

## Search example

排查契約變更與金額問題時，先以 policy id 和 correlation id 找到 API request，再沿著 transaction、event、batch execution、calculation version 查詢。

## Retention

Audit log retention 依公司規範與法遵要求設定。刪除或封存前要確認 incident、稽核與資料修復仍能取得必要證據。

