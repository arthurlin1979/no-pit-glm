# No-Pit: GLM-5.3-Flash (Mac oMLX)

[中文版](README.md)

Updated: 2026-10-28

Practical experience for AI agents and developers integrating GLM-5.3-Flash: Jinja output discipline + OpenAI-compatible proxy + caller-side validation — three layers of defense so GLM on Mac Studio stops tripping you up.

This project consolidates real format/leakage/truncation problems we hit, the fixes we applied, and verifiable external rules. Solutions combine our own experiments, official docs, and community data; partly searched and edited with AI assistance. Not all methods are claimed as our invention. Independent work — not affiliated with or endorsed by Z.ai / Zhipu / oMLX upstream.

## Why this project

GLM-5.3-Flash is no slouch on Mac Studio M3 Ultra (prefill ~253 tok/s) but format-following is unstable: quantized models often emit JSON fences, trailing text, empty replies, bare arrays, truncated code. The model alone is not enough — you need Jinja-level output discipline, proxy-level JSON extraction + retry, and caller-level schema validation.

We organized every pitfall we hit into a queryable database. When something breaks, check: have we seen this before? Before starting work, read: what could affect this?

Benchmark journey (114 questions): Ability 62/100 → 100/100 (theoretical, with caller handling), Code-test 1/11 → 11/11, Think-off 7/10 → 10/10, Speed 32K/64K pass.

## Start here

- [Introduction](INTRO.md)
- [Installation guide](INSTALL.md)
- [Entry for AI agents](AGENTS.md)
- [30-second Quick Start](QUICKSTART.md)
- [Troubleshooting](TROUBLESHOOTING.md)
- [Full record index](catalogue/INDEX.md)
- [Measured speed](catalogue/speed.md)
- [Pitfalls quick reference](PITFALLS.md)
- [Jinja change blocks](BLOCKS.md)
- [Sources & versions](SOURCES.md)
- [Third-party notices](THIRD_PARTY_NOTICES.md)
- [v1 release notes](v1/RELEASE.md)
- [v1 Jinja template](v1/chat_template.jinja)
- [Proxy](proxy/proxy.py)
- [Caller wrapper](caller/caller.py)
- [Caller extensions](caller/caller_ext.py)

## Minimal usage

1. Confirm oMLX has loaded GLM-5.3-Flash and `~/.omlx/model_settings.json` sets alias `glm5.3`.
2. Overwrite the Jinja template: `cp v1/chat_template.jinja ~/.omlx/models/Jundot/GLM-5.3-Flash-oQ4e-mtp/chat_template.jinja`, restart oMLX.
3. Start the proxy: `python3 proxy/proxy.py` (or LaunchAgent), listening on port 8001.
4. Point OpenCode / harness / curl at `http://127.0.0.1:8001/v1`.
5. When results are unclear, read back first; do not blindly replay create/append.

## Three-layer defense

```
OpenCode / harness / curl
        │
        ▼
   Proxy (port 8001)  ←── generic caller logic (JSON extraction + retry + finish_reason check)
        │
        ▼
   oMLX (port 8000)   ←── Jinja template (format rules + output discipline)
        │
        ▼
   GLM-5.3-Flash (M3 Ultra)
```

| Layer | Location | Function | All clients benefit? |
|---|---|---|---|
| Jinja | oMLX template | Format rules (no fence, JSON discipline, spec-fidelity, tool-result) | ✅ Yes |
| Proxy | port 8001 | JSON extraction + retry + finish_reason check | ✅ Yes |
| Caller | `caller/caller.py` | Task-specific validation + response_format + retry | ❌ Programmatic calls only |

## Jinja rules (v1)

| Group | Trigger | Rules |
|---|---|---|
| JSON | user contains `json` and no tools | 7 output-discipline rules + spec-fidelity |
| Code | user contains `原始碼`/`code`/`python` and no tools | no fence + spec-fidelity |
| Tool-result | tools present + tool result + user contains `json` | JSON-only + spec-fidelity |

## Journey overview

| Stage | Ability | Code-test | Fix |
|---|---|---|---|
| Raw (no Jinja) | 62/100 | 1/11 | — |
| + Jinja v7 (7 rules) | 82/100 | 1/11 | format/leakage errors |
| + Jinja code rule | 82/100 | 10/11 | code fence removal |
| + Jinja spec-fidelity | 83/100 | 10/11 | EXT-019 semantic |
| + Proxy (8001) | 86/100 | 10/11 | EXT-023/026/028 |
| + Caller wrapper | 88/100 | 10/11 | EXT-015/044 pass |
| + json_schema (API layer) | 90/100 | 10/11 | V2-Q022/EXT-044 pass |
| + Caller numeric correction | 91/100 | 10/11 | EXT-012 pass |
| + Caller retry (EXT-048) | 91/100 | 11/11 | EXT-048 pass (seed=42) |

## Known limits

- Semantic errors (EXT-012/015): Jinja cannot fix; needs caller validation + retry or stronger model.
- Code truncation (EXT-048): needs caller retry + fixed seed; grader must use Python not JS (large-integer precision).
- Speed suite: GLM prefill is very fast (0.4s for 32K-64K); 128K/200K not measured (prefill too slow).
- Splash (ANE prefill): installed; must be enabled manually in oMLX App UI.

## License

Except where third-party content is explicitly marked, original text, arrangement, and examples in this project are released under the [MIT License](LICENSE).

The Jinja template is derived from the Z.ai original (chat_template.jinja.bak-zai-original-20261027). Proxy/Caller are original work, MIT licensed.

## Scope & maintenance

This is a curated consolidation of existing records, not a complete list of all GLM issues, and does not guarantee the same results in other versions or environments. Status and parameters are historical records; this document package did not re-run live validation and cannot be taken as a guarantee of current production state.

Private raw records, customer data, environment settings, conversation logs, and Git history are not part of this document package.
