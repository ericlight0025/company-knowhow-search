# Underwriting Rule Engine

## Rule version

核保規則以 rule set version 管理，API request 會帶入產品、通路、客戶風險與生效日。規則上線不代表歷史保單會立即重新判定，需看 migration scope。

## Decision trace

每次 decision 要記錄 rule version、input snapshot、matched rule、decision 與 operator override。遇到結果不一致，先比對同一版本的 input，不要只看最後顯示的 decision。

## Release note

規則更新前要建立 regression cases、灰度範圍與 rollback plan。若同時變更 API schema 與 batch consumer，必須確認舊版 client 仍可運作。

