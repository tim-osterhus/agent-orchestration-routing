# Configuration and installation

Python 3.10+ is required for offline inspection. Dispatch requires the selected host, native subagent support, and an already authorized CLI account. No API key is required by these scripts because they never call a model.

## Install only what you use

Retain this checkout as the canonical source. Expose `skills/agent-orch-router` and optionally `skills/claude-delegation` through your host's skill installation mechanism. Codex discovers user skills under `~/.agents/skills`; Claude Code supports `.claude/skills` for project-local skills. Use directory links to the source folders where supported. On Windows, use a directory junction or the host's installer rather than copying only a link file.

Ordinary native routing reads only `agent-orch-router/SKILL.md` and one selected `modes/*.md` file. Copying that skill folder intact supports this path. Keep the full checkout for optional configuration, offline scripts, controller adapters, or the Claude companion, whose external tooling uses shared files. Do not overwrite an existing installation without reviewing it. This package does not install itself or modify global settings.

For Claude Code, invoke the router explicitly and do not add it to always-loaded instructions. This package does not silently create Claude-specific frontmatter or preload the skill. Set `disable-model-invocation: true` in a host-specific installed copy if automatic Claude invocation must be technically disabled. Codex's `agents/openai.yaml` already keeps both skills explicit-only.

## Editable controls

`config/routing.json` drives the optional offline inspector and external CLI plans. Its bundled catalog and pools match the router's Markdown tables. When editing bundled defaults, update both and run the tests. Custom configurations need only be loaded when selected.

| Field | Effect |
| --- | --- |
| `controller_design` | Chooses `codex-first` or `claude-first` routing labels. It does not change the current app/model. |
| `profiles` | One master catalog of exact model, provider, effort, target tier, soft context target, and descriptions. Aliases use `alias_of`. |
| `default_variant`, `variants` | Select `codex-primary` or `claude-primary` pools for Efficient, Balanced, and Performance. |
| `modes` | Shared High-qual and burn pools, plus custom/preset pools. Entries carry role/lifecycle, specialist, independent-review, and escalation markers. |
| `selection.bias` | Low/default/high selection preference. It never changes model effort or sorts unknown benchmark values. |
| `execution_style` | Pure orchestration or supporting delegation. |
| `max_parallel_workers` | Scheduling ceiling, further limited by the actual runtime. |
| `max_external_sessions_per_assignment` | External-session ceiling across the controller and descendants. |
| `claude.modes` | Tools, permission mode, timeout, turn cap, and optional worker policy. |
| `codex` | Sandbox by task role, approval policy, explicit bypass, and optional timeout. |

Keep your edits in an ignored `config/local.json` and pass `--overlay config/local.json`, or pass a complete replacement with `--config`. Recursive object merge preserves unspecified fields. Arrays replace rather than append. Later presets/overlays win. Presets load before overlays, so local policy can narrow a preset. Validate the final merged configuration.

`--variant` selects pool preference independently of controller design, permissions, and bias. Codex-primary is the default. `variants.NAME.modes` defines each variant's normal pools. Top-level `modes` supplies shared High-qual, burns, and custom/preset pools. A legacy top-level normal-mode override takes precedence for every variant. Prefer a variant-specific overlay when only one variant should change. Complete legacy configs without `variants` still use their top-level modes.

Both variants have six base modes with one shared catalog. The [router entrypoint](../skills/agent-orch-router/SKILL.md) links each self-contained mode. Bundled pool order and task-fit guidance are available there without reading JSON. Pool sizes are bundled choices, not hard limits on custom configuration.

Fable `FH`/`FX` remain on-call trials except High-qual's selective `FX` specification-review route. Neither appears in the Opus/Haiku preset. Ultracode is not supported. All model IDs require account/runtime verification.

High-qual is shared and opt-in. Its eight profiles are eligible choices, not required pipeline stages. Muse `MFH`/`MFX` default to investigation and allow implementation when the work order authorizes edits. Their exact efforts remain `high`/`xhigh`. Read [Muse provider checks](../skills/agent-orch-router/references/muse.md) only when selecting them.

