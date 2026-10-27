# 完整紀錄索引（Catalogue Index）

本索引保留 114 題 benchmark 的原編號，分四個 suite：Ability（100 題）、Think-off（10 題）、Code-test（11 題）、Speed（4 題）。各題詳細紀錄見 [records.md](records.md)。

完整脈絡見 [20261027-glm5.3-full-journey-report.md](https://github.com/arthurlin1979/no-pit-glm)（OB 報告，本 repo 外）。

## Ability（100 題）

- V2-Q001 ~ V2-Q030（30 題）：JSON/物件格式、工具呼叫、語意。
- EXT-001 ~ EXT-070（70 題）：擴充題，含 JSON/Code/語意/工具。

詳細見 records.md。

## Think-off（10 題）

- T01 ~ T10：常識/程式碼題，測試 think-off 模式。

## Code-test（11 題）

- EXT-037, EXT-048 等：程式碼生成題。

## Speed（4 題）

- SPEED-01 (32K), SPEED-02 (64K), SPEED-03 (128K), SPEED-04 (200K)。

## 維修／延伸紀錄

- 見 repairs-01-XX.md（若有）。

## 編號規則

- Ability 題目：V2-Qxxx / EXT-xxx。
- Think-off：Txx。
- Code-test：EXT-xxx（程式碼題）。
- Speed：SPEED-xx。

不要把 114 題說成 114 個獨立 GLM 缺陷；多數為 format/leakage 類，Jinja 已修復。
