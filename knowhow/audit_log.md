# 操作紀錄入口

## 用途

定位使用者操作、批次執行與資料異動的 audit log 查詢規格。

## 常見問法

- 誰改過這筆資料？
- 操作紀錄要去哪找？
- batch 執行歷程怎麼看？

## 常見技術詞

audit log、操作紀錄、operator、trace id、資料異動、job log。

## 原始資料位置

- Word：`U:/Company/SPEC/Common/AUDIT_LOG_SPEC.docx`
- SQL Folder：`U:/SQL/Common/AuditLog/`

## 下一步

請用既有 log 平台或 DBeaver 查詢，再由 Copilot CLI 協助閱讀欄位用途。

## 關鍵結論

- 查核需保留時間範圍、操作人與 trace id。
- 正式稽核紀錄以原始系統為準。
