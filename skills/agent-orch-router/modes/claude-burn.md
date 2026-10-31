# claude-burn

Complete useful authorized Claude backlog work before its account endpoint. This provider-only pool is identical under both variants.

Establish explicit burn invocation, intended account, reset/deadline or queue endpoint, and authorized backlog before launch. Ask only for missing inputs.

Restore the prior mode at the endpoint or backlog completion. Stop on quota, billing, authentication, rate-limit, or model-access failures. Do not invent work, change authentication, or enable paid extra usage. An explicit cross-provider exception uses its own account route, not this burn allowance. Burn does not enable Orchestration or change permissions.

## Ordered pool

| Profile | Eligibility | Task fit |
| --- | --- | --- |
| HMAX | one-off | Use for a bounded one-off backlog packet with concrete inputs, ownership, and acceptance checks. |
| SNH | general | Use for scoped authorized implementation or analysis needing more judgment than a small Haiku packet. |
| OM | general | Use for general-purpose authorized implementation and integration spanning related files. |
| OH | general | Use for uncertain backlog implementation or debugging where additional reasoning is justified. |
| OX | general | Use for difficult authorized analysis, implementation, or integration with interacting requirements. |
| OMAX | general | Use for demanding authorized work when sustained reasoning fits the backlog, not merely to consume allowance. |

Choose the earliest suitable eligible profile, not every cheaper profile in sequence. General entries permit all task roles. One-off entries require a fresh bounded worker, never a continuing controller. Specialist entries take precedence for their stated role. Other eligible profiles may still use those tools.

Role/lifecycle exceptions require explicit user authorization and an exact profile. An out-of-pool choice also needs an explicit pool exception. The optional inspector records these as `--role-override` and `--allow-out-of-pool`. Never import another mode's role fences or silently substitute model/effort.

## Execute

Use native workers for the current host's provider with the exact catalog model/effort and required tools. For selected Claude work, load the installed Claude Delegation skill and only its relevant launch reference. QA/spec review defaults to Consultation. Authored work defaults to Implementation. An explicit workflow override does not change task-role eligibility. For external Codex work under Claude, use the optional [controller adapter](../../../docs/controller-designs.md).

Give workers the objective, inputs, disjoint write ownership, acceptance checks, profile, and any deadline. The controller integrates results. An author cannot be the sole acceptance check. Reviewers do not author fixes without reassignment.

Default to at most three workers and one parent-owned external session across descendants, subject to host limits. Native workers are leaves unless assigned a team role. Pass the variant, mode, bias, and role fences to descendants. External workers must not recursively launch the opposite controller.

Preserve actual host permissions and user-selected tool/approval settings. Routing does not impose a new permission policy.
