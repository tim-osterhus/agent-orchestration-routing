# Agent Orchestration Routing

Explicit-invocation skills for developers delegating work across Codex and Claude Code.

Select exact model/effort profiles using the [Artificial Analysis capability–cost Pareto frontier](https://artificialanalysis.ai/evaluations/artificial-analysis-intelligence-index): choose the least-cost suitable capability, then account for tools, latency, and access.

Start with [Agent Orchestration Router](skills/agent-orch-router/SKILL.md) and one selected mode. Native routing needs no script or configuration read. Keep the router folder intact. Use the full checkout for optional [installation/configuration](docs/configuration.md), [controller adapters](docs/controller-designs.md), or Claude companion tooling.

Opt-in [High-qual](skills/agent-orch-router/modes/high-qual.md) adds maintainability review and selective Muse investigation through a separately verified provider adapter.

```sh
python3 scripts/bundle.py validate
python3 scripts/bundle.py resolve --mode balanced --role implementation
```

[MIT License](LICENSE) · Tim Osterhus
