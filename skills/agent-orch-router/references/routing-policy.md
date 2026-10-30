# Variants, modes, and profile selection

## Independent controls

The master `profiles` catalog in [shared configuration](../../../config/routing.json) defines exact model IDs, efforts, and descriptions. A description suggests task fit, not permission or a measured guarantee. Read descriptions for candidate profiles as needed.

`--variant codex-primary` or `--variant claude-primary` chooses the ordered normal-mode pools. `--design` describes the actual controller host and determines native versus external dispatch. Neither changes a running host or its model. Permissions remain in `codex` and `claude.modes`. `--bias` changes selection preference, not effort. There is no separate API-efficient policy.

Both variants expose five modes. Balanced has seven to nine bundled configurations. Specialized modes, including Efficient, Performance, and burn pools, have five to eight. These sizes describe the bundled choices, not validator limits on custom configuration. Exact pool membership and order live only in configuration.

## Mode objectives

- **Efficient:** minimize total resources per accepted task, including failures, retries, and controller repair. Use Luna Medium only for trivial bounded work. Do not mechanically try every cheaper profile first.
- **Balanced:** use the everyday pool and minimize expected total effort. Low chooses the least resource-intensive plausible reliable candidate. Default accounts for retry and repair overhead. High favors additional reasoning capacity when uncertainty or consequences justify it.
- **Performance:** prioritize expected task success and turnaround. An `escalation` entry is available when justified, not a requirement to use the largest model.
- **Codex-burn / Claude-burn:** complete useful authorized work against the identified provider allowance before its endpoint. Burn selection does not maximize tokens or create a backlog.

All three Balanced biases use the same variant pool. High bias can select a different family or preconfigured effort. It does not rewrite a selected profile's effort. Unknown task cost, effective tier, or remaining allowance stays unknown.

## Specialists and independent review

Entries marked `specialist` take precedence for their configured roles. Browser work requires preflight of the actual worker's browser/computer tools and session access. Astra is a candidate, not the only browser-capable model. An explicitly selected eligible general profile can still perform browser work with the required tools.

Claude-primary Performance gives `AMAX` a browser-specialist starting role. This configurable pool role is not a limit on the model's capabilities. For another justified specialist assignment, select `AMAX` explicitly with `--role-override`. No pool override is needed because `AMAX` is already in that pool.

Entries marked `independent_review` are optional review/verification routes with their own role fences. General-purpose Opus entries in Claude-primary and Claude-burn can implement and integrate. Do not import review-only restrictions from another variant. An author must not be the sole acceptance check, but independence does not always require another provider.

## Burn authorization

Before launch, establish explicit burn invocation, the intended provider account, the reset/deadline or queue endpoint, and the authorized backlog/scope. Use available instructions and evidence. Ask only for missing required inputs. `--burn-account` and `--burn-endpoint` record non-secret identifiers, not proof of access or numeric quota. No numeric quota prerequisite or tracking system is imposed.

The six-profile burn pool for each provider is shared across variants. Automatic choices use that provider only. The controller may consume its own provider's allowance while coordinating. Explicit cross-provider exceptions need both existing override flags. Mark these exceptions and verify their separate account route without claiming they spend the selected burn allowance.

Preserve the prior mode and restore it at the endpoint or backlog completion. Stop on quota, billing, authentication, rate-limit, or model-access failures. Do not switch accounts, enable paid extra usage, or invent work. Burn selection does not enable Orchestration, bypass, or extra external-session slots.

## Explicit on-call profiles

Unused catalog profiles remain available without entering automatic pools. Fable `FH` and `FX` appear in no bundled mode or preset. Read their catalog descriptions only when an explicit assignment warrants a trial. Their narrower uses are candidates, not proven task advantages or a default escalation ladder. A lower composite AAI score does not make a model universally unsuitable.

For an authorized Fable trial under the router, select the exact profile with both `--allow-out-of-pool` and `--role-override`. The active pool has no entry specifying its role/lifecycle eligibility. These flags acknowledge that exception. They do not change tools, approvals, task scope, or Claude workflow.

For example, with a saved authorized task packet under Codex-first:

```sh
python3 scripts/bundle.py claude-plan --variant codex-primary --mode balanced --profile FH --role frontend --allow-out-of-pool --role-override --cwd . --prompt-file task.txt --artifacts .runs/fable-trial
```

Verify exact model/effort access before dispatch and evaluate the concrete acceptance checks. Under Claude-first, use native worker controls rather than an external CLI plan. Do not use `--direct` to evade an active router.
