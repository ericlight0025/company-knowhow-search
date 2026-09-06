# 契變電訪

## 用途

說明契約變更後是否需要產生電訪案件的規則與原始設計位置。

## 常見問法

- 契變保額異動後沒有進電訪。
- 電訪案件沒產生要查哪裡？
- 契約變更需要電訪嗎？
- 金額異動卻沒有進 TeleCall。
- contract change telecall 規則在哪？

## 常見技術詞

電訪、電話訪問、TeleCall、Interview、Outbound Call、threshold、amount、change_type。

## 原始資料位置

- Word：`U:/Company/SPEC/ContractChange/TeleCall_SPEC.docx`
- Java：`D:/workspace/contract-change/src/TeleCallRuleService.java`
- JSP：`D:/workspace/contract-change/web/teleCall.jsp`
- JS：`D:/workspace/contract-change/web/teleCall.js`
- SQL Folder：`U:/SQL/ContractChange/`

## 下一步

請用 Copilot CLI 從 TeleCallRuleService 追規則、呼叫端與 SQL；再以規格確認門檻。

## 關鍵結論

- 是否產生電訪取決於 change_type 與金額門檻。
- 規格、Java 與前端欄位需一起比對，不能只看單一畫面。
