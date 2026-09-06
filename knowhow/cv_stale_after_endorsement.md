# 契變畫面舊值

## 用途

定位契變後畫面仍顯示舊值時，前端、快取與資料同步的排查入口。

## 常見問法

- 契變完成後畫面還是舊資料。
- CV 顯示前一天的值是快取嗎？
- 契變頁面沒有刷新怎麼查？

## 常見技術詞

契變、endorsement、CV、舊值、cache、API、畫面刷新、資料同步。

## 原始資料位置

- Word：`U:/Company/Incident/INC_ENDORSEMENT_STALE_SCREEN.docx`
- JSP：`D:/workspace/contract-change/web/contractChange.jsp`
- JS：`D:/workspace/contract-change/web/contractChange.js`

## 下一步

請先用 Copilot CLI 追畫面 API，再比對後端資料與快取時間。

## 關鍵結論

- 畫面舊值不一定是 CV batch 未完成。
- 要分層驗證資料、API 回應與前端快取。
