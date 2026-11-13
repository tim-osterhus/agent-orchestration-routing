# Model benchmark snapshot

Source: **Artificial Analysis**. Accessed **2026-11-13**; **Artificial Analysis Intelligence Index v5.0.1**.

Customization reference only. Deliberately not linked from the router entrypoint or modes; reading it is not part of normal dispatch. This snapshot does not add supported profiles or change routing.

## Reading the tables

Each linked cell is **Artificial Analysis Intelligence Index / Cost per Intelligence Index Task (USD)**, at AA’s displayed precision. Cost/task is AA’s weighted evaluation cost, including applicable input, cache, reasoning, and answer token charges—not price per million tokens or subscription consumption. Links open the exact measured configuration; the model’s default effort is not inferred from an unsuffixed URL.

`—` means no published entry captured here, **not** an unsupported effort. Within a linked cell, `—` means that particular measurement is unavailable. The fixed/non-reasoning column includes models with no effort label. Integer scores are rounded: do not use ties here to assert an exact Pareto frontier.

Scope: selected current general-purpose, reasoning, and budget families from OpenAI, Anthropic, Google, and Meta; latest release per listed family, not a complete inventory of these labs or AA’s database. Spark 1.3 is retained as a labeled legacy comparison. Media-only models and historical predecessors are omitted.

## OpenAI

Artificial Analysis Intelligence Index **v5.0.1** / Cost per Intelligence Index Task **USD** · **2026-11-13** · Source: **Artificial Analysis**

