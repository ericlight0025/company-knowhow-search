# Batch Retry 與補跑作業

## Retry policy

批次失敗時不可直接整批重跑。先將 failed item 與 retryable error 分開，確認是否為 deadlock、temporary network error、外部檔案未到或 business validation failure。只有暫時性錯誤可以進入 retry queue。

## Rerun example

保單金額批次若在寫入 POLICY_VALUE_HISTORY 前中斷，重跑前要先查 execution id、processed count 與 idempotency key。補跑應使用相同的 business date，並避免把已成功的 policy 再計算一次。

## Incident handling

常見描述包括「以前有一個批次失敗後重跑造成金額不一致」、「batch retry 後同一筆資料被算兩次」或「補跑之後畫面才恢復」。完成 rerun 後要比對原始輸入、calculation version 與 audit log。

