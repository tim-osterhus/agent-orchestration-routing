# codex-primary / performance

Apply [shared dispatch](../references/dispatch.md).
Prioritize task success and turnaround. Escalation is available when justified, not required.

## Ordered pool

<!-- BEGIN GENERATED:pool:codex-primary/performance -->
| Slot | Exact profile | Eligibility | Task fit |
| --- | --- | --- | --- |
| deep | SH: gpt-6.1-sol / high | general | Use for substantive implementation or diagnosis when a routine route would leave material uncertainty. |
| hard | SX: gpt-6.1-sol / xhigh | general | Use for difficult debugging, integration, or implementation with several interacting constraints. |
| max-code | SMAX: gpt-6.1-sol / max | general | Consider for demanding implementation, integration, or independent verification. Use Max only when the assignment warrants the additional effort. |
| broad | AMAX: gpt-6-astra / max | general | Consider for demanding analysis, implementation, or verification when task fit warrants Max effort. Verify tools for interactive work. |
| reasoning | AH: gpt-6-astra / high | general | Consider for demanding reasoning, implementation, debugging, or analysis. High effort does not imply a browser specialty. |
| opus-deep | OX: claude-opus-5-5 / xhigh | general | Consider for difficult analysis, implementation, architecture, or independent review, especially when exhaustive investigation or extensive testing is warranted. Keep authorship separate from final acceptance. |
| opus-max | OMAX: claude-opus-5-5 / max | escalation | Use as a justified escalation for demanding analysis or implementation when earlier eligible choices do not fit. |
| fable | FH: claude-fable-5-2 / high | escalation; one-off | Consider for demanding reasoning, implementation, or fresh architectural framing when an approach stalls or offers too-similar alternatives. Return a candidate checked against the same acceptance criteria, or an independent review, within the bounded assignment. |
<!-- END GENERATED:pool:codex-primary/performance -->

FH may reason, implement, integrate, or review as a bounded worker, not an automatic controller or required stage. Independent review needs a fresh assignment separate from authorship.