| Model release | Fixed / non-reasoning | Low | Medium | High | XHigh | Max |
| --- | --- | --- | --- | --- | --- | --- |
| GPT-6 Luna | [9 / $0.0714](https://artificialanalysis.ai/models/gpt-6-luna-non-reasoning) | [10 / $0.0051](https://artificialanalysis.ai/models/gpt-6-luna-low) | [18 / $0.0422](https://artificialanalysis.ai/models/gpt-6-luna-medium) | [21 / $0.0729](https://artificialanalysis.ai/models/gpt-6-luna-high) | [23 / $0.10](https://artificialanalysis.ai/models/gpt-6-luna-xhigh) | [28 / $0.15](https://artificialanalysis.ai/models/gpt-6-luna) |
| GPT-6.1 Terra | [31 / $0.23](https://artificialanalysis.ai/models/gpt-6-1-terra-non-reasoning) | [29 / $0.0713](https://artificialanalysis.ai/models/gpt-6-1-terra-low) | [38 / $0.17](https://artificialanalysis.ai/models/gpt-6-1-terra-medium) | [42 / $0.26](https://artificialanalysis.ai/models/gpt-6-1-terra-high) | [45 / $0.40](https://artificialanalysis.ai/models/gpt-6-1-terra-xhigh) | [51 / $0.96](https://artificialanalysis.ai/models/gpt-6-1-terra) |
| GPT-6.1 Sol | — | [35 / $0.16](https://artificialanalysis.ai/models/gpt-6-1-sol-low) | [46 / $0.36](https://artificialanalysis.ai/models/gpt-6-1-sol-medium) | [50 / $0.59](https://artificialanalysis.ai/models/gpt-6-1-sol-high) | [52 / $0.76](https://artificialanalysis.ai/models/gpt-6-1-sol-xhigh) | [55 / $1.27](https://artificialanalysis.ai/models/gpt-6-1-sol) |
| GPT-6 Astra | — | [43 / $1.42](https://artificialanalysis.ai/models/gpt-6-astra-low) | [52 / $2.73](https://artificialanalysis.ai/models/gpt-6-astra-medium) | [55 / $3.24](https://artificialanalysis.ai/models/gpt-6-astra-high) | [55 / $3.66](https://artificialanalysis.ai/models/gpt-6-astra-xhigh) | [57 / $6.24](https://artificialanalysis.ai/models/gpt-6-astra) |

## Anthropic

Artificial Analysis Intelligence Index **v5.0.1** / Cost per Intelligence Index Task **USD** · **2026-11-13** · Source: **Artificial Analysis**

| Model release | Fixed / non-reasoning | Low | Medium | High | XHigh | Max |
| --- | --- | --- | --- | --- | --- | --- |
| Claude Haiku 5.5 | — | [19 / $0.0438](https://artificialanalysis.ai/models/claude-haiku-5-5-low) | [25 / $0.0918](https://artificialanalysis.ai/models/claude-haiku-5-5-medium) | [30 / $0.16](https://artificialanalysis.ai/models/claude-haiku-5-5-high) | [35 / $0.25](https://artificialanalysis.ai/models/claude-haiku-5-5-xhigh) | [36 / $0.41](https://artificialanalysis.ai/models/claude-haiku-5-5) |
| Claude Sonnet 5.5 | — | [26 / $0.51](https://artificialanalysis.ai/models/claude-sonnet-5-5-low) | [31 / $0.78](https://artificialanalysis.ai/models/claude-sonnet-5-5-medium) | [42 / $1.64](https://artificialanalysis.ai/models/claude-sonnet-5-5-high) | [50 / $4.09](https://artificialanalysis.ai/models/claude-sonnet-5-5-xhigh) | [55 / $10.02](https://artificialanalysis.ai/models/claude-sonnet-5-5) |
| Claude Opus 5.5 | — | [35 / $0.98](https://artificialanalysis.ai/models/claude-opus-5-5-low) | [48 / $2.45](https://artificialanalysis.ai/models/claude-opus-5-5-medium) | [52 / $3.46](https://artificialanalysis.ai/models/claude-opus-5-5-high) | [57 / $6.05](https://artificialanalysis.ai/models/claude-opus-5-5-xhigh) | [59 / $10.04](https://artificialanalysis.ai/models/claude-opus-5-5) |
| Claude Fable 5.2 | — | [54 / $3.10](https://artificialanalysis.ai/models/claude-fable-5-2-low) | [56 / $3.80](https://artificialanalysis.ai/models/claude-fable-5-2-medium) | [62 / $9.08](https://artificialanalysis.ai/models/claude-fable-5-2-high) | [62 / $14.83](https://artificialanalysis.ai/models/claude-fable-5-2-xhigh) | [65 / $26.54](https://artificialanalysis.ai/models/claude-fable-5-2) |

Sonnet, Opus, and Fable results use AA’s **Default Fallback** configuration. Haiku’s published labels do not include that qualifier. These are measured harness configurations, not promises about every CLI or provider route.

## Google

Artificial Analysis Intelligence Index **v5.0.1** / Cost per Intelligence Index Task **USD** · **2026-11-13** · Source: **Artificial Analysis**

| Model release | Fixed / non-reasoning | Low | Medium | High | XHigh | Max |
| --- | --- | --- | --- | --- | --- | --- |
| Gemini 3.5 Flash-Lite | [12 / $0.69](https://artificialanalysis.ai/models/gemini-3-5-flash-lite) | — | — | — | — | — |
| Gemini 3.8 Flash | — | [23 / —](https://artificialanalysis.ai/models/gemini-3-8-flash-low) | [30 / $6.26](https://artificialanalysis.ai/models/gemini-3-8-flash-medium) | [31 / $7.77](https://artificialanalysis.ai/models/gemini-3-8-flash) | — | — |
| Gemini 4 Hydrogen | — | [27 / $0.29](https://artificialanalysis.ai/models/gemini-4-hydrogen-low) | [41 / $0.80](https://artificialanalysis.ai/models/gemini-4-hydrogen-medium) | [51 / $1.87](https://artificialanalysis.ai/models/gemini-4-hydrogen-high) | [54 / $3.16](https://artificialanalysis.ai/models/gemini-4-hydrogen) | — |
| Gemini 4 Argon | — | — | — | [50 / $4.97](https://artificialanalysis.ai/models/gemini-4-argon) | — | — |
| Gemini 4 Carbon | — | [54 / $5.22](https://artificialanalysis.ai/models/gemini-4-carbon-low) | [58 / $4.68](https://artificialanalysis.ai/models/gemini-4-carbon-medium) | [60 / $5.48](https://artificialanalysis.ai/models/gemini-4-carbon) | — | — |

## Meta

Artificial Analysis Intelligence Index **v5.0.1** / Cost per Intelligence Index Task **USD** · **2026-11-13** · Source: **Artificial Analysis**

| Model release | Fixed / non-reasoning | Low | Medium | High | XHigh | Max |
| --- | --- | --- | --- | --- | --- | --- |
| Muse Ember | — | — | — | — | [34 / $0.12](https://artificialanalysis.ai/models/muse-ember-xhigh) | [36 / $0.14](https://artificialanalysis.ai/models/muse-ember) |
| Muse Spark 1.3 (AA-deprecated) | — | — | — | — | [— / —](https://artificialanalysis.ai/models/muse-spark-1-3-xhigh) | [37 / $2.39](https://artificialanalysis.ai/models/muse-spark-1-3) |
| Muse Spark Open | — | — | — | — | [25 / $2.02](https://artificialanalysis.ai/models/muse-spark-open) | — |
| Muse Wonder | — | — | — | [41 / $4.56](https://artificialanalysis.ai/models/muse-wonder-high) | — | [44 / $6.95](https://artificialanalysis.ai/models/muse-wonder) |
| Muse Wonder Full | — | — | — | — | — | [50 / —](https://artificialanalysis.ai/models/muse-wonder-full) |
| Muse Glimmer | — | — | — | [6 / $0.17](https://artificialanalysis.ai/models/muse-glimmer) | — | — |

AA labels Spark 1.3 deprecated and points to Wonder; [Meta’s model guide](https://dev.meta.ai/docs/choose-a-model) still lists `muse-spark-1.3` as its recommended Spark ID. Do not substitute the old v4.3 XHigh score into this v5.0.1 table. Wonder Full has no published API cost/task; it is a Muse Code-only variant in Meta’s guide. Ember and Wonder refer to the releases whose API IDs are `muse-ember-1.0` and `muse-wonder-1.0`.

## Updating

- Check AA’s [release list](https://artificialanalysis.ai/models/releases) for successors; open each selected effort’s model page. Keep provider, fallback, and effort qualifiers intact.
- Record the access date and full index version together. Replace a version’s comparison as a unit rather than mixing scores from different index versions; retain missing measurements as missing.
- Copy the published score and **cost/task**, not the blended token-price column on release tables. Do not infer additional precision, scores, or API costs.
- Keep this reference unlinked from normal routing. Updating it does not automatically change the master catalog or any mode.

## Source and reuse

This is a dated, attributed comparison of selected published figures, not a Free API export or a dataset feed. AA’s [citation guidelines](https://artificialanalysis.ai/brand-kit) distinguish citing scores and rebuilding attributed charts from bulk redistribution of its underlying dataset. Preserve AA attribution, metric names, configuration labels, dates, versions, and source links when reusing this table.
