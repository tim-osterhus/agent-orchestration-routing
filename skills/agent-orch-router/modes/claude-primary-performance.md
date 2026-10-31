# claude-primary / performance

Prioritize task success and turnaround. Escalation is available when justified, not required.

## Ordered pool

| Profile | Eligibility | Task fit |
| --- | --- | --- |
| OM | general | Use for substantive general-purpose implementation or integration with sufficiently clear requirements. |
| OH | general | Use for difficult implementation or diagnosis involving uncertain behavior and related components. |
| OX | general | Use for complex debugging, architecture analysis, or integration with several interacting constraints. |
| OMAX | general | Use for demanding implementation or analysis when sustained reasoning is justified by the assignment. |
| SMAX | qa, spec-review; independent review | Use for optional independent QA or specification review of difficult code, not authored fixes. |
| AMAX | browser; specialist | Start here for demanding browser or computer-use work. Confirm the actual worker's tools and session access. |

Choose the earliest suitable eligible profile, not every cheaper profile in sequence. General entries permit all task roles. One-off entries require a fresh bounded worker, never a continuing controller. Specialist entries take precedence for their stated role. Other eligible profiles may still use those tools.

Role/lifecycle exceptions require explicit user authorization and an exact profile. An out-of-pool choice also needs an explicit pool exception. The optional inspector records these as `--role-override` and `--allow-out-of-pool`. Never import another mode's role fences or silently substitute model/effort.

## Execute

Use native workers for the current host's provider with the exact catalog model/effort and required tools. For selected Claude work, load the installed Claude Delegation skill and only its relevant launch reference. QA/spec review defaults to Consultation. Authored work defaults to Implementation. An explicit workflow override does not change task-role eligibility. For external Codex work under Claude, use the optional [controller adapter](../../../docs/controller-designs.md).

Give workers the objective, inputs, disjoint write ownership, acceptance checks, profile, and any deadline. The controller integrates results. An author cannot be the sole acceptance check. Reviewers do not author fixes without reassignment.

Default to at most three workers and one parent-owned external session across descendants, subject to host limits. Native workers are leaves unless assigned a team role. Pass the variant, mode, bias, and role fences to descendants. External workers must not recursively launch the opposite controller.

Preserve actual host permissions and user-selected tool/approval settings. Routing does not impose a new permission policy.
