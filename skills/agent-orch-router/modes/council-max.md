# Council Max

Select explicitly as a Council sub-mode. Use [shared dispatch](../references/dispatch.md) and the [Council protocol](council.md), replacing its roster with the one below.

All six slots are required: **SMAX, AX, OX, MFX, FH, GNH**. Verify every route before openings. Each member must endorse the same final version. If any seat is unavailable, report an incomplete council and request a distinct alternate. The Fable cap fallback cannot fill FH’s seat with OX because OX already has a seat.

<!-- BEGIN GENERATED:pool:council-max -->
| Slot | Exact profile | Eligibility | Task fit |
| --- | --- | --- | --- |
| max-code | SMAX: gpt-6.2-sol / max | research, planning, qa, spec-review | Develop a decision proposal, test its assumptions, and compare concrete implementation tradeoffs. |
| astra-member | AX: gpt-6.2-astra / xhigh | research, planning, qa, spec-review | Stress-test the decision against cross-system constraints and failure cases. |
| opus-deep | OX: claude-opus-5-5 / xhigh | research, planning, qa, spec-review | Challenge architectural choices against requirements, source evidence, and simpler alternatives. |
| investigate-deep | MFX: muse-wonder-full-1.0 / xhigh | research, planning, qa, spec-review; verified adapter | Investigate competing hypotheses and identify evidence that distinguishes proposed approaches. |
| fable | FH: claude-fable-5-2 / high | research, planning, qa, spec-review | Reframe the decision and propose a materially different approach. Address objections and ratify the final version. |
| neon-member | GNH: gemini-4-neon / high | research, planning, qa, spec-review; verified adapter | Challenge assumptions and compare a distinct, source-backed option. |
<!-- END GENERATED:pool:council-max -->
