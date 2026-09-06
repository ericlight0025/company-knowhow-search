# Batch Monitoring Dashboard

## Key metrics

每個 batch dashboard 至少要顯示 run id、business date、queued、running、success、failed、retrying 與 stuck count。金額計算類批次還要顯示 input policy count、processed count 與 output amount total。

## Alert rules

當最後成功時間超過 SLA、failed ratio 超標、queue depth 持續增加或 calculation version 落後時告警。告警訊息要包含 execution id 與可直接查詢的 correlation id。

## Runbook link

告警不代表立刻重跑。先看 dependency、database lock、external file status 與前一個 execution 是否仍持有 lease，再依 batch retry runbook 決定補跑或人工介入。

