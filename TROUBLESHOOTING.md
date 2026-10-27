# 常見問題（Troubleshooting）

從 114 題 benchmark 與實作紀錄濃縮的先看入口。完整脈絡連回 [catalogue/INDEX.md](catalogue/INDEX.md) 與 [PITFALLS.md](PITFALLS.md)。

## 1. JSON 輸出帶 fence / trailing text

- **症狀**：模型回傳 ```json ... ``` 或 JSON 後接說明文字。
- **原因**：Jinja 未觸發 JSON 規則，或無 tools 但 user 未含 `json`。
- **解法**：確認 Jinja v1 的 JSON 組觸發條件（user 含 `json` 且無 tools）；Proxy 的 `_extract_json` 用 `raw_decode` 剝離 fence/trailing text。
- **Jinja 可解？** 部分（Proxy 補強）。

## 2. 裸陣列（V2-Q022）

- **症狀**：模型輸出 `[0, -24, 0, 0]` 而非 `{"products":[...]}`。
- **原因**：模型忽略「物件」指令。
- **解法**：API 層加 `response_format: {"type": "json_schema", ...}` 強制根為物件。
- **Jinja 可解？** 否（需 API 層）。

## 3. 空回 / 截斷（EXT-028 / EXT-044）

- **症狀**：content 為空，或 `finish_reason === 'length'`。
- **解法**：Proxy 自動重試（最多 3 次）；Caller 端重試（最多 5 次，不同 seed）。
- **Jinja 可解？** 部分（Proxy 補強）。

## 4. 程式碼 fence（Code-test）

- **症狀**：程式碼題輸出 ```python ... ```。
- **解法**：Jinja Code 組規則（user 含 `原始碼`/`code`/`python` 且無 tools）禁 fence + spec-fidelity。EXT-048 用 caller 重試（seed=42）。
- **Jinja 可解？** 是（格式層）。

## 5. 程式碼截斷（EXT-048）

- **症狀**：程式碼在 ~1362 chars 提前停止。
- **解法**：Caller 重試 + 固定 seed；grader 用 Python 而非 JS（大整數精度）。
- **Jinja 可解？** 否。

## 6. 語意錯（EXT-012 / EXT-015）

- **症狀**：數值計算錯誤（markup_percent 等）。
- **解法**：Caller 端數值驗證 + 修正（`caller_ext.py`）；或使用更強模型。
- **Jinja 可解？** 否。

## 7. Speed suite 校準失敗

- **症狀**：SPEED-01~04 全數 runtime-error。
- **原因**：calibration binary search 使用 oMLX 回報的 prompt_tokens，與 262K context 不匹配。
- **解法**：改用 `fitPrompt`（harness/speed.mjs）；降低 target tokens（32000/64000 可用）。
- **Jinja 可解？** 否（harness）。

## 8. 常識題回答過長（T07 / T08）

- **症狀**：Think-off 常識題模型回答過長/錯誤。
- **解法**：Caller 端 prompt 加「只回一句短句」；或使用更強模型。
- **Jinja 可解？** 否。

## 9. Proxy 無法修復裸陣列

- **症狀**：V2-Q022 proxy 輸出 `[0, -24, 0, 0]`（裸陣列正確提取，但結構不符）。
- **解法**：API 層 `response_format: json_schema` 強制根為物件。
- **Proxy 能修？** 結構提取可，schema 需 API 層。

## 10. Splash 未啟用

- **症狀**：ANE prefill 未加速。
- **解法**：在 oMLX App UI → Model Settings → External Engine → Splash 手動切換。`brew install incoai/tap/splash`。
- **Jinja 可解？** 否（需 UI）。
