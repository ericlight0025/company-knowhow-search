# 保單借款 POLICY_LOAN_AMT

## Field usage

POLICY_LOAN_AMT 是保單借款目前未清償的本金欄位，主要使用於 loan quotation、利息計算、解約金試算與 customer portal summary。查詢時通常需要搭配 POLICY_ID、LOAN_STATUS 與 AS_OF_DATE。

## Service flow

Java PolicyLoanService 讀取 POLICY_LOAN_ACCOUNT，依借款交易與還款交易彙總 POLICY_LOAN_AMT。若保單剛完成契約變更，必須確認 policy version 與 loan snapshot 的 effective date 一致。

## SQL hint

不要用最新一筆交易金額直接當成 POLICY_LOAN_AMT。正確方式是依 value date 加總 principal debit、principal credit，並排除 reversal transaction。相關 Oracle table 與 index 見資料表參考文件。

