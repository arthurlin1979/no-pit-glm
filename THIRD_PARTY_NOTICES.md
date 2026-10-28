# 第三方聲明（Third-Party Notices）

核對日期：2026-10-28

本專案原創部分採根目錄的 MIT License。下列第三方內容保留其原授權，不屬於根目錄 MIT 對原創內容的授權範圍。

## 1. GLM-5.3-Flash-oQ4e-mtp（含 Z.ai 原版 chat template）

- 專案及原作者：Jundot（量化包發布者）、Z.ai／智譜（模型與原版 template）。
- 來源：HuggingFace `Jundot/GLM-5.3-Flash-oQ4e-mtp` 模型包內附的 `chat_template.jinja`。
- 本地收錄檔：`v1/chat_template.jinja.bak-zai-original-20261027`（diff 基線，逐字未改）。
- 適用授權：MIT（模型包宣稱）。
- 用途：作為 `v1/v1_vs_original.diff` 的基準線；本專案的修改皆相對於此原版，修改部分由 Arthur Lin 以 MIT 釋出。

## 2. froggeric/Qwen-Fixed-Chat-Templates（規則參考，未收錄檔案）

- 專案及原作者：Frédéric Guigand（froggeric）。
- 來源：https://huggingface.co/froggeric/Qwen-Fixed-Chat-Templates（v22.5，commit `855bffc`）。
- 適用授權：Apache License, Version 2.0。
- 本地收錄檔：**無**——未搬入其 Jinja 檔案、原文說明或程式碼片段。
- 使用方式：僅參考其 7 條 JSON 輸出紀律的**規則條文精神**（單一 JSON 值、鍵名逐字、原詞保留、型別照題、null/[] 區分、啟動≠完成、不確定用 null），由 Arthur Lin 針對 GLM-5.3-Flash 重新撰寫並擴充（加 spec-fidelity、Code 組、tool-result 組）。條文與結構與上游不同，屬獨立重寫。
- 修改標示：v1 規則全文見 `v1/v1_vs_original.diff`；歸屬說明見 `SOURCES.md` 上游表與 `BLOCKS.md`。

## 3. oMLX

- 專案：oMLX（Mac 推理引擎）。
- 用途：本專案的目標推理環境；本 repo 不收錄其任何檔案。
- 本專案的 MIT 不取代 oMLX 的適用授權。

## 4. 社群內容（連結與自行摘要，未收錄檔案）

- mlx-serve、LiveKit、Agenta、vLLM docs、n8n、arXiv LlmFix：僅保留連結與自主摘要（見 `SOURCES.md` 社群表），沒有搬入原文、翻譯或程式。各內容授權依各站各頁為準；GitHub issue／留言不能一律假設受該 repo 程式碼授權涵蓋。

## 收錄原則

每次新增第三方資料都要記錄：檔案、來源、固定版本、授權、修改方式及必要聲明；無法確認就只留可核對的連結或暫不收錄。本檔不是法律意見，也不宣稱所有歷史內容權利均已查明。