# 銀行入帳與應收

## 用途

定位銀行入帳、應收帳款與對帳差異的處理文件。

## 常見問法

- 銀行入帳時應收相關內容在哪？
- 收款與應收對不起來怎麼查？
- payment reconciliation SOP 在哪？

## 常見技術詞

銀行入帳、應收、payment reconciliation、settlement、對帳、收款、差異。

## 原始資料位置

- Word：`U:/Company/SPEC/Payment/PAYMENT_RECONCILIATION_SPEC.docx`
- SQL Folder：`U:/SQL/Payment/`
- Java Folder：`D:/workspace/payment/`

## 下一步

請先由 Copilot Chat 讀對帳 SOP，再用 Copilot CLI 追收款批次與資料表。

## 關鍵結論

- 先區分銀行回檔、入帳與應收更新的時間點。
- 對帳差異需保留交易日、批號與銀行 reference。
