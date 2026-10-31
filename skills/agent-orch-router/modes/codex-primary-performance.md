# codex-primary / performance

Prioritize task success and turnaround. Escalation is available when justified, not required.

## Ordered pool

| Profile | Eligibility | Task fit |
| --- | --- | --- |
| SH | general | Use for substantive implementation or diagnosis when a routine route would leave material uncertainty. |
| SX | general | Use for difficult debugging, integration, or implementation with several interacting constraints. |
| SMAX | general | Use for demanding code changes or independent verification requiring sustained reasoning across a large change surface. |
| AMAX | general | Use for demanding analysis, visual reasoning, or implementation where Astra's task and tool fit justify the route. |
| AH | browser; specialist | Start here for difficult browser or computer-use assignments. Confirm actual tools and session access. |
| OX | qa, spec-review; independent review | Use for optional independent QA or specification review of complex work, not authored fixes. |
| OMAX | escalation | Use as a justified escalation for demanding analysis or implementation when earlier eligible choices do not fit. |

Choose the earliest suitable eligible profile, not every cheaper profile in sequence. General entries permit all task roles. One-off entries require a fresh bounded worker, never a continuing controller. Specialist entries take precedence for their stated role. Other eligible profiles may still use those tools.

Role/lifecycle exceptions require explicit user authorization and an exact profile. An out-of-pool choice also needs an explicit pool exception. The optional inspector records these as `--role-override` and `--allow-out-of-pool`. Never import another mode's role fences or silently substitute model/effort.

## Execute

Use native workers for the current host's provider with the exact catalog model/effort and required tools. For selected Claude work, load the installed Claude Delegation skill and only its relevant launch reference. QA/spec review defaults to Consultation. Authored work defaults to Implementation. An explicit workflow override does not change task-role eligibility. For external Codex work under Claude, use the optional [controller adapter](../../../docs/controller-designs.md).

Give workers the objective, inputs, disjoint write ownership, acceptance checks, profile, and any deadline. The controller integrates results. An author cannot be the sole acceptance check. Reviewers do not author fixes without reassignment.

Default to at most three workers and one parent-owned external session across descendants, subject to host limits. Native workers are leaves unless assigned a team role. Pass the variant, mode, bias, and role fences to descendants. External workers must not recursively launch the opposite controller.

Preserve actual host permissions and user-selected tool/approval settings. Routing does not impose a new permission policy.
