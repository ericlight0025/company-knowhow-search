# Customer Portal Cache

## Cache behavior

前台 portal 會快取 policy summary、cash value 與 loan balance，以降低查詢主系統的頻率。cache key 必須包含 policy id 與 policy version，不能只使用 policy id。

## Stale display

使用者看到舊金額不一定是 calculation 失敗，也可能是 cache invalidation 晚於資料 commit。排查時比對 API response version、cache created time、origin query time 與最後一次同步時間。

## Safe invalidation

只有在新 calculation version 已 commit 且 read model 已更新後才清除 cache。直接清 cache 可以暫時掩蓋問題，但不能取代 batch、event 或資料庫一致性檢查。

