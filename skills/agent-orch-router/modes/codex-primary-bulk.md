# codex-primary / bulk

Use this pool when Codex should author most work and Claude should take hard or quality-sensitive work. Low/default/high bias keeps this pool and its exact efforts. The controller keeps planning, integration, and final acceptance.

## Ordered pool

<!-- BEGIN GENERATED:pool:codex-primary/bulk -->
| Slot | Exact profile | Eligibility | Task fit |
| --- | --- | --- | --- |
| routine | SL: gpt-6.1-sol / low | general | Use for routine, clearly specified edits whose output is easy to check. |
| visual | TM: gpt-6.1-terra / medium | general | Use for everyday bounded implementation, source-grounded writing, visual interpretation, or screen-based workflows. |
| visual-deep | TH: gpt-6.1-terra / high | general | Use for harder diagnosis, multi-step visual reasoning, or computer-use work needing more deliberation than TM. |
| standard | SM: gpt-6.1-sol / medium | general | Use for general implementation, related-file changes, or independent verification with moderate ambiguity. |
| deep | SH: gpt-6.1-sol / high | general | Use for debugging, unclear behavior, or integration where controller repair would otherwise be substantial. |
| hard | SX: gpt-6.1-sol / xhigh | general | Use for difficult implementation or debugging with interacting constraints and explicit acceptance checks. |
| max-code | SMAX: gpt-6.1-sol / max | general | Use for demanding implementation or independent code verification when the task warrants sustained reasoning. |
| browser | AL: gpt-6-astra / low | browser; specialist | Start here for browser interaction or visual inspection. Confirm the worker has the required browser tools and session. |
| opus-max | OX: claude-opus-5-5 / xhigh | escalation | Escalate hard or quality-sensitive implementation or analysis after an unconvincing Codex attempt or when errors would be costly. |
| opus | OH: claude-opus-5-5 / high | qa, spec-review; independent review | Use for independent QA or specification review of a Codex-authored candidate, not implementation. |
| fable-review | FH: claude-fable-5-2 / high | research, planning, qa, spec-review; independent review; escalation; one-off | Selectively escalate difficult reasoning, specification analysis, or independent review. Use a bounded worker, not authored fixes or team management. |
<!-- END GENERATED:pool:codex-primary/bulk -->

OX is an escalation, not a default author. Prefer it after a failed or unconvincing Codex attempt, or when a mistake would be costly: security-sensitive code, data migrations, public interfaces, or subtle concurrency. FH advises or reviews; it does not author fixes or manage a team.

Choose the earliest suitable eligible slot, not every cheaper profile in sequence. General slots permit all task roles. Bindings never change slot eligibility. One-off slots require a fresh bounded worker, never a continuing controller. Specialist slots take precedence for their stated role. Other eligible profiles may still use those tools.

Role/lifecycle exceptions require explicit user authorization and an exact profile. An out-of-pool choice also needs an explicit pool exception. The optional inspector records these as `--role-override` and `--allow-out-of-pool`. Never import another mode's role fences or silently substitute model/effort.

## Execute

Use native workers for the current host's provider with the exact catalog model/effort and required tools. For selected Claude work, load the installed Claude Delegation skill and only its relevant launch reference. QA/spec review defaults to Consultation. Authored work defaults to Implementation. An explicit workflow override does not change task-role eligibility. For external Codex work under Claude, use the optional [controller adapter](../../../docs/controller-designs.md).

Give workers the objective, inputs, disjoint write ownership, acceptance checks, profile, and any deadline. Run overlapping or dependent work in sequence. The controller integrates results. An author cannot be the sole acceptance check. Reviewers do not author fixes without reassignment.

Default to at most three workers and one parent-owned external session across descendants, subject to host limits. Native workers are leaves unless assigned a team role. Pass the variant, mode, bias, and role fences to descendants. External workers must not recursively launch the opposite controller.

Preserve actual host permissions and user-selected tool/approval settings. Routing does not impose a new permission policy.
