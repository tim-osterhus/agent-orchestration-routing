# Routing policy compatibility note

The [router entrypoint](../SKILL.md) and its selected mode document contain the complete bundled routing instructions. Existing Claude companion links may land here; no additional policy read is needed after that pair.

For a burn assignment, retain the selected mode's account, endpoint, backlog, provider pool, and external-session ownership. Burn does not enable Orchestration or bypass.

For an explicit on-call trial outside the selected pool, select the exact catalog profile with user-authorized pool and role/lifecycle exceptions. The optional inspector records these as `--allow-out-of-pool --role-override`.

FH can reason, implement, integrate, or review in Performance, Bulk, and Amusing without a role override. Council remains a decision-only workflow: FH advises unless explicitly appointed as a member. Required members default to SMAX/OX/MFX. FM, FX, and FMAX remain on-call outside bundled pools.

Other in-pool role/lifecycle exceptions require an explicit profile and user-authorized `--role-override`. Do not use standalone `--direct` calls to evade an active router.

Custom pools and the optional Opus/Haiku preset are documented in [configuration](../../../docs/configuration.md).
