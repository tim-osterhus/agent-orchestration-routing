# codex-primary / performance

Prioritize task success and turnaround. Escalation is available when justified, not required.

## Ordered pool

<!-- BEGIN GENERATED:pool:codex-primary/performance -->
| Slot | Exact profile | Eligibility | Task fit |
| --- | --- | --- | --- |
| deep | SH: gpt-6.1-sol / high | general | Use for substantive implementation or diagnosis when a routine route would leave material uncertainty. |
| hard | SX: gpt-6.1-sol / xhigh | general | Use for difficult debugging, integration, or implementation with several interacting constraints. |
| max-code | SMAX: gpt-6.1-sol / max | general | Use for demanding code changes or independent verification requiring sustained reasoning across a large change surface. |
| broad | AMAX: gpt-6-astra / max | general | Use for demanding analysis, visual reasoning, or implementation where Astra's task and tool fit justify the route. |
| browser | AH: gpt-6-astra / high | browser; specialist | Start here for difficult browser or computer-use assignments. Confirm actual tools and session access. |
| opus-deep | OX: claude-opus-5-5 / xhigh | qa, spec-review; independent review | Use for optional independent QA or specification review of complex work, not authored fixes. |
| opus-max | OMAX: claude-opus-5-5 / max | escalation | Use as a justified escalation for demanding analysis or implementation when earlier eligible choices do not fit. |
| fable-review | FH: claude-fable-5-2 / high | research, planning, qa, spec-review; independent review; escalation; one-off | Selectively escalate difficult reasoning, specification analysis, or independent review. Use a bounded worker, not authored fixes or team management. |
<!-- END GENERATED:pool:codex-primary/performance -->

FH is a one-off escalation, not a required stage. Review assignments remain independent of the author.

Choose the earliest suitable eligible slot, not every cheaper profile in sequence. General slots permit all task roles. Bindings never change slot eligibility. One-off slots require a fresh bounded worker, never a continuing controller. Specialist slots take precedence for their stated role. Other eligible profiles may still use those tools.

Role/lifecycle exceptions require explicit user authorization and an exact profile. An out-of-pool choice also needs an explicit pool exception. The optional inspector records these as `--role-override` and `--allow-out-of-pool`. Never import another mode's role fences or silently substitute model/effort.

## Execute

Use native workers for the current host's provider with the exact catalog model/effort and required tools. For selected Claude work, load the installed Claude Delegation skill and only its relevant launch reference. QA/spec review defaults to Consultation. Authored work defaults to Implementation. An explicit workflow override does not change task-role eligibility. For external Codex work under Claude, use the optional [controller adapter](../../../docs/controller-designs.md).

Give workers the objective, inputs, disjoint write ownership, acceptance checks, profile, and any deadline. The controller integrates results. An author cannot be the sole acceptance check. Reviewers do not author fixes without reassignment.

Default to at most three workers and one parent-owned external session across descendants, subject to host limits. Native workers are leaves unless assigned a team role. Pass the variant, mode, bias, and role fences to descendants. External workers must not recursively launch the opposite controller.

Preserve actual host permissions and user-selected tool/approval settings. Routing does not impose a new permission policy.
