# Frontier Research

Apply [shared dispatch](../references/dispatch.md).
Opt in for hard technical questions needing competing mechanisms, falsifiable experiments, and independent evidence checks. Keep the current controller responsible for scope, integration, and acceptance. Eligible profiles are not mandatory stages.

<!-- BEGIN GENERATED:pool:frontier-research -->
| Slot | Exact profile | Eligibility | Task fit |
| --- | --- | --- | --- |
| frontier-proposer | FH: claude-fable-5-2 / high | research, planning | Propose a mechanism, identify its hardest assumption, and design the cheapest decisive test. |
| frontier-reviewer | AMAX: gpt-6-astra / max | qa, spec-review; independent review | Independently challenge the proposal with counterexamples, violated invariants, and decisive tests. |
| opus-deep | OX: claude-opus-5-5 / xhigh | qa, spec-review; independent review | Provide an alternate review of runtime constraints and failure cases when useful. |
| investigate-deep | MFX: muse-wonder-full-1.0 / xhigh | research, planning, qa | Seek a materially different representation or implementation when the first approach stalls. |
| hard | SX: gpt-6.1-sol / xhigh | implementation, integration, qa | Build, integrate, or reproduce a bounded probe with explicit write ownership and acceptance checks. |
| opus-max | OMAX: claude-opus-5-5 / max | research, planning, qa, spec-review; escalation | Investigate a named unresolved question after focused evidence or cheaper checks have narrowed it. |
<!-- END GENERATED:pool:frontier-research -->

## Proposal and independent challenge

Default to frontier-proposer/FH and frontier-reviewer/AMAX. Give both the same requirements, pinned inputs, and raw evidence, including measured failed probes and refuted hypotheses. Reopen refutations only with new data or changed assumptions. A short evidence ledger can help but is not required.

Use fresh isolated openings without preferred answers, peer opinions, or prior verdicts. Check auto-loaded context/memory and disclose contamination. Collect the reviewer's blind failure modes before revealing the proposal, even sequentially. Then share the actual proposal/evidence for decisive counterexamples. This informed critique may resume the exact reviewer session. Routine follow-ups need not repeat blind openings or the pair. Prefer an available authorized discriminating test before another opinion when useful.

OX is an alternate reviewer, not an automatic extra pass. Use MFX for a materially different hypothesis on blocked or branching questions. Use OMAX only for a named unresolved question that another pass could resolve, not merely because it is eligible. SX builds or reproduces authorized bounded probes.

Keep author and acceptance reviewer distinct after rebinding or fallback. Disclose shared-model overlap and prefer cross-family challenge where useful, without requiring it universally. Critically review the evaluator or probe when overlap could hide shared errors. Two same-model runs do not establish model diversity.

## Evidence and stopping

Define the finish line, pinned inputs, failure criteria, reference/oracle, and resource budget. An exploratory finish line may be the decision the next test informs. Each proposal names its hardest assumption, falsifiable prediction, and cheapest decisive experiment distinguishing mechanisms. Separate measurements from estimates and hypotheses.

Validate the evaluator proportionately, using a negative control or known-bad input where feasible. Surface circular validation and shared failure modes. If no independent oracle exists, state the weaker substitute and limit the claim. Bind results to tested revisions/artifacts, inputs, configuration, environment, and conditions where relevant. Fixture success does not establish release or production behavior. Serialize measurements only where competing resource use would invalidate them.

Reproducible evidence, not votes or consensus, resolves disagreements. Retain commands, results, and limits. Blocked tests are not passes. Stop at verified acceptance, budget/deadline, or a blocker without useful authorized checks. Report unresolved hypotheses, blockers, and the next decisive check.

If asked to compare pairings, start with four to six frozen tasks on identical inputs/checks. Compare verified results, useful counterexamples, time, and usage before revising defaults.
