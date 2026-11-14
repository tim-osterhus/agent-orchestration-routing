# Routing policy compatibility note

The [router entrypoint](../SKILL.md) and its selected mode document contain the complete bundled routing instructions. Existing Claude companion links may land here; no additional policy read is needed after that pair.

For a burn assignment, retain the selected mode's account, endpoint, backlog, provider pool, and external-session ownership. Burn does not enable Orchestration or bypass.

For an explicit on-call trial outside the selected pool, select the exact catalog profile with user-authorized pool and role/lifecycle exceptions. The optional inspector records these as `--allow-out-of-pool --role-override`.

The invoked router preauthorizes the narrow [Fable usage-cap fallback](fable-prompting.md#automatic-usage-cap-fallback): FM→OH, FH→OX, FX→OMAX, FMAX→OMAX. Follow its trigger, terminal-run, permission, independent-review, diversity, and receipt rules. This exception overrides required-profile, outside-pool, no-alternate, and mapped Opus role/lifecycle fences only for explicit provider usage exhaustion. Continue the same authorized Fable role and lifecycle without expanding scope, permissions, or capabilities. Offline plans record mapped-role exceptions with `--role-override` even in-pool; add `--allow-out-of-pool` when needed. They do not execute retries.

FH can reason, implement, integrate, or review in Performance, Bulk, and Amusing without a role override. Council remains a decision-only workflow: FH advises unless explicitly appointed as a member. Required members default to SMAX/OX/MFX. FM, FX, and FMAX remain on-call outside bundled pools.

Other in-pool role/lifecycle exceptions require an explicit profile and user-authorized `--role-override`. Do not use standalone `--direct` calls to evade an active router.

Custom pools and the optional Opus/Haiku preset are documented in [configuration](../../../docs/configuration.md).
