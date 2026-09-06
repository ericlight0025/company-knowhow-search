# 批次處理標準作業

## Lifecycle

批次工作由 scheduler 建立 execution，依序執行 prepare、process、commit、publish 四個階段。每個 execution 都有 business date、run id、worker id 與 status。不要只看 Windows Task Scheduler 顯示的啟動成功。

## Data consistency

長時間批次應採 chunked processing 與 checkpoint。每個 chunk 完成後寫入 progress，讓失敗時可以從 checkpoint 繼續，而不是重複處理全部保單。跨表更新要確認 transaction boundary。

## Monitoring

監控項目包含 queue depth、success rate、平均處理時間、retry count、stuck execution 與最後成功 business date。若 calculation batch 沒有完成，應先確認 upstream contract event 是否已送出。

