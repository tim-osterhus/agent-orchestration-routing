---
name: agent-orch-router
description: Explicit-only configurable routing for delegated research, implementation, and review across Codex and Claude Code. Use ordered profile pools with task-role and lifecycle constraints.
---

# Agent Orchestration Router

Activate only when the user invokes this skill for the current assignment. Keep the active variant, mode, and bias in conversation/compaction context. Do not change the parent model or other chats. Default to pure orchestration: delegate substantive work while the controller decomposes, integrates, verifies, and communicates. The user can select supporting delegation instead.

Resolve the physical bundle root from this skill's directory. Read [the shared configuration](../../config/routing.json), [routing policy](references/routing-policy.md), and [execution contract](references/execution.md). Apply the selected configuration/preset. `scripts/bundle.py resolve` inspects eligibility without dispatching work. Read a profile's central catalog description when considering it, not a second model-policy list.

Choose the earliest suitable eligible profile from the selected mode. Low/default/high selection bias never changes a profile's configured effort. Never silently change an exact model, effort, provider, service tier, or workflow.

An out-of-pool profile requires both `--allow-out-of-pool` and `--role-override`. Its role/lifecycle eligibility is unspecified without an active-pool entry. Do not infer global model restrictions from other modes. Role exceptions need explicit user authorization.

One catalog serves `codex-primary` and `claude-primary`. `--variant` selects pool preference, not the running host. Both have Efficient, Balanced, Performance, and identical shared Codex-burn/Claude-burn modes. Defaults are Codex-primary and Balanced. Selection bias changes preference within the same pool, never configured effort. Retired Fast codes, `fast`, `tokenburn`, and `CMAX` fail instead of redirecting.

Bundled Codex profiles target Standard tier without enforcing it. Launch plans do not set a tier and may inherit runtime settings. Verify and report the effective or inherited tier, or disclose unavailable verification. Do not change global speed settings.

Before burn work, establish explicit invocation, the intended account, reset/deadline or queue endpoint, and authorized backlog from available instructions or evidence. Ask only for missing required inputs. Pass `--mode`, `--burn-account`, and `--burn-endpoint` to the inspector. These are offline metadata, not quota verification. Restore the prior mode at the endpoint. Do not invent work, enable paid extra usage, or switch authentication.

Separate implementation, QA, spec review, frontend work, and independent acceptance. An author cannot be the sole acceptance check. Cross-provider review is optional. Reviewers must not implement their own fixes unless the user changes the assignment. Use fresh reviewer context after authorship.

Model eligibility and task roles do not assign permissions. Resolve tool access, approval rules, prompt handling, and sandbox settings independently from configuration. Mode defaults are examples, not mandatory security policies. Do not silently escalate after a denial or treat broad tools as authority to exceed the task.

Follow the configured controller design. Codex-first uses native Codex workers and the optional [Claude companion](../claude-delegation/SKILL.md). Claude-first uses native Claude workers and the external Codex contract in [controller designs](../../docs/controller-designs.md). A design setting does not switch a running chat's host or grant its missing tools.

Use the optional `opus-haiku` preset only when requested. Its permission-bypass orchestration requires explicit user approval for the assignment. Selecting a model code or the generic router alone does not grant bypass. The preset has no default orchestration timeout; Consultation and Implementation retain their configured deadlines.

Read [selection evidence](references/evidence.md) only for a requested profile refresh or rationale. Profile availability and suitability must be checked at dispatch. These files are instructions and configuration, not a scheduler or security sandbox.
