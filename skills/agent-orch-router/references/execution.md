# Execution contract

## Routing and ownership

Read the shared configuration once per assignment and only the selected preset. Resolve aliases before checking eligibility. A model appearing in the registry is not automatically eligible in every mode. Treat context targets as soft unless the selected runtime can enforce them.

One-off means a fresh bounded worker assignment, not a continuing controller. Ongoing-thread restrictions require a real multi-stage assignment, not an invented age threshold. Final-only profiles review an existing completed candidate independently. Propagate the active mode, role limits, model settings, and lifecycle constraints to descendants.

Each work order includes the objective, relevant inputs, allowed writes, shared-file owner, dependencies, acceptance checks, selected profile, and deadline or none. Parallel writers own disjoint files/components. Reserve shared schemas, lockfiles, generated indexes, Git staging, binary assets, and live editors for one owner. Preserve pre-existing changes. Do not create worktrees, plans, or repository log files by default.

Respect the configured concurrency ceiling and the host's lower runtime ceiling. Native workers are leaves unless explicitly assigned a permitted team role. External workers must not recursively start the opposite controller or create unrelated chats. Keep one external session per assignment by default, including launches through descendants. A slot remains held until its worker is terminal. Native workers inside an authorized Claude team are not extra external sessions.

## Controllers and adapters

Codex-first delegates through native Codex tools when available. Pass exact model and effort using supported controls. Fast is a service-tier requirement, not a model suffix. Verify it on the actual route; do not relabel an inherited Standard tier as Fast.

Claude-first delegates through native Claude Agent definitions. The active Claude model need not match every worker. Use only the allowed profiles for the task role. External Codex work uses a separate signed-in CLI session, not Anthropic tools pretending to be Codex. Browser and computer-control tools are not automatically shared across CLI sessions.

Use [the Claude companion](../../claude-delegation/SKILL.md) for external Claude work. QA/spec review defaults to Consultation and authored work defaults to Implementation. An explicit execution-mode override is allowed without changing the assigned task role. Tool access and approvals come from the selected mode's configuration, not from the model code. Only an explicit orchestration request can select the optional team preset. Permission bypass requires assignment-level authorization whenever configured. Resolve timeouts from `claude.modes[mode].timeout_seconds`; `null` means no skill-imposed timeout. Do not repeat a fixed timeout in router policy.

`bundle.py claude-plan` and `codex-plan` print launch arguments and required checks. They do not authenticate, execute, enforce deadlines, monitor workers, or prove account access. The controlling agent supplies the owned execution session and captures results. On the native route, use equivalent supported controls rather than launching an unnecessary second controller.

## Waiting, recovery, and evidence

Prefer native completion events and useful independent work. Do not repeatedly read unchanged logs or poll idle workers. An external process must survive the turn and have a verified callback before promising automatic continuation. Otherwise explain where results go and that the user must return.

Verify the exact owned job before cancellation. Stop its descendants on cancellation or an applicable timeout, preserve partial edits, and release the external slot only after termination. No default orchestration timeout does not disable native runtime limits or stop-on-error behavior.

Resume only an exact saved session ID. Keep permissions and remaining deadlines consistent. Do not use latest-session shortcuts or titles. Check exit status, errors, permission denials, completeness, effective model metadata, changed files, and proportionate independent tests. Self-identification is not model verification.

Never switch accounts, enable paid extra usage, broaden credentials, or retry quota failures automatically. Track distinct account/reset windows separately. Unknown allowance stays unknown. Configuration controls task routing, not organizational policy, OS protections, or the user's authorization scope.
