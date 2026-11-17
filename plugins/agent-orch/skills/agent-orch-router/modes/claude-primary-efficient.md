# claude-primary / efficient

Apply [shared dispatch](../references/dispatch.md).
Minimize resources per accepted task, including retries and controller repair. Prefer Claude for cheap bounded work and the middle escalation band, retaining TL/TM/SM for suitable Codex work. HM replaces EX; SNH replaces TH. Select by task fit, not a mandatory escalation sequence.

## Ordered pool

<!-- BEGIN GENERATED:pool:claude-primary/efficient -->
| Slot | Exact profile | Eligibility | Task fit |
| --- | --- | --- | --- |
| cheap | HL: claude-haiku-5-5 / low | one-off | Use for a tiny one-off extraction, lookup, or specified edit with a cheap acceptance check. |
| small | TL: gpt-6.1-terra / low | general | Use for small, specified changes, source transformations, or straightforward visual interpretation following an established pattern, with inexpensive checks. Prefer another eligible profile when substantial interpretation or reframing is needed. |
| haiku-xhigh | HM: claude-haiku-5-5 / xhigh | one-off | Use for bounded analysis, implementation, or verification with concrete inputs and inexpensive acceptance checks. This Claude-preferred bridge is not a task-specific equivalence to Ember. |
| visual | TM: gpt-6.1-terra / medium | general | Execute established implementation or screen-based workflows and structure source-rich writing, including substantial multi-step work. Supply relevant patterns, decision boundaries, and acceptance checks, and surface unresolved choices instead of narrowing the task. |
| sonnet | SNH: claude-sonnet-5-5 / high | general | Use for scoped implementation, diagnosis, or synthesis when stronger judgment is warranted. Sonnet High fills the Claude-preferred capability band, without inheriting Terra-specific visual guidance. |
| standard | SM: gpt-6.2-sol / medium | general | Use for general implementation spanning related files or a bounded integration with explicit checks. |
<!-- END GENERATED:pool:claude-primary/efficient -->

Known patterns can span long workflows. A clear outcome alone does not make the solution path known.

Return unresolved framing or repeated UI loops to the coordinator with the current state, attempts, and open decision. Reassignment follows existing pool, role, and route authorization, without silent substitution.
