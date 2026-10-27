# 維修紀錄（Repairs）

本檔保留 A/B/C 實作紀錄與 Proxy/Caller 改善紀錄。

## A. Jinja tool-result JSON-only 規則

- 在 tools present 但有 tool result 且 user 含 `json` 時，注入：「After tool results, output only the final JSON value. No fence, no preamble, no trailing explanation.」
- 不影響 tool_calls（規則只控制最終回覆）。
- EXT-023 測試仍出現 trailing text（因無 tool result，規則不觸發）；需 caller 端 JSON 提取。

## B. Harness 重試機制

- `run-omlx.mjs` 的 `chat()` 現在在 content 為空或 `finish_reason === 'length'` 時自動重試（最多 5 次）。
- 目的：處理 EXT-048 類截斷/空回。

## C. Speed harness 改用 fitPrompt

- `calibrate()` 改用 `fitPrompt`（harness/speed.mjs），正確追蹤 best record_count（僅在 actual_tokens <= target 時更新）。
- 預期修復 32000/64000/128000 targets；200000 仍超 262K context。

## Proxy 能力邊界

| 問題類型 | Proxy 能修？ | 方式 |
|---|---|---|
| Trailing text（JSON 完整） | ✅ | raw_decode 提取第一個 JSON 值 |
| Code fence | ✅ | raw_decode 提取 |
| 空回 / 截斷（finish_reason=length） | ✅ | 重試 |
| 不完整 JSON（finish_reason=stop） | ✅ | 重試 |
| 裸陣列（無 `{}`） | ✅ | raw_decode 支援陣列 |
| 語意錯 | ❌ | 需 caller 驗證 / 更強模型 |
| 程式碼截斷 | ❌ | 需 caller 重試 + 不同 seed |

## Proxy 改善紀錄

- `_extract_json` 改用 `json.JSONDecoder().raw_decode()`（逐步解析，忽略 trailing text）。
- 重試條件新增：incomplete JSON（JSON 預期但 parse 失敗）。
- EXT-044 測試：proxy 輸出乾淨 JSON（無 trailing text）。
- V2-Q022 測試：proxy 輸出 `[0, -24, 0, 0]`（裸陣列正確提取）。

## Caller 重構

`caller.py` 現在只做 task-specific 部分（驗證 + response_format），通用部分交給 proxy。

## response_format 實測結果

| ID | 無 response_format | json_object | json_schema |
|---|---|---|---|
| V2-Q022 | ❌ 裸陣列 | ❌ 裸陣列 | ✅ `{"products":[0,-24,0,0]}` |
| EXT-044 | ❌ trailing text | ❌ trailing text | ✅ 完整 JSON |
| EXT-012 | ❌ 數值錯 | ❌ 數值錯 | ❌ 數值錯（schema 不管正確性） |
| EXT-015 | ❌ f1=3/4 | ❌ f1=3/4 | ❌ f1=3/4（schema 不管正確性） |

結論：`json_schema` 是約束解碼，比 `json_object` 更嚴格。可修復 format 類問題，但無法修復語意錯。
