#!/usr/bin/env python3
"""Inspect routing configuration and print launch plans. Never execute models."""

import argparse
from copy import deepcopy
import json
from pathlib import Path
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
EFFORTS = {"low", "medium", "high", "xhigh", "max", "ultra"}
PERMISSION_MODES = {"default", "manual", "dontAsk", "auto", "acceptEdits", "plan", "bypassPermissions"}


def valid_tools(value):
    return value == "default" or isinstance(value, list) and all(isinstance(tool, str) and tool for tool in value)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def merge(base, patch):
    result = deepcopy(base)
    for key, value in patch.items():
        result[key] = merge(result[key], value) if isinstance(value, dict) and isinstance(result.get(key), dict) else deepcopy(value)
    return result


def profile(config, code, seen=None):
    seen = set() if seen is None else seen
    require(code in config["profiles"], f"Unknown profile: {code}")
    require(code not in seen, f"Alias cycle at {code}")
    item = config["profiles"][code]
    if "alias_of" in item:
        return profile(config, item["alias_of"], seen | {code})
    return deepcopy(item)


def validate(config):
    require(config.get("schema_version") == 1, "Expected schema_version 1")
    require(config["controller_design"] in config["designs"], "Unknown controller design")
    require(config["default_mode"] in config["modes"], "Unknown default mode")
    require(config["execution_style"] in {"pure-orchestration", "supporting"}, "Invalid execution style")
    for key in ("max_parallel_workers", "max_external_sessions_per_assignment"):
        require(type(config[key]) is int and config[key] > 0, f"Invalid {key}")
    require(config["selection"]["bias"] in config["selection"]["bias_options"], "Invalid selection bias")
    for name, design in config["designs"].items():
        require(design["controller"] in {"codex", "claude"}, f"Invalid controller in {name}")
        require(design["native_workers"] == design["controller"], f"Native provider mismatch in {name}")
        require(design["external_workers"] in {"codex", "claude"} - {design["controller"]}, f"Invalid external provider in {name}")
    for code in config["profiles"]:
        item = profile(config, code)
        require(item["provider"] in {"codex", "claude"}, f"Unknown provider in {code}")
        require(isinstance(item["model"], str) and item["model"].strip(), f"Missing model in {code}")
        require(item["effort"] in EFFORTS, f"Invalid effort in {code}")
        require(item["provider"] != "claude" or item["effort"] != "ultra", f"Claude does not use the Codex ultra effort in {code}")
        require(item.get("service_tier", "standard") in {"standard", "fast"}, f"Invalid tier in {code}")
        target = item.get("context_target_tokens")
        require(target is None or type(target) is int and target > 0, f"Invalid context target in {code}")
    for name, pool in config["modes"].items():
        require(isinstance(pool, list) and pool, f"Empty pool: {name}")
        require(len({entry["profile"] for entry in pool}) == len(pool), f"Duplicate profiles in {name}")
        for entry in pool:
            profile(config, entry["profile"])
            require(set(entry.get("roles", config["roles"])) <= set(config["roles"]), f"Unknown role in {name}")
            for flag in ("one_off_only", "ongoing_thread_only", "final_only", "specialist"):
                require(flag not in entry or type(entry[flag]) is bool, f"Invalid {flag} in {name}")
    codex = config["codex"]
    require(all(value in {"read-only", "workspace-write", "danger-full-access"} for value in codex["sandbox_by_role"].values()), "Invalid Codex sandbox")
    require("default" in codex["sandbox_by_role"], "Missing default Codex sandbox")
    require(codex["approval_policy"] in {"never", "on-request", "on-failure", "untrusted"}, "Invalid Codex approval policy")
    require(type(codex["bypass_approvals_and_sandbox"]) is bool, "Invalid Codex bypass setting")
    require(codex["timeout_seconds"] is None or type(codex["timeout_seconds"]) is int and codex["timeout_seconds"] > 0, "Invalid Codex timeout")
    claude = config["claude"]
    require(profile(config, claude["default_profile"])["provider"] == "claude", "Claude default must be a Claude profile")
    require(claude["default_mode"] in claude["modes"], "Unknown Claude default mode")
    for name, mode in claude["modes"].items():
        require(name in {"consultation", "implementation", "orchestration"}, f"Unknown Claude mode: {name}")
        for field in ("timeout_seconds", "max_turns"):
            value = mode[field]
            require(value is None or type(value) is int and value > 0, f"Invalid {field} for {name}")
        require(mode["permission_mode"] in PERMISSION_MODES, f"Invalid permissions for {name}")
        require(mode["permission_prompts"] in {"none", "host"}, f"Invalid prompt handling for {name}")
        require(valid_tools(mode["tools"]), f"Invalid tool list for {name}")
        for field in ("allowed_tools", "disallowed_tools"):
            require(isinstance(mode[field], list) and all(isinstance(rule, str) and rule for rule in mode[field]), f"Invalid {field} for {name}")
        for field in ("restricted", "suppress_mcp", "no_chrome"):
            require(type(mode[field]) is bool, f"Invalid {field} for {name}")
        require(not (mode["restricted"] and mode["permission_mode"] == "bypassPermissions"), "Claude restricted mode is incompatible with bypassPermissions")
        if name == "consultation":
            reviewer = mode["reviewer"]
            require(type(reviewer["enabled"]) is bool and valid_tools(reviewer["tools"]), "Invalid reviewer configuration")
            require(reviewer["permission_mode"] in PERMISSION_MODES and reviewer["model"], "Invalid reviewer mode/model")
            require(isinstance(reviewer.get("prompt"), str) and reviewer["prompt"].strip(), "Missing reviewer prompt")
        if name == "orchestration" and mode.get("enabled"):
            worker = mode["worker"]
            require(worker["effort"] in EFFORTS - {"ultra"} and worker["model"], "Invalid orchestration worker")
            require(valid_tools(worker["tools"]), "Invalid orchestration worker tools")
            require(type(mode["nested_delegation"]) is bool, "Invalid nested-delegation setting")
            require(mode["controller_profiles"], "Missing orchestration controllers")
            for code in mode["controller_profiles"]:
                require(profile(config, code)["provider"] == "claude", "Orchestration controller must be Claude")
    return config


