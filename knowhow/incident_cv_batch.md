# 契變後保價金未更新

## 用途

記錄契變成功但保價金仍為前一日資料的歷史 Incident 導航。

## 常見問法

- 契變完成但保價金還是昨天的資料。
- 契變做完後畫面金額還是舊的。
- contract adjustment 成功但 cash value 沒更新。
- CV calculation batch 沒跑嗎？
- 契變畫面金額怪怪的怎麼查？

## 常見技術詞

CV、cash value、保價金、現金價值、recalculation、previous day、batch、contract adjustment。

## 原始資料位置

- Word：`U:/Company/Incident/INC_CV_BATCH_2025.docx`
- Java Folder：`D:/workspace/policy-value/`
- SQL Folder：`U:/SQL/PolicyValue/Incident/`

## 下一步

請由 Copilot Chat 讀 Incident 全文，確認契變狀態、CV batch 與畫面查詢時間。

## 關鍵結論

- 契變完成與 CV recalculation 是兩個不同處理點。
- 必須同時驗證 contract state 與 CV batch 是否完成。
