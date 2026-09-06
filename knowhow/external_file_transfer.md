# 外部檔案傳輸與 SFTP

## Transfer flow

對外檔案交換使用 SFTP outbound／inbound directory。產檔完成後先寫入 staging，再以 checksum、檔案大小與 naming convention 驗證，最後才移到 outbound ready。不要直接對正在寫入的檔案執行傳送。

## Failure and resend

若外部檔案傳輸失敗，先區分 authentication error、network timeout、remote disk full 與檔案格式錯誤。可重送的項目要使用相同 file id 與 idempotency key，避免合作方收到兩份相同檔案。

## Monitoring

監控 transfer status、remote acknowledgement、retry count、checksum 與最後成功時間。當使用者說「檔案沒有送出去」或「失敗後要重送」，先查 transfer execution 與 application log。