`resolve` returns `external-muse` with adapter-required metadata. Bundled launch plans reject Muse. Use a separately verified adapter rather than substituting Codex or Claude settings. Configure Muse permissions through that adapter independently of model and role. Honor and read back the selected profile. This bundle imposes neither read-only nor maximum access.

Bundled Codex profiles target Standard tier without enforcing it. Launch plans do not set a tier and may inherit runtime settings. Verify and report the effective or inherited tier, or disclose unavailable verification. Do not change global speed settings.

`fast` and `tokenburn` are retired modes, not aliases. Select `efficient`, `performance`, or `balanced` explicitly, or select the relevant provider burn mode. Retired Fast codes (`LF`, `SF`, `SMF`, `SHF`, `SXF`, `ALF`, `AMF`, `AHF`, `AXF`, `AUF`) fail with migration guidance. Their Standard counterparts retain model and effort.

`CMAX` is retired. Select `SNX` explicitly to change Sonnet from Max to XHigh. Remove retired entries from complete configs and overlays before validation.

## Approvals are a separate choice

Model routing is opinionated. Permissions are not tied to a model or hard-locked to a task role. For each Claude mode, configure `permission_mode`, `permission_prompts`, `tools`, `allowed_tools`, `disallowed_tools`, `restricted`, `suppress_mcp`, and `no_chrome`. Consultation also configures its reviewer tools, model, prompt, and requested permission mode. Empty tool lists disable task tools. `default` means the native tool pool, not approval for every action.

For example, an overlay can enable authorized test execution in Consultation while retaining the review task:

```json
{
  "claude": {
    "modes": {
      "consultation": {
        "permission_mode": "auto",
        "tools": ["Read", "Glob", "Grep", "Bash"],
        "allowed_tools": ["Read", "Glob", "Grep", "Agent(review-worker)", "Bash(python -m pytest *)"],
        "reviewer": {"tools": ["Read", "Glob", "Grep", "Bash"]}
      }
    }
  }
}
```

Available tools and approval rules are separate. Bash-enabled tests can write generated files, so they are not strictly read-only. The task packet must state authorized checks and outputs. Full parent tools can also expose additional native agent types; verify the effective tool pool instead of assuming that reviewer definitions constrain every spawn.

Claude's parent auto/acceptEdits/bypass mode can override a child's requested permission mode. Native tool filters and managed policy still apply. `permission_prompts: host` needs a real host responder. The validator rejects native contradictions, such as restricted mode plus bypass. It does not ban a supported permission mode just because the workflow is called Consultation or Implementation.

Codex separately configures `sandbox_by_role`, `approval_policy`, `bypass_approvals_and_sandbox`, and `timeout_seconds`. Bypass overrides ordinary sandbox/approval settings in the generated plan. Any provider's bypass needs explicit assignment-level authorization. Neither config nor an approval mode expands the task's scope, and neither adapter retries with broader permissions after a denial.

## Examples

```sh
python3 scripts/bundle.py validate
python3 scripts/bundle.py resolve --mode efficient --role research
python3 scripts/bundle.py resolve --mode performance --role browser
python3 scripts/bundle.py resolve --mode high-qual --profile MFH --role research
python3 scripts/bundle.py resolve --mode balanced --profile OH --role qa
python3 scripts/bundle.py resolve --mode balanced --profile SM --role implementation --design claude-first
python3 scripts/bundle.py resolve --variant claude-primary --design claude-first --mode balanced --profile OH --role implementation --bias high
python3 scripts/bundle.py resolve --mode codex-burn --role browser --burn-account codex-work --burn-endpoint "next account reset"
python3 scripts/bundle.py resolve --mode claude-burn --profile HMAX --design claude-first --burn-account claude-work --burn-endpoint "authorized queue exhausted"
python3 scripts/bundle.py resolve --mode codex-burn --profile OH --role qa --allow-out-of-pool --role-override --burn-account codex-work --burn-endpoint "next account reset"
python3 scripts/bundle.py validate --preset opus-haiku
python3 scripts/bundle.py resolve --preset opus-haiku --mode opus-haiku --profile OH --role implementation --claude-mode orchestration
```

