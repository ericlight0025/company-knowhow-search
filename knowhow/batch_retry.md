# 批次重跑

## 用途

定位批次失敗後的 retry 原則、相依工作與重跑前檢查。

## 常見問法

- 批次失敗可以直接重跑嗎？
- Batch Retry 前要確認什麼？
- 重跑造成金額異常要看哪裡？
- 哪些 JOB 有前後相依？

## 常見技術詞

Batch Retry、restart、rerun、job dependency、補跑、重跑、rollback。

## 原始資料位置

- Word：`U:/Company/SOP/Batch/BATCH_RETRY_GUIDE.docx`
- SQL Folder：`U:/SQL/Batch/Retry/`

## 下一步

請先讀重跑 SOP，並由 Copilot CLI 檢查相關 JOB log 與相依程式。

## 關鍵結論

- 重跑前必須確認上游輸入與下游未重複入帳。
- 金額異常時要先比對重跑範圍與資料修正紀錄。
