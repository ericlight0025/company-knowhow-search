# 保價金重算

## 用途

定位 Cash Value recalculation 的批次規格、資料條件與驗證方式。

## 常見問法

- 保價金批次重新計算要看哪裡？
- CV 沒重新計算以前是不是遇過？
- 現金價值重算 JOB 是哪一支？
- cash value recalculation 失敗如何檢查？

## 常見技術詞

保價金、Cash Value、CV、現金價值、recalculation、batch、valuation date。

## 原始資料位置

- Word：`U:/Company/SPEC/PolicyValue/CV_RECALCULATION_SPEC.docx`
- Java Folder：`D:/workspace/policy-value/`
- SQL Folder：`U:/SQL/PolicyValue/`

## 下一步

請用 Copilot CLI 找出重算 JOB 與輸入條件，再以 batch log 驗證執行日。

## 關鍵結論

- CV 重算通常以批次與 valuation date 為準。
- 異常時先確認是否有符合重算條件，再看 JOB 是否完成。
