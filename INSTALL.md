# 安裝指引（Installation Guide）

本指引從零開始，在 Mac Studio 上安裝 GLM-5.3-Flash + oMLX + Jinja v1 + Proxy + Caller 三層防護。

## 前置需求

- Mac Studio M3 Ultra（或 M 系列 Mac），建議 512GB RAM。
- macOS 26+（oMLX DMG macos26-27）。
- Homebrew。
- Python 3.10+。
- （選用）OpenCode CLI。

## Step 1：安裝 oMLX

1. 下載 oMLX 0.7.3.dev2 DMG（macos26-27），安裝至 `/Applications/oMLX.app`。
2. 啟動 oMLX，確認服務監聽 `http://127.0.0.1:8000`。

## Step 2：下載模型

```bash
# 需 HF_TOKEN
huggingface-cli download Jundot/GLM-5.3-Flash-oQ4e-mtp \
  --local-dir ~/.omlx/models/Jundot/GLM-5.3-Flash-oQ4e-mtp \
  --resume-download
```

模型大小 ~174 GB（35 個 safetensors）。若下載中斷，重新執行即可 resume；必要時清除 stale locks。

## Step 3：設定模型參數

編輯 `~/.omlx/model_settings.json`，新增 alias `glm5.3`：

```json
{
  "glm5.3": {
    "path": "~/.omlx/models/Jundot/GLM-5.3-Flash-oQ4e-mtp",
    "ctx": 262144,
    "max_tokens": 8192,
    "temperature": 1.0,
    "top_p": 0.95,
    "top_k": 40,
    "reasoning_effort": "low",
    "thinking_budget": 1024,
    "mtp_enabled": true,
    "turboquant_kv": "4-bit",
    "is_pinned": true
  }
}
```

## Step 4：覆寫 Jinja 模板

```bash
cp v1/chat_template.jinja \
   ~/.omlx/models/Jundot/GLM-5.3-Flash-oQ4e-mtp/chat_template.jinja
```

先備份原版（若尚未備份）：

```bash
cp ~/.omlx/models/Jundot/GLM-5.3-Flash-oQ4e-mtp/chat_template.jinja \
   ~/.omlx/models/Jundot/GLM-5.3-Flash-oQ4e-mtp/chat_template.jinja.bak-zai-original-$(date +%Y%m%d)
```

重啟 oMLX（App UI 或重啟服務）。

載入前核對首行版本字串（浮水印），確認模板是否在位。

## Step 5：安裝 Proxy

複製 proxy 程式：

```bash
cp proxy/proxy.py ~/.omlx/proxy.py
chmod +x ~/.omlx/proxy.py
```

啟動：

```bash
python3 ~/.omlx/proxy.py
# 監聽 127.0.0.1:8001，轉發至 oMLX 127.0.0.1:8000
```

### 設定 LaunchAgent（開機自啟）

建立 `~/Library/LaunchAgents/com.arthur.omlx-proxy.plist`：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.arthur.omlx-proxy</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/python3</string>
    <string>/Users/arthur/.omlx/proxy.py</string>
  </array>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
  <key>StandardOutPath</key>
  <string>/tmp/omlx-proxy.log</string>
  <key>StandardErrorPath</key>
  <string>/tmp/omlx-proxy.log</string>
</dict>
</plist>
```

載入：

```bash
launchctl load ~/Library/LaunchAgents/com.arthur.omlx-proxy.plist
```

重啟 proxy：

```bash
launchctl unload ~/Library/LaunchAgents/com.arthur.omlx-proxy.plist
launchctl load ~/Library/LaunchAgents/com.arthur.omlx-proxy.plist
```

## Step 6：安裝 Caller（選用）

```bash
cp caller/caller.py caller/caller_ext.py ~/.omlx/
```

使用：

```python
from caller import call_glm, validate_v2q022
result = call_glm(prompt, validate_fn=validate_v2q022,
                 response_format={"type": "json_schema", ...})
```

## Step 7：OpenCode 整合

編輯 `~/.config/opencode/opencode.json`，`mac` provider 的 `baseURL` 改為 `http://127.0.0.1:8001/v1`，新增 model entry `glm5.3`：

```json
{
  "provider": {
    "mac": {
      "baseURL": "http://127.0.0.1:8001/v1",
      "models": {
        "glm5.3": {
          "context": 262144,
          "output": 8192,
          "image": true,
          "reasoning": true
        }
      }
    }
  }
}
```

呼叫 ID：`mac/glm5.3`。

## Step 8：Splash（選用，ANE prefill 加速）

```bash
brew install incoai/tap/splash
```

在 oMLX App UI → Model Settings → External Engine → Splash 手動切換啟用。

## 驗證安裝

```bash
# 1. oMLX
curl -s http://127.0.0.1:8000/v1/models

# 2. Proxy
curl -s -H "Authorization: Bearer Yuka1001" \
  -H "Content-Type: application/json" \
  http://127.0.0.1:8001/v1/chat/completions \
  -d '{"model":"glm5.3","messages":[{"role":"user","content":"Hello"}],"max_tokens":50}'

# 3. Jinja 浮水印
head -1 ~/.omlx/models/Jundot/GLM-5.3-Flash-oQ4e-mtp/chat_template.jinja
```

## 常見問題

見 [TROUBLESHOOTING.md](TROUBLESHOOTING.md) 與 [PITFALLS.md](PITFALLS.md)。
