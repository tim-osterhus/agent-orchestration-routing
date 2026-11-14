# UI-Pro

Opt in for UI improvement through independent critique, focused implementation, and fresh visual/functional evidence. Seven eligible profiles do not imply seven simultaneous workers.

## Ordered pool

<!-- BEGIN GENERATED:pool:ui-pro -->
| Slot | Exact profile | Eligibility | Task fit |
| --- | --- | --- | --- |
| browser | TM: gpt-6.1-terra / medium | browser; specialist | Capture screenshots and run interaction, keyboard, and focus checks with verified browser/computer-control tools. Record build, route, viewport, theme, and state. |
| visual-deep | TH: gpt-6.1-terra / high | research, planning, qa, spec-review | Diagnose concrete defects in baseline and intermediate screenshots. Return unresolved framing to the coordinator; this critique does not replace the final council. |
| standard | SM: gpt-6.1-sol / medium | implementation, frontend, integration | Own focused UI implementation in the project's existing design system and idioms. |
| opus-medium | OM: claude-opus-5-5 / medium | implementation, frontend, integration | Own substantial scoped UI implementation or refactoring across related components. |
| max-code | SMAX: gpt-6.1-sol / max | qa, spec-review; independent review | Review the final candidate independently against the requirements, rubric, and functional evidence. Fresh intermediate reviews are also eligible. |
| opus-deep | OX: claude-opus-5-5 / xhigh | qa, spec-review; independent review | Critique visual design, interaction, and rendering code from a separate model's perspective. Fresh intermediate reviews are also eligible. |
| investigate-deep | MFX: muse-wonder-full-1.0 / xhigh | qa, spec-review; independent review | Critique the candidate against existing components, tokens, and repository patterns. Fresh intermediate reviews are also eligible. |
<!-- END GENERATED:pool:ui-pro -->

The browser binding defaults to TM. Verify actual browser/computer-control tools and session access, not merely shell access. If unavailable, report visual/interaction acceptance as blocked. Do not silently substitute another model or shell-only capture route. Explicit user choices and configured bindings override defaults.

SM or OM implements. TH critiques baseline/intermediate evidence. SMAX, OX, and MFX form the final council and may give fresh intermediate reviews. Reviewers do not edit unless reassigned. These jobs are workflow choices, not measured model specialties.

## Independent review packets

Every independent review uses a fresh native worker or provider session. Do not fork or resume an author/reviewer conversation. Check auto-loaded memory and project context for prior verdicts. Use session-scoped isolation. Disclose unresolved contamination instead of claiming independence.

Give each reviewer the same neutral inputs:

- Requirements, product intent, acceptance criteria, and relevant project instructions.
- Existing design-system components, tokens, and patterns.
- Baseline/candidate revision or diff identity and build.
- Unannotated screenshots at matching route, viewport, theme, and UI state.
- Relevant raw functional/test evidence and the rubric below.

Exclude implementation chat, earlier findings, verdicts, scores, coordinator preferences, and target scores. Keep the coordinator's findings ledger outside normal reviewed-source browsing and instruct reviewers not to seek it. A filesystem location alone is not an access barrier. Sequential reviewers receive the same neutral packet without earlier replies.

A targeted check may name a known defect. Label it verification, not an independent review or vote. If a relevant installed frontend-design skill is supplied, give the same pointer to all council members. Do not require a separate design skill.

## Rubric and iteration

Review task clarity, hierarchy, typography/readability, spacing/density, contrast/color, interaction states, and design-system consistency. Report each finding with artifact/location, viewport/theme/state, severity, evidence, and a concrete correction. Name uninspected states.

Blockers prevent or mislead the intended task or fail an applicable accessibility requirement. Material findings substantially impair use or consistency. Separate these from minor, optional, or out-of-scope suggestions. Scores, if used, are advisory. Do not chase a numeric target.

1. Capture representative baseline evidence and agree on criteria.
2. Obtain fresh independent critique of the baseline or current candidate.
3. Let the coordinator verify, deduplicate, and prioritize material findings.
4. Assign focused implementation with disjoint surface ownership and one owner for shared tokens, styles, or components.
5. Capture fresh screenshots and functional evidence for the exact updated revision.
6. Repeat while new actionable findings justify changes, then run the final council.

Review an existing candidate when supplied. Do not reimplement it to create review work. Distinguish capture, viewport, build, and evaluator failures from UI defects before redesigning. Keep criteria stable unless requirements or evidence change. If product and evaluator changes obscure a failure, check the corrected evaluator against unchanged product behavior.

Keep a concise coordinator-owned findings ledger, including accepted/rejected findings and reasons. Reopen settled findings only for relevant changes or new material evidence. Keep prior verdicts out of fresh review packets. Intermediate rounds may use TH or any council profile in a fresh context. Staging does not remove the final council.

## Final council and acceptance

Required default members are the max-code, opus-deep, and investigate-deep bindings: **SMAX, OX, MFX**. Each reviews the identical final revision/build independently in a fresh context. Record that identity in every packet and confirm each reply names it. Withhold council findings and verdicts until all assigned members return.

Run sequentially when concurrency or external-session limits require it. If a required member/route is unavailable, report an incomplete council and request an explicit alternate. Do not substitute silently, count several sessions of one model as model diversity, or claim consensus from a partial council.

Resolve disagreements through artifact inspection, interaction checks, and the user's requirements or taste. Majority vote alone is insufficient. Ask the user only when a material preference cannot be resolved from the requirements.

Acceptance also requires same-build evidence of:

- The intended journey working end to end.
- Supported viewport sizes and light/dark themes where applicable.
- Keyboard operation, visible focus, and applicable contrast/accessibility checks.
- Relevant regression checks.

A screenshot alone does not prove usability or accessibility. Material design/behavior changes require fresh evidence and council review for affected surfaces. Unrelated text changes need updated-build verification, not an automatic full rerun. Report the reviewed build and verification of later changes.

Stop when material findings are resolved and final evidence is accepted, at a user/project budget or deadline, or when rounds stop yielding useful improvements. Report remaining issues and missing evidence. UI-Pro imposes no new time, turn, or round cap and does not authorize publication, deployment, or merging.

## Execution

Use native workers for the host provider with exact model/effort and verified tools. The installed Claude Delegation skill supplies external Claude launch mechanics. Keep review authority separate from permissions: full tool access does not authorize edits. Use configured tools/approvals. If required checks need a broader profile, obtain that selection rather than silently widening access. The optional planner accepts `--claude-mode implementation` for a full-tool, review-scoped Claude launch. Its name does not authorize product edits. Verify session-scoped memory/context isolation separately before calling any review independent.

For MFX use the Muse checks linked from the entrypoint and a verified Muse Code subscription adapter, never Wonder's API. Preserve exact effort, data handling, selected local/remote route, result metadata, and owned-session lifecycle. If the route fails, do not switch silently. The bundled planner does not launch Muse.

The host coordinator owns the brief, ledger, integration, and acceptance. Claude helpers stay within permissions/tools/pool/scope/roles. Pass fences, limits, and allocated capacity to descendants. Native Codex workers remain leaves unless assigned team roles. External workers cannot recursively launch opposite controllers. Helpers add no votes or diversity. Preserve permissions, positive worker/external-session caps, shared deadlines, cancellation, and completion handling. No default router ceiling applies. Honor runtime/provider/project and explicit assignment limits. Idle threads consume no active capacity. UI-Pro adds no capacity, accounts, global changes, or mandatory worktrees.
