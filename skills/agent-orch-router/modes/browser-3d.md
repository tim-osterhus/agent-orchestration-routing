# Browser-3D

Use for browser-based 3D scenes, games, viewers, simulations, and visualizations. Fable directs Codex production and verification. No engine, asset tool, or host is required.

## Controller

Use an existing Claude Code **FH: `claude-fable-5-2` / `high`** session unless explicitly overridden. Verify model/effort and report host mismatches. Mode selection never changes the running parent or starts another controller.

FH owns the visual brief, work orders, integration decisions, and milestone acceptance. Delegate implementation, debugging, export, and routine checks. This mode permits a focused controller-authored visual prototype when direct work would clarify the intended result. Finish the prototype before dispatching writers and take a fresh ownership snapshot. Hand production work back to Codex afterward.

The controller is not a delegated worker-pool entry. Do not launch another FH worker or a native Claude implementation team by default. Worker assignments in other modes do not restrict this controller.

## Ordered worker pool

<!-- BEGIN GENERATED:pool:browser-3d -->
| Slot | Exact profile | Eligibility | Task fit |
| --- | --- | --- | --- |
| standard | SM: gpt-6.1-sol / medium | general | Implement conventional UI, interactions, asset manifests, automation, and tests. Also handle routine browser journeys and screenshot collection with verified tool access. |
| deep | SH: gpt-6.1-sol / high | general | Build scene-generation and export pipelines, browser rendering, and asset integration. Diagnose performance problems while preserving the approved visual direction. |
| hard | SX: gpt-6.1-sol / xhigh | general | Resolve difficult rendering, shader, transform, collision, or integration failures with interacting constraints. Return demonstrated causes and verified corrections. |
| max-code | SMAX: gpt-6.1-sol / max | general | Handle exceptional engineering problems or independently review a complex candidate against functional and performance requirements. Use a fresh reviewer when this profile authored the work. |
| broad | AMAX: gpt-6-astra / max | general | Create and refine geometry, materials, lighting, and spatial composition through the available 3D toolchain. Inspect actual browser output for visual fidelity and interaction defects, separately from authored work when reviewing. |
<!-- END GENERATED:pool:browser-3d -->

Choose by task fit, not an escalation ladder. SM handles routine browser work. AMAX handles demanding visuals. Verify tools and session access. Terra is outside this pool.

## Produce and inspect

Define the visual/interaction brief from project references, goals, and constraints. Record target devices, loading/runtime budgets, and acceptance evidence.

Resolve scale, camera, navigation, and major rendering risks in an early blockout or prototype. Finish one representative browser slice before expanding asset production. Compare real-time rendering, pre-rendered views, or a hybrid only when the product permits those choices.

Keep editable sources and reproducible build/export steps. When using Blender or another asset tool, separate source modules and assets for independent work. Give shared scene assembly, binary project files, and export outputs one owner. Track third-party asset provenance and licenses.

Review the actual browser build against the brief. Use consistent cameras, lighting states, viewport, and quality settings for comparisons. Check exported transforms, materials, lighting, animation, and interaction where applicable. A successful export or attractive offline render is not proof of browser fidelity.

Workers return build identity, screenshots/recordings, checks, measured performance, and defects. Fable ranks corrections by impact and reviews milestones, not every build log. Return unresolved design choices rather than narrowing the brief.

Use a fresh independent reviewer for significant candidates. Supply the brief and raw evidence without the author's verdict. Verify affected checks after corrections. An author cannot be the sole acceptance check, including for controller-authored prototypes. Stop iteration when criteria pass, or report the blocker or exhausted configured budget without inventing a pass.

By default, `qa` and `spec-review` run read-only and review supplied evidence. For live builds, serving, or capture generation, use the writable `browser` role. Limit Write to declared capture, cache, and build-output paths, not source edits. Preserve any user-configured sandbox overrides.

## Execute

Use native workers through the verified host route. With the Claude plugin, select design `claude-plugin` and use pinned Codex agents under the existing [plugin dispatch](../references/claude-plugin.md) contract. Resume continuing workers by exact thread ID. Without the plugin, explicitly select the [Claude-first controller adapter](../../../docs/controller-designs.md) (`--design claude-first`), not the repository's Codex-first default. Never silently substitute accounts, profiles, or billing routes.

Honor runtime/provider/project and positive configured limits, without default router ceilings. Pass fences, limits, and allocated capacity to descendants. Under `claude-first`, Codex consumes worker/external capacity; plugin relays are native. Native Codex workers remain leaves unless assigned team roles. Claude helpers stay within permissions/tools/pool/scope/roles. External workers cannot recursively launch opposite controllers.

Give workers objectives, references, disjoint write ownership, and acceptance checks. Sequence dependent or overlapping changes. Codex workers remain leaves. SH may integrate assigned components, not become another controller. Preserve configured concurrency and lifecycle controls.

An explicitly authorized Claude worker is an out-of-pool exception, dispatched through the native Agent route on this Claude host. Under the plugin, use its pinned Claude agent. The installed Claude Delegation skill applies only from a Codex controller, not this FH host. Preserve user-selected tools, permissions, approvals, and timeouts independently of routing.

Run tools on the designated build host and measure intended browser/device targets. Resolve missing tools within task authority. Report unavailable measurements, not estimated passes. On quota exhaustion, save session IDs, artifacts, and next actions. The entrypoint's Fable fallback covers owned delegated assignments, not automatic replacement of this running FH parent. Do not enable paid extra usage or promise resumption without authorization and a verified mechanism.
