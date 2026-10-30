---
name: claude-delegation
description: Explicit-only headless Claude Code consultation, implementation, or opt-in Opus/Haiku orchestration using the user's signed-in subscription and shared bundle configuration.
---

# Claude Delegation

Use only when the user requests Claude involvement, directly or through an explicitly invoked router configuration that permits it. Use native Claude Code subscription login, not an API wrapper or browser project. Default to Consultation. A request to implement/build/fix selects Implementation. Permission-bypass Orchestration requires an explicit request, not merely a model name.

Router-driven work retains the selected provider-primary variant and mode. Read [routing policy](../agent-orch-router/references/routing-policy.md) for burn gating or an explicit on-call trial. Before burn launch, establish the intended account, endpoint, and authorized backlog from available evidence. Ask only for missing required inputs. Burn eligibility does not enable Orchestration or bypass. Preserve the parent-owned external-session limit across descendants. Native Claude workers under Claude-first do not require a second CLI controller.

Read [the launch contract](references/headless-cli.md). Resolve model, effort, tools, timeouts, turn limits, and worker settings from [shared configuration](../../config/routing.json) plus the selected preset. Default profile: OH. Consultation/Implementation default to 3600 seconds; Orchestration has no default timeout. No mode has a default turn cap. Do not duplicate deadline constants in the router or silently add them to workers/resumes.

- **Consultation defaults:** Read/Glob/Grep with optional reviewers using the same read tools. Configure reviewer tools, model, prompt, and permission mode independently. Authorized test execution can use an explicit tool/approval override rather than a mandatory role change.
- **Implementation defaults:** auto permission mode and the full built-in tool pool, including subagents. Normal configured integrations may load. Auto still performs safety checks. Approval mode, allow/deny rules, prompt handling, tools, and configuration isolation are independently editable.
- **Orchestration:** disabled in the base configuration. The optional Opus/Haiku preset defaults to bypass, but its permission mode and worker tools are configurable. Bypass requires explicit assignment-level authorization. The Opus controller delegates basic and parallelizable work to the configured Haiku worker, defaulting to Haiku 5.5 XHigh. Opus retains very complex reasoning and integration. The entire team shares an explicit deadline if supplied; otherwise it has none.

These mode names describe workflows, not immutable permission boundaries. Validation rejects invalid controls and native incompatibilities, not an operator's supported approval choice. No mode automatically escalates after a denial. Task scope remains separate from tool availability.

Check the CLI version/help, first-party subscription auth status, and credential/provider overrides before dispatch. Never read credential stores, extract tokens, buy credits, enable paid extra usage, or change billing/authentication automatically. Remove effort/history environment overrides only from the launched child when needed; report managed policy caps and forced subagent-model overrides.

Give the session a trusted cwd, relevant project instructions, bounded scope, file ownership, dependencies, acceptance checks, and originating assignment ID. Keep the existing checkout unless isolation is required or requested. Preserve user changes. Full tools and bypass do not authorize unrelated deletion, account changes, deployment, purchases, outbound messages, or Git history changes.

Capture a unique session ID, prompt, result, stderr, and exit status outside the project. Fresh sessions are the default. Resume only the exact saved ID with the same mode and remaining deadline. Never choose a session by title or latest-session shortcut.

Use owned completion mechanisms rather than tight polling. Cancel only the verified owned process tree. Preserve partial work and stop on quota, billing, auth, rate-limit, or model-access errors. No timeout does not mean indefinite retries or guaranteed background continuation.

Inspect JSON errors, permission denials, result completeness, returned model metadata, diffs, and independent tests. Report requested versus observed model/effort, verification limits, session ID, artifact paths, changes/findings, tests, and remaining issues. Do not treat model prose or success exit alone as proof.
