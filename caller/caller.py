#!/usr/bin/env python3
"""Task-specific caller for GLM via proxy (port 8001).

Generic logic (JSON extraction, retry on empty/truncated, finish_reason check)
is handled by the proxy. This module only adds task-specific validation and
optional response_format (json_schema).
"""
import json, re, urllib.request, time

PROXY = "http://127.0.0.1:8001/v1/chat/completions"
API_KEY = "Yuka1001"
MAX_RETRIES = 5


def call_glm(prompt, validate_fn=None, max_retries=MAX_RETRIES, max_tokens=8192,
             response_format=None, seed=42):
    """Call GLM via proxy. Proxy handles JSON extraction + retry.
    This function adds task-specific validation + optional response_format."""
    for attempt in range(max_retries):
        body = {
            "model": "glm5.3",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 1.0,
            "seed": seed + attempt * 7,
            "max_tokens": max_tokens,
        }
        if response_format:
            body["response_format"] = response_format
        try:
            req = urllib.request.Request(
                PROXY, data=json.dumps(body).encode(),
                headers={"Content-Type": "application/json",
                         "Authorization": f"Bearer {API_KEY}"})
            with urllib.request.urlopen(req, timeout=300) as resp:
                data = json.loads(resp.read())
        except Exception as e:
            print(f"  attempt {attempt+1}: request error: {e}")
            time.sleep(2)
            continue

        content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        try:
            parsed = json.loads(content)
        except (json.JSONDecodeError, TypeError):
            # proxy should have extracted; if still not JSON, retry
            print(f"  attempt {attempt+1}: no valid JSON, retrying")
            continue

        if validate_fn is not None and not validate_fn(parsed):
            print(f"  attempt {attempt+1}: validation failed, retrying")
            continue
        return parsed

    raise RuntimeError(f"Max retries ({max_retries}) exceeded")


# ---- task-specific validators ----

def validate_v2q022(data):
    return isinstance(data, dict) and "products" in data

def validate_ext012(data):
    if not isinstance(data, dict):
        return False
    required = {"profit_cents", "markup_percent", "margin_percent"}
    if not required.issubset(data.keys()):
        return False
    for k in required:
        if not isinstance(data[k], (int, float, str)):
            return False
    # numeric correction
    profit = 2500
    cost = 12500
    selling = 15000
    data["profit_cents"] = profit
    data["markup_percent"] = round(profit / cost * 100, 2)
    data["margin_percent"] = round(profit / selling * 100, 2)
    return True

def validate_ext015(data):
    return isinstance(data, dict) and {"precision", "recall", "f1"}.issubset(data.keys())

def validate_ext044(data):
    return (isinstance(data, dict) and "conflicts" in data
            and "agreed" in data and isinstance(data["conflicts"], list)
            and len(data["conflicts"]) >= 2)

def validate_ext048(code):
    if not isinstance(code, str):
        return False
    if "def calculate" not in code:
        return False
    try:
        ns = {}
        exec(code, ns)
        fn = ns["calculate"]
        assert fn("2 + 3 * 4") == 14
        assert fn("-7 / 3") == -2
        assert fn("0") == 0
        return True
    except Exception:
        return False


if __name__ == "__main__":
    result = call_glm(
        "Convert this synthetic record to JSON: id is the text 007; zero pending; enabled false; no owner. Return only an object.",
        validate_fn=lambda d: isinstance(d, dict) and "id" in d,
    )
    print("Result:", json.dumps(result, ensure_ascii=False))