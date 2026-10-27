#!/usr/bin/env python3
"""OpenAI-compatible proxy in front of oMLX (Mac GLM).

Listens on 127.0.0.1:8001, forwards to oMLX at 127.0.0.1:8000.
For non-streaming chat completions, extracts the first JSON value from the
model's content (stripping fences / trailing text) and retries on empty or
truncated responses. Streaming requests are passed through untouched.
"""
import json, re, threading, time, urllib.request, urllib.error
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

OMLX = "http://127.0.0.1:8000"
LISTEN = ("127.0.0.1", 8001)
MAX_RETRIES = 3
TIMEOUT = 600


def _forward(path, method, headers, body=None):
    url = OMLX + path
    req = urllib.request.Request(url, data=body, method=method)
    for k, v in headers.items():
        if k.lower() in ("host", "content-length", "connection", "transfer-encoding"):
            continue
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return resp.status, dict(resp.headers), resp.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read()


def _extract_json(content):
    # Try to parse the first JSON value (object or array) using raw_decode,
    # which stops at the end of the value and ignores trailing text.
    content = content.strip()
    # Find the first { or [
    idx = -1
    for i, ch in enumerate(content):
        if ch in '{[':
            idx = i
            break
    if idx == -1:
        return None
    try:
        obj, end = json.JSONDecoder().raw_decode(content[idx:])
        return obj
    except json.JSONDecodeError:
        # fallback: greedy regex
        m = re.search(r'\{[\s\S]*\}|\[[\s\S]*\]', content)
        if not m:
            return None
        try:
            return json.loads(m.group(0))
        except json.JSONDecodeError:
            return None


def _chat_with_retry(body):
    """Return (status, headers, parsed_json_response) with cleaned content."""
    last_err = None
    for attempt in range(MAX_RETRIES):
        status, headers, raw = _forward("/v1/chat/completions", "POST",
                                       {"Content-Type": "application/json",
                                        "Authorization": body.get("_auth", "")},
                                       json.dumps({k: v for k, v in body.items() if k != "_auth"}).encode())
        if status != 200:
            return status, headers, raw
        try:
            data = json.loads(raw)
        except Exception as e:
            last_err = e
            continue
        choice = (data.get("choices") or [{}])[0]
        msg = choice.get("message") or {}
        content = msg.get("content") or ""
        tcs = msg.get("tool_calls") or []
        fr = choice.get("finish_reason")
        # try to extract a complete JSON value
        extracted = _extract_json(content)
        is_json_prompt = "json" in content.lower() or any("json" in str(m.get("content","")).lower() for m in body.get("messages",[]))
        # retry on empty, truncated, or incomplete JSON (when JSON was expected)
        if len(tcs) == 0 and (content.strip() == "" or fr == "length" or (is_json_prompt and extracted is None)):
            last_err = Exception(f"empty/truncated/incomplete-json (finish_reason={fr})")
            continue
        # clean content: extract first JSON value if present
        if extracted is not None:
            msg["content"] = json.dumps(extracted, ensure_ascii=False)
            data["choices"][0]["message"] = msg
        return 200, headers, json.dumps(data, ensure_ascii=False).encode()
    # all retries failed: return last raw
    return 500, {}, json.dumps({"error": {"message": str(last_err)}}).encode()


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _auth(self):
        return self.headers.get("Authorization", "")

    def do_GET(self):
        if self.path == "/v1/models" or self.path.startswith("/v1/models"):
            status, headers, raw = _forward(self.path, "GET",
                                           {"Authorization": self._auth()})
            self.send_response(status)
            self.send_header("Content-Type", headers.get("Content-Type", "application/json"))
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length) if length else b""
        try:
            body = json.loads(raw) if raw else {}
        except Exception:
            body = {}
        body["_auth"] = self._auth()
        path = self.path.split("?")[0]
        if path == "/v1/chat/completions":
            # streaming pass-through
            if body.get("stream"):
                status, headers, raw2 = _forward(path, "POST",
                                                {"Content-Type": "application/json",
                                                 "Authorization": self._auth()},
                                                json.dumps({k: v for k, v in body.items() if k != "_auth"}).encode())
                self.send_response(status)
                self.send_header("Content-Type", headers.get("Content-Type", "text/event-stream"))
                self.send_header("Content-Length", str(len(raw2)))
                self.end_headers()
                self.wfile.write(raw2)
                return
            status, headers, out = _chat_with_retry(body)
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(out)))
            self.end_headers()
            self.wfile.write(out)
        else:
            status, headers, raw2 = _forward(path, "POST",
                                            {"Content-Type": "application/json",
                                             "Authorization": self._auth()},
                                            json.dumps({k: v for k, v in body.items() if k != "_auth"}).encode())
            self.send_response(status)
            self.send_header("Content-Type", headers.get("Content-Type", "application/json"))
            self.send_header("Content-Length", str(len(raw2)))
            self.end_headers()
            self.wfile.write(raw2)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    httpd = ThreadingHTTPServer(LISTEN, Handler)
    print(f"proxy listening on http://{LISTEN[0]}:{LISTEN[1]} -> {OMLX}", flush=True)
    httpd.serve_forever()