def load_config(path=None, presets=(), overlays=()):
    with open(path or ROOT / "config/routing.json", encoding="utf-8") as handle:
        config = json.load(handle)
    for name in presets:
        require(name and name.replace("-", "").isalnum(), "Preset names must be simple names")
        with open(ROOT / "config/presets" / (name + ".json"), encoding="utf-8") as handle:
            config = merge(config, json.load(handle))
    for path in overlays:
        with open(path, encoding="utf-8") as handle:
            config = merge(config, json.load(handle))
    return validate(config)


def eligible(entry, role, assignment_kind, ongoing, final):
    return (role in entry.get("roles", [role])
            and not (entry.get("one_off_only") and assignment_kind != "bounded")
            and not (entry.get("ongoing_thread_only") and not ongoing)
            and not (entry.get("final_only") and not final))


def resolve(config, *, mode=None, code=None, role="implementation", design=None,
            assignment_kind="bounded", ongoing=False, final=False,
            allow_out_of_pool=False, role_override=False, claude_mode=None):
    mode = mode or config["default_mode"]
    design = design or config["controller_design"]
    require(mode in config["modes"], f"Unknown routing mode: {mode}")
    require(design in config["designs"], f"Unknown controller design: {design}")
    require(role in config["roles"], f"Unknown task role: {role}")
    require(assignment_kind in {"bounded", "controller"}, "Invalid assignment kind")
    require(not final or role in {"qa", "spec-review"}, "Final review must have a review role")
    pool = config["modes"][mode]
    if code:
        requested = profile(config, code)
        matches = [entry for entry in pool if profile(config, entry["profile"]) == requested]
        require(matches or allow_out_of_pool, "Profile is outside the active pool; explicit out-of-pool authorization is required")
        entries = matches or [{"profile": code}]
        require(role_override or any(eligible(entry, role, assignment_kind, ongoing, final) for entry in entries), "Profile violates role/lifecycle restrictions; explicit override required")
        codes = [code]
    else:
        require(not role_override, "Role override requires an explicit profile")
        candidates = [entry for entry in pool if eligible(entry, role, assignment_kind, ongoing, final)]
        specialists = [entry for entry in candidates if entry.get("specialist")]
        codes = [entry["profile"] for entry in specialists or candidates]
    require(codes, "No eligible profile; do not substitute silently")
    choices = []
    for candidate in codes:
        item = profile(config, candidate)
        native = item["provider"] == config["designs"][design]["controller"]
        choice = {"code": candidate, **item, "dispatch": ("native-" if native else "external-") + item["provider"]}
        if item["provider"] == "claude":
            selected_mode = claude_mode or ("consultation" if role in {"research", "planning", "qa", "spec-review"} else "implementation")
            require(selected_mode in config["claude"]["modes"], "Unknown Claude mode")
            settings = deepcopy(config["claude"]["modes"][selected_mode])
            if selected_mode == "orchestration":
                require(settings.get("enabled"), "Orchestration is disabled; select an opt-in preset")
                require(candidate in settings["controller_profiles"], "Profile cannot control this orchestration preset")
            choice.update(claude_mode=selected_mode, execution=settings)
        else:
            choice["execution"] = deepcopy(config["codex"])
        choices.append(choice)
    return {"controller_design": design, "controller": config["designs"][design]["controller"],
            "routing_mode": mode, "role": role, "selection_bias": config["selection"]["bias"],
            "execution_style": config["execution_style"], "choices": choices,
            "overrides": {"out_of_pool": allow_out_of_pool, "role_or_lifecycle": role_override},
            "limits": {key: config[key] for key in ("max_parallel_workers", "max_external_sessions_per_assignment")},
            "notice": "Eligibility only, not measured suitability, account access, or dispatch verification."}


