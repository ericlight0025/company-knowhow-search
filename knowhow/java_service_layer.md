# Java Service Layer

## Transaction boundary

ContractChangeService 負責驗證異動、寫入 POLICY_CONTRACT_CHANGE 並發布 domain event。CVCalculationService 負責消費事件與計算現金價值；兩者不應被誤認為同一個 transaction。

## Common bug

如果 service 在 transaction commit 前就 publish event，consumer 可能查不到新的 policy version，造成 calculation 使用舊資料。另一種常見問題是 API 回傳 success 後才非同步執行 batch，前台因此短時間顯示 previous value。

## Debugging

排查時記錄 correlation id、transaction id、event id、policy version、consumer lag 與 calculation execution id。Java exception stack trace 要連同 root cause、retry 次數與資料庫 timeout 一起保存。

