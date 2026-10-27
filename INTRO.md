# 專案簡介（Introduction）

## 這是什麼

「不踩坑：GLM-5.3-Flash」是一個面向 AI agents 與開發者的 GLM-5.3-Flash 整合經驗資料庫，聚焦 Mac Studio + oMLX 環境。它整理實際遭遇的格式／洩漏／截斷問題、已有的實作紀錄及可核對的外部規則，讓你開工前先讀、出事時能查。

## 為什麼需要

GLM-5.3-Flash 在 Mac Studio M3 Ultra 上跑得很快（prefill ~265 tok/s），但格式遵循不穩定：量化模型常出現 JSON fence、trailing text、空回、裸陣列、程式碼截斷。只靠模型本身不夠，實務上需要：

1. **Jinja 層**：輸出紀律（禁 fence、JSON 7 條、spec-fidelity、tool-result）。
2. **Proxy 層**：JSON 提取 + 重試 + finish_reason 檢查。
3. **Caller 層**：Task-specific 驗證 + response_format + 重試。

三層分工，所有 client 受益（Jinja/Proxy），task-specific 部分僅程式呼叫受益（Caller）。

## 本專案提供什麼

- **Jinja 模板**（`v1/chat_template.jinja`）：現行預設版本，移植 Qwen v7 的 7 條 JSON 輸出紀律。
- **Proxy**（`proxy/proxy.py`）：OpenAI-compatible proxy，port 8001，JSON 提取 + 重試。
- **Caller**（`caller/caller.py` + `caller_ext.py`）：Task-specific 驗證 + 數值修正 + Python grader。
- **文件**：PITFALLS 24 主題、TROUBLESHOOTING、BLOCKS、catalogue 索引、records、repairs。
- **安裝指引**：[INSTALL.md](INSTALL.md)。

## Benchmark 成績（114 題）

| Suite | 題數 | 最終通過 |
|---|---|---|
| Ability | 100 | 100/100（理論值，含 caller 處理） |
| Think-off | 10 | 10/10 |
| Code-test | 11 | 11/11 |
| Speed | 4 | 2/2 (32K/64K) |

全程改善：Ability 62/100 → 100/100、Code-test 1/11 → 11/11。

## 與其他「不踩坑」repo 的關係

- [no-pit-qwen38](https://github.com/arthurlin1979/no-pit-qwen38)：Qwen3.8 輸出模板修正（Jinja 為主）。
- [no-pit-google-workspace](https://github.com/arthurlin1979/no-pit-google-workspace)：Google Workspace 整合經驗（文件為主）。
- 本 repo：GLM-5.3-Flash 三層防護（Jinja + Proxy + Caller）。

## 授權

除明確標示的第三方內容外，本專案有權授權的原創文字、編排與範例採 [MIT License](LICENSE)。這是獨立整理，與 Z.ai / 智譜 / oMLX 上游無隸屬或背書關係。
