# Payment Reconciliation

## Matching

Payment reconciliation 將銀行入帳檔、payment transaction 與保單應收資料配對。核心欄位包含 payment id、settlement date、amount、currency、policy id 與 matching status。

## Mismatch

若 settlement amount mismatch，先檢查重複檔案、匯率、小數進位、partial payment 與 reversal。不要只用客戶姓名或保單號碼人工配對，需保留原始銀行 reference。

## Batch recovery

對帳 batch 失敗後要以 file id 與 business date 進行 controlled rerun，並確認已成功的 payment 不會再次入帳。所有差異要進 exception queue 供財務複核。

