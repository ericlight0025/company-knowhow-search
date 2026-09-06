# Premium Adjustment

## Adjustment flow

保費調整依契約變更、費率版本、生效日與收費週期重新計算 premium。調整結果會影響後續 cash value calculation，但不一定在同一個 API request 內完成。

## Error pattern

若契變後保費正確而保價金未變，通常要看 calculation queue、rate version 與批次 execution，而不是重新送出相同的 contract change request。

## Validation

驗證時以 policy id、effective date、premium version 與 calculation version 對照。所有人工調整都要能在 audit log 還原。

