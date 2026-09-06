# 契變後 CV 未重新計算

## Incident summary

某次契約變更（契變）完成後，保單畫面仍顯示前一日的保價金。表面看起來像 contract adjustment 沒有更新金額，實際檢查發現 CV calculation batch 在上游資料寫入後沒有完成，因此後續查詢沿用了 previous day cash value。

這個案例常被描述成「契變做完之後金額還是舊的」、「保價金沒有刷新」或「變更成功但現金價值沒有跟著變」。這些描述都指向同一個問題：契約變更流程完成與現金價值重算工作之間存在時間差。

## Root cause

Contract adjustment service 只更新 POLICY_CONTRACT_CHANGE 與保單主檔，沒有同步等待 CV recalculation job。當 batch queue 堵塞或 job status 不是 SUCCESS 時，查詢 API 仍然可以回傳前一日的 cash value。

## Recovery

先確認 contract change transaction 已 commit，再查詢 CV calculation batch 的 execution id。必要時依 batch retry runbook 補跑重算，重新檢查 cash value、保價金與前台顯示時間。不要直接手動改畫面資料，因為下一次批次可能把人工值覆蓋。

