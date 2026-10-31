# codex-primary / balanced

Use this everyday pool for low/default/high bias. Low favors the least resource-intensive reliable fit. Default accounts for repair overhead. High favors reasoning capacity when uncertainty warrants it. All biases retain this same pool and exact efforts.

## Ordered pool

| Profile | Eligibility | Task fit |
| --- | --- | --- |
| SL | general | Use for routine, clearly specified edits whose output is easy to check. |
| TM | general | Use for everyday bounded implementation, source-grounded writing, visual interpretation, or screen-based workflows. |
| TH | general | Use for harder diagnosis, multi-step visual reasoning, or computer-use work needing more deliberation than TM. |
| SM | general | Use for general implementation, related-file changes, or independent verification with moderate ambiguity. |
| SH | general | Use for debugging, unclear behavior, or integration where controller repair would otherwise be substantial. |
| SX | general | Use for difficult implementation or debugging with interacting constraints and explicit acceptance checks. |
| SMAX | general | Use for demanding implementation or independent code verification when the task warrants sustained reasoning. |
| AL | browser; specialist | Start here for browser interaction or visual inspection. Confirm the worker has the required browser tools and session. |
| OH | qa, spec-review; independent review | Use for an optional independent QA or specification review of a completed candidate, not implementation. |

Choose the earliest suitable eligible profile, not every cheaper profile in sequence. General entries permit all task roles. One-off entries require a fresh bounded worker, never a continuing controller. Specialist entries take precedence for their stated role. Other eligible profiles may still use those tools.

Role/lifecycle exceptions require explicit user authorization and an exact profile. An out-of-pool choice also needs an explicit pool exception. The optional inspector records these as `--role-override` and `--allow-out-of-pool`. Never import another mode's role fences or silently substitute model/effort.

## Execute

Use native workers for the current host's provider with the exact catalog model/effort and required tools. For selected Claude work, load the installed Claude Delegation skill and only its relevant launch reference. QA/spec review defaults to Consultation. Authored work defaults to Implementation. An explicit workflow override does not change task-role eligibility. For external Codex work under Claude, use the optional [controller adapter](../../../docs/controller-designs.md).

Give workers the objective, inputs, disjoint write ownership, acceptance checks, profile, and any deadline. The controller integrates results. An author cannot be the sole acceptance check. Reviewers do not author fixes without reassignment.

Default to at most three workers and one parent-owned external session across descendants, subject to host limits. Native workers are leaves unless assigned a team role. Pass the variant, mode, bias, and role fences to descendants. External workers must not recursively launch the opposite controller.

Preserve actual host permissions and user-selected tool/approval settings. Routing does not impose a new permission policy.
