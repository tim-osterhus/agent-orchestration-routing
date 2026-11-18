# claude-primary / performance

Apply [shared dispatch](../references/dispatch.md).
Prioritize task success and turnaround. Escalation is available when justified, not required.

Name the unresolved question or check that warrants deeper effort. After a stall, say what the next pass will do differently. For optimization, compare the primary metric and guardrails against the same baseline under matching conditions. Example: reduce bundle size without worsening load time on the same fixture.

## Ordered pool

<!-- BEGIN GENERATED:pool:claude-primary/performance -->
| Slot | Exact profile | Eligibility | Task fit |
| --- | --- | --- | --- |
| opus-medium | OM: claude-opus-5-5 / medium | general | Use for substantive general-purpose implementation or integration with sufficiently clear requirements. |
| opus | OH: claude-opus-5-5 / high | general | Consider for thorough implementation, investigation, or independent review when reproductions and edge-case coverage warrant additional diligence. Use a fresh reviewer for work it authored. |
| opus-deep | OX: claude-opus-5-5 / xhigh | general | Consider for difficult analysis, implementation, architecture, or independent review, especially when exhaustive investigation or extensive testing is warranted. Keep authorship separate from final acceptance. |
| opus-max | OMAX: claude-opus-5-5 / max | general | Use for demanding implementation or analysis when sustained reasoning is justified by the assignment. |
| max-code | SMAX: gpt-6.2-sol / max | general | Consider for demanding implementation, integration, or independent verification. Use Max only when the assignment warrants the additional effort. |
| broad | AMAX: gpt-6.2-astra / max | general | Consider for demanding analysis, implementation, or verification when task fit warrants Max effort. Verify tools for interactive work. |
| fable | FH: claude-fable-5-2 / high | escalation; one-off | Consider for demanding reasoning, implementation, or fresh architectural framing when an approach stalls or offers too-similar alternatives. Return a candidate checked against the same acceptance criteria, or an independent review, within the bounded assignment. |
<!-- END GENERATED:pool:claude-primary/performance -->

FH may reason, implement, integrate, or review as a bounded worker, not an automatic controller or required stage. Independent review needs a fresh assignment separate from authorship.
