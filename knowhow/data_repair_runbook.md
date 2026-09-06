# Data Repair Runbook

## Before repair

資料修復前先建立 read-only snapshot，記錄 affected policy ids、policy version、原始輸入、目前輸出與 incident ticket。確認修復範圍只包含已確認的 business date，不要用模糊條件更新整張表。

## Rebuild value

對保單金額不一致的案例，優先重建 calculation request，再讓標準 batch 產生新版本。若只能手動補資料，必須使用 idempotency key、保留 before／after、執行人與 approval。

## Verification

修復完成後比對主檔、history、read model、portal API 與 export output。若是 batch retry 造成重複計算，要檢查 duplicate execution、ledger balance 與 audit log。

