# Release Checklist

## Before release

確認 database migration、Java service、API contract、batch schedule、feature flag 與 rollback package。若包含 calculation rule，準備代表性 policy 的 before／after expected value。

## After release

觀察 error rate、latency、queue depth、batch success、retry count、cache stale rate 與金額 reconciliation。不要只看服務健康檢查為 green 就結束驗證。

## Incident readiness

Release notes 必須列出 correlation id 查法、常見 log pattern、資料修復方式與聯絡人。若出現 API 成功但 downstream value 沒更新，優先確認 event、consumer、batch 與 cache 的順序。

