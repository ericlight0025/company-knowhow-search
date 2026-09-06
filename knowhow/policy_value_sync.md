# 保單價值同步

## 用途

定位保單價值在服務、批次與查詢畫面間同步的規格。

## 常見問法

- 保單價值同步在哪裡做？
- Cash Value 更新後畫面何時會看到？
- value sync 異常怎麼查？

## 常見技術詞

policy value、同步、sync、Cash Value、CV、batch、API、畫面。

## 原始資料位置

- Word：`U:/Company/SPEC/PolicyValue/POLICY_VALUE_SYNC_SPEC.docx`
- Java Folder：`D:/workspace/policy-value/`
- SQL Folder：`U:/SQL/PolicyValue/`

## 下一步

請用 Copilot CLI 比對 batch、service 與 API 的資料流，再讀正式同步規格。

## 關鍵結論

- 同步完成時間可能不同於主交易完成時間。
- 要以資料基準日與同步批號共同判斷。
