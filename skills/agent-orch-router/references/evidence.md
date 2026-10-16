# Selection evidence

The selection method follows the [Artificial Analysis capability–cost chart](https://artificialanalysis.ai/evaluations/artificial-analysis-intelligence-index). Prefer nondominated model/effort configurations: no alternative has at least the same measured capability at lower or equal measured cost, with one strict improvement. Then apply task fit, tool access, latency, context, and account constraints.

The supplied chart is a dated, filtered view. Frontier membership depends on the comparison set, benchmark version, effort, fallback behavior, and provider pricing. A capability score is not proof that a model will succeed at a particular repository task. Do not convert the plotted values into fabricated exact scores or prices.

[Artificial Analysis methodology](https://artificialanalysis.ai/methodology) defines cost per task using benchmark token consumption and API prices. It does not measure the user's subscription quota per completed assignment. Fast service tiers, compact-context policies, and specialist routes can be useful even when their precise configurations are unmeasured or off the plotted frontier.

The registry is a configurable example informed by that method, not an automatic frontier calculator. Refresh it only when requested. Record source/date, exact model and effort, benchmark version, measured cost and latency, fallback behavior, and any specialization exception. Leave unavailable measurements unknown. Review changes before replacing the active registry.

Native Codex behavior was checked against [OpenAI's subagent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents). External launch planning was checked against [Codex exec](https://learn.chatgpt.com/docs/developer-commands#codex-exec) and the [Claude CLI reference](https://code.claude.com/docs/en/cli-reference). Local CLI help checked on 2026-10-16: Codex 0.153.2 and Claude Code 2.1.296. No live model or account-access test is implied.
