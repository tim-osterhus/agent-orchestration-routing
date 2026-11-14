# Fable assignment briefs

For selected FM/FH/FX/FMAX assignments only. Include relevant points in the work order.

- State the outcome, relevant context, approved specification, acceptance checks, and boundaries. Prefer the smallest in-scope approach over micromanaged steps.
- For narrow maintenance, request the specific change, not ownership of the entire system. Report related findings without automatic refactors.
- Name the precise actions that require approval. When relaying approval, name the authorized action instead of saying only “continue.” Put task-specific exceptions in the rule itself. Preserve hard prohibitions and existing permission controls.
- Persist until authorized work is verified or a real blocker requires outside input. Diagnose recoverable failures and retry safely. Avoid unproductive retry loops. Do not invent authority or bypass deliberate limits. Report blockers with evidence.
- Delegate only when the mode, work order, and runtime permit useful independent work. Specify each worker's exact model, scope, and checks. Do not assume an expensive inherited model. Preserve assignment-scoped delegation limits and pure-orchestration coordinator policy.
- Keep the exact selected model and effort except for the preauthorized usage-cap fallback below. Never silently change profiles.
- Distinguish review-only from implementation authority regardless of tool access.
- Retain required tests and acceptance evidence despite model self-verification claims. Return self-contained results, completed checks, remaining findings, and unverified items.

Supply new instructions through a supported CLI in a new turn or conversation, without rewriting historical system, tool, or thinking blocks.

## Automatic usage-cap fallback

Invoking this router preauthorizes the following fallback for owned delegated Fable assignments, not replacement of a running host/controller. No renewed approval is needed, including outside the selected mode pool:

| Requested profile | Actual fallback profile | Exact model | Effort |
| --- | --- | --- | --- |
| FM | OH | claude-opus-5-5 | high |
| FH | OX | claude-opus-5-5 | xhigh |
| FX | OMAX | claude-opus-5-5 | max |
| FMAX | OMAX | claude-opus-5-5 | max |

FMAX→OMAX is capped at Opus's supported Max ceiling. It is not an effort above Max or a claim of equivalent performance.

Trigger only when the provider explicitly reports usage exhaustion on a Fable attempt. A confirmed Fable-specific cap qualifies. If model-specific versus shared scope is unclear, allow one mapped Opus attempt without a browser quota check. Explicit shared plan exhaustion does not qualify. Authentication, billing, model-access, transport, overload, and ordinary transient rate-limit errors do not qualify. A 429 alone is insufficient.

Stop the failed owned Fable attempt and confirm it is terminal before starting Opus. Preserve partial work, task scope, permissions, ownership, and remaining deadlines. Use a fresh owned Opus session, not a relabeled or resumed Fable session. Transfer only decision-relevant partial work. Independent reviewers receive fresh neutral packets without author conversations or prior verdicts. Avoid duplicate writers and retain owned-process cancellation and cleanup controls.

If Opus is also usage-blocked, or the provider identifies plan-wide exhaustion, stop and report the blocker. Do not cycle profiles, switch accounts, add API billing, enable extra usage, or bypass reserves and explicit project limits. Other failures follow their normal diagnosis and authorization rules. This policy is not generic unavailable-model fallback.

Record the provider's usage-exhaustion evidence, requested and actual profiles, exact model and effort, owned session IDs, and remaining limits. Disclose the automatic switch. Never label an Opus result as Fable or transfer Fable-specific evidence claims to Opus.

This fallback narrowly overrides required-profile, outside-pool, no-alternate, and mapped Opus role/lifecycle fences for this trigger only. It continues the original authorized Fable assignment, not a new role or lifecycle. Preserve the original scope, role, permissions, tools, and remaining limits without granting capabilities. For example, Amusing FH implementation may continue on OX despite OX's normal review-role fence. Preserve independent conclusions, same-version ratification, and required Council/UI-Pro membership and model diversity. Helpers add no votes. Two Opus runs are not distinct model opinions. If substitution collapses required diversity, report incomplete membership and request a distinct alternate.

The offline inspector and launch planner do not detect exhaustion or execute retries. The coordinator records mapped role/lifecycle exceptions with `--role-override`, even for an in-pool fallback. Add `--allow-out-of-pool` only when needed. Preserve the original role and selected Claude workflow in the plan. These flags record this narrow preauthorization, not broader task authority.

Sources: [video discussion](https://youtu.be/ha1Iu9YWMtw?t=384), [official prompting guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2).
