# Claude plugin dispatch

For design `claude-plugin` only: a Claude Code controller with the agent-orch plugin installed. `<plugin-root>` is two directories above this skill's folder.

## Dispatch

Every Codex and Claude catalog profile has a pinned agent named `agent-orch:<provider>-<code>` in lowercase, for example `agent-orch:codex-sm` or `agent-orch:claude-fh`. Dispatch with the Agent tool's `subagent_type` set to that name. Do not pass model or effort overrides; the agent definition fixes them. Muse has no agent and still needs its separately verified adapter.

Codex agents are Haiku relays. Each starts or resumes one Codex app-server thread on the user's Codex login, then returns the companion's JSON. A detached companion worker runs the turn. The relay checks on it in calls of 30 to 100 seconds, under Claude Code's 2-minute Bash timeout, so it stays active until Codex finishes. In the terminal UI, each Codex relay's agent row shows Codex's current action, Codex token total, and elapsed time. It refreshes about every 5 seconds in a trusted workspace. Elsewhere the relay's activity line carries the same text at each check-in. Under this design, never use `codex exec` or `bundle.py codex-plan`. Codex threads are native workers, not external sessions. Honor actual runtime, provider, project, and explicit configured concurrency limits across descendants. The router adds no default ceiling. Claude helpers may delegate within selected permissions, tools, pool, scope, and role fences. Codex workers remain leaves unless assigned a team role. Do not start nested Codex controllers.

## Work order

Give each worker one self-contained work order in this shape. Send Claude agents the work order itself. For a Codex agent, write the work order to a new file in a private run directory outside the project, one file per dispatch including resumes, then send the relay only `Role:`, `Work order file: <absolute path>`, and any `Resume thread:` line. The relay passes the file to Codex unchanged, so the work order never appears in a shell command.

```text
Role: implementation
Profile: SM
Assignment: <originating assignment id>
Variant / mode: <selected variant and mode>
Pool / role fences: <eligible exact profiles and inherited role/lifecycle restrictions>
Objective: <outcome>
Write: <files or patterns this worker may change>
Read: <inputs and context>
Forbidden: <paths that must not change, including pre-existing uncommitted changes>
Acceptance checks: <commands or criteria>
Context isolation: <required isolation; neutral review inputs without author conversations or prior verdicts>
Assignment limits: <actual runtime/provider/project and explicit configured limits, or no router ceiling>
Delegation capacity: <optional coordinator allocation under positive assignment-wide caps>
Deadline: <only when the user supplied one>
Rules: Change only Write paths. If the work needs any other change, stop and return a handoff request naming the file, the change, and the reason. Return changed files, checks with results, findings, handoff requests, and unverified items.
Resume thread: <exact thread id, only when continuing that worker's thread>
```

Patterns ending in `/` own a directory tree. Other patterns use shell-style matching, where `*` also crosses `/`.

Pass variant, mode, pool, role, scope, ownership, permissions, tools, context isolation, remaining deadlines, and limits to descendants. Review helpers receive neutral packets and add no votes. Under positive assignment-wide caps, the parent allocates remaining worker/external-session capacity across descendants. Without allocation, return a capacity request instead of launching helpers. Null/omitted caps impose no quota or allocation gate. Do not infer extra authority from available capacity.

## Ownership without worktrees

All workers share the user's checkout. Before dispatching any writer, snapshot it outside the project and check the planned Write lists:

```text
python3 <plugin-root>/scripts/bundle.py snapshot --cwd <project> --out <private-run-dir>/baseline.json [--protect <ignored path>]
python3 <plugin-root>/scripts/bundle.py check-ownership --snapshot <private-run-dir>/baseline.json --owners <private-run-dir>/owners.json
```

`owners.json` maps each worker to its Write patterns. Use `--protect` for ignored material that must not change.

- Run workers in parallel only when the check reports no overlaps and no owned files with uncommitted changes from before the run.
- Run them in sequence when overlap is reported or likely: the same module, shared types or interfaces, lockfiles, configuration, generated files, migrations, or one task's output feeding another. Start the next worker after the previous result is integrated, from a fresh snapshot.
- After each worker finishes, rerun the check against the same snapshot. Treat unowned, multiply owned, or protected changes as violations. Stop and inspect them; do not accept or revert them silently. Compare Codex `touchedFiles` with the worker's Write list.

## Results and coordination

- Codex JSON includes `route`. Treat any `route.mismatches` entry, including a reroute, as an inexact route and report it. `exact: true` means the thread reported the requested model and effort; it does not prove output quality.
- When a Codex relay finishes, read `<work order file>.result.json`. The companion's worker writes its JSON there when the run ends, including failures, so use that file, not the relay's reply, for status, `threadId`, `route`, `touchedFiles`, and `tokenUsage`. `tokenUsage` sums the Codex thread and its subagent threads; a resumed thread's totals include earlier turns. If the file is missing, the run failed before it started; the relay's reply should carry the exit status and stderr.
- A relay that stops early does not stop Codex. `<work order file>.job.json` names the job. To wait for it again without starting new work, run `node <plugin-root>/runtime/codex/scripts/codex-companion.mjs task --json --attach --prompt-file <work order file>` until its status is no longer `running`. A result whose error says the worker exited without recording a result needs the reconciliation steps below before any retry.
- Workers never message each other. The controller decides each handoff request, then sends it to the owning worker as a new work order with that worker's exact `Resume thread:` id, or reassigns ownership. Never resume a thread chosen by recency or title.
- To cancel, run `node <plugin-root>/runtime/codex/scripts/codex-companion.mjs status --json`, then `cancel <job-id>` for jobs this assignment started. The controller enforces any user deadline this way; relays have no timer.

## Interrupted connections and uncertain acceptance

Relay failures can produce a nonzero exit and a failure result file. Inspect its `error.relayContext`, or the saved job's `relayError`, before any retry. `acceptedRequests` counts acknowledged responses, not every request the native server may have accepted. A missing turn ID does not prove that no turn started.

The relay retries only the exact pre-forward broker-busy rejection on the same client. Resumed or acknowledged work never falls back to another native server. Fresh creation may use a direct server only after an explicitly rejected first `thread/start`. The 120-second busy-wait budget is shared across requests. It is not a general request or model-turn timeout.

When `reconciliationRequired` is true:

If the failed transport was direct, or no original broker endpoint is recorded, stop and report for manual recovery. No companion inspection command is provided. If no verified read-only RPC client can inspect the existing endpoint, stop rather than improvising a resume or direct connection.

1. Keep the failed job ID, exact thread/turn IDs, broker endpoint, work order, and ownership snapshot. Read `result <job-id> --json` for the persisted cause and context.
2. Verify the recorded endpoint still belongs to the original broker. Connect only to that existing endpoint. Do not create or replace a broker for inspection.
3. Read the exact thread through `thread/read`, without `thread/resume`. Inspect its current status and stored turns with the installed version's read-only history APIs. If the turn response was lost, identify any accepted turn from that history and work-order timing before sending another prompt.
4. If work is running, observe its owned job or request its identified interrupt when cancellation is authorized. Do not replay it. If completed, recover its output and inspect the checkout against the ownership snapshot before accepting it.
5. Retry only after establishing that no prior turn remains running or unaccounted for. Use the same conversation and owning broker at a safe lifecycle boundary. If ownership or acceptance cannot be established, report the uncertainty and stop for reconciliation.

Do not delete locks, kill a shared broker, or switch servers to force a resume. Unreachable endpoints and silently stalled requests require separate diagnosis. Source updates affect new workers. Do not restart active shared work to load a patch.
