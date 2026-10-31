---
name: agent-orch-router
description: Explicit-only routing for delegated work across Codex, Claude Code, and configured Muse adapters. Select exact model/effort profiles from ordered, role-aware mode pools.
---

# Agent Orchestration Router

Activate only on explicit invocation for this assignment. Default to **codex-primary / balanced / default bias** and **pure orchestration**: delegate substantive work, then integrate and accept results. Use supporting delegation when requested. Retain these choices through compaction.

Read this file and **only the selected mode document**:

| Variant | Efficient | Balanced | Performance |
| --- | --- | --- | --- |
| codex-primary | [Efficient](modes/codex-primary-efficient.md) | [Balanced](modes/codex-primary-balanced.md) | [Performance](modes/codex-primary-performance.md) |
| claude-primary | [Efficient](modes/claude-primary-efficient.md) | [Balanced](modes/claude-primary-balanced.md) | [Performance](modes/claude-primary-performance.md) |

Shared across variants: [High-qual](modes/high-qual.md) · [Codex-burn](modes/codex-burn.md) · [Claude-burn](modes/claude-burn.md).

Variant selects pool preference, not the running host. Never change the parent model. Shorthand selects the exact model and effort below, not an automatic pool exception. Retired Fast codes, `fast`, `tokenburn`, and `CMAX` fail without substitution.

## Exact catalog

| Code | Model | Effort |
| --- | --- | --- |
| LM | gpt-6-luna | medium |
| L | gpt-6-luna | max |
| TL | gpt-6.1-terra | low |
| TM | gpt-6.1-terra | medium |
| TH | gpt-6.1-terra | high |
| SL | gpt-6.1-sol | low |
| SM | gpt-6.1-sol | medium |
| SH | gpt-6.1-sol | high |
| SX | gpt-6.1-sol | xhigh |
| SMAX | gpt-6.1-sol | max |
| AL | gpt-6-astra | low |
| AM | gpt-6-astra | medium |
| AH | gpt-6-astra | high |
| AX | gpt-6-astra | xhigh |
| AMAX | gpt-6-astra | max |
| AU | gpt-6-astra | ultra |
| HMED | claude-haiku-5-5 | medium |
| HH | claude-haiku-5-5 | high |
| HM | claude-haiku-5-5 | xhigh |
| HK | claude-haiku-5-5 | xhigh |
| HMAX | claude-haiku-5-5 | max |
| SNH | claude-sonnet-5-5 | high |
| SNX | claude-sonnet-5-5 | xhigh |
| OM | claude-opus-5-5 | medium |
| OH | claude-opus-5-5 | high |
| OX | claude-opus-5-5 | xhigh |
| OMAX | claude-opus-5-5 | max |
| FH | claude-fable-5-1 | high |
| FX | claude-fable-5-1 | xhigh |
| MFH | muse-wonder-full-1.0 | high |
| MFX | muse-wonder-full-1.0 | xhigh |

Codex profiles target Standard tier. HK has a soft 100K context target. HM does not. Catalog entries outside the selected pool are on-call only. FH/FX are opt-in trials for prose, UI copy, alternative hypotheses, or security-sensitive implementation, not proven specialist advantages. High-qual additionally permits selective FX specification review.

For selected Muse work only, read [Muse provider checks](references/muse.md). Exact catalog entries do not establish account access or an available dispatcher.

Optional: [configuration and installation](../../docs/configuration.md), [selection evidence](references/evidence.md). Neither is required for ordinary routing. Custom configuration or the Opus/Haiku preset applies only when selected.
