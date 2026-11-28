---
name: agent-orch-router
description: Explicit-only routing for delegated work through exact model/effort profiles, stable job slots, and role-aware mode pools. Catalog discovery does not establish an available provider adapter.
---

# Agent Orchestration Router

Activate only by explicit invocation. Default: **codex-primary / balanced / default bias, pure orchestration**. Read [shared dispatch](references/dispatch.md) once and **only the selected mode**:

| Variant | Efficient | Balanced | Performance |
| --- | --- | --- | --- |
| codex-primary | [Efficient](modes/codex-primary-efficient.md) | [Balanced](modes/codex-primary-balanced.md) | [Performance](modes/codex-primary-performance.md) · [Bulk](modes/codex-primary-bulk.md) |
| claude-primary | [Efficient](modes/claude-primary-efficient.md) | [Balanced](modes/claude-primary-balanced.md) | [Performance](modes/claude-primary-performance.md) |

Both variants: [Balanced Split](modes/balanced-split.md) · [Amusing](modes/amusing.md) · [UI-Pro](modes/ui-pro.md) · [Council](modes/council.md) [Max](modes/council-max.md) · [Frontier Research](modes/frontier-research.md) · [Browser-3D](modes/browser-3d.md) · [Codex-burn](modes/codex-burn.md) · [Claude-burn](modes/claude-burn.md).

## Exact profile index

Efforts: l=low, m=medium, h=high, x=xhigh, max=max. Catalog entries do not grant mode eligibility.

| Exact model | Frontier aliases → efforts |
| --- | --- |
| gpt-6-luna | LL/LM → l/m |
| claude-haiku-5-5 | HL → l |
| gpt-6.1-terra | TL/TM/TH/TX → l/m/h/x |
| muse-ember-1.0 | EX/EMAX → x/max |
| gpt-6.2-sol | SL/SM/SH/SX/SMAX → l/m/h/x/max |
| gpt-6.2-astra | AH/AX/AMAX → h/x/max |
| claude-fable-5-2 | FX/FMAX → x/max |

| Exact model | Specialist alias → effort |
| --- | --- |
| claude-opus-5-5 | OH → h |
| muse-wonder-1.0 | MWM → max |
| muse-spark-1.3 | MSX → x |
| claude-sonnet-5-5 | SNMAX → max |
| muse-wonder-full-1.0 | MFMAX → max |
| kimi-k3.1-pro | KK31 → unspecified |
| gemini-4-argon | GA4H → h |
| gemini-4-neon | GNH/GNX → h/x |
| deepseek-flash | DSFH → h |
| gemini-3.8-flash | G38FH → h |

For specialty/access gates, compatibility profiles, or retired aliases, read [full catalog](references/catalog.md). For selection rationale read [model fit](references/model-fit.md).

Optional: [configuration/generation](../../docs/configuration.md), [selection evidence](references/evidence.md). Generate tables from `config/routing.json` plus presets/overlays. Native instructions must match bindings.
