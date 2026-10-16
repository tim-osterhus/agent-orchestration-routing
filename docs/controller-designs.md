# Two controller designs

Both designs share the registry, routing pools, role restrictions, work-order contract, and evidence checks. Choose `controller_design` in the configuration or use `--design` when inspecting a route. This chooses dispatch interpretation, not the host of an already running conversation.

| Responsibility | Codex-first | Claude-first |
| --- | --- | --- |
| Primary controller | Existing Codex chat | Existing Claude Code session |
| Native workers | Codex subagents | Claude Agent workers |
| Secondary provider | Claude through `claude-delegation` | Codex through a bounded `codex exec` session |
| Default cross-provider review | Read-only Claude consultation | Read-only Codex worker |
| Optional team | External Opus controller plus Haiku workers | Native Opus controller plus Haiku workers |
| Integration owner | Codex controller | Claude controller |

The primary host is not a claim that its models are always cheaper or better. Apply task suitability and the configured pools on either host. A caller may maintain different mode pools per design through configuration overlays. Account availability and specialist tools can justify an explicit exception to the benchmark frontier.

## Codex-first

This is the default and follows the source router's architecture. Invoke the router in a Codex chat. Use native model/effort controls for eligible Codex workers. Use the Claude companion for independent Claude consultation or authored work. The optional Opus/Haiku preset permits a Claude-led subtree only when explicitly requested.

The Codex controller retains task authority and final acceptance. Give an external team a bounded packet, disjoint write ownership, and an evidence contract. Do not let it start a second Codex controller or delegate through unrelated chats. Native service-tier inheritance and browser access must be checked rather than assumed.

## Claude-first

Start in Claude Code and invoke the same router through its local skill mechanism. Native Agent definitions use the selected Claude profiles and role restrictions. The optional preset is applied to that native controller only after the user requests its permission mode. A configuration change cannot retroactively enable bypass or change the model of the running parent.

For secondary Codex work, preflight the native `codex` executable, relevant help flags, and `codex login status`. Check alternate credential/provider routing without reading secret stores. Use the existing authorized account. Do not silently switch to API billing.

From the bundle root, with an existing `task.txt`:

```sh
python3 scripts/bundle.py codex-plan --design claude-first --profile SM --role implementation --cwd . --prompt-file task.txt --artifacts .runs/codex
```

The plan uses `codex exec` with an exact model/effort and JSONL output. Sandbox and approval choices come from the separate Codex configuration. The supplied defaults use read-only or workspace-write sandboxing and no interactive prompts. An operator can override them or explicitly configure bypass. The caller verifies that the unattended route supports the configured approval policy, records the session ID, and checks results independently. Sandbox restrictions do not authorize connector side effects or prove that every tool is read-only.

Cross-provider Codex workers are leaves by default. They must not reopen this router, recursively call Claude, or broaden ownership. Claude retains integration and acceptance. The primary session owns cancellation, any user deadline, and the external-session slot.

## Initial implementation boundary

Both designs have configuration, skill instructions, offline eligibility checks, and new-session launch-plan generation. There is no dispatcher, durable scheduler, live installer, or verified completion callback. Native spawning is performed by the host agent, not by the Python script.

The external Codex plan generator supports Standard-tier new sessions only. It rejects Fast because this version does not verify the CLI's tier controls. Exact-session Codex resume and native Claude-first launch/permission changes are caller responsibilities, not implemented automation. Claude plans support exact-ID resume but do not manage the original deadline's elapsed time.

A later runtime layer could add portable process-tree supervision, owner-bound callbacks, and capability probes without changing the shared routing policy. Those are proposed next steps, not claims about the current template.
