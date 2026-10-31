# Routing policy compatibility note

The [router entrypoint](../SKILL.md) and its selected mode document contain the complete bundled routing instructions. Existing Claude companion links may land here; no additional policy read is needed after that pair.

For a burn assignment, retain the selected mode's account, endpoint, backlog, provider pool, and external-session ownership. Burn does not enable Orchestration or bypass.

For an explicit on-call trial, select the exact catalog profile with user-authorized pool and role/lifecycle exceptions. The optional inspector records these as `--allow-out-of-pool --role-override`. FH/FX remain outside automatic pools. Do not use standalone `--direct` calls to evade an active router.

Custom pools and the optional Opus/Haiku preset are documented in [configuration](../../../docs/configuration.md).
