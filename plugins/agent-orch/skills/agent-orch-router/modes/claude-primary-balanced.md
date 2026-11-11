# claude-primary / balanced

Use this everyday pool for low/default/high bias. Low favors the least resource-intensive reliable fit. Default accounts for repair overhead. High favors reasoning capacity when uncertainty warrants it. All biases retain this same pool and exact efforts.

## Ordered pool

<!-- BEGIN GENERATED:pool:claude-primary/balanced -->
| Slot | Exact profile | Eligibility | Task fit |
| --- | --- | --- | --- |
| haiku-high | HH: claude-haiku-5-5 / high | one-off | Use for a simple one-off task with concrete inputs and an inexpensive check. |
| haiku-xhigh | HM: claude-haiku-5-5 / xhigh | one-off | Use for bounded one-off implementation or analysis with clear ownership and acceptance criteria. |
| haiku-max | HMAX: claude-haiku-5-5 / max | one-off | Use for a harder one-off packet that still has a narrow scope and a direct acceptance check. |
| sonnet | SNH: claude-sonnet-5-5 / high | general | Use for scoped implementation, research synthesis, or diagnosis needing judgment beyond a small Haiku packet. |
| opus-medium | OM: claude-opus-5-5 / medium | general | Use for everyday general-purpose implementation and integration, including work spanning related files. |
| opus | OH: claude-opus-5-5 / high | general | Use for uncertain implementation, debugging, or integration where additional reasoning is justified. |
| opus-deep | OX: claude-opus-5-5 / xhigh | general | Use for difficult implementation or analysis with interacting requirements and substantial ambiguity. |
| standard | SM: gpt-6.1-sol / medium | qa, spec-review; independent review | Use for optional independent QA or specification review of a candidate, not implementation. |
| max-code | SMAX: gpt-6.1-sol / max | qa, spec-review; independent review | Use for optional independent code or specification review when complex failure paths need sustained analysis. |
<!-- END GENERATED:pool:claude-primary/balanced -->

Choose the earliest suitable eligible slot, not every cheaper profile in sequence. General slots permit all task roles. Bindings never change slot eligibility. One-off slots require a fresh bounded worker, never a continuing controller. Specialist slots take precedence for their stated role. Other eligible profiles may still use those tools.

Role/lifecycle exceptions require explicit user authorization and an exact profile. An out-of-pool choice also needs an explicit pool exception. The optional inspector records these as `--role-override` and `--allow-out-of-pool`. Never import another mode's role fences or silently substitute model/effort.

## Execute

Use native workers for the current host's provider with the exact catalog model/effort and required tools. For selected Claude work, load the installed Claude Delegation skill and only its relevant launch reference. QA/spec review defaults to Consultation. Authored work defaults to Implementation. An explicit workflow override does not change task-role eligibility. For external Codex work under Claude, use the optional [controller adapter](../../../docs/controller-designs.md).

Give workers the objective, inputs, disjoint write ownership, acceptance checks, profile, and any deadline. The controller integrates results. An author cannot be the sole acceptance check. Reviewers do not author fixes without reassignment.

Default to at most three workers and one parent-owned external session across descendants, subject to host limits. Native workers are leaves unless assigned a team role. Pass the variant, mode, bias, and role fences to descendants. External workers must not recursively launch the opposite controller.

Preserve actual host permissions and user-selected tool/approval settings. Routing does not impose a new permission policy.