`resolve` returns eligible candidates, not the final suitability decision. The agent evaluates task complexity and tool fit before choosing one. Entries marked `specialist` take precedence for their stated roles. High-qual uses nonpreemptive role restrictions instead. Unknown profiles, alias cycles, ineligible roles, and disabled orchestration fail rather than silently selecting something else. An empty eligible set is a blocker.

An explicit out-of-pool profile requires both `--allow-out-of-pool` and `--role-override`. The active pool has no entry defining that profile's role/lifecycle eligibility. The second flag acknowledges this unspecified eligibility, not a global model restriction inferred from another mode.

An in-pool role/lifecycle exception requires only `--role-override` with an explicit profile. These switches record an exception. They do not obtain user authorization or expand task scope. Use them only for the user's explicit request.

`codex-burn` and `claude-burn` require explicit `--mode`, a non-secret `--burn-account`, and `--burn-endpoint`. The mode identifies the worker provider, not the parent host. Before launch, establish the intended account, reset/deadline or queue endpoint, and authorized backlog/scope from available instructions or evidence. Ask only for missing required inputs. Preserve the prior mode and restore it at the endpoint or queue end. Do not invent work to consume allowance.

The offline inspector records these identifiers but cannot verify account access or resets. It never reads quotas, pools accounts, or changes authentication.

The same two six-profile burn pools serve both variants. Automatic burn choices use only the selected provider. General-purpose Opus entries permit implementation. Native bounded Haiku workers are available under Claude-first without enabling Orchestration. Unknown remaining allowance stays unknown. No numeric quota prerequisite or tracking infrastructure is imposed. Never switch authentication or enable paid extra usage automatically.

Existing out-of-pool and role/lifecycle override controls remain available for explicit user-authorized exceptions. The inspector marks cross-provider exceptions. These exceptions do not consume the selected provider's allowance. Verify their own account route separately.

## Claude plans and the optional preset

Use an actual self-contained task file and existing workspace. For example, if a task packet has been saved as `task.txt` at this checkout's root:

```sh
python3 scripts/bundle.py claude-plan --profile OH --role qa --cwd . --prompt-file task.txt --artifacts .runs/review
python3 scripts/bundle.py claude-plan --variant claude-primary --profile OH --role implementation --cwd . --prompt-file task.txt --artifacts .runs/implementation
python3 scripts/bundle.py claude-plan --direct --role implementation --cwd . --prompt-file task.txt --artifacts .runs/implementation
python3 scripts/bundle.py claude-plan --preset opus-haiku --mode opus-haiku --profile OH --role implementation --claude-mode orchestration --cwd . --prompt-file task.txt --artifacts .runs/team
```

The optional preset defaults to permission bypass and full tools. Its approvals and tools can be overridden like any other mode. Loading it does not launch or authorize an assignment. The controller must obtain an explicit request for orchestration, and bypass needs assignment-level authorization when selected. The preset defaults to Opus 5.5 High with Haiku 5.5 XHigh workers; change these fields if your account supports other exact models.

Consultation and Implementation default to 60 minutes with no turn limit. Orchestration defaults to no timeout and no turn limit. `null` is deliberate, not a missing value. A plan's timeout is metadata: the caller must enforce a non-null deadline across its owned process tree. Actual execution limits and account errors still apply. Resumes share the original assignment deadline if one exists.

Balanced under Claude-primary permits general-purpose Opus implementation. Under Codex-primary, Balanced's OH entry is an optional independent-review route. An authored OH assignment there needs an explicit role exception. Standalone `--direct` calls have no router pool. They use the companion's configured default model and the user's assigned role, not an exception to an active router. Do not add `--direct` to evade restrictions while the router remains active.

CLI plans apply only to external routes. A native dispatch label now fails launch planning instead of producing a second CLI controller. Use the host's native worker controls. `--design` must describe the actual controller host, not serve as a way to evade this check.

## Checks and publication

```sh
python3 -m unittest discover -s tests -v
```

The tests are offline and spend no model usage. Launch plans do not prove model access, effective effort, Standard tier enforcement, timeout cleanup, or successful cross-provider execution. Report requested versus observed or inherited tier without changing global speed settings. Disclose unavailable tier controls or verification. Run bounded, authorized live tests before making execution claims publicly. This bundle is available under the [MIT License](../LICENSE).
