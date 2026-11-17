# Full profile catalog

## Standard frontier

All **19 raw-score nondominated configurations** from the November 17 four-provider Standard comparison of selected releases. Membership does not establish task fit, subscription cost, or dispatch availability.

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
| SL | gpt-6.2-sol | low |
| TH | gpt-6.1-terra | high |
| TX | gpt-6.1-terra | xhigh |
| SM | gpt-6.2-sol | medium |
| SH | gpt-6.2-sol | high |
| SX | gpt-6.2-sol | xhigh |
| SMAX | gpt-6.2-sol | max |
| AH | gpt-6.2-astra | high |
| AX | gpt-6.2-astra | xhigh |
| AMAX | gpt-6.2-astra | max |
| FX | claude-fable-5-2 | xhigh |
| FMAX | claude-fable-5-2 | max |
<!-- END GENERATED:catalog-frontier -->

## Specialist exceptions

These disjoint exceptions neither expand pools nor authorize spending. See [model fit and specialist evidence](model-fit.md) for evidence, limitations, and conditional candidates.

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

Kimi needs a supported runtime effort. Wonder Full uses Muse Code subscription, not Wonder's API. Verify adapter, account, tools, effort, and data handling. Unavailable routes fail without substitution except the Fable usage-cap fallback. Permissions remain independently configurable.

See [other exact profiles](compatibility.md) for models that modes and custom pools can use outside the benchmark frontier. Outside-pool selections require an explicit request. Retired Fast codes, `fast`, `tokenburn`, and `CMAX` fail with migration guidance. Retired `hiq` requires explicit `amusing` reselection.

Eligible Fable profiles may reason, implement, or review. Prefer FH for selective trials. FX/FMAX are optional higher-effort comparisons.

For dispatch gates, provider checks, and the conditional Fable fallback, follow [shared dispatch](dispatch.md).
