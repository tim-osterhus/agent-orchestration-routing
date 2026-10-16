# Configuration and installation

Python 3.10+ is required for offline inspection. Dispatch requires the selected host, native subagent support, and an already authorized CLI account. No API key is required by these scripts because they never call a model.

## Keep the bundle together

Retain this checkout as the canonical source. Expose `skills/agent-orch-router` and optionally `skills/claude-delegation` through your host's skill installation mechanism. Codex discovers user skills under `~/.agents/skills`; Claude Code supports `.claude/skills` for project-local skills. Use directory links to the source folders where supported. On Windows, use a directory junction or the host's installer rather than copying only a link file.

These skills reference the shared configuration by physical source path. Copying an individual skill without its sibling configuration, scripts, and docs is not a complete installation. Do not overwrite an existing installation without reviewing it. This initial version does not install itself or modify global settings.

For Claude Code, invoke the router explicitly and do not add it to always-loaded instructions. This package does not silently create Claude-specific frontmatter or preload the skill. Set `disable-model-invocation: true` in a host-specific installed copy if automatic Claude invocation must be technically disabled. Codex's `agents/openai.yaml` already keeps both skills explicit-only.

## Editable controls

`config/routing.json` is the source of truth:

| Field | Effect |
| --- | --- |
| `controller_design` | Chooses `codex-first` or `claude-first` routing labels. It does not change the current app/model. |
| `profiles` | Exact model, provider, effort, service tier, and soft context target. Aliases use `alias_of`. |
| `modes` | Ordered pools with role, one-off, ongoing-thread, specialist, and final-review eligibility. |
| `selection.bias` | Low/default/high selection preference. It never changes model effort or sorts unknown benchmark values. |
| `execution_style` | Pure orchestration or supporting delegation. |
| `max_parallel_workers` | Scheduling ceiling, further limited by the actual runtime. |
| `max_external_sessions_per_assignment` | External-session ceiling across the controller and descendants. |
| `claude.modes` | Tools, permission mode, timeout, turn cap, and optional worker policy. |
| `codex` | Sandbox by task role, approval policy, explicit bypass, and optional timeout. |

Keep your edits in an ignored `config/local.json` and pass `--overlay config/local.json`, or pass a complete replacement with `--config`. Recursive object merge preserves unspecified fields. Arrays replace rather than append. Later presets/overlays win. Presets load before overlays, so local policy can narrow a preset. Validate the final merged configuration.

The initial mode structure retains the source router's eligibility boundaries. Personal names, local helper paths, account prices, and the required private helper were removed. Sol Max and Sonnet Max examples extend the Balanced pool to reflect the supplied frontier chart. Unsupported Ultracode-specific profiles were omitted instead of advertised as working integrations. All model IDs require account/runtime verification.

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
python3 scripts/bundle.py resolve --mode balanced --profile OH --role qa
python3 scripts/bundle.py resolve --mode balanced --profile SM --role implementation --design claude-first
python3 scripts/bundle.py validate --preset opus-haiku
python3 scripts/bundle.py resolve --preset opus-haiku --mode opus-haiku --profile OH --role implementation --claude-mode orchestration
```

`resolve` returns eligible candidates, not the final suitability decision. The agent evaluates task complexity and tool fit before choosing one. Specialist entries take precedence for their stated roles. Unknown profiles, alias cycles, ineligible roles, and disabled orchestration fail rather than silently selecting something else. An empty eligible set is a blocker.

An explicit out-of-pool profile requires `--allow-out-of-pool`. A role/lifecycle exception requires `--role-override` with an explicit profile. These switches record an exception; they do not obtain user authorization or expand task scope. Use them only for the user's explicit request.

Tokenburn also requires the controller to establish the relevant account, reset/deadline, authorized queue, and prior mode. The offline inspector cannot verify a reset. It never reads quotas, pools accounts, or changes authentication.

## Claude plans and the optional preset

Use an actual self-contained task file and existing workspace. For example, if a task packet has been saved as `task.txt` at this checkout's root:

```sh
python3 scripts/bundle.py claude-plan --profile OH --role qa --cwd . --prompt-file task.txt --artifacts .runs/review
python3 scripts/bundle.py claude-plan --direct --role implementation --cwd . --prompt-file task.txt --artifacts .runs/implementation
python3 scripts/bundle.py claude-plan --preset opus-haiku --mode opus-haiku --profile OH --role implementation --claude-mode orchestration --cwd . --prompt-file task.txt --artifacts .runs/team
```

The optional preset defaults to permission bypass and full tools. Its approvals and tools can be overridden like any other mode. Loading it does not launch or authorize an assignment. The controller must obtain an explicit request for orchestration, and bypass needs assignment-level authorization when selected. The preset defaults to Opus 5.5 High with Haiku 5.5 XHigh workers; change these fields if your account supports other exact models.

Consultation and Implementation default to 60 minutes with no turn limit. Orchestration defaults to no timeout and no turn limit. `null` is deliberate, not a missing value. A plan's timeout is metadata: the caller must enforce a non-null deadline across its owned process tree. Actual execution limits and account errors still apply. Resumes share the original assignment deadline if one exists.

Without `--direct`, an Implementation plan under Balanced uses an eligible profile such as HM. OH Implementation needs the selected `opus-haiku` pool or a user-approved role exception. Standalone `--direct` calls have no router pool. They use the companion's configured default model and the user's assigned role, not an exception to an active router. Do not add `--direct` to evade restrictions while the router remains active.

## Checks and publication

```sh
python3 -m unittest discover -s tests -v
```

The tests are offline and spend no model usage. Launch plans do not prove model access, effective effort, Fast support, timeout cleanup, or successful cross-provider execution. Run bounded, authorized live tests before making those claims publicly. This bundle is available under the [MIT License](../LICENSE).
