# high-qual

Opt in for maintainable changes with functional evidence and independent review. This shared mode has eight eligible profiles, not an eight-stage pipeline.

## Ordered pool

| Profile | Eligibility | Task fit |
| --- | --- | --- |
| SM | general | Implement bounded changes in the repository's existing idioms. Prefer the smallest complete change and inexpensive acceptance checks. |
| SX | general | Debug difficult invariants or integrate changes with interacting constraints. Require evidence that the fix addresses the cause without expanding scope. |
| OM | general | Prefer for substantial scoped implementation or refactoring when the task fits Opus Medium. Medium is not a universal optimum, so compare the actual candidate and checks. |
| OX | planning, qa, spec-review; independent review | Independently review maintainability and architecture against the repository's existing design. Propose concrete simpler alternatives where they preserve the required behavior. |
| AX | qa, browser; independent review | Perform demanding functional or adversarial verification with checked tool access. Report observed behavior and failures without treating this route as clean-code authority. |
| FX | spec-review; independent review | Selectively review conformance to explicit requirements and acceptance criteria. Cite mismatches and omissions without implementing fixes or requiring this reviewer for every change. |
| MFH | research, planning, qa, implementation | Investigate repository structure, existing fixes, and root causes using source evidence. Default to diagnosis and focused checks. Implement when the work order authorizes edits. |
| MFX | research, planning, qa, implementation | Examine cross-system failures with competing hypotheses and challenge a proposed plan against evidence. Default to discriminating checks, not a second dispatcher. Implement when the work order authorizes edits. |

Choose the earliest suitable eligible profile. Use specialists only when their task fit warrants them. Role-restricted entries do not preempt general candidates. Preserve exact model/effort and role fences. Exceptions require explicit user authorization and an exact profile. The optional inspector records pool and role exceptions as `--allow-out-of-pool` and `--role-override`.

## Accept the candidate

Define functional checks and maintainability expectations before implementation. Check the repository's conventions, scope, duplication, and unnecessary abstractions alongside behavior. Do not impose mandatory worktrees, documentation, linter frameworks, or arbitrary complexity thresholds.

Give a fresh independent reviewer the requirements, relevant source, candidate diff or revision, and authorized checks. Let the reviewer form findings without the author's conclusions. Record the reviewed revision or diff identity. The controller resolves findings, verifies corrections, and repeats affected checks when the candidate changes. An author cannot be the sole acceptance check.

## Execute

Use native workers for the current host's provider with the exact catalog model/effort and required tools. For selected Claude work, load the installed Claude Delegation skill and only its relevant launch reference. Review defaults to Consultation. Authored work defaults to Implementation. For external Codex work under Claude, use the optional [controller adapter](../../../docs/controller-designs.md).

Selected Muse work requires the conditional provider checks linked from the entrypoint and an available, verified adapter, including a durable adapter when configured. No adapter or model availability is implied.

Give workers the objective, inputs, disjoint write ownership, acceptance checks, profile, and any deadline. Reviewers do not author fixes without reassignment. The controller retains integration and acceptance.

Default to at most three workers and one parent-owned active external session across descendants, subject to host limits and configured overrides. `max_external_sessions_per_assignment` counts all active external-provider runs, including Muse and durable T3 runs, together across descendants. An idle persistent thread is not an active session. Native workers are leaves unless assigned a team role. Pass the variant, mode, bias, and role fences to descendants. External workers must not recursively launch the opposite controller.

Preserve actual host permissions and user-selected tools, approvals, concurrency, and timeouts. High-qual changes routing and acceptance guidance, not those controls.
