# codex-primary / performance

Apply [shared dispatch](../references/dispatch.md).
Prioritize task success and turnaround. Escalation is available when justified, not required.

Name the unresolved question or check that warrants deeper effort. After a stall, say what the next pass will do differently. For optimization, compare the primary metric and guardrails against the same baseline under matching conditions. Example: reduce bundle size without worsening load time on the same fixture.

## Ordered pool

<!-- BEGIN GENERATED:pool:codex-primary/performance -->
| Slot | Exact profile | Eligibility | Task fit |
| --- | --- | --- | --- |
| deep | SH: gpt-6.2-sol / high | general | Use for substantive implementation or diagnosis when a routine route would leave material uncertainty. |
| hard | SX: gpt-6.2-sol / xhigh | general | Use for difficult debugging, integration, or implementation with several interacting constraints. |
| max-code | SMAX: gpt-6.2-sol / max | escalation | Escalate demanding implementation or verification when a concrete risk justifies more reasoning. |
| reasoning | AX: gpt-6.2-astra / xhigh | general | First Astra choice for difficult cross-component diagnosis or independent analysis. Verify tools for interactive work. |
| broad | AMAX: gpt-6.2-astra / max | escalation | Use Astra Max when the stakes or unresolved evidence justify going beyond XHigh. |
| opus-deep | OX: claude-opus-5-5 / xhigh | general | Consider for difficult analysis, implementation, architecture, or independent review, especially when exhaustive investigation or extensive testing is warranted. Keep authorship separate from final acceptance. |
| opus-max | OMAX: claude-opus-5-5 / max | escalation | Use as a justified escalation for demanding analysis or implementation when earlier eligible choices do not fit. |
| fable | FH: claude-fable-5-2 / high | escalation; one-off | Consider for demanding reasoning, implementation, or fresh architectural framing when an approach stalls or offers too-similar alternatives. Return a candidate checked against the same acceptance criteria, or an independent review, within the bounded assignment. |
<!-- END GENERATED:pool:codex-primary/performance -->

FH may reason, implement, integrate, or review as a bounded worker, not an automatic controller or required stage. Independent review needs a fresh assignment separate from authorship.
