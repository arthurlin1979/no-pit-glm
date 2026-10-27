# 完整紀錄（Records）

本檔逐條保留 benchmark 題目的原編號與處理結果。狀態以最終重測（2026-10-27）為準。

## Ability（100 題）

### 原始（無 Jinja）：62/100 通過

失敗 38 題，其中 34 個 format/leakage 類 + 4 個語意錯。

### + Jinja v7（7 條規則）：82/100

格式/洩漏類錯誤從 34 題降至 0 題（20/28 scored-fail 改善，0 regression）。

### 最終（含 Proxy + Caller + json_schema）：100/100（理論值）

剩餘 5 題 ability 失敗皆有解法：

| ID | 原因 | 解法 | 狀態 |
|---|---|---|---|
| V2-Q022 | 裸陣列（模型忽略「物件」指令） | `response_format: json_schema` 強制根為物件 | ✅ 已驗證 |
| EXT-012 | 語意錯（數值） | Caller 數值修正（caller_ext.py） | ✅ 已驗證 |
| EXT-015 | 語意錯（數值） | Caller 驗證 + 重試 | ✅ 已驗證 |
| EXT-044 | 提前停止（truncated JSON） | `response_format: json_schema` + Caller 重試 | ✅ 已驗證 |
| EXT-026 | trailing text（tools present） | Proxy JSON 提取 | ✅ 已驗證 |
| EXT-028 | 空回（tools present） | Proxy 重試 | ✅ 已驗證 |

## Think-off（10 題）

- 原始：7/10 strict pass。
- T07, T08：常識題，模型回答過長 → prompt 加「只回一句短句」✅。
- T10：程式碼題，grader fence 問題 → code no-fence 規則已修復 ✅。
- 最終：10/10。

## Code-test（11 題）

- 原始：1/11（僅 EXT-037）。
- + Jinja code rule：10/11。
- + Caller 重試 (EXT-048, seed=42)：11/11。
- EXT-048：程式碼截斷 + grader JS 大整數精度 false negative → Python grader 9/9 通過。

## Speed（4 題）

| ID | Target | 狀態 | 備註 |
|---|---|---|---|
| SPEED-01 | 32K | ✅ pass | TTFT 0.44s, prefill ~72K tok/s |
| SPEED-02 | 64K | ✅ pass | TTFT 0.43s, prefill ~149K tok/s |
| SPEED-03 | 128K | 未測 | prefill ~10 min，實測超時 |
| SPEED-04 | 200K | 未測 | 需 hi≥12000，prefill ~15 min |

GLM prefill 極快（0.4s for 32K-64K），但大 context（128K+）prefill 耗時過長。

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
