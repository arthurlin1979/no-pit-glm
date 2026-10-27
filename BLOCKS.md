# 本專案的變更區塊說明（僅列本專案修改部分，上游原有內容不列）

每項包含：說明、中英文術語、所屬版本、實證狀態（有效／未證實／有害）。

## v1（相對於 Z.ai 原版 3 組規則 + spec-fidelity）

### 組 1：JSON 輸出紀律（JSON output discipline）

1. 版本浮水印（version watermark）：首行 `template_version` 標示 `...-arthur-glm-v1`。因模型更新可能覆寫客製模板，載入前核對此行即可確認模板是否在位。狀態：有效（維運用途）。
2. JSON 7 條輸出紀律（JSON output discipline）：最後一則使用者訊息含 `json` 且無工具呼叫時，於 system 尾端附加 7 條 JSON 輸出規則（單一 JSON 值、鍵名逐字照抄、原詞保留、型別照題目、null/[] 語意區分、啟動≠完成、不確定用 null 不編造）。114 子集 7 題：格式類錯誤歸零（6/7，唯一殘留 EXT-036 屬語意理解，非模板能力範圍）。狀態：有效。
3. spec-fidelity 條款（spec-fidelity clause）：兩組規則後追加「Follow the specification exactly; do not add extra validation, assumptions, or commentary beyond what is requested.」目的：降低 EXT-037 類「模型多加驗證邏輯」的生成波動。實測：EXT-037 PASS、V2-Q003 PASS。狀態：有效。

### 組 2：Code 輸出規則（Code output rule）

4. Code no-fence 規則（code no-fence rule）：user 含 `原始碼`/`code`/`python` 且無 tools 時，只輸出原始碼，禁 fence/前言/說明。Code-test 從 1/11 提升到 10/11（EXT-037 退步 1 題因生成波動，EXT-048 為 grader JS 大整數精度 false negative）。狀態：有效。

### 組 3：Tool-result JSON-only 規則（Tool-result JSON-only rule）

5. Tool-result JSON-only 規則（tool-result JSON-only rule）：tools present + 有 tool result + user 含 `json` 時，注入「After tool results, output only the final JSON value. No fence, no preamble, no trailing explanation.」不影響 tool_calls（規則只控制最終回覆）。EXT-023 測試仍出現 trailing text（因無 tool result，規則不觸發）；需 caller 端 JSON 提取。狀態：部分有效。

## 不予收錄

* 降低 temperature（lower temperature）：官方建議 temp=1.0；格式問題用 Jinja/Proxy/Caller 解，不降 temp。具副作用，不予收錄。
* Grammar-constrained generation：oMLX 尚未支援 `--grammar`；切換 llama.cpp 會失去 Mac 優化。不予收錄。
