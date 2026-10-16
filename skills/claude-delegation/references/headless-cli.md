# Headless launch contract

## Preflight

Resolve the native `claude` executable on the current host. Check `--version`, `--help`, and `claude auth status`. Require the user's existing logged-in first-party Claude subscription for this bundle. Inspect only non-secret status fields and environment variable names. Resolve alternate providers, API keys, OAuth-token overrides, forced subagent models, and effort caps before launch. Never extract credentials.

The included agent-file recipes need Claude Code 2.1.281 or later. Check the requested mode, model, and effort on the installed runtime. Auth status does not prove model access or remaining quota. Do not silently substitute models or update software.

Generate a plan with `scripts/bundle.py claude-plan` from the bundle root. Supply the config, optional preset, task role, cwd, prompt file, and artifact directory. For direct companion use without the router, add `--direct`. It uses the configured default Claude profile and Consultation when the role is omitted. Explicit authored roles select Implementation. Router-driven calls instead retain the active pool and its role/lifecycle restrictions. The output contains an argument vector, a child-environment removal list, optional agent definitions, a timeout, and required verification checks. It does not launch anything.

The controlling agent creates a private artifact directory and saves the task packet. It runs the argument vector without shell interpolation, feeds the prompt file through stdin, and saves stdout/stderr/exit status. On Windows, prefer native `claude.exe`; do not silently change the execution environment to WSL. Do not use `--bare` with subscription login or combine `--bg` with `-p`.

## Permission recipes

The supplied Consultation example uses restricted configuration, explicit read tools, empty MCP configuration, no Chrome, and read-only reviewer definitions. All those choices are configurable. Reviewer tool lists are actual capability controls, not promises in a prompt. Broader tool access requires reevaluating any read-only claim. `--safe-mode` is omitted because custom agent definitions are needed. Managed policy/hooks can still apply. Session persistence still writes Claude's own history.

The Implementation example uses auto mode and the full tool pool without suppressing normal configuration. An operator can instead choose manual approvals, plan mode, dontAsk, acceptEdits, or bypass, and set tool allow/deny lists. Tool availability is not unconditional approval. A configured host prompt target needs an actual responder. Native inheritance rules can override a requested child permission mode.

Orchestration requires an explicit user request. The supplied preset uses bypass, but can be overridden with any supported permission mode. Whenever bypass is configured, obtain explicit assignment-level authorization. Do not combine it with restricted mode, which the CLI rejects. Do not add safe mode when custom agent definitions are needed. The Haiku worker can inherit all available tools or a configured subset. Child permission labels do not restore checks under a bypass parent. Broad capabilities never authorize exceeding the task.

Provide this orchestration work-order instruction:

```text
Delegate basic, bounded, and parallelizable work to the configured Haiku worker.
Use its exact model and effort. Keep very complex reasoning, architecture,
difficult debugging, and integration with the Opus controller. Give workers
disjoint ownership and acceptance checks. Share an explicit deadline only when
provided; otherwise there is no default timeout. Return worker evidence and
check it independently. Stop owned workers when completed or cancelled.
```

## Deadlines and recovery

The configuration is the single timeout source. `timeout_seconds: null` means no skill-imposed timer for the controller, workers, or resumes. Positive values are whole-assignment deadlines, not new budgets per worker or resume. `max_turns: null` means omit both main-session `--max-turns` and subagent `maxTurns`.

The caller must enforce a configured deadline on the exact owned process group/tree and stop its descendants on expiry or cancellation. An output-yield interval is not a job deadline. Do not promise detached lifetime or automatic continuation without a tested owner-specific callback. When no safe lifetime mechanism exists, report the limitation rather than inventing one.

Check saved session ID and terminal state before resuming. Reapply mode, tools, model, effort, and configuration. Preserve normal history for recovery. If configuration changes during an assignment, do not silently broaden the saved session's permissions. Stop on auth, billing, quota, rate-limit, and exact-model errors; preserve partial work.

Validate returned model metadata instead of self-identification. Effective effort and context limits may not be observable. HK's 100K target is soft unless supported controls are independently verified; do not advertise a hard cap. This initial plan generator does not enable Ultracode or auto-refresh benchmarks.

References: [Claude CLI](https://code.claude.com/docs/en/cli-reference), [subagents](https://code.claude.com/docs/en/sub-agents), [permission modes](https://code.claude.com/docs/en/permission-modes).
