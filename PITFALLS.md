# GLM 避坑表

核對日期：2026-10-28

本檔保留快速查閱主題。需要完整經驗與處理細節，請從 [114 題 benchmark 紀錄](catalogue/INDEX.md) 進入；那裡逐條保留 Ability/Think-off/Code-test/Speed 的原編號。

GLM 主題編號與 benchmark 題目編號是兩套導航，不能把主題數當成全部案例數。

「建議驗證」不代表所有情境都已在 GLM live 實測。官方規則及版本資訊請對照 [來源表](SOURCES.md)。

## Jinja 層

| ID | 主題／來源層 | 容易誤判的地方 | 建議處理與驗證 |
|---|---|---|---|
| GLM-001 | Jinja 觸發條件；本專案 | user 含 `json` 但有 tools 時不觸發 JSON 規則 | 確認最後一則 user 含 `json` 且無 tools 才注入 7 條規則。 |
| GLM-002 | Jinja Code 規則；本專案 | 只檢查 `json`，忽略 `code`/`python`/`原始碼` | Code 組獨立觸發，禁 fence + spec-fidelity。 |
| GLM-003 | Jinja spec-fidelity；本專案 | 認為 Jinja 能修語意錯 | spec-fidelity 只降低「多加驗證」波動，不修數值錯。 |
| GLM-004 | Jinja tool-result 規則；本專案 | 有 tools 就一定觸發 | 僅在 tools present + 有 tool result + user 含 `json` 時觸發。 |
| GLM-005 | Jinja 浮水印；本專案 | 模板被模型更新覆寫 | 載入前核對首行 `template_version`。 |
| GLM-006 | Jinja 備份；本專案 | 直接覆寫無備份 | 先備份 `chat_template.jinja.bak-zai-original-YYYYMMDD`。 |

## Proxy 層

| ID | 主題／來源層 | 容易誤判的地方 | 建議處理與驗證 |
|---|---|---|---|
| GLM-007 | Proxy JSON 提取；本專案 | 認為 regex greedy 就夠 | 用 `json.JSONDecoder().raw_decode()` 逐步解析，忽略 trailing text。 |
| GLM-008 | Proxy 重試；本專案 | 只重試空回 | 重試條件含 empty / `finish_reason=length` / incomplete JSON（JSON 預期但 parse 失敗）。 |
| GLM-009 | Proxy 串流；本專案 | 串流也做 JSON 提取 | 串流請求直接 pass-through，不做提取。 |
| GLM-010 | Proxy 裸陣列；本專案 | 認為 Proxy 能修結構 | Proxy 能提取裸陣列，但 schema 需 API 層 `response_format: json_schema`。 |
| GLM-011 | Proxy 連線；本專案 | 直接打 oMLX port 8000 | 所有 client 走 proxy port 8001，享受 JSON 提取 + 重試。 |

## Caller 層

| ID | 主題／來源層 | 容易誤判的地方 | 建議處理與驗證 |
|---|---|---|---|
| GLM-012 | Caller 驗證；本專案 | 認為 Jinja 就夠 | Task-specific 驗證 + response_format + 重試在 Caller 層。 |
| GLM-013 | Caller 數值修正；本專案 | 信任模型算的數值 | EXT-012 markup_percent/margin_percent 由 caller 重新計算。 |
| GLM-014 | Caller 重試 seed；本專案 | 固定 seed 不變 | 每次重試 seed += 7，降低生成波動。 |
| GLM-015 | Caller grader；本專案 | 用 JS grader | 大整數精度問題，改用 Python grader（`grade_code_python`）。 |
| GLM-016 | response_format json_schema；社群 + 本專案 | 認為 json_object 就夠 | json_schema 是約束解碼，比 json_object 更嚴格；可修 format 類，無法修語意錯。 |

## Speed / Infra

| ID | 主題／來源層 | 容易誤判的地方 | 建議處理與驗證 |
|---|---|---|---|
| GLM-017 | Speed 校準；本專案 | 用 oMLX prompt_tokens 做 binary search | 改用 `fitPrompt`；降低 target tokens（32000/64000 可用）。 |
| GLM-018 | Speed 大 context；本專案 | 128K/200K 超過 context | 128K/200K < 262K，可測但 prefill 太慢（~10+ min）。 |
| GLM-019 | Splash 啟用；本專案 | brew install 就啟用 | 需在 oMLX App UI 手動切換 External Engine → Splash。 |
| GLM-020 | Temperature；官方建議 | 降低 temperature 改善格式 | 官方建議 temp=1.0；格式問題用 Jinja/Proxy/Caller 解，不降 temp。 |

## 已知限制

| ID | 主題／來源層 | 容易誤判的地方 | 建議處理與驗證 |
|---|---|---|---|
| GLM-021 | 語意錯；本專案 | Jinja 能修數值錯 | EXT-012/015 屬模型推理能力，需 caller 驗證 + 重試或更強模型。 |
| GLM-022 | 程式碼截斷；本專案 | max_tokens 不夠 | EXT-048 截斷發生在 ~1362 chars（遠低於 8192），屬模型提前停止。 |
| GLM-023 | 常識題；本專案 | 模型能力不足 | T07/T08 需 prompt 加「只回一句短句」或更強模型。 |
| GLM-024 | Grammar-constrained；社群 | 期待 oMLX 支援 grammar | oMLX 尚未支援 `--grammar`；切換 llama.cpp 會失去 Mac 優化。 |
| GLM-025 | 重試上限與失敗處理；本專案 | 無限重試或自動降級換模型 | 兩層都有上限：Proxy `MAX_RETRIES=3`（只救格式錯），Caller `MAX_RETRIES=5`（驗證錯，每次換 seed）。用盡即回 500 / raise RuntimeError 停下等人，不自動降級。格式錯可自動救，語意錯連續失敗代表任務有問題，自動重試沒意義。 |

## 使用這份表的限制

來源層用來幫助選擇驗證方法，不表示每個條目都是 GLM 自身缺陷。
我們沒有在本次文件整理中重跑全部 live 流程，也沒有復原所有歷史搜尋鏈。
新問題應先歸類再補來源；不要因相似錯誤碼就套用過去事故的根因。
