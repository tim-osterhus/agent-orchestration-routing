# Muse provider checks

Read only when selecting MFH or MFX. Use an available provider adapter, including a configured durable adapter, only after checking its actual controls and lifecycle.

A read-only Muse 1.4.14 provider-catalog check on 2026-10-30 listed `muse-wonder-full-1.0` variants `minimal`, `low`, `medium`, `high`, `xhigh`, and `max`. Its reported default was `max`, not `high`. The catalog did not advertise `ultra`. The check sent no model turn and does not prove inference access. Configuration syntax validation does not verify model-specific efforts.

T3 Code's [versioned catalog adapter](https://github.com/pingdotgg/t3code/blob/v0.1.5/packages/provider-muse/src/server/modelCatalog.ts) derives reasoning choices from each model's advertised variants and default. Its [turn adapter](https://github.com/pingdotgg/t3code/blob/v0.1.5/packages/provider-muse/src/server/adapter.ts) reads and validates the selected `reasoningEffort` option. These sources describe adapter behavior, not universal model availability.

Before dispatch, verify the intended account route, exact model, requested effort, tools, and result metadata through the selected adapter. Set MFH to `high` and MFX to `xhigh` explicitly. Do not accept a default, fallback model, or unverified effort as an exact match. Stop if the adapter cannot establish the required route.

MFH/MFX default to investigation. Implementation is eligible when the work order authorizes edits. Reviewers do not author fixes without reassignment.

Permissions are independent of model and role. Honor the selected permission profile and verify its effective tools and controls through the adapter. No read-only or maximum-access profile is required. Tool access does not expand work-order authority.

Before sending private repository inputs, verify effective Contributor mode is off and confirm the route's data-handling terms permit the work. [Meta's subscription documentation](https://dev.meta.ai/docs/muse-code/subscriptions) describes training use when Contributor mode is on and host-specific saved settings. A catalog check does not establish this privacy setting. Contributor mode off does not establish zero retention. Do not change global settings without authorization. Stop confidential work if effective data handling remains unknown.

Keep credentials and private account, host, and session details out of public evidence. Use only authorized inputs and checks. Preserve configured permissions, concurrency, timeouts, cancellation ownership, and completion handling. Do not promise background continuation without a verified originating assignment and working completion mechanism.

The offline inspector labels Muse as `external-muse` with adapter-required metadata. The bundled launch planner rejects Muse instead of generating a Codex or Claude command. It does not implement a Muse launcher.
