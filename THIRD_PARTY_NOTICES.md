# 第三方聲明（Third-Party Notices）

本專案包含或參考以下第三方內容，依各自授權。

## 1. Z.ai 原版 chat template

- 檔案：`v1/chat_template.jinja.bak-zai-original-20261027`
- 來源：GLM-5.3-Flash-oQ4e-mtp 模型包內附的原始 `chat_template.jinja`。
- 授權：依模型上游授權（MIT，模型本身 MIT）。
- 用途：作為 diff 基線，本專案的修改皆相對於此原版。

## 2. Qwen-Fixed-Chat-Templates（參考）

- 來源：https://huggingface.co/froggeric/Qwen-Fixed-Chat-Templates（v22.5，commit 855bffc）
- 作者：Frédéric Guigand
- 授權：Apache-2.0
- 用途：本專案移植其 7 條 JSON 輸出紀律（v7 規則），未整份搬入；僅參考其規則設計。

## 3. oMLX

- 來源：oMLX 0.7.3.dev2
- 用途：推理引擎，本專案在其上運行。
- 本專案的 MIT 不取代 oMLX 的適用授權。

## 4. GLM-5.3-Flash-oQ4e-mtp

- 來源：Jundot/GLM-5.3-Flash-oQ4e-mtp
- 授權：MIT
- 用途：本專案的目標模型。

## 其他

其他 Google 文件、社群回答及 repo 目前只作參考連結與自行摘要，沒有整份搬入。收錄第三方原文或程式前，要確認具體檔案的來源、固定版本及授權，保留必要聲明與修改標示；無法確認就只留可核對的連結或暫不收錄。
