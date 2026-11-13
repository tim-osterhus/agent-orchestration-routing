# Vendored Codex companion runtime

Source: [openai/codex-plugin-cc](https://github.com/openai/codex-plugin-cc) v1.0.6, commit `db52e28f4d9ded852ab3942cea316258ae4ef346` (2026-07-07). Licensed under Apache-2.0; see `LICENSE` and `NOTICE` in this folder. The rest of this repository is MIT.

Included: `scripts/` (companion, broker, session hook, `lib/`), `prompts/adversarial-review.md`, and `schemas/review-output.schema.json`, so the copied companion still loads every module it imports.

Added for agent-orch, not vendored: `scripts/subagent-status.mjs` and `scripts/lib/relay-activity.mjs`. The plugin's `settings.json` names the first as Claude Code's `subagentStatusLine` command. About every 5 seconds it maps each running Codex relay to its job, through the relay's transcript (`<project>/<session>/subagents/agent-<task id>.jsonl`, whose first line carries the work order path) and the work order's marker. It then prints that row's Codex activity, Codex token total, and elapsed time. Rows it cannot resolve keep Claude Code's default rendering.

Not included: the Stop-hook review gate and its prompt, the `/codex:*` slash commands, the `codex-rescue` agent, and the bundled prompting skills. The agent-orch plugin dispatches through its own generated profile agents instead.

## Modifications

Each modified file starts with a notice line. All changes are on top of the unmodified import commit.

| File | Change |
| --- | --- |
| `scripts/codex-companion.mjs` | Accept `max` effort. Add `--resume-thread <id>` for exact-thread resume; it cannot be combined with `--resume`, `--resume-last`, or `--fresh`. Task JSON adds `jobId` and `route`. A foreground task with `--prompt-file <file>` removes any stale `<file>.result.json` before it runs and writes the task JSON there when the run returns, so a controller does not depend on the relay repeating stdout. `task --detach` and `task --attach` add bounded relay waits; see below. Task JSON adds `tokenUsage`. |
| `scripts/lib/codex.mjs` | Pass the requested effort as `model_reasoning_effort` thread configuration on start and resume. Report requested versus observed model, effort, service tier, approval policy, sandbox, and cwd from the thread response, plus any `model/rerouted` notifications, as `route`. Record `thread/tokenUsage/updated` totals for the task thread and its subagent threads as `tokenUsage`. Service name `agent_orch_router`. |
| `scripts/lib/app-server.mjs` | Read this plugin's manifest from the plugin root. Client title `Agent Orch Router`. Broker endpoint variable renamed. |
| `scripts/lib/state.mjs` | State root comes from `AGENT_ORCH_CODEX_DATA`, falling back to `<tmp>/agent-orch-codex`. |
| `scripts/session-lifecycle-hook.mjs` | Exports this plugin's `CLAUDE_PLUGIN_DATA` as `AGENT_ORCH_CODEX_DATA` instead of re-exporting `CLAUDE_PLUGIN_DATA`, so the official plugin cannot redirect state. |
| `scripts/lib/broker-lifecycle.mjs`, `lib/claude-session-transfer.mjs`, `lib/tracked-jobs.mjs`, `app-server-broker.mjs` | `CODEX_COMPANION_*` environment names renamed to `AGENT_ORCH_CODEX_*`; broker user agent renamed. |

Relay repair (2026-11-11): `lib/codex.mjs` retries only exact pre-forward broker-busy rejections on the same client. It never replays resumed or acknowledged work on a different server. Direct fallback is limited to explicitly rejected fresh creation. Connection loss during an accepted turn rejects with recovery identity rather than waiting for missing notifications. Cleanup errors cannot trigger replay or mask the primary failure.

Bounded relay waits (2026-11-13): Claude Code moves a Bash call that outlives its timeout (120 seconds by default) to the background, so a relay holding one foreground `task` call for a long Codex turn looked finished after two minutes. `task --detach --prompt-file <file>` starts the existing detached `task-worker`, waits at most 100 seconds (less when `BASH_DEFAULT_TIMEOUT_MS` is lower; `--wait-ms` overrides it), and prints the task JSON or `{"status": "running", ...}` with the job ID, phase, elapsed time, token totals, and recent progress. `<file>.job.json` records the job and a fingerprint of the work order and task options. Rerunning the identical command, or adding `--attach`, waits on that job again and never starts a second run; `--attach` never starts one at all. A changed work order in a reused file starts a new job. The worker writes `<file>.result.json`, including failures, before it marks the job finished. A waiter that finds the worker gone with the job unfinished records a failure that keeps the thread and turn IDs. `lib/tracked-jobs.mjs` writes the latest token totals to the job file at most every 5 seconds.

Live relay progress (2026-11-13): a `--detach` or `--attach` call that has waited at least 30 seconds (`AGENT_ORCH_CODEX_RELAY_HOLD_MS`) returns as soon as the job log grows, otherwise at the 100-second budget. The running JSON is now `{"status": "running", "jobId", "description", "next"}`. `description` reads `Codex · <latest activity> · <tokens> · <elapsed>`. Relays copy it into their next Bash call's description, which Claude Code shows as the subagent's activity. The marker also records `jobFile` and `logFile`.

`lib/tracked-jobs.mjs` persists structured relay context and bounded cause chains. `codex-companion.mjs` also writes relay failures beside foreground work orders and emits their JSON with a nonzero exit. Permission and routing policy are unchanged. Read-only reconciliation is documented in the plugin dispatch reference.

Offline regression command from the repository root:

```sh
node --test plugins/agent-orch/runtime/codex/tests/*.test.mjs
```

`tests/test_plugin.py` runs these suites as part of the repository checks. Tests use fake clients and an offline broker fixture, not provider requests. They cover the public read-only/workspace-write contract rather than importing private full-access policy.

`route.observed.reasoningEffort` is what the thread reports after the effort configuration. Treat any entry in `route.mismatches`, including a reroute, as an inexact route.

Some human-readable messages still mention the official plugin's `/codex:status`, `/codex:result`, `/codex:cancel`, and `/codex:setup` commands. Under agent-orch, run `node <plugin-root>/runtime/codex/scripts/codex-companion.mjs status|result|cancel|setup` instead.

## Updating

Copy the same file set from a newer upstream commit into a fresh commit, reapply these changes, run `node --check` on every module and the repository tests, and update the commit above.
