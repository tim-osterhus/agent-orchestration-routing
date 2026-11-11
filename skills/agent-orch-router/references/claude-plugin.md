# Claude plugin dispatch

For design `claude-plugin` only: a Claude Code controller with the agent-orch plugin installed. `<plugin-root>` is two directories above this skill's folder.

## Dispatch

Every Codex and Claude catalog profile has a pinned agent named `agent-orch:<provider>-<code>` in lowercase, for example `agent-orch:codex-sm` or `agent-orch:claude-fh`. Dispatch with the Agent tool's `subagent_type` set to that name. Do not pass model or effort overrides; the agent definition fixes them. Muse has no agent and still needs its separately verified adapter.

Codex agents are Haiku relays. Each starts or resumes one Codex app-server thread on the user's Codex login, then returns the companion's JSON. Under this design, never use `codex exec` or `bundle.py codex-plan`. Codex threads are native workers, not external sessions. The parallel worker limit still applies.

## Work order

Send each worker one self-contained work order in this shape. Relays read only `Role:` and `Resume thread:`; everything is forwarded to Codex unchanged.

```text
Role: implementation
Profile: SM
Assignment: <originating assignment id>
Objective: <outcome>
Write: <files or patterns this worker may change>
Read: <inputs and context>
Forbidden: <paths that must not change, including pre-existing uncommitted changes>
Acceptance checks: <commands or criteria>
Deadline: <only when the user supplied one>
Rules: Change only Write paths. If the work needs any other change, stop and return a handoff request naming the file, the change, and the reason. Return changed files, checks with results, findings, handoff requests, and unverified items.
Resume thread: <exact thread id, only when continuing that worker's thread>
```

Patterns ending in `/` own a directory tree. Other patterns use shell-style matching, where `*` also crosses `/`.

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
- Workers never message each other. The controller decides each handoff request, then sends it to the owning worker as a new work order with that worker's exact `Resume thread:` id, or reassigns ownership. Never resume a thread chosen by recency or title.
- To cancel, run `node <plugin-root>/runtime/codex/scripts/codex-companion.mjs status --json`, then `cancel <job-id>` for jobs this assignment started. The controller enforces any user deadline this way; relays have no timer.
