# 實測速度（Measured Speed）

測試環境：Mac Studio M3 Ultra 512GB，oMLX 0.7.3.dev2，模型 glm5.3（Jundot/GLM-5.3-Flash-oQ4e-mtp，oQ4e 4.641 bits/w，173.6 GiB），ctx 262144，mtp_enabled，turboquant_kv 4-bit。

數據來源：harness results.json（`glm5.3-pre-v7` 首輪完整跑、`glm5.3-speed` 32K/64K 重跑），OB 存檔 `AIout/Reports/20261027-glm5.3-full-journey-report.md`。

## 110 題生成速度（Ability 100 + Think-off 10，2026-10-26 首輪完整跑）

| 指標 | 數值 |
|---|---|
| 題數（有生成數據） | 110 |
| 生成速度平均 | 52.1 tok/s |
| 中位數 | 53.3 tok/s |
| P25 / P75 | 48.5 / 58.4 tok/s |
| 排除離群值後平均 / 中位數 | 52.5 / 53.4 tok/s |
| 最小（排除離群值） | 23.4 tok/s |
| 最大 | 75.1 tok/s |
| TTFT 平均 / 中位數 | 0.88s / 0.90s |
| 總生成 tokens | 6,950 |

離群值：V2-Q001 僅 2 tokens（1.52 tok/s），屬超短回覆，統計意義低。

分 suite：

| Suite | 題數 | 生成速度平均 | TTFT 平均 | 平均生成 tokens |
|---|---|---|---|---|
| Ability | 100 | 53.8 tok/s（中位 54.0） | 0.90s | 66 |
| Think-off | 10 | 34.3 tok/s（中位 35.5） | 0.67s | 34 |

重測輪（Jinja v7 之後，走 oMLX 直連）單題區間約 47–63 tok/s；走 proxy（port 8001）約 35–58 tok/s。

## Speed suite 實測（2026-10-27）

| ID | Target | Pass | TTFT | Prefill 速度 | Decode | 備註 |
|---|---|---|---|---|---|---|
| SPEED-01 | 32K（31,982 tokens） | ✅ | 0.44s | ~72K tok/s | 23.6 tok/s | cached_tokens 31,980 |
| SPEED-02 | 64K（63,985 tokens） | ✅ | 0.43s | ~149K tok/s | 25.0 tok/s | cached_tokens 63,983 |
| SPEED-03 | 128K | 未完成 | — | — | — | prefill ~10 min，實測超時 |
| SPEED-04 | 200K | 未測 | — | — | — | 需 hi≥12000，prefill ~15 min |

附註（誠實邊界）：

- oMLX usage 回報的 `cached_tokens` 幾乎全命中（32K/64K 兩題 99.99%），0.4s TTFT 是 KV cache 命中下的重跑數字，不代表冷啟動 prefill 速度。
- oMLX 回報的 `prompt_tokens_per_second` 欄位值（4.5/4.69）與實際計算不符；本表 prefill 速度由 `prompt_tokens ÷ prompt_eval_duration` 重算（31,982 ÷ 0.44s ≈ 72.7K；63,985 ÷ 0.43s ≈ 148.8K）。
- SPEED-03/04 並非超過 262K context（128K、200K 均 < 262K），未完成原因是 harness calibration 的 token 計數不一致（oMLX 對 32,768 records 探測回報 573,231 tokens），已改用 fitPrompt，但大 context prefill 耗時（~10–15 min）實測不實際。

## 其他單點實測

- 基本 React 測試（首次安裝後）：94 completion tokens，30.23 tok/s，reasoning_tokens 0。
- Speed suite decode：~24 tok/s（45–50 tokens 短生成）。

## 觀察

- 短題（平均 66 tokens）生成速度 ~52 tok/s；Speed suite 短生成 ~24 tok/s。兩者皆是 oMLX usage 回報，差異可能來自 MTP/speculative 行為與 prompt 長度，未深入查證，僅記錄現象。
- 253 tok/s 為另一次實測口徑，速度定位為「不算慢」，非極快。
- 128K+ 大 context prefill 耗時 ~10–15 min，實務上不建議在 GLM 上跑 Speed 128K/200K target。