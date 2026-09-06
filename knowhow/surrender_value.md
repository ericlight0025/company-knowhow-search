# 解約金計算與查詢

## Business definition

解約金（surrender value）是保單終止或解約時依保單年度、累積保費、保價金與費用規則計算的金額。部分文件稱 cash surrender value，不要與一般 cash value 混用。

## Calculation dependency

解約金服務會讀取最新的 policy version、cash value、loan balance 與 surrender factor。契約變更完成後若保價金尚未重新計算，解約金也可能暫時沿用舊版資料。

## Support check

遇到金額爭議，先記錄 policy id、effective date、calculation version，再確認是否有 pending batch、保單借款扣除或人工調整紀錄。

