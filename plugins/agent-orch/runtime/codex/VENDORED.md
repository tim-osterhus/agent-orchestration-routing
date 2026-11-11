# Vendored Codex companion runtime

Source: [openai/codex-plugin-cc](https://github.com/openai/codex-plugin-cc) v1.0.6, commit `db52e28f4d9ded852ab3942cea316258ae4ef346` (2026-07-07). Licensed under Apache-2.0; see `LICENSE` and `NOTICE` in this folder. The rest of this repository is MIT.

Included: `scripts/` (companion, broker, session hook, `lib/`), `prompts/adversarial-review.md`, and `schemas/review-output.schema.json`, so the copied companion still loads every module it imports.

Not included: the Stop-hook review gate and its prompt, the `/codex:*` slash commands, the `codex-rescue` agent, and the bundled prompting skills. The agent-orch plugin dispatches through its own generated profile agents instead.

## Modifications

Each modified file starts with a notice line. All changes are on top of the unmodified import commit.

| File | Change |
| --- | --- |
| `scripts/codex-companion.mjs` | Accept `max` effort. Add `--resume-thread <id>` for exact-thread resume; it cannot be combined with `--resume`, `--resume-last`, or `--fresh`. Task JSON adds `jobId` and `route`. |
| `scripts/lib/codex.mjs` | Pass the requested effort as `model_reasoning_effort` thread configuration on start and resume. Report requested versus observed model, effort, service tier, approval policy, sandbox, and cwd from the thread response, plus any `model/rerouted` notifications, as `route`. Service name `agent_orch_router`. |
| `scripts/lib/app-server.mjs` | Read this plugin's manifest from the plugin root. Client title `Agent Orch Router`. Broker endpoint variable renamed. |
| `scripts/lib/state.mjs` | State root comes from `AGENT_ORCH_CODEX_DATA`, falling back to `<tmp>/agent-orch-codex`. |
| `scripts/session-lifecycle-hook.mjs` | Exports this plugin's `CLAUDE_PLUGIN_DATA` as `AGENT_ORCH_CODEX_DATA` instead of re-exporting `CLAUDE_PLUGIN_DATA`, so the official plugin cannot redirect state. |
| `scripts/lib/broker-lifecycle.mjs`, `lib/claude-session-transfer.mjs`, `lib/tracked-jobs.mjs`, `app-server-broker.mjs` | `CODEX_COMPANION_*` environment names renamed to `AGENT_ORCH_CODEX_*`; broker user agent renamed. |

`route.observed.reasoningEffort` is what the thread reports after the effort configuration. Treat any entry in `route.mismatches`, including a reroute, as an inexact route.

Some human-readable messages still mention the official plugin's `/codex:status`, `/codex:result`, `/codex:cancel`, and `/codex:setup` commands. Under agent-orch, run `node <plugin-root>/runtime/codex/scripts/codex-companion.mjs status|result|cancel|setup` instead.

## Updating

Copy the same file set from a newer upstream commit into a fresh commit, reapply these changes, run `node --check` on every module and the repository tests, and update the commit above.
