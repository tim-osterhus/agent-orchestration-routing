# Controller designs

All designs share the master catalog, variants, work-order contract, and evidence checks. `--variant` chooses pool preference. `--design` describes the actual controller host and determines dispatch. Neither changes an already running conversation. Permissions and bias are independent controls.

Shared Amusing also permits Muse investigation or authorized implementation through a separately verified provider adapter, including a configured durable adapter. Muse is external under both designs. The bundled planner cannot launch it. Use the conditional [Muse provider checks](../skills/agent-orch-router/references/muse.md).

| Responsibility | Codex-first | Claude-first | Claude plugin |
| --- | --- | --- | --- |
| Primary controller | Existing Codex chat | Existing Claude Code session | Claude Code session with the agent-orch plugin |
| Native workers | Codex subagents | Claude Agent workers | Pinned Claude and Codex profile agents |
| Secondary provider | Claude through `claude-delegation` | Codex through a bounded `codex exec` session | None; Codex runs through app-server relay agents |
| Optional cross-provider review | Read-only Claude consultation | Read-only Codex worker | Claude or Codex profile agent in a review role |
| Optional team | External Opus controller plus Haiku workers | Native Opus controller plus Haiku workers | Native Opus controller plus Haiku workers |
| Integration owner | Codex controller | Claude controller | Claude controller |

The primary host is not a claim that its models are always cheaper or better. Both provider-primary variants work with either host design. For example, `--variant claude-primary --design claude-first --profile OH` resolves a native Claude worker. The variant alone leaves the current design unchanged. An author cannot be the sole acceptance check, but cross-provider review is optional.

Burn mode names select the allowance provider, not the controller. `codex-burn` uses native Codex workers under Codex-first and external Codex workers under Claude-first. `claude-burn` uses external Claude workers under Codex-first and native Claude workers, including bounded Haiku, under Claude-first. Each requires explicit account and endpoint identifiers. Neither changes authentication or enables Orchestration. The parent tracks active external sessions across descendants and honors actual runtime, provider, project, and explicit configured limits. The router adds no default concurrency ceiling.

## Codex-first

This is the default and follows the source router's architecture. Invoke the router in a Codex chat. Use native model/effort controls for eligible Codex workers. Use the Claude companion for independent Claude consultation or authored work. The optional Opus/Haiku preset permits a Claude-led subtree only when explicitly requested.

The Codex controller retains task authority and final acceptance. Give Claude assignments bounded packets, disjoint write ownership, and evidence contracts. Claude helpers may delegate within selected permissions, tools, pool, and role fences without a router-imposed leaf-only rule. Do not let them start a second Codex controller or delegate through unrelated chats. Native service-tier inheritance and browser access must be checked rather than assumed.

## Claude-first

Start in Claude Code and invoke the same router through its local skill mechanism. Native Agent definitions use the selected Claude profiles and role restrictions. The optional preset is applied to that native controller only after the user requests its permission mode. A configuration change cannot retroactively enable bypass or change the model of the running parent.

For secondary Codex work, preflight the native `codex` executable, relevant help flags, and `codex login status`. Check alternate credential/provider routing without reading secret stores. Use the existing authorized account. Do not silently switch to API billing.

From the bundle root, with an existing `task.txt`:

```sh
python3 scripts/bundle.py codex-plan --design claude-first --profile SM --role implementation --cwd . --prompt-file task.txt --artifacts .runs/codex
```

The plan uses `codex exec` with an exact model/effort and JSONL output. Sandbox and approval choices come from the separate Codex configuration. The supplied defaults use read-only or workspace-write sandboxing and no interactive prompts. An operator can override them or explicitly configure bypass. The caller verifies that the unattended route supports the configured approval policy, records the session ID, and checks results independently. Sandbox restrictions do not authorize connector side effects or prove that every tool is read-only.

Cross-provider Codex workers are leaves by default. They must not reopen this router, recursively call Claude, or broaden ownership. Claude retains integration and acceptance. The primary session owns cancellation, any user deadline, and accounting for configured external-session limits across descendants.

## Claude plugin

Install the agent-orch plugin as described in [configuration](configuration.md#claude-code-plugin) and invoke the router in Claude Code. `--design claude-plugin` resolves every Codex and Claude profile to a pinned agent such as `agent-orch:codex-sm` or `agent-orch:claude-oh`. Codex agents are Haiku relays for persistent Codex app-server threads, so Codex counts as native here and `codex-plan` refuses these routes. Muse remains external.

Workers share the checkout. The controller assigns disjoint Write lists, checks them with `bundle.py snapshot` and `check-ownership`, sequences overlapping or dependent work, and routes every handoff itself by resuming the owning worker's exact thread. See [Claude plugin dispatch](../skills/agent-orch-router/references/claude-plugin.md).

## Initial implementation boundary

Codex-first and Claude-first have configuration, skill instructions, offline eligibility checks, and new-session launch-plan generation. There is no dispatcher, durable scheduler, live installer, or verified completion callback. Native spawning is performed by the host agent, not by the Python script. The Claude plugin adds pinned host agents, a vendored app-server runtime, and offline ownership checks; the Python script still never dispatches a model.

CLI plan generators reject native routes. Use native host controls instead of launching another CLI controller. External Codex plans accept Standard-targeted new-session profiles only. They do not set a tier. Verify and report the actual inherited/effective tier without changing global speed settings. Retired Fast codes and modes fail instead of falling back. Exact-session Codex resume and native Claude-first launch/permission changes remain caller responsibilities. Claude plans support exact-ID resume but do not manage elapsed deadlines.

A later runtime layer could add portable process-tree supervision, owner-bound callbacks, and capability probes without changing the shared routing policy. Those are proposed next steps, not claims about the current template.
