# codex-primary / efficient

Minimize resources per accepted task, including retries and controller repair.

## Ordered pool

| Profile | Eligibility | Task fit |
| --- | --- | --- |
| LM | one-off | Use for a trivial one-off edit, extraction, or lookup with an immediate, inexpensive check. |
| TL | general | Use for a small specified code fix, concise writing task, or straightforward visual interpretation. |
| SL | general | Use for routine implementation with a narrow change surface and clear expected output. |
| TM | general | Use for bounded implementation, source-grounded writing, or screen-based work requiring several connected steps. |
| TH | general | Use for a harder diagnosis or multi-step visual task when Medium leaves important uncertainty. |
| SM | general | Use for general implementation spanning related files or a bounded integration with explicit checks. |
| SH | general | Use when uncertain requirements, debugging, or likely repair work justify more reasoning within this efficiency pool. |

Choose the earliest suitable eligible profile, not every cheaper profile in sequence. General entries permit all task roles. One-off entries require a fresh bounded worker, never a continuing controller. Specialist entries take precedence for their stated role. Other eligible profiles may still use those tools.

Role/lifecycle exceptions require explicit user authorization and an exact profile. An out-of-pool choice also needs an explicit pool exception. The optional inspector records these as `--role-override` and `--allow-out-of-pool`. Never import another mode's role fences or silently substitute model/effort.

## Execute

Use native workers for the current host's provider with the exact catalog model/effort and required tools. For selected Claude work, load the installed Claude Delegation skill and only its relevant launch reference. QA/spec review defaults to Consultation. Authored work defaults to Implementation. An explicit workflow override does not change task-role eligibility. For external Codex work under Claude, use the optional [controller adapter](../../../docs/controller-designs.md).

Give workers the objective, inputs, disjoint write ownership, acceptance checks, profile, and any deadline. The controller integrates results. An author cannot be the sole acceptance check. Reviewers do not author fixes without reassignment.

Default to at most three workers and one parent-owned external session across descendants, subject to host limits. Native workers are leaves unless assigned a team role. Pass the variant, mode, bias, and role fences to descendants. External workers must not recursively launch the opposite controller.

Preserve actual host permissions and user-selected tool/approval settings. Routing does not impose a new permission policy.
