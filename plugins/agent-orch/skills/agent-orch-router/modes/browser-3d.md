# Browser-3D

Apply [shared dispatch](../references/dispatch.md).
Use for browser-based 3D scenes, games, viewers, simulations, and visualizations. Fable directs Codex production and verification. No engine, asset tool, or host is required.

## Controller

Use an existing Claude Code **FH: `claude-fable-5-2` / `high`** session unless explicitly overridden. Verify model/effort and report host mismatches. Mode selection never changes the running parent or starts another controller.

FH owns the brief, work orders, integration, and milestone acceptance. Delegate implementation, debugging, export, and routine checks. A focused controller-authored visual prototype may clarify the result. Finish it before dispatching writers, take a fresh ownership snapshot, then return production to Codex.

The controller is outside the worker pool. Do not launch another FH worker or native Claude implementation team by default. Other modes' worker fences do not restrict this controller.

## Ordered worker pool

<!-- BEGIN GENERATED:pool:browser-3d -->
| Slot | Exact profile | Eligibility | Task fit |
| --- | --- | --- | --- |
| standard | S62M: gpt-6.2-sol / medium | general | Implement conventional UI, interactions, asset manifests, automation, and tests. Also handle routine browser journeys and screenshot collection with verified tool access. |
| deep | S62H: gpt-6.2-sol / high | general | Build scene-generation and export pipelines, browser rendering, and asset integration. Diagnose performance problems while preserving the approved visual direction. |
| hard | S62X: gpt-6.2-sol / xhigh | general | Resolve difficult rendering, shader, transform, collision, or integration failures with interacting constraints. Return demonstrated causes and verified corrections. |
| max-code | S62MAX: gpt-6.2-sol / max | general | Handle exceptional engineering problems or independently review a complex candidate against functional and performance requirements. Use a fresh reviewer when this profile authored the work. |
| broad | A62MAX: gpt-6.2-astra / max | general | Create and refine geometry, materials, lighting, and spatial composition through the available 3D toolchain. Inspect actual browser output for visual fidelity and interaction defects, separately from authored work when reviewing. |
<!-- END GENERATED:pool:browser-3d -->

Choose by task fit, not an escalation ladder. S62M handles routine browser work. A62MAX handles demanding visuals. Verify tools and session access. Terra is outside this pool.

## Produce and inspect

Define the visual/interaction brief from project references, goals, and constraints. Record target devices, loading/runtime budgets, and acceptance evidence.

Resolve scale, camera, navigation, and rendering risks in an early blockout/prototype. Finish one browser slice before expanding assets. Compare real-time, pre-rendered, or hybrid views only when the product permits.

Keep editable sources and reproducible build/export steps. Separate asset-tool modules/assets for independent work. Give shared scene assembly, binary files, and exports one owner. Track third-party provenance and licenses.

Review the actual browser build against the brief with consistent camera, lighting, viewport, and quality settings. Check exported transforms, materials, lighting, animation, and interaction where applicable. Successful exports and offline renders do not prove browser fidelity.

Workers return build identity, screenshots/recordings, checks, measured performance, and defects. Fable prioritizes corrections and reviews milestones, not every log. Return unresolved choices rather than narrowing the brief.

Use a fresh independent reviewer for significant candidates. Supply the brief and raw evidence without the author's verdict. Verify affected checks after corrections. An author cannot be the sole acceptance check, including for controller-authored prototypes. Stop iteration when criteria pass, or report the blocker or exhausted configured budget without inventing a pass.

By default, `qa` and `spec-review` run read-only and review supplied evidence. For live builds, serving, or capture generation, use the writable `browser` role. Limit Write to declared capture, cache, and build-output paths, not source edits. Preserve any user-configured sandbox overrides.

## Execute

Use verified native host routes. With the plugin, select `claude-plugin` and pinned Codex agents under [plugin dispatch](../references/claude-plugin.md). Resume workers by exact thread ID. Without the plugin, select the [Claude-first adapter](../../../docs/controller-designs.md) (`--design claude-first`), not the Codex-first default. Never silently substitute accounts, profiles, or billing routes.

Under `claude-first`, Codex consumes worker/external capacity. Plugin relays are native.

S62H may integrate assigned components, not become another controller.

An explicitly authorized Claude worker is an out-of-pool exception, dispatched through the native Agent route on this Claude host. Under the plugin, use its pinned Claude agent. The installed Claude Delegation skill applies only from a Codex controller, not this FH host.

Use the designated build host and measure target browsers/devices. Resolve missing tools within task authority. Report unavailable measurements, not estimated passes. On quota exhaustion, save session IDs, artifacts, and next actions. Fable fallback covers delegated assignments, not replacement of this running FH parent. Never enable paid extra usage or promise resumption without authorization and a verified mechanism.
