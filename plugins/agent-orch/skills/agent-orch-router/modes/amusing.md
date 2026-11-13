# Amusing

Opt in for maintainable changes with functional evidence and independent review. This shared mode has eight eligible profiles, not an eight-stage pipeline.

## Ordered pool

<!-- BEGIN GENERATED:pool:amusing -->
| Slot | Exact profile | Eligibility | Task fit |
| --- | --- | --- | --- |
| standard | SM: gpt-6.1-sol / medium | general | Implement bounded changes in the repository's existing idioms. Prefer the smallest complete change and inexpensive acceptance checks. |
| hard | SX: gpt-6.1-sol / xhigh | general | Debug difficult invariants or integrate changes with interacting constraints. Require evidence that the fix addresses the cause without expanding scope. |
| opus-medium | OM: claude-opus-5-5 / medium | general | Prefer for substantial scoped implementation or refactoring when the task fits Opus Medium. Medium is not a universal optimum, so compare the actual candidate and checks. |
| opus-deep | OX: claude-opus-5-5 / xhigh | planning, qa, spec-review; independent review | Independently review maintainability and architecture against the repository's existing design. Propose concrete simpler alternatives where they preserve the required behavior. |
| broad | AMAX: gpt-6-astra / max | qa, browser; independent review | Independently test functional behavior, failure cases, and implementation assumptions against the requirements. Report evidence and maintainability concerns without claiming model-specific code-quality authority. |
| fable | FH: claude-fable-5-2 / high | general | Consider for demanding implementation or a fresh framing when the current approach overcomplicates the task or offers too-similar alternatives. Preserve acceptance criteria and distinguish authorship from independent review. |
| investigate | MFH: muse-wonder-full-1.0 / high | general | Investigate repository structure, existing fixes, and root causes using source evidence. Default to diagnosis and focused checks. Implement when the work order authorizes edits. |
| investigate-deep | MFX: muse-wonder-full-1.0 / xhigh | general | Examine cross-system failures with competing hypotheses and challenge a proposed plan against evidence. Default to discriminating checks, not a second dispatcher. Implement when the work order authorizes edits. |
<!-- END GENERATED:pool:amusing -->

Choose the earliest suitable eligible slot. Use specialists only when their task fit warrants them. Role-restricted entries do not preempt general candidates. Preserve exact model/effort and role fences. Exceptions require explicit user authorization and an exact profile. The optional inspector records pool and role exceptions as `--allow-out-of-pool` and `--role-override`.

## Accept the candidate

Define functional checks and maintainability expectations before implementation. Check the repository's conventions, scope, duplication, and unnecessary abstractions alongside behavior. Do not impose mandatory worktrees, documentation, linter frameworks, or arbitrary complexity thresholds.

Give a fresh independent reviewer the requirements, relevant source, candidate diff or revision, and authorized checks. Let the reviewer form findings without the author's conclusions. Record the reviewed revision or diff identity. The controller resolves findings, verifies corrections, and repeats affected checks when the candidate changes. An author cannot be the sole acceptance check.

Before requesting fixes, the coordinator separates evidenced defects and material risks from optional or out-of-scope improvements. Accept, reject, or defer findings against the agreed requirements; suggestions do not automatically expand implementation scope.

The coordinator retains resolved and rejected findings. Reopen them only for relevant changes or new material evidence. Keep prior verdicts out of fresh review packets. Use targeted verification for known corrections, without replacing required independent acceptance.

If an unexplained failure follows product and evaluator changes, check the corrected evaluator against unchanged product behavior before further product edits.

## Execute

Use native workers for the current host's provider with the exact catalog model/effort and required tools. For selected Claude work, load the installed Claude Delegation skill and only its relevant launch reference. Review defaults to Consultation. Authored work defaults to Implementation. For external Codex work under Claude, use the optional [controller adapter](../../../docs/controller-designs.md).

Selected Muse work requires the conditional provider checks linked from the entrypoint and an available, verified adapter, including a durable adapter when configured. No adapter or model availability is implied.

Give workers the objective, inputs, disjoint write ownership, acceptance checks, profile, and any deadline. Reviewers do not author fixes without reassignment. The controller retains integration and acceptance.

Default to at most three workers and one parent-owned active external session across descendants, subject to host limits and configured overrides. `max_external_sessions_per_assignment` counts all active external-provider runs, including Muse and durable T3 runs, together across descendants. An idle persistent thread is not an active session. Native workers are leaves unless assigned a team role. Pass the variant, mode, bias, and role fences to descendants. External workers must not recursively launch the opposite controller.

Preserve actual host permissions and user-selected tools, approvals, concurrency, and timeouts. Amusing changes routing and acceptance guidance, not those controls.
