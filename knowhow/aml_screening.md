# AML Screening 批次

## Scope

AML（anti-money laundering）screening batch 每日依 customer、policy、payment 與 beneficiary data 執行風險篩檢。結果會產生 risk level、screening status 與 review queue，供合規人員人工複核。

## Data flow

夜間 job 先匯入 watchlist，再處理 customer matching、transaction threshold 與 sanction hit。外部名單檔案沒有完成交換時，batch 不應把所有客戶標成 clean，而要維持 INPUT_PENDING。

## Troubleshooting

查詢 AML screening 結果時，確認 batch run id、watchlist version、risk level、match score 與 exception reason。若重跑，必須使用相同的 business date 並保留原始結果與 audit trail。

