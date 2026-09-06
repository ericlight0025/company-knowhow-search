# 外部檔案重送

## 用途

提供外部檔案傳輸失敗後的重送條件、SOP 與紀錄位置。

## 常見問法

- 外部檔案失敗後要找哪份重送 SOP？
- 檔案可以重送嗎？
- SFTP failed 要怎麼 resend？
- 重送後如何確認對方已收到？

## 常見技術詞

外部檔案、重送、resend、retry、SFTP、傳輸失敗、duplicate、acknowledgement。

## 原始資料位置

- Word：`U:/Company/SOP/ExternalFile/FILE_RESEND_GUIDE.docx`
- Folder：`U:/Company/SOP/ExternalFile/`
- Log Folder：`U:/Company/Logs/ExternalFile/`

## 下一步

請先依重送 SOP 檢查檔案版本與接收狀態，再由 Copilot CLI 協助閱讀傳輸 log。

## 關鍵結論

- 重送前要確認對方未成功收檔，避免 duplicate。
- 重送後需保留檔案批號、時間與確認結果。
