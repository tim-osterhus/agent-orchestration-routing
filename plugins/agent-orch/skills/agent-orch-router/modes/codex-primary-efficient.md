# codex-primary / efficient

Apply [shared dispatch](../references/dispatch.md).
Minimize resources per accepted task, including retries and controller repair. This Codex-primary pool retains LM/TL/EX/TM/TH/S62M. EX requires a verified exact Muse adapter and account access. Otherwise report EX unavailable, without substituting for an explicit EX request.

## Ordered pool

<!-- BEGIN GENERATED:pool:codex-primary/efficient -->
| Slot | Exact profile | Eligibility | Task fit |
| --- | --- | --- | --- |
| cheap | LM: gpt-6-luna / medium | one-off | Use for a trivial one-off edit, extraction, or lookup with an immediate, inexpensive check. |
| small | TL: gpt-6.1-terra / low | general | Use for small, specified changes, source transformations, or straightforward visual interpretation following an established pattern, with inexpensive checks. Prefer another eligible profile when substantial interpretation or reframing is needed. |
| ember | EX: muse-ember-1.0 / xhigh | verified adapter | Use for bounded reasoning only after verifying the exact Muse API adapter and account route. |
| visual | TM: gpt-6.1-terra / medium | general | Execute established implementation or screen-based workflows and structure source-rich writing, including substantial multi-step work. Supply relevant patterns, decision boundaries, and acceptance checks, and surface unresolved choices instead of narrowing the task. |
| visual-deep | TH: gpt-6.1-terra / high | general | Handle harder bounded diagnosis, implementation, synthesis, or visual analysis with explicit ownership and checks. Ask the coordinator to reframe unresolved problems rather than assuming more Terra effort will resolve them. |
| standard | S62M: gpt-6.2-sol / medium | general | Use for general implementation spanning related files or a bounded integration with explicit checks. |
<!-- END GENERATED:pool:codex-primary/efficient -->

Known patterns can span long workflows. A clear outcome alone does not make the solution path known.

Return unresolved framing or repeated UI loops to the coordinator with the current state, attempts, and open decision. Reassignment follows existing pool, role, and route authorization, without silent substitution.
