# claude-primary / balanced

Apply [shared dispatch](../references/dispatch.md).
Use this everyday pool for low/default/high bias. Low favors the least resource-intensive reliable fit. Default accounts for repair overhead. High favors reasoning capacity when uncertainty warrants it. All biases retain this same pool and exact efforts.

## Ordered pool

<!-- BEGIN GENERATED:pool:claude-primary/balanced -->
| Slot | Exact profile | Eligibility | Task fit |
| --- | --- | --- | --- |
| haiku-high | HH: claude-haiku-5-5 / high | one-off | Use for a simple one-off task with concrete inputs and an inexpensive check. |
| haiku-xhigh | HM: claude-haiku-5-5 / xhigh | one-off | Use for bounded one-off implementation or analysis with clear ownership and acceptance criteria. |
| haiku-max | HMAX: claude-haiku-5-5 / max | one-off | Use for a harder one-off packet that still has a narrow scope and a direct acceptance check. |
| sonnet | SNH: claude-sonnet-5-5 / high | general | Use for scoped implementation, research synthesis, or diagnosis needing judgment beyond a small Haiku packet. |
| opus-medium | OM: claude-opus-5-5 / medium | general | Use for everyday general-purpose implementation and integration, including work spanning related files. |
| opus | OH: claude-opus-5-5 / high | general | Consider for thorough implementation, investigation, or independent review when reproductions and edge-case coverage warrant additional diligence. Use a fresh reviewer for work it authored. |
| opus-deep | OX: claude-opus-5-5 / xhigh | general | Consider for difficult analysis, implementation, architecture, or independent review, especially when exhaustive investigation or extensive testing is warranted. Keep authorship separate from final acceptance. |
| standard | S62M: gpt-6.2-sol / medium | general | Consider for general implementation or verification across related components. Cross-provider review is a preference, not an implementation ban. |
| max-code | S62MAX: gpt-6.2-sol / max | general | Consider for demanding implementation, integration, or independent verification. Use Max only when the assignment warrants the additional effort. |
<!-- END GENERATED:pool:claude-primary/balanced -->
