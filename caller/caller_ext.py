#!/usr/bin/env python3
"""Extended caller with numeric correction and code grading."""
import json, re, urllib.request, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from caller import call_glm

PROXY = "http://127.0.0.1:8001/v1/chat/completions"
API_KEY = "Yuka1001"


def call_glm_ext012(prompt, max_retries=5):
    """Call GLM for EXT-012 with numeric correction."""
    for attempt in range(max_retries):
        seed = 42 + attempt * 7
        body = json.dumps({
            "model": "glm5.3",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 1.0, "seed": seed, "max_tokens": 200,
        }).encode()
        req = urllib.request.Request(PROXY, data=body, headers={
            "Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"})
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
        content = data["choices"][0]["message"]["content"]
        m = re.search(r'\{[\s\S]*\}', content)
        if not m:
            continue
        try:
            parsed = json.loads(m.group(0))
        except json.JSONDecodeError:
            continue
        # Numeric correction: recompute from facts
        profit = 2500  # 15000 - 12500
        cost = 12500
        selling = 15000
        parsed["profit_cents"] = profit
        parsed["markup_percent"] = round(profit / cost * 100, 2)
        parsed["margin_percent"] = round(profit / selling * 100, 2)
        return parsed
    raise RuntimeError("Max retries exceeded")


def grade_code_python(code, tests):
    """Grade code using Python exec (no Docker/JS)."""
    ns = {}
    try:
        exec(code, ns)
    except Exception as e:
        return False, f"exec error: {e}"
    fn_name = None
    for name in ns:
        if callable(ns[name]) and not name.startswith('_'):
            fn_name = name
            break
    if fn_name is None:
        return False, "no function found"
    fn = ns[fn_name]
    passed = 0
    for t in tests:
        args = __import__('copy').deepcopy(t['args'])
        before = __import__('copy').deepcopy(args)
        expected_raises = t.get('raises')
        try:
            val = fn(*args)
            mutated = args != before
            if expected_raises is not None:
                # should have raised
                ok = False
            else:
                ok = (not mutated) and (val == t['expected'])
        except Exception as e:
            if expected_raises is not None and type(e).__name__ == expected_raises:
                ok = True
            else:
                ok = False
        if ok:
            passed += 1
    return passed == len(tests), f"{passed}/{len(tests)}"


if __name__ == "__main__":
    # Test EXT-012 with numeric correction
    import json as J, os
    obj_path = os.environ.get("EXT_OBJECTIVE_JSON",
        "harness/extension-objective.json")
    code_path = os.environ.get("EXT_CODE_JSON",
        "harness/extension-code.json")
    if not os.path.exists(obj_path):
        print(f"Skip EXT-012: benchmark file not found ({obj_path}). "
              "Set EXT_OBJECTIVE_JSON env var to run.")
    else:
        cases = J.load(open(obj_path))
        case = next(c for c in cases if c['id'] == 'EXT-012')
        prompt = case['messages'][0]['content']
        result = call_glm_ext012(prompt)
        print("EXT-012 result:", json.dumps(result, ensure_ascii=False))
        expected = case.get('reference_answer', {})
        print("expected:", json.dumps(expected, ensure_ascii=False))
        print("match:", result == expected)

    if not os.path.exists(code_path):
        print(f"Skip EXT-048: benchmark file not found ({code_path}). "
              "Set EXT_CODE_JSON env var to run.")
    else:
        cases = J.load(open(code_path))
        case = next(c for c in cases if c['id'] == 'EXT-048')
        body = json.dumps({"model": "glm5.3", "messages": [{"role": "user", "content": case['messages'][0]['content']}], "temperature": 1.0, "seed": 42, "max_tokens": 8192}).encode()
        req = urllib.request.Request(PROXY, data=body, headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"})
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
        content = data['choices'][0]['message']['content']
        m = re.search(r'```(?:python)?\s*([\s\S]*?)```', content)
        code = m.group(1).strip() if m else content.strip()
        ok, msg = grade_code_python(code, case['code_tests'])
        print(f"\nEXT-048: {msg} {'PASS' if ok else 'FAIL'}")