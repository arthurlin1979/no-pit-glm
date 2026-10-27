# 30 秒 Quick Start

## 人用：三步確認

1. 確認 oMLX 已載入 GLM-5.3-Flash，alias `glm5.3`，context 262144。
2. 覆寫 Jinja 模板並重啟 oMLX：`cp v1/chat_template.jinja ~/.omlx/models/Jundot/GLM-5.3-Flash-oQ4e-mtp/chat_template.jinja`
3. 啟動 Proxy：`python3 proxy/proxy.py`，確認監聽 127.0.0.1:8001。

## AI 用：三頁開工

1. 讀 [AGENTS.md](AGENTS.md)：了解三層防護與 Jinja 規則。
2. 讀 [PITFALLS.md](PITFALLS.md)：判斷問題屬於 Jinja / Proxy / Caller 哪一層。
3. 讀 [catalogue/INDEX.md](catalogue/INDEX.md)：查是否有歷史紀錄。

## 常用命令

```bash
# 驗證 proxy
curl -s -H "Authorization: Bearer Yuka1001" \
  -H "Content-Type: application/json" \
  http://127.0.0.1:8001/v1/chat/completions \
  -d '{"model":"glm5.3","messages":[{"role":"user","content":"Hello"}],"max_tokens":50}'

# 重啟 proxy (LaunchAgent)
launchctl unload ~/Library/LaunchAgents/com.arthur.omlx-proxy.plist
launchctl load ~/Library/LaunchAgents/com.arthur.omlx-proxy.plist

# 重啟 oMLX (after template change)
# (via oMLX app UI or restart service)
```
