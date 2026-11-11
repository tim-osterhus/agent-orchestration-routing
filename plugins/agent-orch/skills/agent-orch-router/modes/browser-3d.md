# Browser-3D

Use for browser-based 3D experiences: interactive scenes, games, product viewers, simulations, and visualizations. Fable directs the work. Codex workers perform most production and verification. The mode does not require a particular scene, engine, asset tool, or host machine.

## Controller

Run in an existing Claude Code session using **FH: `claude-fable-5-2` / `high`**, unless the user explicitly selects another controller. Verify the actual model and effort. Selecting this mode never changes the running parent or starts a second controller. Report a host mismatch before dispatch.

FH owns the visual brief, work orders, integration decisions, and milestone acceptance. Delegate implementation, debugging, export, and routine checks. This mode permits a focused controller-authored visual prototype when direct work would clarify the intended result. Finish the prototype before dispatching writers and take a fresh ownership snapshot. Hand production work back to Codex afterward.

The controller is not a delegated worker-pool entry. Do not launch another FH worker or a native Claude implementation team by default. Fable's bounded-review fences in other modes do not restrict this controller.

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

Choose by task fit, not a mandatory escalation ladder. SM handles routine browser work. AMAX handles demanding visual production and inspection. Verify actual tools and session access before either assignment. No Terra profiles belong to this pool.

## Produce and inspect

Define the visual and interaction brief from the project's references, goals, and constraints. Record target devices, loading and runtime budgets, and the evidence needed for acceptance. Keep these choices project-specific.

Resolve scale, camera, navigation, and major rendering risks in an early blockout or prototype. Finish one representative browser slice before expanding asset production. Compare real-time rendering, pre-rendered views, or a hybrid only when the product permits those choices.

Keep editable sources and reproducible build/export steps. When using Blender or another asset tool, separate source modules and assets for independent work. Give shared scene assembly, binary project files, and export outputs one owner. Track third-party asset provenance and licenses.

Review the actual browser build against the brief. Use consistent cameras, lighting states, viewport, and quality settings for comparisons. Check exported transforms, materials, lighting, animation, and interaction where applicable. A successful export or attractive offline render is not proof of browser fidelity.

Workers return a compact evidence packet: build identity, screenshots or recordings, check results, measured performance, and remaining defects. Fable ranks corrections by visual or functional impact and reviews meaningful milestones, not every build log. Return unresolved design choices to Fable rather than narrowing the brief.

Use a fresh independent reviewer for significant candidates. Supply the brief and raw evidence without the author's verdict. Verify affected checks after corrections. An author cannot be the sole acceptance check, including for controller-authored prototypes. Stop iteration when criteria pass, or report the blocker or exhausted configured budget without inventing a pass.

By default, `qa` and `spec-review` run read-only and review supplied evidence. For live builds, serving, or capture generation, use the writable `browser` role. Limit Write to declared capture, cache, and build-output paths, not source edits. Preserve any user-configured sandbox overrides.

## Execute

Use native workers through the verified host route. With the Claude plugin, select design `claude-plugin` and use pinned Codex agents under the existing [plugin dispatch](../references/claude-plugin.md) contract. Resume continuing workers by exact thread ID. Without the plugin, explicitly select the [Claude-first controller adapter](../../../docs/controller-designs.md) (`--design claude-first`), not the repository's Codex-first default. Never silently substitute accounts, profiles, or billing routes.

Default limits are three parallel workers and one parent-owned active external session across descendants. Under `claude-first`, every Codex worker counts against both limits, so default to one active Codex session. Under `claude-plugin`, Codex relays count as native workers. Honor configured overrides and stricter host limits.

Give each worker the objective, references, disjoint write ownership, and acceptance checks. Sequence dependent or overlapping changes. Workers remain leaves. SH may integrate assigned components but does not become another controller. Keep existing configured concurrency and lifecycle controls.

An explicitly authorized Claude worker is an out-of-pool exception, dispatched through the native Agent route on this Claude host. Under the plugin, use its pinned Claude agent. The installed Claude Delegation skill applies only from a Codex controller, not this FH host. Preserve user-selected tools, permissions, approvals, and timeouts independently of routing.

Run tools on the designated build host and measure the intended browser/device targets. Resolve missing tool dependencies within task authority. Report unavailable device measurements rather than estimating passes. On quota exhaustion, save session IDs, artifacts, and the next action. Do not enable paid extra usage, switch providers, or promise automatic resumption without authorization and a verified mechanism.
