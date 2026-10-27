# v1 版自述（Release Notes）

更新日期：2026-10-28

## 版本定位

v1 是本專案的現行預設版本，移植 Qwen v7 的 7 條 JSON 輸出紀律至 GLM-5.3-Flash，並加入 Code no-fence 規則與 spec-fidelity 條款、Tool-result JSON-only 規則。

## 相對於 Z.ai 原版的變更

見 [BLOCKS.md](../BLOCKS.md) 與 [v1_vs_original.diff](./v1_vs_original.diff)。

- 組 1：JSON 7 條輸出紀律 + spec-fidelity（觸發：user 含 `json` 且無 tools）。
- 組 2：Code no-fence + spec-fidelity（觸發：user 含 `原始碼`/`code`/`python` 且無 tools）。
- 組 3：Tool-result JSON-only + spec-fidelity（觸發：tools present + 有 tool result + user 含 `json`）。

## 實測結果

- Ability：62/100 → 91/100（+ Jinja/Proxy/Caller）。
- Code-test：1/11 → 11/11。
- Think-off：7/10 → 10/10。
- Speed：32K/64K pass。

## 使用方式

```bash
# oMLX
cp ./v1/chat_template.jinja ~/.omlx/models/Jundot/GLM-5.3-Flash-oQ4e-mtp/chat_template.jinja
# 重啟 oMLX

# vLLM
vllm serve <model> --chat-template ./v1/chat_template.jinja

# llama.cpp
llama-server -m <model.gguf> --jinja --chat-template-file ./v1/chat_template.jinja
```

## 已知限制

- 語意錯（EXT-012/015）：需 caller 驗證 + 重試或更強模型。
- 程式碼截斷（EXT-048）：需 caller 重試 + 固定 seed。
- Speed 大 context（128K/200K）：prefill 太慢，未測。

## 授權

MIT（見 [LICENSE](../LICENSE)）。
