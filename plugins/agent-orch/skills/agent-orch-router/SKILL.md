---
name: agent-orch-router
description: Explicit-only routing for delegated work through exact model/effort profiles, stable job slots, and role-aware mode pools. Catalog discovery does not establish an available provider adapter.
disable-model-invocation: true
---

# Agent Orchestration Router

Activate only on explicit invocation for this assignment. Default to **codex-primary / balanced / default bias** and **pure orchestration**: delegate substantive work, then integrate and accept results. Use supporting delegation when requested. Retain these choices through compaction.

Read this file and **only the selected mode document**:

| Variant | Efficient | Balanced | Performance |
| --- | --- | --- | --- |
| codex-primary | [Efficient](modes/codex-primary-efficient.md) | [Balanced](modes/codex-primary-balanced.md) | [Performance](modes/codex-primary-performance.md) · [Bulk](modes/codex-primary-bulk.md) |
| claude-primary | [Efficient](modes/claude-primary-efficient.md) | [Balanced](modes/claude-primary-balanced.md) | [Performance](modes/claude-primary-performance.md) |

Shared across variants: [Amusing](modes/amusing.md) · [Council](modes/council.md) · [Browser-3D](modes/browser-3d.md) · [Codex-burn](modes/codex-burn.md) · [Claude-burn](modes/claude-burn.md).

Variant selects pool preference, not the running host. Never change the parent model. Select a stable job slot through its active-mode binding, or honor an explicit exact profile. Rebinding a slot changes its model, not its role, lifecycle, or review authority. Two slots sharing a model remain separate jobs.

## Standard frontier

These are all **21 raw-score nondominated configurations** in the dated four-provider Standard comparison, not a curated subset. Frontier membership is comparison-specific, not proof of suitability, subscription economics, access, or an available dispatcher.

<!-- BEGIN GENERATED:catalog-frontier -->
| Code | Exact model | Effort |
| --- | --- | --- |
| LL | gpt-6-luna | low |
| LM | gpt-6-luna | medium |
| HL | claude-haiku-5-5 | low |
| TL | gpt-6.1-terra | low |
| EX | muse-ember-1.0 | xhigh |
| EMAX | muse-ember-1.0 | max |
| TM | gpt-6.1-terra | medium |
| TH | gpt-6.1-terra | high |
| SM | gpt-6.1-sol | medium |
| SH | gpt-6.1-sol | high |
| SX | gpt-6.1-sol | xhigh |
| SMAX | gpt-6.1-sol | max |
| AH | gpt-6-astra | high |
| AX | gpt-6-astra | xhigh |
| FM | claude-fable-5-2 | medium |
| OX | claude-opus-5-5 | xhigh |
| GCM | gemini-4-carbon | medium |
| GCH | gemini-4-carbon | high |
| FH | claude-fable-5-2 | high |
| FX | claude-fable-5-2 | xhigh |
| FMAX | claude-fable-5-2 | max |
<!-- END GENERATED:catalog-frontier -->

## Specialist exceptions

Consider these disjoint exceptions only when their task evidence fits. They do not automatically expand a mode pool or authorize spending. Evidence types, limitations, and three conditional candidates are in [model fit and specialist evidence](references/model-fit.md).

<!-- BEGIN GENERATED:catalog-specialists -->
| Code | Exact model | Effort | Task exception | Access |
| --- | --- | --- | --- | --- |
| OH | claude-opus-5-5 | high | Agentic frontend and full-stack implementation | public_api |
| MWM | muse-wonder-1.0 | max | Website design and visual aesthetics | public_api_standard |
| MSX | muse-spark-1.3 | xhigh | Lower-cost website and UI generation | public_api_standard |
| SNMAX | claude-sonnet-5-5 | max | Professional deliverables and knowledge work | public_api |
| MFMAX | muse-wonder-full-1.0 | max | Orchestration and steerable prose trials | muse_code_subscription |
| KK31 | kimi-k3.1-pro | unspecified | Terminal-intensive engineering | public_api_or_self_hosted_weights |
| GA4H | gemini-4-argon | high | Visual reasoning and MCP tool use | public_api |
| DSFH | deepseek-flash | high | Budget workflow automation experiments | public_api_rolling_alias_or_self_hosted_weights |
| G38FH | gemini-3.8-flash | high | Audio understanding with text output | public_api |
<!-- END GENERATED:catalog-specialists -->

Kimi's benchmark does not specify effort. Its record is documentary until an explicit supported runtime effort is selected. Wonder Full is a Muse Code subscription model, not Wonder's public API. Verify the exact adapter, account, tools, effort, and effective data handling before dispatch. Unavailable routes fail without Codex/Claude substitution. Ordinary permissions remain independently configurable.

Existing exact profiles outside these catalogs remain available in [compatibility profiles](references/compatibility.md). They are not specialists merely because they are retained. Retired Fast codes, `fast`, `tokenburn`, and `CMAX` fail with explicit migration guidance. `hiq` was renamed to `amusing` and requires explicit reselection.

FM is a selective on-call comparison. FH is the preferred Fable reasoning/specification/review trial. FX is an explicit hardest long-running trial. FMAX is exceptional and on-call. These are task-fit proposals, not guaranteed effort rankings.

For selected FM/FH/FX/FMAX assignments only, read [Fable prompting](references/fable-prompting.md) before briefing or dispatch. Include relevant work-order guidance. Pool eligibility alone does not trigger this read.

For selected Muse work only, read [Muse provider checks](references/muse.md). Other provider references are optional until selecting that route.

In Claude Code with the agent-orch plugin, use design `claude-plugin` and read [Claude plugin dispatch](references/claude-plugin.md) before the first dispatch.

Optional: [configuration and generation](../../docs/configuration.md), [selection evidence](references/evidence.md). `config/routing.json`, followed by selected presets/overlays, is the source of generated tables. Regenerate installed Markdown when selecting an overlay so native instructions use the same bindings.
