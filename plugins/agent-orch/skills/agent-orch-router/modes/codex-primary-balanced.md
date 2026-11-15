# codex-primary / balanced

Apply [shared dispatch](../references/dispatch.md).
Use this everyday pool for low/default/high bias. Low favors the least resource-intensive reliable fit. Default accounts for repair overhead. High favors reasoning capacity when uncertainty warrants it. All biases retain this same pool and exact efforts.

## Ordered pool

<!-- BEGIN GENERATED:pool:codex-primary/balanced -->
| Slot | Exact profile | Eligibility | Task fit |
| --- | --- | --- | --- |
| routine | SL: gpt-6.1-sol / low | general | Use for routine, clearly specified edits whose output is easy to check. |
| visual | TM: gpt-6.1-terra / medium | general | Execute established implementation or screen-based workflows and structure source-rich writing, including substantial multi-step work. Supply relevant patterns, decision boundaries, and acceptance checks, and surface unresolved choices instead of narrowing the task. |
| visual-deep | TH: gpt-6.1-terra / high | general | Handle harder bounded diagnosis, implementation, synthesis, or visual analysis with explicit ownership and checks. Ask the coordinator to reframe unresolved problems rather than assuming more Terra effort will resolve them. |
| standard | SM: gpt-6.1-sol / medium | general | Consider for general implementation or verification across related components. Cross-provider review is a preference, not an implementation ban. |
| deep | SH: gpt-6.1-sol / high | general | Use for debugging, unclear behavior, or integration where controller repair would otherwise be substantial. |
| hard | SX: gpt-6.1-sol / xhigh | general | Use for difficult implementation or debugging with interacting constraints and explicit acceptance checks. |
| max-code | SMAX: gpt-6.1-sol / max | general | Consider for demanding implementation, integration, or independent verification. Use Max only when the assignment warrants the additional effort. |
| reasoning | AL: gpt-6-astra / low | general | Consider for general analysis or implementation at Low effort. Browser assignments require verified tools and session access. |
| opus | OH: claude-opus-5-5 / high | general | Consider for thorough implementation, investigation, or independent review when reproductions and edge-case coverage warrant additional diligence. Use a fresh reviewer for work it authored. |
<!-- END GENERATED:pool:codex-primary/balanced -->

Known patterns can span long workflows. A clear outcome alone does not make the solution path known.

Return unresolved framing or repeated UI loops to the coordinator with the current state, attempts, and open decision. Reassignment follows existing pool, role, and route authorization, without silent substitution.
