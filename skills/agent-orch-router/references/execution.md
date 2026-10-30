# Execution contract

## Routing and ownership

Read the shared configuration once per assignment and only the selected preset. Resolve the variant and mode before checking profile eligibility. Resolve aliases before comparing profiles. Catalog membership does not confer pool eligibility. Treat context targets as soft unless the selected runtime can enforce them.

Out-of-pool profiles require both explicit pool and role/lifecycle overrides. Without an active-pool entry, role/lifecycle eligibility is unspecified. Do not derive global restrictions from unrelated modes. Pool overrides alone never waive an active entry's role or lifecycle fences.

One-off means a fresh bounded worker assignment, not a continuing controller. Ongoing-thread restrictions require a real multi-stage assignment, not an invented age threshold. Final-only profiles review an existing completed candidate independently. Propagate variant, mode, bias, role limits, model settings, and lifecycle constraints to descendants.

Each work order includes the objective, relevant inputs, allowed writes, shared-file owner, dependencies, acceptance checks, selected profile, and deadline or none. Parallel writers own disjoint files/components. Reserve shared schemas, lockfiles, generated indexes, Git staging, binary assets, and live editors for one owner. Preserve pre-existing changes. Do not create worktrees, plans, or repository log files by default.

Respect the configured concurrency ceiling and the host's lower runtime ceiling. Native workers are leaves unless explicitly assigned a permitted team role. External workers must not recursively start the opposite controller or create unrelated chats. Keep one external session per assignment by default, including launches through descendants. A slot remains held until its worker is terminal. Native workers inside an authorized Claude team are not extra external sessions.

## Controllers and adapters

Codex-first delegates through native Codex tools when available. Pass exact model and effort using supported controls. Bundled Codex profiles target Standard tier without enforcing it. Report the target versus observed or inherited tier. Disclose unavailable per-worker tier controls or verification. Do not change global speed settings or claim that a native spawn enforced an unsupported tier selector.

Claude-first delegates through native Claude Agent definitions. The active Claude model need not match every worker. Use only the allowed profiles for the task role. External Codex work uses a separate signed-in CLI session, not Anthropic tools pretending to be Codex. Browser and computer-control tools are not automatically shared across CLI sessions.

Codex-burn and Claude-burn preserve these native/external designs. Before launch, establish explicit burn invocation, the intended account, endpoint, and authorized backlog from available instructions or evidence. Ask only for missing required inputs. Preserve the prior mode and restore it at the endpoint. Automatic choices remain provider-exclusive. Mark explicit cross-provider exceptions and verify their separate account route. Neither burn mode enables Orchestration or changes permissions.

Use [the Claude companion](../../claude-delegation/SKILL.md) for external Claude work. QA/spec review defaults to Consultation and authored work defaults to Implementation. An explicit execution-mode override is allowed without changing the assigned task role. Tool access and approvals come from the selected mode's configuration, not from the model code. Only an explicit orchestration request can select the optional team preset. Permission bypass requires assignment-level authorization whenever configured. Resolve timeouts from `claude.modes[mode].timeout_seconds`; `null` means no skill-imposed timeout. Do not repeat a fixed timeout in router policy.

`bundle.py claude-plan` and `codex-plan` print external launch arguments and required checks. They reject native routes. They do not authenticate, execute, enforce deadlines, monitor workers, or prove account access. The controlling agent supplies the owned execution session and captures results. On native routes, use the host's supported worker controls without launching a second controller.

## Waiting, recovery, and evidence

Prefer native completion events and useful independent work. Do not repeatedly read unchanged logs or poll idle workers. An external process must survive the turn and have a verified callback before promising automatic continuation. Otherwise explain where results go and that the user must return.

Verify the exact owned job before cancellation. Stop its descendants on cancellation or an applicable timeout, preserve partial edits, and release the external slot only after termination. No default orchestration timeout does not disable native runtime limits or stop-on-error behavior.

Resume only an exact saved session ID. Keep permissions and remaining deadlines consistent. Do not use latest-session shortcuts or titles. Check exit status, errors, permission denials, completeness, effective model metadata, changed files, and proportionate independent tests. Self-identification is not model verification.

Never switch accounts, enable paid extra usage, broaden credentials, or retry quota failures automatically. Track distinct account/reset windows separately. Unknown allowance stays unknown. Configuration controls task routing, not organizational policy, OS protections, or the user's authorization scope.
