# Fable assignment briefs

For selected FM/FH/FX/FMAX assignments only. Include relevant points in the work order.

- State the outcome, relevant context, approved specification, acceptance checks, and boundaries. Prefer the smallest in-scope approach over micromanaged steps.
- For narrow maintenance, request the specific change, not ownership of the entire system. Report related findings without automatic refactors.
- Name the precise actions that require approval. When relaying approval, name the authorized action instead of saying only “continue.” Put task-specific exceptions in the rule itself. Preserve hard prohibitions and existing permission controls.
- Persist until authorized work is verified or a real blocker requires outside input. Diagnose recoverable failures and retry safely. Avoid unproductive retry loops. Do not invent authority or bypass deliberate limits. Report blockers with evidence.
- Delegate only when the mode, work order, and runtime permit useful independent work. Specify each worker's exact model, scope, and checks. Do not assume an expensive inherited model. Preserve Fable leaf/no-team fences and pure-orchestration coordinator policy.
- Keep the exact selected model and effort. Never silently change profiles.
- Distinguish review-only from implementation authority regardless of tool access.
- Retain required tests and acceptance evidence despite model self-verification claims. Return self-contained results, completed checks, remaining findings, and unverified items.

Supply new instructions through a supported CLI in a new turn or conversation, without rewriting historical system, tool, or thinking blocks.

Sources: [video discussion](https://youtu.be/ha1Iu9YWMtw?t=384), [official prompting guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2).
