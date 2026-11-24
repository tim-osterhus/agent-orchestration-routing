# Local Antigravity CLI

Read only for GNH or GNX. Use standalone `agy` on the existing Google subscription, not the Gemini API, a Claude relay, T3, Orchestrator (Neon), or `/swarm`.

| Alias | Exact `agy --model` ID | Effort |
| --- | --- | --- |
| GNH | `gemini-4-neon-high` | High |
| GNX | `gemini-4-neon-xhigh` | XHigh |

Check `agy --version`, `agy --help`, and `agy models` in the intended workspace and login context. A listed model does not prove live entitlement. Check for API key, ADC, endpoint, or billing overrides without printing credentials. Stop on route ambiguity, access failure, or quota exhaustion. Do not switch accounts, enable billing, or substitute models.

Use a fresh session for these read-only assignments. Pass the exact question, allowed inputs, and required evidence. Do not ask the worker to edit, delegate, or use unrelated tools. Verify auto-loaded instructions and memory before claiming an independent review.

Run from the authorized workspace. Store the prompt and results in a private run directory. Set `neon_model` to the exact ID above. Plan mode and the terminal sandbox do not by themselves prove that every available tool is read-only.

```sh
jq -cn --rawfile prompt "$run_dir/prompt.txt" '{event:"user",message:{content:$prompt}}' |
  agy --model "$neon_model" --mode plan --sandbox \
    --input-format stream-json --output-format stream-json \
    > "$run_dir/result.jsonl" 2> "$run_dir/stderr.log"
```

Do not disable slash command expansion when relying on plan mode. Start the prompt with a plain-text work-order header, not a slash command.

Check the process exit, reported model selection, terminal result, and conversation ID. Verify material claims against local evidence and inspect any tool actions. Disclose missing route metadata. For continuity, resume only the recorded conversation. Never resume an earlier conversation for independent review.

[Google model selector](https://antigravity.google/docs/models) · [Headless CLI](https://antigravity.google/docs/cli/headless/)
