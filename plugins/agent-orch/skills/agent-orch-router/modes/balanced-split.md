# Balanced Split

Choose explicitly from either provider preference. Use this pool instead of provider-specific Balanced. Keep the current coordinator and route. Low favors economical fits. Default chooses the smallest suitable profile, accounting for likely rework. High favors deeper reasoning when justified. All biases use the same profiles and efforts.

Split High prefers available specialists for their listed jobs: AL for browser work, MFH for final artifact QA, and GNH for scoped diagnosis or fix critique. Choosing High opts in to GNH; select its exact profile or slot when the task fits. Do not add workers just to use the pool. Low and Default still require an explicit GNH request.

## Default jobs

<!-- BEGIN GENERATED:pool:balanced-split -->
| Slot | Exact profile | Eligibility | Task fit |
| --- | --- | --- | --- |
| routine | SL: gpt-6.2-sol / low | general | Mechanical edits. Apply a prescribed change, such as a rename, fixture update, or repeated pattern. Run focused checks. |
| standard | SM: gpt-6.2-sol / medium | general | Scoped feature build. Implement specified behavior in one component with clear ownership and acceptance checks. |
| browser | AL: gpt-6.2-astra / low | browser; specialist | Use for visual desktop control and browser interaction. Verify the required tools and session access before dispatch. Report missing capabilities rather than silently substituting another profile. |
| opus-medium | OM: claude-opus-5-5 / medium | general | Planned integration. Wire components together or carry out a migration or API adoption after the design is settled. |
| claude-review | OH: claude-opus-5-5 / high | general | Independent acceptance review. Check the candidate against the brief, test evidence, and unverified requirements. |
| deep | SX: gpt-6.2-sol / xhigh | general | Hard debugging. Reproduce the failure, distinguish competing causes, and verify a focused fix. |
| opus-deep | OX: claude-opus-5-5 / xhigh | general | Complex refactoring. Restructure tangled code across boundaries while preserving behavior and reducing maintenance burden. |
| adversarial-review | AH: gpt-6.2-astra / high | general | Adversarial technical verification. Challenge a high-stakes candidate with failure cases, cross-system invariants, and neglected assumptions. |
| fable | FH: claude-fable-5-2 / high | general | Architectural reframing. Compare materially different approaches and test the most consequential tradeoff with a bounded probe. |
| muse-artifact-review | MFH: muse-wonder-full-1.0 / high | qa; independent review; verified adapter; final review | Specialist final QA for copywriting, documentation, and UI design only. Review the final candidate against the brief. Use rendered evidence for UI design and report what remains unverified. |
| neon-diagnosis | GNH: gemini-4-neon / high | research, planning; verified adapter; explicit selection | Trace a scoped repository issue or critique a fix. Return source anchors and a check that distinguishes competing causes. |
<!-- END GENERATED:pool:balanced-split -->

The general jobs are routing defaults, not role restrictions or required stages. AH challenges the candidate. FH challenges the approach. Acceptance still requires a fresh, author-independent reviewer.

MFH is optional and only reviews its listed artifact types. It does not edit. For UI design, supply renders captured by AL or another verified route. Without renders, mark the visual result unverified. OH remains the general acceptance reviewer.

## Split the work

Aim for roughly even Codex and Claude workload across the backlog, not equal launches or subscription spend. Track estimated work by provider, including repeat work. Count MFH and GNH separately from Codex and Claude. Compare like-sized packets. Do not equate a quick review with a long implementation.

Start with the default profile for the job. When multiple eligible profiles fit equally well, prefer the provider with less substantive work. Let both providers own implementation where they fit. Accept temporary imbalance rather than forcing a second worker, expanding scope, or weakening review. Use [shared dispatch](../references/dispatch.md) for exact-profile overrides, unavailable routes, and provider guidance.
