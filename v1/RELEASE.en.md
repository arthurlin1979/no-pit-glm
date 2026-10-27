# v1 Release Notes

Updated: 2026-10-28

## Position

v1 is the current default version of this project: it ports Qwen v7's 7 JSON output-discipline rules to GLM-5.3-Flash, plus a Code no-fence rule, a spec-fidelity clause, and a tool-result JSON-only rule.

## Changes vs. Z.ai original

See [BLOCKS.md](../BLOCKS.md) and [v1_vs_original.diff](./v1_vs_original.diff).

- Group 1: 7 JSON output-discipline rules + spec-fidelity (trigger: user contains `json` and no tools).
- Group 2: Code no-fence + spec-fidelity (trigger: user contains `原始碼`/`code`/`python` and no tools).
- Group 3: Tool-result JSON-only + spec-fidelity (trigger: tools present + tool result + user contains `json`).

## Measured results

- Ability: 62/100 → 91/100 (with Jinja/Proxy/Caller).
- Code-test: 1/11 → 11/11.
- Think-off: 7/10 → 10/10.
- Speed: 32K/64K pass.

## Usage

```bash
# oMLX
cp ./v1/chat_template.jinja ~/.omlx/models/Jundot/GLM-5.3-Flash-oQ4e-mtp/chat_template.jinja
# restart oMLX

# vLLM
vllm serve <model> --chat-template ./v1/chat_template.jinja

# llama.cpp
llama-server -m <model.gguf> --jinja --chat-template-file ./v1/chat_template.jinja
```

## Known limits

- Semantic errors (EXT-012/015): needs caller validation + retry or stronger model.
- Code truncation (EXT-048): needs caller retry + fixed seed.
- Speed large context (128K/200K): prefill too slow, not measured.

## License

MIT (see [LICENSE](../LICENSE)).
