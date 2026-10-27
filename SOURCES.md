# 來源與版本（Sources）

核對日期：2026-10-28

## 模型與引擎

- 模型：`glm5.3`（Jundot/GLM-5.3-Flash-oQ4e-mtp，173.6 GiB，4.641 bits/w，MIT）。
- 引擎：oMLX 0.7.3.dev2（DMG macos26-27），支援 GLM oQ4e Better Low-Bit oQ。
- 機器：Mac Studio M3 Ultra 512GB。
- 配置：`~/.omlx/model_settings.json`：alias `glm5.3`，ctx 262144，max_tokens 8192，temp 1.0，top_p 0.95，top_k 40，reasoning_effort low，thinking_budget 1024，mtp_enabled true，turboquant_kv 4-bit，is_pinned。

## 上游

- Z.ai 原版 chat template：`chat_template.jinja.bak-zai-original-20261027`（本 repo `v1/chat_template.jinja.bak-zai-original-20261027`）。
- Qwen v7 輸出紀律：移植自 `froggeric/Qwen-Fixed-Chat-Templates` v22.5（Apache-2.0，原作者 Frédéric Guigand）的 7 條 JSON 輸出紀律。
- oMLX：https://github.com/oMLX/oMLX（或對應上游）。

## 社群參考

- HuggingFace froggeric v22.5：tool-call 規則「If you choose to call a tool, you MUST output the block IMMEDIATELY after thinking, with NO conversational text before or after.」
- mlx-serve：tool-call repair（僅在 strict parsing 失敗後執行）。
- LiveKit / Agenta：`response_format: json_object` 或 JSON schema mode 事後驗證。
- vLLM / n8n：max_tokens 限制導致截斷；`finish_reason` 檢查。
- arXiv LlmFix：三步修復法（過濾 → 定位 → 修復）。

## 本專案檔案

- Jinja 模板：`v1/chat_template.jinja`（現行）；備份：`v1/chat_template.jinja.bak-zai-original-20261027`。
- Proxy 程式：`proxy/proxy.py`。
- Caller wrapper：`caller/caller.py`。
- Caller 擴充：`caller/caller_ext.py`。
- LaunchAgent：`~/Library/LaunchAgents/com.arthur.omlx-proxy.plist`。
- OB 報告：`AIout/Reports/20261027-glm5.3-full-journey-report.md`。
- 重構指南：`AIout/Reports/20261027-glm5.3-reconstruction-guide.md`。

## 授權

- GLM-5.3-Flash-oQ4e-mtp：MIT。
- 本專案原創內容：MIT。
- Qwen-Fixed-Chat-Templates：Apache-2.0（僅參考，未整份搬入）。
- Z.ai 原版 chat template：依原上游授權。

## 證據邊界

本專案的狀態與參數是原紀錄的歷史描述；本次文件整理沒有重新跑 live 驗證，不能據此判斷目前正式環境的狀態。歷史搜尋鏈未完整保留的地方會揭露，不以今天找到的官方文件冒充當年採用解法的確切出處。
