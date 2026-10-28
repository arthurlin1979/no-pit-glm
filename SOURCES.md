# 來源與版本（Sources）

核對日期：2026-10-28

感謝 Z.ai／智譜、oMLX、HuggingFace 社群及相關工具的維護者與參與者。
列為來源不代表合作、背書、共同作者，或我們使用過其程式碼。

## 來源種類

- **本專案實作**：三層防護（Jinja 規則、Proxy、Caller）為我們自行實作，來自 114 題 benchmark 與實戰紀錄；公開的是去識別化摘要，不公開原始客戶資料、log 或資源 ID。
- **移植內容**：v1 的 7 條 JSON 輸出紀律移植自 froggeric/Qwen-Fixed-Chat-Templates v22.5 的規則設計；僅參考其規則條文精神，未整份搬入，未複製其 Jinja 程式碼。
- **上游基底**：Z.ai 原版 chat template 以備份檔形式收錄（diff 基線），依模型上游授權。
- **本次社群佐證**：現在可讀取且支持相關做法的社群討論，不假裝是當時搜尋採用的同一個網頁。
- **背景回報**：他人的做法與建議，未在我們環境全部重現，不拿來證明我們的修法有效。

完整脈絡逐條分清自家實作、移植內容、上游基底與背景參考，不能把 114 題當成 114 個獨立 GLM 缺陷。

## 模型與引擎

- 模型：`glm5.3`（Jundot/GLM-5.3-Flash-oQ4e-mtp，173.6 GiB，4.641 bits/w，MIT）。
- 引擎：oMLX 0.7.3.dev2（DMG macos26-27），支援 GLM oQ4e Better Low-Bit oQ。
- 機器：Mac Studio M3 Ultra 512GB。
- 配置：`~/.omlx/model_settings.json`：alias `glm5.3`，ctx 262144，max_tokens 8192，temp 1.0，top_p 0.95，top_k 40，reasoning_effort low，thinking_budget 1024，mtp_enabled true，turboquant_kv 4-bit，is_pinned。

## 上游

| 來源 | 適用主題 | 使用方式 |
|---|---|---|
| Z.ai 原版 chat template（備份檔 `v1/chat_template.jinja.bak-zai-original-20261027`） | Jinja diff 基線 | 原檔收錄，依模型上游授權（MIT）。 |
| [froggeric/Qwen-Fixed-Chat-Templates](https://huggingface.co/froggeric/Qwen-Fixed-Chat-Templates) v22.5（作者 Frédéric Guigand） | 7 條 JSON 輸出紀律 | 規則設計參考；未整份搬入、未複製其 Jinja 程式碼。Apache-2.0。 |
| [Qwen/Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B) | v7 規則原始脈絡 | 僅連結說明出處。 |
| oMLX | 推理引擎、oQ4e 量化 | 本專案在其上運行；本專案 MIT 不取代 oMLX 適用授權。 |
| Jundot/GLM-5.3-Flash-oQ4e-mtp | 模型權重 | MIT。 |

## 社群佐證與背景回報（未全部重現）

| 來源 | 適用主題 | 使用方式 |
|---|---|---|
| HuggingFace froggeric v22.5 tool-call 規則 | tool-call 前後不夾對話文字 | 規則設計參考，已納入 v1 tool-result 組。 |
| mlx-serve | tool-call repair（strict parsing 失敗後） | 背景參考；未採用其程式。 |
| LiveKit / Agenta | `response_format: json_object` / JSON schema mode | 技術做法的自行整理；我們以 `json_schema` 實測驗證（見 catalogue/repairs-01.md）。 |
| vLLM docs / n8n | `finish_reason` 檢查、max_tokens 截斷 | 技術做法的自行整理，已實測。 |
| arXiv LlmFix | 三步修復法（過濾→定位→修復） | 背景參考；未收錄原文。 |

社群討論的授權依各站各頁為準；本專案只保留連結與自行摘要，沒有搬入原文、翻譯或程式片段。

## 本專案檔案

- Jinja 模板：`v1/chat_template.jinja`（現行）；備份：`v1/chat_template.jinja.bak-zai-original-20261027`；差異：`v1/v1_vs_original.diff`。
- Proxy 程式：`proxy/proxy.py`。
- Caller wrapper：`caller/caller.py`；擴充：`caller/caller_ext.py`。
- 實測速度：`catalogue/speed.md`（數據重算自 harness results.json）。
- LaunchAgent：`~/Library/LaunchAgents/com.arthur.omlx-proxy.plist`（機器本地，未收錄）。
- OB 存檔：`AIout/Reports/20261027-glm5.3-full-journey-report.md`、`20261027-glm5.3-reconstruction-guide.md`、`20261027-glm5.3-jinja-v7-port-bench.md`（私人 vault，未收錄，數據可回溯）。

## 授權

- 本專案原創內容（文字、編排、Proxy、Caller）：MIT。
- GLM-5.3-Flash-oQ4e-mtp（含 Z.ai 原版 template）：MIT。
- froggeric/Qwen-Fixed-Chat-Templates：Apache-2.0（僅規則參考，未整份搬入）。
- 各社群內容依各自授權；本專案的 MIT 不取代其他適用條件。

## 尚未核實與未收錄的內容

- 部分歷史搜尋只留網站名稱（mlx-serve、Agenta、LlmFix 等），未保留完整搜尋鏈；不作已驗證佐證，不猜填作者，不搬原文。
- LaunchAgent plist 與 OB 私人報告屬環境與私人紀錄，不屬於本文件包。
- 每次新增第三方資料都要記錄：檔案、來源、固定版本、授權、修改方式及必要聲明；無法確認就只留可核對的連結或暫不收錄。

## 證據邊界

本專案的狀態與參數是原紀錄的歷史描述；本次文件整理沒有重新跑 live 驗證，不能據此判斷目前正式環境的狀態。歷史搜尋鏈未完整保留的地方已在本檔揭露，不以今天找到的社群討論冒充當年採用解法的確切出處。