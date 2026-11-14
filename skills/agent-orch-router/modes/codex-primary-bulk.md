# codex-primary / bulk

Use this pool when Codex should author most work and Claude should take hard or quality-sensitive work. Low/default/high bias keeps this pool and its exact efforts. The controller keeps planning, integration, and final acceptance.

## Ordered pool

<!-- BEGIN GENERATED:pool:codex-primary/bulk -->
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
| opus-max | OX: claude-opus-5-5 / xhigh | escalation | Escalate hard or quality-sensitive implementation or analysis after an unconvincing Codex attempt or when errors would be costly. |
| opus | OH: claude-opus-5-5 / high | qa, spec-review; independent review | Use for independent QA or specification review of a Codex-authored candidate, not implementation. |
| fable | FH: claude-fable-5-2 / high | escalation; one-off | Consider for demanding reasoning, implementation, or fresh architectural framing when an approach stalls or offers too-similar alternatives. Return a candidate checked against the same acceptance criteria, or an independent review, within the bounded assignment. |
<!-- END GENERATED:pool:codex-primary/bulk -->

Known patterns can span long workflows. A clear outcome alone does not make the solution path known.

Return unresolved framing or repeated UI loops to the coordinator with the current state, attempts, and open decision. Reassignment follows existing pool, role, and route authorization, without silent substitution.

OX is an escalation, not a default author. Prefer it after a failed or unconvincing Codex attempt, or when a mistake would be costly: security-sensitive code, data migrations, public interfaces, or subtle concurrency. FH may analyze, implement, or review demanding work as a bounded worker. OH retains this mode's dedicated independent-review assignment.

Choose the earliest suitable eligible slot, not every cheaper profile in sequence. General slots permit all task roles. Bindings never change slot eligibility. One-off slots require a fresh bounded worker, never a continuing controller. Specialist slots take precedence for their stated role. Other eligible profiles may still use those tools.

Role/lifecycle exceptions require explicit user authorization and an exact profile. An out-of-pool choice also needs an explicit pool exception. The optional inspector records these as `--role-override` and `--allow-out-of-pool`. Never import another mode's role fences or silently substitute model/effort.

## Execute

Use native workers for the current host's provider with the exact catalog model/effort and required tools. For selected Claude work, load the installed Claude Delegation skill and only its relevant launch reference. QA/spec review defaults to Consultation. Authored work defaults to Implementation. An explicit workflow override does not change task-role eligibility. For external Codex work under Claude, use the optional [controller adapter](../../../docs/controller-designs.md).

Give workers the objective, inputs, disjoint write ownership, acceptance checks, profile, and any deadline. Run overlapping or dependent work in sequence. The controller integrates results. An author cannot be the sole acceptance check. Reviewers do not author fixes without reassignment.

No default router concurrency ceiling applies. Honor runtime/provider/project and explicit assignment limits across descendants. Claude helpers may delegate within tools, permissions, pool, scope, and roles. Pass variant, mode, bias, fences, limits, and allocated capacity to descendants. Native Codex workers remain leaves unless assigned team roles. External workers cannot recursively launch opposite controllers.

Preserve actual host permissions and user-selected tool/approval settings. Routing does not impose a new permission policy.
