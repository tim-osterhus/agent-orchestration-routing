---
name: agent-orch-router
description: Explicit-only configurable routing for delegated research, implementation, and review across Codex and Claude Code. Use ordered profile pools with task-role and lifecycle constraints.
---

# Agent Orchestration Router

Activate only when the user invokes this skill for the current assignment. Keep the active mode in conversation/compaction context. Do not change the parent model or other chats. Default to pure orchestration: delegate substantive work while the controller decomposes, integrates, verifies, and communicates. The user can select supporting delegation instead.

Resolve the physical bundle root from this skill's directory. Read [the shared configuration](../../config/routing.json) and [execution contract](references/execution.md). Apply an explicitly selected configuration/preset. Use `scripts/bundle.py resolve` at the bundle root to inspect eligible profiles; it does not dispatch work or choose suitability for you.

Choose the earliest suitable eligible profile from the selected mode. Low/default/high selection bias never changes a profile's configured effort. An explicit profile can select outside the mode's pool, but does not waive role or lifecycle restrictions. Role exceptions need explicit user authorization. Never silently change an exact model, effort, provider, service tier, or workflow.

The configuration supplies Efficient, Fast, Performance, Balanced, and Tokenburn pools adapted from the source router. Balanced is the default. Tokenburn requires an explicit request and an identified account/reset endpoint. Return to the prior mode when its endpoint or authorized queue ends. Do not invent work to spend allowance.

Separate implementation, QA, spec review, frontend work, and final independent review. Review existing work without authoring its replacement. Reviewers must not implement their own fixes unless the user changes the assignment. Use fresh reviewer context after authorship.

Model eligibility and task roles do not assign permissions. Resolve tool access, approval rules, prompt handling, and sandbox settings independently from configuration. Mode defaults are examples, not mandatory security policies. Do not silently escalate after a denial or treat broad tools as authority to exceed the task.

Follow the configured controller design. Codex-first uses native Codex workers and the optional [Claude companion](../claude-delegation/SKILL.md). Claude-first uses native Claude workers and the external Codex contract in [controller designs](../../docs/controller-designs.md). A design setting does not switch a running chat's host or grant its missing tools.

Use the optional `opus-haiku` preset only when requested. Its permission-bypass orchestration requires explicit user approval for the assignment. Selecting a model code or the generic router alone does not grant bypass. The preset has no default orchestration timeout; Consultation and Implementation retain their configured deadlines.

Read [selection evidence](references/evidence.md) only for a requested profile refresh or rationale. Profile availability and suitability must be checked at dispatch. These files are instructions and configuration, not a scheduler or security sandbox.
