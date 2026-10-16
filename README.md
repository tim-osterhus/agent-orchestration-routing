# Agent Orchestration Routing

Configurable skill bundles for developers coordinating Codex and Claude Code workers.

Model policies are opinionated. Tool access and approvals are configurable.

Select exact model/effort profiles using the [Artificial Analysis capability–cost Pareto frontier](https://artificialanalysis.ai/evaluations/artificial-analysis-intelligence-index): choose the least-cost suitable capability, then account for tools, latency, and access.

```sh
python3 scripts/bundle.py validate
python3 scripts/bundle.py resolve --mode balanced --role implementation
```

Keep this checkout together. [Configure and install](docs/configuration.md) the router and optional Claude companion. Choose [Codex-first or Claude-first](docs/controller-designs.md). Enable the Opus/Haiku preset only when wanted.

[MIT License](LICENSE) · Tim Osterhus · tim@millrace.ai