def launch_plan(resolved, cwd, prompt_file, artifacts, resume=None):
    require(len(resolved["choices"]) == 1, "Select one explicit --profile for a launch plan")
    choice = resolved["choices"][0]
    cwd, prompt_file, artifacts = (str(Path(path).expanduser().resolve()) for path in (cwd, prompt_file, artifacts))
    require(Path(cwd).is_dir(), "cwd must be an existing directory")
    require(Path(prompt_file).is_file(), "prompt file must exist")
    if resume:
        uuid.UUID(resume)
    plan = {"executes": False, "profile": choice, "cwd": cwd, "stdin_file": prompt_file,
            "stdout_file": str(Path(artifacts) / "result.json"), "stderr_file": str(Path(artifacts) / "stderr.log"),
            "required_checks": ["signed-in subscription route", "exact returned model", "requested effort versus effective effort", "exit status and complete result", "owned-process lifecycle"],
            "environment_unset": [], "timeout_seconds": None}
    if choice["provider"] == "codex":
        require(not resume, "Codex resume planning is not implemented; use the documented exact-session CLI route")
        require(choice.get("service_tier") != "fast", "This external Codex adapter does not enforce Fast; use a verified native route or explicitly choose Standard")
        settings = choice["execution"]
        sandbox = settings["sandbox_by_role"].get(resolved["role"], settings["sandbox_by_role"]["default"])
        args = ["codex", "exec", "--model", choice["model"], "-c", "model_reasoning_effort=" + json.dumps(choice["effort"]),
                "--cd", cwd, "--json"]
        if settings["bypass_approvals_and_sandbox"]:
            args += ["--dangerously-bypass-approvals-and-sandbox"]
            plan["required_checks"].append("explicit user authorization for approval and sandbox bypass")
        else:
            args += ["--sandbox", sandbox, "-c", "approval_policy=" + json.dumps(settings["approval_policy"])]
        args += ["-"]
        plan["timeout_seconds"] = settings["timeout_seconds"]
        plan["stdout_file"] = str(Path(artifacts) / "events.jsonl")
        plan["required_checks"] += ["configured approval policy supported by unattended route", "sandbox does not constrain connector side effects", "no recursive controller launches", "caller-supplied deadline if required"]
    else:
        settings = choice["execution"]
        plan["timeout_seconds"] = settings["timeout_seconds"]
        plan["environment_unset"] = ["CLAUDE_CODE_EFFORT_LEVEL", "CLAUDE_CODE_SKIP_PROMPT_HISTORY"]
        args = ["claude", "-p", "--model", choice["model"], "--effort", choice["effort"]]
        args += ["--resume", resume] if resume else ["--session-id", str(uuid.uuid4())]
        if settings["max_turns"] is not None:
            args += ["--max-turns", str(settings["max_turns"])]
        if settings["restricted"]:
            args += ["--restricted", "--setting-sources", "", "--disable-slash-commands", "--settings", '{"autoMemoryEnabled":false}']
        if settings["suppress_mcp"]:
            args += ["--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}']
        if settings["no_chrome"]:
            args += ["--no-chrome"]
        if choice["claude_mode"] == "consultation":
            tools = settings["tools"]
            reviewer = settings["reviewer"]
            if reviewer["enabled"]:
                definitions = {"consultation-controller": {"description": "Consultation controller", "prompt": "",
                    "permissionMode": settings["permission_mode"]},
                    "review-worker": {"description": "Bounded independent review", "prompt": reviewer["prompt"],
                    "model": reviewer["model"], "permissionMode": reviewer["permission_mode"], "omitClaudeMd": True}}
                if tools != "default":
                    definitions["consultation-controller"]["tools"] = tools + ["Agent(review-worker)"]
                if reviewer["tools"] != "default":
                    definitions["review-worker"]["tools"] = reviewer["tools"]
                if settings["max_turns"] is not None:
                    definitions["review-worker"]["maxTurns"] = settings["max_turns"]
                args += ["--agents", json.dumps(definitions), "--agent", "consultation-controller",
                         "--tools", "default" if tools == "default" else ",".join(tools + ["Agent"])]
            else:
                args += ["--tools", "default" if tools == "default" else ",".join(tools)]
        else:
            args += ["--tools", "default" if settings["tools"] == "default" else ",".join(settings["tools"])]
            if choice["claude_mode"] == "orchestration":
                worker = settings["worker"]
                definition = {"description": "Bounded orchestration worker", "prompt": "Complete the assigned work and checks. Preserve ownership. Return evidence. Escalate very complex work to the controller. Share a supplied deadline; otherwise no default timeout applies. Stop on cancellation.",
                              "model": worker["model"], "effort": worker["effort"]}
                if worker["tools"] != "default":
                    definition["tools"] = worker["tools"]
                if not settings["nested_delegation"]:
                    definition["disallowedTools"] = ["Agent"]
                if settings["max_turns"] is not None:
                    definition["maxTurns"] = settings["max_turns"]
                args += ["--agents", json.dumps({"haiku-worker": definition})]
                plan["work_order_requirement"] = "Delegate basic and parallelizable work to haiku-worker at the configured model/effort. The Opus controller retains very complex work and integration."
                plan["required_checks"] += ["explicit user authorization for orchestration", "worker model and effort"]
        if settings["permission_mode"] == "bypassPermissions":
            args += ["--dangerously-skip-permissions"]
            plan["required_checks"].append("explicit assignment-level permission-bypass authorization")
        else:
            args += ["--permission-mode", settings["permission_mode"]]
        if settings["allowed_tools"]:
            args += ["--allowedTools", *settings["allowed_tools"]]
        if settings["disallowed_tools"]:
            args += ["--disallowedTools", *settings["disallowed_tools"]]
        args += ["--permission-prompts", settings["permission_prompts"], "--output-format", "json"]
        if settings["permission_prompts"] == "host":
            plan["required_checks"].append("configured host permission responder is available")
        if settings["permission_mode"] in {"auto", "acceptEdits", "bypassPermissions"}:
            plan["required_checks"].append("native child permission modes may be overridden by parent inheritance")
        if choice.get("context_target_tokens"):
            plan["required_checks"].append("context target is soft unless independently enforced")
    plan["argv"] = args
    return plan


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["validate", "resolve", "claude-plan", "codex-plan"])
    parser.add_argument("--config", type=Path)
    parser.add_argument("--preset", action="append", default=[])
    parser.add_argument("--overlay", type=Path, action="append", default=[])
    parser.add_argument("--mode")
    parser.add_argument("--profile")
    parser.add_argument("--role")
    parser.add_argument("--design")
    parser.add_argument("--assignment-kind", choices=["bounded", "controller"], default="bounded")
    parser.add_argument("--ongoing-thread", action="store_true")
    parser.add_argument("--final-review", action="store_true")
    parser.add_argument("--allow-out-of-pool", action="store_true")
    parser.add_argument("--role-override", action="store_true")
    parser.add_argument("--claude-mode", choices=["consultation", "implementation", "orchestration"])
    parser.add_argument("--direct", action="store_true", help="Standalone Claude companion assignment, without router pool restrictions")
    parser.add_argument("--cwd")
    parser.add_argument("--prompt-file")
    parser.add_argument("--artifacts")
    parser.add_argument("--resume")
    args = parser.parse_args(argv)
    try:
        config = load_config(args.config, args.preset, args.overlay)
        require(not args.direct or args.action == "claude-plan", "--direct applies only to claude-plan")
        if args.action == "validate":
            output = {"valid": True, "profiles": len(config["profiles"]), "modes": list(config["modes"])}
        else:
            role = args.role or ("qa" if args.action == "claude-plan" else "implementation")
            code = args.profile or (config["claude"]["default_profile"] if args.action == "claude-plan" else None)
            mode = args.mode
            claude_mode = args.claude_mode
            if args.direct:
                require(not mode, "Standalone --direct does not use a router --mode")
                config = deepcopy(config)
                config["modes"]["direct-claude"] = [{"profile": code}]
                mode = "direct-claude"
                if args.role is None and claude_mode is None:
                    claude_mode = config["claude"]["default_mode"]
            output = resolve(config, mode=mode, code=code, role=role, design=args.design,
                             assignment_kind=args.assignment_kind, ongoing=args.ongoing_thread, final=args.final_review,
                             allow_out_of_pool=args.allow_out_of_pool, role_override=args.role_override, claude_mode=claude_mode)
            if args.action.endswith("-plan"):
                require(args.cwd and args.prompt_file and args.artifacts, "Launch planning requires --cwd, --prompt-file, and --artifacts")
                require(len(output["choices"]) == 1 and output["choices"][0]["provider"] == args.action.split("-")[0], "Profile provider does not match the requested adapter")
                output = launch_plan(output, args.cwd, args.prompt_file, args.artifacts, args.resume)
        print(json.dumps(output, indent=2))
        return 0
    except (KeyError, TypeError, ValueError, OSError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    sys.exit(main())
