# Council

Opt in for decision, architecture, or research tradeoffs through independent openings, shared critique, revision, and explicit consensus.

## Eligibility and membership

<!-- BEGIN GENERATED:pool:council -->
| Slot | Exact profile | Eligibility | Task fit |
| --- | --- | --- | --- |
| max-code | SMAX: gpt-6.1-sol / max | research, planning, qa, spec-review | Develop a decision proposal, test its assumptions, and compare concrete implementation tradeoffs. |
| opus-deep | OX: claude-opus-5-5 / xhigh | research, planning, qa, spec-review | Challenge architectural choices against requirements, source evidence, and simpler alternatives. |
| investigate-deep | MFX: muse-wonder-full-1.0 / xhigh | research, planning, qa, spec-review | Investigate competing hypotheses and identify evidence that distinguishes proposed approaches. |
| broad | AMAX: gpt-6-astra / max | research, planning, qa, spec-review | Add an optional fourth perspective on assumptions, alternatives, and decision criteria. |
| fable-review | FH: claude-fable-5-2 / high | research, planning, spec-review | Advise on requirements, overlooked constraints, and alternative hypotheses without an additional vote. |
<!-- END GENERATED:pool:council -->

Default required member slots: **max-code, opus-deep, investigate-deep**, with their exact active bindings. The bundled bindings are SMAX, OX, and MFX. The broad slot is optional. If added as a member, it must endorse. The fable-review slot advises without a vote unless explicitly appointed. Rebinding changes the model, not membership or voting authority.

Record required membership before openings. Five eligible profiles do not mean five members or concurrent workers. These task fits do not claim measured superiority.

Honor explicit user changes to membership, effort, and route. If a required member or route is unavailable, report an incomplete council and request an explicit alternate. Never substitute silently. The optional inspector resolves eligibility only, not membership, debate, or consensus. Role exceptions require an explicit profile and user authorization. Existing `--allow-out-of-pool` and `--role-override` controls record exceptions, not authority.

## Independent openings

Give every member the same neutral question, goals, non-goals, constraints, decision criteria, project instructions, research, documentation, and raw evidence. Include known alternatives and uncertainties without a preferred answer.

Use fresh opening contexts without the coordinator's preference, implementation chats, other members' answers, or prior verdicts. Check auto-loaded context and memory. Use session-scoped isolation rather than global changes. Disclose unresolved contamination instead of claiming independence.

Each member returns a proposal, tradeoffs, assumptions, strongest alternative, and evidence that would change its position. Collect every opening before revealing any opening to another member, even with sequential dispatch.

## Shared critique and revision

Exchange actual positions and supporting evidence, not just the coordinator's summary. Each member critiques the strongest competing arguments and answers material objections. Verify important factual claims through relevant non-mutating checks. Separate verified facts from assumptions and preferences.

Maintain a concise, versioned proposal/evidence/dispute ledger with source pointers, objections, responses, and unresolved dissent. Do not cherry-pick objections. Each member explicitly retains or revises its position with reasons.

Require openings, meaningful peer-response/revision, and separate final ratification. Additional deliberation rounds must address a material unresolved objection, new evidence, or a meaningful proposal change. Do not impose arbitrary round, turn, or time caps.

Later rounds intentionally share debate. Continue only a supported exact session, or send fresh contexts the complete decision-relevant debate packet, evidence, and proposal version. Fresh later sessions are not blind reviews.

## Ratification and stopping

Send each required member the identical final proposal version and evidence/assumption/tradeoff packet, including relevant debate. Withhold other members' final endorsements. Collect separate explicit endorsements or objections naming that version and any material concerns.

Consensus requires every required member to endorse the same final proposal and its evidence, assumptions, and tradeoffs without unresolved material objections. Majority votes, silence, and coordinator synthesis cannot replace endorsements. Agreement is not proof of objective truth.

Material changes invalidate affected ratifications. Redistribute the updated proposal to all required members and obtain same-version endorsements. Never combine mixed-version endorsements.

Stop at consensus, a configured budget/deadline, or a blocker. Also stop when no useful new information remains or an evidence-backed dispute stays unchanged. Do not coerce agreement. Without consensus, report dissent, missing members, verification limits, the last proposal version, and a discriminating experiment or needed user preference.

## Execute within existing authority

The active host coordinator owns the brief, ledger, proposal versions, and consensus record. Workers are bounded leaves, not additional dispatchers. Analysis does not authorize implementation, deployment, messages, purchases, commits, or publication. Those actions require separate task authority.

Use native workers for the host's provider with exact catalog model/effort and checked tools. For selected Claude work, load the installed Claude Delegation skill and its relevant launch reference. Use its configured permission/tool profile independently of review scope. Preserve authentication, owned-process, result-metadata, and lifecycle checks. For external Codex under Claude, use the optional [controller adapter](../../../docs/controller-designs.md).

For selected Muse work, read the provider checks linked from the entrypoint. Use a verified adapter, including a local CLI or configured durable adapter. Preserve exact MFX `xhigh`, account, privacy, effective permissions, owned-session, and result-metadata checks. Unless actual continuation is supported, use a fresh execution with the complete relevant debate packet. A reused session identifier alone does not establish continuation.

Preserve user-configured tools, permissions, approvals, and timeouts. Tool availability does not expand authority. Do not change accounts, global settings, or runtime capacity automatically.

Honor `max_parallel_workers` and `max_external_sessions_per_assignment` across descendants and all external providers, including Muse. Defaults are three workers and one active external session. Native workers consume worker capacity, not external slots. Sequential dispatch is valid. An idle persistent thread is not an active session.

Retain any configured Claude 60-minute assignment lifecycle unless overridden. Share remaining budgets across resumes and later rounds rather than resetting them. Council adds no cap. Prefer completion events, verify exact session ownership and result delivery, and report failures instead of endorsements.
