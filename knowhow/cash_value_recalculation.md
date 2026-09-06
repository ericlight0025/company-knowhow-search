# Cash Value Recalculation

## Calculation timing

保價金（cash value、CV）不是每次畫面查詢都即時計算。契約異動、保費入帳、利率更新後，系統會將保單放入 CV calculation batch，由夜間 scheduled process 重新計算。

## Common symptom

使用者可能說「保價金批次重新計算了嗎？」或「契變完成後金額還沒變」。技術上要看 CALCULATION_STATUS、CALCULATION_VERSION 及 LAST_CALCULATED_AT，而不是只看前台顯示值。

## Recalculation procedure

若 calculation job failed，先確認是否有 lock、資料庫 timeout 或上游 contract change 尚未 commit。修正原因後執行 controlled rerun，並以同一個 policy id 比對舊版與新版 cash value。所有人工補算都要留下 audit record。

