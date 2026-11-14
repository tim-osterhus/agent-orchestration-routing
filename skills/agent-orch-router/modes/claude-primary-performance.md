# claude-primary / performance

Prioritize task success and turnaround. Escalation is available when justified, not required.

## Ordered pool

<!-- BEGIN GENERATED:pool:claude-primary/performance -->
| Slot | Exact profile | Eligibility | Task fit |
| --- | --- | --- | --- |
| opus-medium | OM: claude-opus-5-5 / medium | general | Use for substantive general-purpose implementation or integration with sufficiently clear requirements. |
| opus | OH: claude-opus-5-5 / high | general | Consider for thorough implementation, investigation, or independent review when reproductions and edge-case coverage warrant additional diligence. Use a fresh reviewer for work it authored. |
| opus-deep | OX: claude-opus-5-5 / xhigh | general | Consider for difficult analysis, implementation, architecture, or independent review, especially when exhaustive investigation or extensive testing is warranted. Keep authorship separate from final acceptance. |
| opus-max | OMAX: claude-opus-5-5 / max | general | Use for demanding implementation or analysis when sustained reasoning is justified by the assignment. |
| max-code | SMAX: gpt-6.1-sol / max | general | Consider for demanding implementation, integration, or independent verification. Use Max only when the assignment warrants the additional effort. |
| broad | AMAX: gpt-6-astra / max | general | Consider for demanding analysis, implementation, or verification when task fit warrants Max effort. Verify tools for interactive work. |
| fable | FH: claude-fable-5-2 / high | escalation; one-off | Consider for demanding reasoning, implementation, or fresh architectural framing when an approach stalls or offers too-similar alternatives. Return a candidate checked against the same acceptance criteria, or an independent review, within the bounded assignment. |
<!-- END GENERATED:pool:claude-primary/performance -->

FH may reason, implement, integrate, or review as a bounded worker, not an automatic controller or required stage. Independent review needs a fresh assignment separate from authorship.

Choose the earliest suitable eligible slot, not every cheaper profile in sequence. General slots permit all task roles. Bindings never change slot eligibility. One-off slots require a fresh bounded worker, never a continuing controller. Specialist slots take precedence for their stated role. Other eligible profiles may still use those tools.

Role/lifecycle exceptions require explicit user authorization and an exact profile. An out-of-pool choice also needs an explicit pool exception. The optional inspector records these as `--role-override` and `--allow-out-of-pool`. Never import another mode's role fences or silently substitute model/effort.

## Execute

Use native workers for the current host's provider with the exact catalog model/effort and required tools. For selected Claude work, load the installed Claude Delegation skill and only its relevant launch reference. QA/spec review defaults to Consultation. Authored work defaults to Implementation. An explicit workflow override does not change task-role eligibility. For external Codex work under Claude, use the optional [controller adapter](../../../docs/controller-designs.md).

Give workers the objective, inputs, disjoint write ownership, acceptance checks, profile, and any deadline. The controller integrates results. An author cannot be the sole acceptance check. Reviewers do not author fixes without reassignment.

No default router concurrency ceiling applies. Honor runtime/provider/project and explicit assignment limits across descendants. Claude helpers may delegate within tools, permissions, pool, scope, and roles. Pass variant, mode, bias, fences, limits, and allocated capacity to descendants. Native Codex workers remain leaves unless assigned team roles. External workers cannot recursively launch opposite controllers.

Preserve actual host permissions and user-selected tool/approval settings. Routing does not impose a new permission policy.
