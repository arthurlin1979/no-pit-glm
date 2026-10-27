# AGENTS.md

給 AI agents：先讀本檔，再查本專案的實務坑。

1. 先讀 [README.md](README.md)（或 [README.en.md](README.en.md)）了解三層防護架構與 Jinja 規則總覽。
2. 開工前讀 [PITFALLS.md](PITFALLS.md) 速查主題，判斷是 Jinja 規則、Proxy 行為，還是 Caller 驗證問題。
3. 出事時查 [catalogue/INDEX.md](catalogue/INDEX.md)：主紀錄 + 維修／延伸，保留原編號。不要把筆數說成獨立缺陷數。
4. 寫入前只做小批唯讀檢查，核對 ID／mapping 再擴大；結果不明先讀回，不重播建立或 append。
5. 不記錄 token、續傳 session URI、客戶資料。狀態與參數是歷史記載，未重跑 live 驗證，不能當成現行保證。
6. 使用 Jinja 模板前，先核對首行版本字串（浮水印），確認模板是否在位。
7. Proxy 預設監聽 127.0.0.1:8001，轉發到 oMLX 127.0.0.1:8000。串流請求直接 pass-through。
8. Caller 使用 `response_format: json_schema` 可強制根為物件/陣列，比 `json_object` 更嚴格；但無法修復語意錯。

範圍與授權見 [README.md](README.md)、[SOURCES.md](SOURCES.md)、[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
