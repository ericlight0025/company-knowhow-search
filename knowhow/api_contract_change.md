# API Contract Change

## Endpoint

POST `/api/policies/{policyId}/contract-changes` 接收契約變更請求，request 需要 changeType、effectiveDate、requestId 與 operator。成功回應代表請求已接受，不代表 cash value 或 surrender value 已完成重新計算。

## Callback and event

完成後會送出 POLICY_CONTRACT_CHANGE event；部分整合客戶仍使用 callback。若 callback timeout，producer 應保留 delivery status 並進入 retry，而不是重建一筆新的契約變更。

## Compatibility

新增欄位要維持 backward compatibility，enum 變更要先確認 Java client 與 batch consumer。Incident 排查可用 requestId、changeId、eventId 串起 API、database 與 downstream job。

