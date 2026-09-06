# Incident：政策金額短暫不一致

## Symptoms

release 後少數客戶看到的保單金額與後台查詢不同，重新整理或等待下一次 job 後恢復。客服描述為「金額跳回去」或「今天看到的跟昨天不一樣」。

## Investigation

比對 read model、policy master、calculation history 與 cache timestamp，確認是否存在 eventual consistency。此次事件不是資料遺失，而是 API 讀到尚未 publish 的舊版本。

## Action

增加 version check 與 stale response warning，並將 cache invalidation 放在 calculation commit 後。所有 temporary workaround 都要有期限，避免長期保留人工刷新流程。

