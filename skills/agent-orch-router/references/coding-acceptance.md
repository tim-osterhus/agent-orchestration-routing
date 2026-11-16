# Coding acceptance

Read for code/documentation changes, implementation reviews, or commit/push/release delivery. Council deliberation and Frontier Research retain their own output and acceptance protocols.

## Proof

- Establish intended behavior, scope, and the relevant baseline. Identify the candidate by revision or scoped diff, including relevant untracked files.
- For bug fixes, reproduce the failure and rerun the same reproduction after fixing it when feasible. A focused regression test should detect the original defect. Explain removed or weakened coverage.
- Run existing affected and required project checks. For UI/runtime claims, exercise the actual application. Mocked tests or screenshots alone do not establish the complete user experience.
- Match proof to the change. Documentation may need link or generation checks, not an application launch. Report missing proof and pre-existing failures separately.
- Reuse verified worker evidence while its candidate, inputs, and assumptions remain valid. The coordinator checks provenance and coverage without automatically repeating every command.

Example: a revoked share must reject the next protected request. Hiding its button is not proof of revoked access.

## Reviewer output

For implementation reviews, use this compact form. UI-Pro adds its artifact, viewport, theme, state, and rubric fields.

```text
Candidate: <revision or scoped diff identity>
Verdict: APPROVE | CHANGES | BLOCKED
Checked: <checks or scenarios covered>
R1 [blocker|material|minor] <location>: <failure and impact>
Evidence: <source, reproduction, or check>
Correction: <smallest suitable change>
Unverified: <relevant gaps, or none>
```

Use finding lines only for actual findings. Classify severity by impact, credible reachability, and requirements, not frequency alone. A rare data-loss path can be material. Optional minor findings need not block approval. Unresolved material findings or missing required evidence prevent approval.

The coordinator retains stable finding IDs and accepted, rejected, resolved, or deferred outcomes with reasons. Corrections may use targeted verification. Continued checks are not fresh independent acceptance. Preserve the selected mode's final-review requirements and context isolation.

## Requested finish state

Finish at the requested state: verified changes, committed work, pushed work, or an explicitly requested release/deployment. Report the achieved state and remaining blockers. Verification alone grants no publication authority.

Before delivery, confirm accepted evidence covers the delivered candidate and no material issue remains unresolved. Inspect concurrent changes for invalidated assumptions, including shared interfaces beyond overlapping files. Repeat affected checks or reviews when necessary, not every check automatically.

Before an authorized commit/push, inspect the final diff, staging, and current branch/head. Include only owned changes and verify the resulting commit and requested remote update. Preserve unrelated staged work. Do not require a branch, worktree, rebase, or merge.

Before pushing, inspect the complete outgoing commit range against the intended remote. If it includes unauthorized work, stop before pushing and report.

Example: “verify only” leaves changes uncommitted. “Commit/push once green” includes publication after acceptance, not a new PR workflow.
