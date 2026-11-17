# codex-primary / balanced

Apply [shared dispatch](../references/dispatch.md).
Use this everyday pool for low/default/high bias. Low favors the least resource-intensive reliable fit. Default accounts for repair overhead. High favors reasoning capacity when uncertainty warrants it. All biases retain this same pool and exact efforts.

## Ordered pool

<!-- BEGIN GENERATED:pool:codex-primary/balanced -->
| Slot | Exact profile | Eligibility | Task fit |
| --- | --- | --- | --- |
| routine | S62L: gpt-6.2-sol / low | general | Use for routine, clearly specified edits whose output is easy to check. |
| visual | TM: gpt-6.1-terra / medium | general | Execute established implementation or screen-based workflows and structure source-rich writing, including substantial multi-step work. Supply relevant patterns, decision boundaries, and acceptance checks, and surface unresolved choices instead of narrowing the task. |
| visual-deep | TH: gpt-6.1-terra / high | general | Handle harder bounded diagnosis, implementation, synthesis, or visual analysis with explicit ownership and checks. Ask the coordinator to reframe unresolved problems rather than assuming more Terra effort will resolve them. |
| standard | S62M: gpt-6.2-sol / medium | general | Consider for general implementation or verification across related components. Cross-provider review is a preference, not an implementation ban. |
| deep | S62H: gpt-6.2-sol / high | general | Use for debugging, unclear behavior, or integration where controller repair would otherwise be substantial. |
| hard | S62X: gpt-6.2-sol / xhigh | general | Use for difficult implementation or debugging with interacting constraints and explicit acceptance checks. |
| max-code | S62MAX: gpt-6.2-sol / max | general | Consider for demanding implementation, integration, or independent verification. Use Max only when the assignment warrants the additional effort. |
| opus | OH: claude-opus-5-5 / high | general | Consider for thorough implementation, investigation, or independent review when reproductions and edge-case coverage warrant additional diligence. Use a fresh reviewer for work it authored. |
<!-- END GENERATED:pool:codex-primary/balanced -->

Known patterns can span long workflows. A clear outcome alone does not make the solution path known.

Return unresolved framing or repeated UI loops to the coordinator with the current state, attempts, and open decision. Reassignment follows existing pool, role, and route authorization, without silent substitution.
