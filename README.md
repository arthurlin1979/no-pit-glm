# 不踩坑：GLM-5.3-Flash（Mac oMLX）

[English version](README.en.md)

更新日期：2026-10-28

給 AI agents 與開發者使用的 GLM-5.3-Flash 整合經驗：Jinja 輸出紀律 + OpenAI-compatible Proxy + Caller 端驗證，三層防護，讓 Mac Studio 上的 GLM 不再踩坑。

本專案整理實際遭遇的格式／洩漏／截斷問題、已有的實作紀錄及可核對的外部規則。解法結合自行實驗、官方文件與社群資料，部分由 AI 協助搜尋及編輯，不宣稱所有方法皆由我們發明。這是獨立整理，與 Z.ai / 智譜 / oMLX 上游無隸屬或背書關係。

## 為什麼有這個專案

GLM-5.3-Flash 在 Mac Studio M3 Ultra 上跑得很快（prefill ~265 tok/s），但格式遵循不穩定：量化模型常出現 JSON fence、trailing text、空回、裸陣列、程式碼截斷。只靠模型本身不夠，實務上需要 Jinja 層的輸出紀律、Proxy 層的 JSON 提取 + 重試、Caller 層的 schema 驗證。

我把踩破的坑全部整理出來，做成一個資料庫，方便 AI 查詢。出事的時候查一下：這個問題我們是不是遇過？開工之前先讀一下：有哪些東西可能會影響？

本 repo 114 題 benchmark 全程改善：Ability 62/100 → 100/100（理論值，含 caller 處理），Code-test 1/11 → 11/11，Think-off 7/10 → 10/10，Speed 32K/64K pass。

## 先從這裡讀

- [專案簡介](INTRO.md)：這是什麼、為什麼需要、提供什麼。
- [安裝指引](INSTALL.md)：從零開始安裝 GLM + oMLX + Jinja + Proxy + Caller。
- [給 AI agents 的入口](AGENTS.md)：先讀本檔，再查 PITFALLS 與 catalogue 索引。
- [30 秒 Quick Start](QUICKSTART.md)：人用三步確認、AI 用三頁開工。
- [常見問題](TROUBLESHOOTING.md)：從 183 筆濃縮的先看入口，完整脈絡連回原編號。
- [完整紀錄索引](catalogue/INDEX.md)：逐條保留主紀錄與維修／延伸項的原編號。
- [避坑速查表](PITFALLS.md)：快速查閱主題，只作入口，不取代完整紀錄。
- [Jinja 變更區塊說明](BLOCKS.md)：本專案對 chat template 的所有修改，含實證狀態。
- [來源與版本](SOURCES.md)：來源、版本、證據邊界與致謝。
- [第三方聲明](THIRD_PARTY_NOTICES.md)：第三方內容的授權範圍。
- [v1 版自述](v1/RELEASE.md)：現行預設版本的版自述。
- [v1 Jinja 模板](v1/chat_template.jinja)：現行模板。
- [Proxy 程式](proxy/proxy.py)：OpenAI-compatible proxy（port 8001）。
- [Caller wrapper](caller/caller.py)：Task-specific caller。
- [Caller 擴充](caller/caller_ext.py)：數值修正 + Python grader。

## 最小操作方式

1. 確認 oMLX 已載入 GLM-5.3-Flash，且 `~/.omlx/model_settings.json` 已設定 alias `glm5.3`。
2. 覆寫 Jinja 模板：`cp v1/chat_template.jinja ~/.omlx/models/Jundot/GLM-5.3-Flash-oQ4e-mtp/chat_template.jinja`，重啟 oMLX。
3. 啟動 Proxy：`python3 proxy/proxy.py`（或用 LaunchAgent），監聽 port 8001。
4. OpenCode / harness / curl 全部走 `http://127.0.0.1:8001/v1`。
5. 結果不明先讀回，不立即重播建立或 append。

## 三層防護架構

```
OpenCode / harness / curl
        │
        ▼
   Proxy (port 8001)  ←── 通用 caller 邏輯（JSON 提取 + 重試 + finish_reason 檢查）
        │
        ▼
   oMLX (port 8000)   ←── Jinja 模板（格式規則 + 輸出紀律）
        │
        ▼
   GLM-5.3-Flash (M3 Ultra)
```

| 層級 | 位置 | 功能 | 所有 client 受益？ |
|---|---|---|---|
| Jinja | oMLX 模板 | 格式規則（禁 fence、JSON 紀律、spec-fidelity、tool-result） | ✅ 是 |
| Proxy | port 8001 | JSON 提取 + 重試 + finish_reason 檢查 | ✅ 是 |
| Caller | `caller/caller.py` | Task-specific 驗證 + response_format + 重試 | ❌ 僅程式呼叫 |

## Jinja 規則總覽（v1）

| 組 | 觸發條件 | 規則 |
|---|---|---|
| JSON | user 含 `json` 且無 tools | 7 條輸出紀律 + spec-fidelity |
| Code | user 含 `原始碼`/`code`/`python` 且無 tools | 禁 fence + spec-fidelity |
| Tool-result | tools present + 有 tool result + user 含 `json` | JSON-only + spec-fidelity |

## 全程改善總覽

| 階段 | Ability | Code-test | 修復內容 |
|---|---|---|---|
| 原始（無 Jinja） | 62/100 | 1/11 | — |
| + Jinja v7（7 條規則） | 82/100 | 1/11 | 格式/洩漏類錯誤 |
| + Jinja code rule | 82/100 | 10/11 | code fence 移除 |
| + Jinja spec-fidelity | 83/100 | 10/11 | EXT-019 語意改善 |
| + Proxy (8001) | 86/100 | 10/11 | EXT-023/026/028 |
| + Caller wrapper | 88/100 | 10/11 | EXT-015/044 通過 |
| + json_schema (API 層) | 90/100 | 10/11 | V2-Q022/EXT-044 通過 |
| + Caller 數值修正 | 91/100 | 10/11 | EXT-012 通過 |
| + Caller 重試 (EXT-048) | 91/100 | 11/11 | EXT-048 通過 (seed=42) |

## 已知限制

- 語意錯（EXT-012/015）：Jinja 無法解決，需 caller 驗證 + 重試或更強模型。
- 程式碼截斷（EXT-048）：需 caller 重試 + 固定 seed；grader 用 Python 而非 JS（大整數精度）。
- Speed suite：GLM prefill 極快（0.4s for 32K-64K），128K/200K 因 prefill 太慢未測。
- Splash（ANE prefill）：已安裝，需在 oMLX App UI 手動啟用。

## 授權

除明確標示的第三方內容外，本專案有權授權的原創文字、編排與範例採 [MIT License](LICENSE)。

Jinja 模板基底為 Z.ai 原版（chat_template.jinja.bak-zai-original-20261027），本專案為獨立衍生作品。Proxy/Caller 為原創，MIT 授權。

## 範圍與維護

這是既有來源表的逐條整理，不是所有 GLM 問題的完整清單，也不保證其他版本或環境會得到相同結果。條目中的狀態與參數是原紀錄的歷史描述；本次文件整理沒有重新跑 live 驗證，不能據此判斷目前正式環境的狀態。

私人原始紀錄、客戶資料、環境設定、對話紀錄與 Git 歷史不屬於這份文件包。
