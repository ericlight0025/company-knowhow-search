# Policy Value Sync

## Purpose

Policy Value Sync 將主系統的保價金、解約金與貸款餘額同步到查詢 read model。同步可能由 event-driven consumer 或 daily batch 觸發，兩種路徑的 status 欄位不同。

## Stale data check

遇到查詢結果落後，檢查 source version、target version、last sync time、consumer lag 與 dead-letter queue。不要只看 target table 有沒有資料；有資料不代表它是最新版本。

## Repair

repair job 應以 policy id 與 version 為範圍，先產生 dry-run 差異，再執行受控同步。完成後要確認 portal cache、API response 與下游 export 都讀到相同版本。

