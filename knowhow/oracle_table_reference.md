# Oracle Table Reference

## Core tables

POLICY_MASTER 保存保單主資料，POLICY_CONTRACT_CHANGE 保存契約異動，POLICY_VALUE_HISTORY 保存每次 cash value calculation 的結果，POLICY_LOAN_ACCOUNT 保存保單借款帳戶與 POLICY_LOAN_AMT。

## Useful columns

查詢金額問題時，常用 POLICY_ID、POLICY_VERSION、EFFECTIVE_DATE、CASH_VALUE、SURRENDER_VALUE、POLICY_LOAN_AMT、CALCULATION_VERSION 與 LAST_CALCULATED_AT。欄位名稱可能在 Java DTO 使用 camelCase，但 database 使用 uppercase snake case。

## Relationship

POLICY_CONTRACT_CHANGE.CHANGE_ID 會關聯 calculation request。用 POLICY_ID 找資料時，不能忽略 POLICY_VERSION，否則可能把前一版契約與新一版現金價值混在一起。

