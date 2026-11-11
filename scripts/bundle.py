#!/usr/bin/env python3
"""Inspect routing configuration and print launch plans. Never execute models."""

import argparse
from copy import deepcopy
from fnmatch import fnmatchcase
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_DIR = ROOT / "plugins/agent-orch"
# Tracked sources copied into the generated Claude Code plugin; runtime/, hooks/ and .claude-plugin/ are maintained by hand.
PLUGIN_COPIES = ("skills/agent-orch-router", "docs", "scripts/bundle.py", "config", "LICENSE")
PLUGIN_GENERATED = PLUGIN_COPIES + ("agents",)
PLUGIN_PROVIDERS = {"codex", "claude"}
# Added only to the plugin's router copy; the canonical router stays host-neutral.
PLUGIN_POINTER = ("In Claude Code with the agent-orch plugin, use design `claude-plugin` and read "
                  "[Claude plugin dispatch](references/claude-plugin.md) before the first dispatch.\n\n")
REVIEW_ROLES = {"research", "planning", "qa", "spec-review"}
RELAY = {"model": "haiku", "effort": "low"}
EFFORTS = {"minimal", "low", "medium", "high", "xhigh", "max", "ultra"}
PERMISSION_MODES = {"default", "manual", "dontAsk", "auto", "acceptEdits", "plan", "bypassPermissions"}
RETIRED_PROFILES = {"LF": "L", "SF": "SM", "SMF": "SM", "SHF": "SH", "SXF": "SX",
                    "ALF": "AL", "AMF": "AM", "AHF": "AH", "AXF": "AX",
                    "AUF": "a verified current Astra profile", "CMAX": "SNX (XHigh) or SNMAX (Max)"}
BURN_PROVIDERS = {"codex-burn": "codex", "claude-burn": "claude"}


def check_mode(mode):
    require(mode != "hiq", "Routing mode hiq was renamed. Select amusing explicitly.")
    require(mode != "fast", "Routing mode fast is retired. Select efficient, performance, or balanced explicitly.")
    require(mode != "tokenburn", "Routing mode tokenburn is retired. Select codex-burn or claude-burn explicitly.")


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
    require(code not in RETIRED_PROFILES,
            f"Profile {code} is retired. Select {RETIRED_PROFILES.get(code)} explicitly and review its model, effort, and tier.")
    require(code in config["profiles"], f"Unknown profile: {code}")
    require(code not in seen, f"Alias cycle at {code}")
    item = config["profiles"][code]
    if "alias_of" in item:
        return profile(config, item["alias_of"], seen | {code})
    return deepcopy(item)


def mode_pools(config, variant=None):
    variant = variant or config.get("default_variant")
    variants = config.get("variants", {})
    require(variant in variants if variants else variant is None, f"Unknown routing variant: {variant}")
    # Shared/custom top-level modes also preserve legacy mode overlays and presets.
    pools = {**variants.get(variant, {}).get("modes", {}), **config["modes"]}
    result = {}
    for mode, pool in pools.items():
        scope = "shared" if mode in config["modes"] else variant
        bindings = config.get("bindings", {}).get(scope, {}).get(mode, {})
        bound = []
        for source in pool:
            entry = deepcopy(source)
            if "slot" in entry:
                slot = entry["slot"]
                require(slot in config.get("slots", {}), f"Unknown slot: {slot}")
                require(slot in bindings, f"Missing binding for slot {slot} in {scope}/{mode}")
                require("profile" not in entry, f"Slot {slot} must use its binding, not a duplicate profile")
                entry["profile"] = bindings[slot]
            else:
                require("profile" in entry, f"Missing slot/profile in {mode}")
            bound.append(entry)
        result[mode] = bound
    return result


def adapter_available(config, item):
    """Known adapter routes do not prove current account access or tool availability."""
    if item.get("executable", True) is False:
        return False
    if item["provider"] in {"codex", "claude"}:
        return True
    route = item["provider"]
    if item.get("access_mode"):
        # A known Muse Code route must never enable a different public API route.
        route += ":" + item["access_mode"]
    return config.get("adapters", {}).get(route, {}).get("verified", False) is True


def validate(config):
    require(config.get("schema_version") == 1, "Expected schema_version 1")
    require(config["controller_design"] in config["designs"], "Unknown controller design")
    check_mode(config["default_mode"])
    require(config["default_mode"] in mode_pools(config), "Unknown default mode")
    require(config["execution_style"] in {"pure-orchestration", "supporting"}, "Invalid execution style")
    for key in ("max_parallel_workers", "max_external_sessions_per_assignment"):
        require(type(config[key]) is int and config[key] > 0, f"Invalid {key}")
    require(config["selection"]["bias"] in config["selection"]["bias_options"], "Invalid selection bias")
    for name, design in config["designs"].items():
        require(design["controller"] in {"codex", "claude"}, f"Invalid controller in {name}")
        require(design["native_workers"] == design["controller"], f"Native provider mismatch in {name}")
        require(design["external_workers"] in {"codex", "claude"} - {design["controller"]}, f"Invalid external provider in {name}")
        plugin = design.get("plugin_agents")
        require(plugin is None or design["controller"] == "claude" and isinstance(plugin, str) and plugin.replace("-", "").isalnum(),
                f"Plugin agents require a Claude controller and a simple plugin name in {name}")
    for code in config["profiles"]:
        item = profile(config, code)
        require(item["provider"] in {"codex", "claude", "muse", "gemini", "kimi", "deepseek", "glm"}, f"Unknown provider in {code}")
        documentary = item.get("executable", True) is False
        require(isinstance(item["model"], str) and item["model"].strip() or
                documentary and item["model"] is None and item.get("label"), f"Missing model in {code}")
        require(item["effort"] in EFFORTS or documentary and item["effort"] is None, f"Invalid effort in {code}")
        require(item["provider"] != "claude" or item["effort"] != "ultra", f"Claude does not use the Codex ultra effort in {code}")
        require("description" not in item or isinstance(item["description"], str) and item["description"].strip(), f"Invalid description in {code}")
        require(item.get("service_tier", "standard") == "standard", f"Only Standard service tier is supported in {code}")
        require(code != "SNX" or item["effort"] == "xhigh", "SNX retains Sonnet XHigh. Select SNMAX explicitly for Max.")
        target = item.get("context_target_tokens")
        require(target is None or type(target) is int and target > 0, f"Invalid context target in {code}")
    pools = []
    for name, variant in config.get("variants", {}).items():
        require(variant.get("modes"), f"Missing mode pools in variant {name}")
        require(not set(variant["modes"]) & set(BURN_PROVIDERS), "Burn pools must be shared top-level modes")
        require(config["default_mode"] in mode_pools(config, name), f"Unknown default mode in variant {name}")
        pools.extend(mode_pools(config, name).items())
    if not config.get("variants"):
        pools.extend(mode_pools(config).items())
    for scope, modes in config.get("bindings", {}).items():
        # Legacy complete configs can discard variants while retaining unused bindings.
        if scope != "shared" and not config.get("variants"):
            continue
        require(scope == "shared" or scope in config.get("variants", {}), f"Unknown binding scope: {scope}")
        source_modes = config["modes"] if scope == "shared" else config["variants"][scope]["modes"]
        for mode, bindings in modes.items():
            require(mode in source_modes, f"Unknown binding mode: {scope}/{mode}")
            for slot, code in bindings.items():
                require(slot in config.get("slots", {}), f"Unknown slot: {slot}")
                profile(config, code)
    catalogs = config.get("catalogs", {})
    catalog_codes = [code for codes in catalogs.values() for code in codes]
    require(len(set(catalog_codes)) == len(catalog_codes), "Catalogs must be disjoint")
    for code in catalog_codes:
        profile(config, code)
    for name, pool in pools:
        check_mode(name)
        require(isinstance(pool, list) and pool, f"Empty pool: {name}")
        identities = [entry.get("slot", entry["profile"]) for entry in pool]
        require(len(set(identities)) == len(pool), f"Duplicate slot/profile identity in {name}")
        for entry in pool:
            item = profile(config, entry["profile"])
            require(name not in BURN_PROVIDERS or item["provider"] == BURN_PROVIDERS[name],
                    f"{name} requires {BURN_PROVIDERS.get(name)} profiles only")
            require(set(entry.get("roles", config["roles"])) <= set(config["roles"]), f"Unknown role in {name}")
            for flag in ("one_off_only", "ongoing_thread_only", "final_only", "specialist", "independent_review", "escalation", "requires_verified_adapter"):
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


def load_config(path=None, presets=(), overlays=(), root=None, validate_config=True):
    root = Path(root) if root is not None else ROOT
    with open(path or root / "config/routing.json", encoding="utf-8") as handle:
        config = json.load(handle)
    for name in presets:
        require(name and name.replace("-", "").isalnum(), "Preset names must be simple names")
        with open(root / "config/presets" / (name + ".json"), encoding="utf-8") as handle:
            config = merge(config, json.load(handle))
    for path in overlays:
        with open(path, encoding="utf-8") as handle:
            config = merge(config, json.load(handle))
    return validate(config) if validate_config else config


def eligible(entry, role, assignment_kind, ongoing, final):
    return (role in entry.get("roles", [role])
            and not (entry.get("one_off_only") and assignment_kind != "bounded")
            and not (entry.get("ongoing_thread_only") and not ongoing)
            and not (entry.get("final_only") and not final))


def resolve(config, *, mode=None, code=None, slot=None, role="implementation", design=None,
            assignment_kind="bounded", ongoing=False, final=False,
            allow_out_of_pool=False, role_override=False, claude_mode=None,
            burn_account=None, burn_endpoint=None, variant=None, bias=None):
    explicit_mode = mode is not None
    mode = mode or config["default_mode"]
    check_mode(mode)
    design = design or config["controller_design"]
    variant = variant or config.get("default_variant")
    pools = mode_pools(config, variant)
    bias = bias or config["selection"]["bias"]
    require(bias in config["selection"]["bias_options"], "Invalid selection bias")
    require(mode in pools, f"Unknown routing mode: {mode}")
    require(design in config["designs"], f"Unknown controller design: {design}")
    require(role in config["roles"], f"Unknown task role: {role}")
    require(assignment_kind in {"bounded", "controller"}, "Invalid assignment kind")
    require(not final or role in {"qa", "spec-review"}, "Final review must have a review role")
    burn_provider = BURN_PROVIDERS.get(mode)
    if burn_provider:
        require(explicit_mode, "Burn modes require explicit invocation with --mode")
        require(isinstance(burn_account, str) and burn_account.strip(), "Burn modes require an identified --burn-account")
        require(isinstance(burn_endpoint, str) and burn_endpoint.strip(), "Burn modes require an identified reset/deadline or queue endpoint with --burn-endpoint")
    else:
        require(burn_account is None and burn_endpoint is None, "Burn account and endpoint apply only to burn modes")
    pool = pools[mode]
    require(not (code and slot), "Select a slot or exact profile, not both")
    unavailable = []
    if slot:
        require(slot in config.get("slots", {}), f"Unknown slot: {slot}")
        selected = [entry for entry in pool if entry.get("slot") == slot]
        require(selected, f"Slot {slot} is outside the active pool")
        require(role_override or eligible(selected[0], role, assignment_kind, ongoing, final),
                "Slot violates role/lifecycle restrictions; explicit override required")
    elif code:
        requested = profile(config, code)
        matches = [entry for entry in pool if profile(config, entry["profile"]) == requested]
        require(matches or allow_out_of_pool, "Profile is outside the active pool; explicit out-of-pool authorization is required")
        require(matches or role_override, "Out-of-pool profile has no role/lifecycle eligibility in the active pool. Explicit --role-override required.")
        require(role_override or any(eligible(entry, role, assignment_kind, ongoing, final) for entry in matches), "Profile violates role/lifecycle restrictions; explicit override required")
        allowed = [entry for entry in matches if role_override or eligible(entry, role, assignment_kind, ongoing, final)]
        # An exact profile request stays exact even if its aliases or slot bindings change.
        # A profile request needs one exact launch target, not duplicate model launches.
        # Take the first eligible job only. Never merge flags from other slots.
        selected = [{**allowed[0], "profile": code}] if allowed else [{"profile": code}]
    else:
        require(not role_override, "Role override requires an explicit profile")
        candidates = [entry for entry in pool if eligible(entry, role, assignment_kind, ongoing, final)]
        unavailable = [entry["profile"] for entry in candidates if not adapter_available(config, profile(config, entry["profile"]))]
        candidates = [entry for entry in candidates if adapter_available(config, profile(config, entry["profile"]))]
        specialists = [entry for entry in candidates if entry.get("specialist")]
        selected = specialists or candidates
    require(selected, "No eligible profile with a verified adapter; do not substitute silently")
    plugin = config["designs"][design].get("plugin_agents")
    choices = []
    for entry in selected:
        candidate = entry["profile"]
        item = profile(config, candidate)
        # A plugin design dispatches every Codex and Claude profile through its pinned host agent.
        plugin_route = bool(plugin) and item["provider"] in PLUGIN_PROVIDERS and item.get("executable", True)
        native = plugin_route or item["provider"] == config["designs"][design]["controller"]
        choice = {"code": candidate, **item, "dispatch": ("native-" if native else "external-") + item["provider"]}
        if "slot" in entry:
            choice["slot"] = entry["slot"]
        if plugin_route:
            if item["provider"] == "codex":
                codex_write_roles(config)
            choice["agent"] = plugin + ":" + agent_name(candidate, item)
        for flag in ("specialist", "independent_review", "escalation"):
            if entry.get(flag):
                choice[flag] = True
        if item["provider"] == "claude":
            selected_mode = claude_mode or ("consultation" if role in {"research", "planning", "qa", "spec-review"} else "implementation")
            require(selected_mode in config["claude"]["modes"], "Unknown Claude mode")
            settings = deepcopy(config["claude"]["modes"][selected_mode])
            if selected_mode == "orchestration":
                require(settings.get("enabled"), "Orchestration is disabled; select an opt-in preset")
                require(candidate in settings["controller_profiles"], "Profile cannot control this orchestration preset")
            choice.update(claude_mode=selected_mode, execution=settings)
        elif item["provider"] == "codex":
            choice["execution"] = deepcopy(config["codex"])
        else:
            choice["execution"] = {"launch_plan_supported": False, "adapter_required": True,
                                   "adapter_route_available": adapter_available(config, item),
                                   "account_access_verified": False,
                                   "notice": "Requires a separately verified provider adapter and exact account access. No bundled launcher or substitution."}
        choices.append(choice)
    result = {"controller_design": design, "controller": config["designs"][design]["controller"],
            "routing_variant": variant, "routing_mode": mode, "role": role, "selection_bias": bias,
            "execution_style": config["execution_style"], "choices": choices,
            "overrides": {"out_of_pool": allow_out_of_pool, "role_or_lifecycle": role_override},
            "limits": {key: config[key] for key in ("max_parallel_workers", "max_external_sessions_per_assignment")},
            "notice": "Eligibility only, not measured suitability, account access, or dispatch verification."}
    if unavailable:
        result["unavailable_profiles"] = unavailable
    if burn_provider:
        result["burn"] = {"provider": burn_provider, "account": burn_account, "endpoint": burn_endpoint}
        if any(choice["provider"] != burn_provider for choice in choices):
            result["burn"]["out_of_provider_exception"] = True
            result["notice"] += " Explicit cross-provider exception. The selected burn account does not apply to this worker."
    return result


def launch_plan(resolved, cwd, prompt_file, artifacts, resume=None):
    require(len(resolved["choices"]) == 1, "Select one explicit --profile for a launch plan")
    choice = resolved["choices"][0]
    require(choice.get("executable", True), "Documentary catalog record has no verified executable configuration")
    require(choice["provider"] in {"codex", "claude"},
            f"No bundled launch adapter for provider {choice['provider']}; use a separately verified provider adapter")
    require(choice["dispatch"].startswith("external-"), "Native routes require the host's worker controls, not an external CLI launch plan")
    cwd, prompt_file, artifacts = (str(Path(path).expanduser().resolve()) for path in (cwd, prompt_file, artifacts))
    require(Path(cwd).is_dir(), "cwd must be an existing directory")
    require(Path(prompt_file).is_file(), "prompt file must exist")
    if resume:
        uuid.UUID(resume)
    plan = {"executes": False, "profile": choice, "cwd": cwd, "stdin_file": prompt_file,
            "stdout_file": str(Path(artifacts) / "result.json"), "stderr_file": str(Path(artifacts) / "stderr.log"),
            "required_checks": ["signed-in subscription route", "exact returned model", "requested effort versus effective effort", "exit status and complete result", "owned-process lifecycle"],
            "environment_unset": [], "timeout_seconds": None}
    if "burn" in resolved:
        plan["burn"] = deepcopy(resolved["burn"])
        plan["required_checks"].append("explicit burn authorization, identified provider account and endpoint, authorized queue, and prior mode")
        if resolved["burn"].get("out_of_provider_exception"):
            plan["required_checks"].append("explicit cross-provider exception uses a separate account route, not the selected burn account")
    if choice["provider"] == "codex":
        require(not resume, "Codex resume planning is not implemented; use the documented exact-session CLI route")
        require(choice.get("service_tier", "standard") == "standard", "Only Standard service tier is supported")
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
        plan["required_checks"] += ["Standard service tier on the actual route", "configured approval policy supported by unattended route", "sandbox does not constrain connector side effects", "no recursive controller launches", "caller-supplied deadline if required"]
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


def agent_name(code, item):
    return item["provider"] + "-" + code.lower()


def codex_write_roles(config):
    """Roles whose Codex sandbox is workspace-write; plugin agents support only unattended read-only/workspace-write threads."""
    codex = config["codex"]
    require(not codex["bypass_approvals_and_sandbox"] and codex["approval_policy"] == "never",
            "Codex plugin agents run unattended app-server threads: approval_policy must be never and bypass disabled")
    sandboxes = {role: codex["sandbox_by_role"].get(role, codex["sandbox_by_role"]["default"]) for role in config["roles"]}
    require(set(sandboxes.values()) <= {"read-only", "workspace-write"},
            "Codex plugin agents support only read-only and workspace-write sandboxes")
    return [role for role in config["roles"] if sandboxes[role] == "workspace-write"]


def frontmatter(fields):
    return "---\n" + "".join(f"{key}: {value}\n" for key, value in fields.items()) + "---\n"


def codex_agent(config, code, item):
    write_roles = codex_write_roles(config)
    read_roles = [role for role in config["roles"] if role not in write_roles]
    summary = f"profile {code} (Codex {item['model']}, {item['effort']})"
    return frontmatter({
        "name": agent_name(code, item),
        "description": f"Router-only relay for {summary}. Dispatch only when agent-orch-router selects {code}.",
        "model": RELAY["model"], "effort": RELAY["effort"], "tools": "Bash"}) + f"""
You relay one agent-orch-router work order to {summary}. You are a forwarder, not a worker.

Your prompt has a `Role:` line, a `Work order file:` line with an absolute path, and optionally a `Resume thread:` line.

1. Roles {", ".join(read_roles)} run read-only. Roles {", ".join(write_roles)} add `--write`. If the role is missing or not listed, return `RELAY ERROR: missing or unknown Role` and run nothing.
2. Use the work order file only if its path is absolute and contains no double quote, backtick, dollar sign, or line break. Otherwise return `RELAY ERROR: unusable Work order file` and run nothing.
3. If there is a `Resume thread:` id, add `--resume-thread <id>`. Use it only if it contains just letters, digits, hyphens, and underscores. Otherwise return `RELAY ERROR: unusable Resume thread` and run nothing.
4. Run exactly one single-line Bash command:

```bash
node "${{CLAUDE_PLUGIN_ROOT}}/runtime/codex/scripts/codex-companion.mjs" task --json --model {item['model']} --effort {item['effort']} [--write] [--resume-thread <id>] --prompt-file "<work order file>"
```

5. Return the command's stdout exactly. If the command fails, return its stderr and exit status exactly.

Do not read or edit files, inspect the repository, retry, poll, change the model, effort, or sandbox, or add commentary.
"""


def claude_agent(config, code, item):
    fields = {"name": agent_name(code, item),
              "description": f"Router-only worker for profile {code} ({item['model']}, {item['effort']}). Dispatch only when agent-orch-router selects {code}.",
              "model": item["model"], "effort": item["effort"]}
    target = item.get("context_target_tokens")
    if target:
        require(100000 <= target <= 1000000, f"Context target for {code} is outside the supported auto-compact window")
        fields["autoCompactWindow"] = target  # A compaction threshold, still a soft context target.
    return frontmatter(fields) + f"""
You are an agent-orch-router worker for profile {code}: `{item['model']}` at effort `{item['effort']}`. Complete only the attached work order.

- Change only files matching its `Write:` list. Treat `Forbidden:` paths and changes that existed before you started as read-only.
- If the work needs a change outside your `Write:` list, stop and return a handoff request naming the file, the change, and the reason. Do not make the change.
- Roles {", ".join(role for role in config["roles"] if role in REVIEW_ROLES)} do not edit files unless the work order explicitly authorizes edits.
- Run the listed acceptance checks. Return changed files, checks with results, findings, handoff requests, and anything unverified.
- Do not start other workers unless the work order assigns you a team role.
"""


def git_lines(cwd, *args):
    result = subprocess.run(["git", "-C", str(cwd), *args], capture_output=True)
    require(result.returncode == 0, f"git {args[0]} failed in {cwd}: {result.stderr.decode(errors='replace').strip()}")
    return [entry.decode() for entry in result.stdout.split(b"\0") if entry]


def source_files(prefix):
    """Tracked and untracked-but-not-ignored files, so ignored local material never enters the plugin."""
    return git_lines(ROOT, "ls-files", "-z", "--cached", "--others", "--exclude-standard", "--", prefix)


def plugin_files(config):
    require((ROOT / ".claude-plugin/marketplace.json").is_file(), "Run plugin generation from the repository checkout")
    files = {}
    for prefix in PLUGIN_COPIES:
        for rel in source_files(prefix):
            if not (ROOT / rel).is_file():
                continue
            data = (ROOT / rel).read_bytes()
            if rel == "skills/agent-orch-router/SKILL.md":
                head, separator, body = data.decode().partition("\n---\n")
                require(separator and head.startswith("---\n") and "disable-model-invocation" not in head, "Unexpected router frontmatter")
                require(body.count("\nOptional: ") == 1, "Router copy needs one Optional paragraph for the plugin pointer")
                # Host-specific installed copy: Claude Code may not invoke the router implicitly.
                body = body.replace("\nOptional: ", "\n" + PLUGIN_POINTER + "Optional: ")
                data = (head + "\ndisable-model-invocation: true" + separator + body).encode()
            files[rel] = data
    for code in config["profiles"]:
        item = profile(config, code)
        if not item.get("executable", True):
            continue  # Documentary catalog records have no verified model or effort to pin.
        if item["provider"] == "codex":
            files[f"agents/{agent_name(code, item)}.md"] = codex_agent(config, code, item).encode()
        elif item["provider"] == "claude":
            files[f"agents/{agent_name(code, item)}.md"] = claude_agent(config, code, item).encode()
    return files


def sync_plugin(config, check):
    expected = plugin_files(config)
    actual = {}
    for top in PLUGIN_GENERATED:
        path = PLUGIN_DIR / top
        candidates = [path] if path.is_file() else path.rglob("*") if path.is_dir() else []
        for item in candidates:
            if item.is_file() and not {"__pycache__", ".DS_Store"} & set(item.parts):
                actual[item.relative_to(PLUGIN_DIR).as_posix()] = item.read_bytes()
    stale = sorted(rel for rel in expected if actual.get(rel, expected[rel]) != expected[rel])
    missing = sorted(rel for rel in expected if rel not in actual)
    extra = sorted(rel for rel in actual if rel not in expected)
    if check:
        require(not (stale or missing or extra),
                f"Plugin copy is out of date (stale {stale}, missing {missing}, extra {extra}). Regenerate it with the plugin action.")
    else:
        for rel in stale + missing:
            (PLUGIN_DIR / rel).parent.mkdir(parents=True, exist_ok=True)
            (PLUGIN_DIR / rel).write_bytes(expected[rel])
        for rel in extra:
            (PLUGIN_DIR / rel).unlink()
    return {"plugin": PLUGIN_DIR.relative_to(ROOT).as_posix(), "in_sync": check or not (stale or missing or extra),
            "files": len(expected), "agents": sum(rel.startswith("agents/") for rel in expected),
            **({} if check else {"written": stale + missing, "removed": extra})}


def worktree_hashes(cwd, protect=()):
    """Hash tracked and untracked-unignored files, plus explicitly protected paths even when ignored."""
    paths = set(git_lines(cwd, "ls-files", "-z", "--cached", "--others", "--exclude-standard"))
    for spec in protect:
        target = cwd / spec
        if target.is_dir():
            paths.update(item.relative_to(cwd).as_posix() for item in target.rglob("*") if item.is_file() and ".git" not in item.parts)
        elif target.is_file():
            paths.add(target.relative_to(cwd).as_posix())
    return {rel: hashlib.sha256((cwd / rel).read_bytes()).hexdigest() for rel in sorted(paths) if (cwd / rel).is_file()}


def dirty_paths(cwd):
    entries, dirty = git_lines(cwd, "status", "--porcelain=v1", "-z", "--untracked-files=all"), []
    while entries:
        entry = entries.pop(0)
        dirty.append(entry[3:])
        if entry[0] in "RC":
            dirty.append(entries.pop(0))  # Rename/copy source path follows the destination.
    return sorted(set(dirty))


def snapshot(cwd, out, protect=()):
    cwd, out = Path(cwd).expanduser().resolve(), Path(out).expanduser().resolve()
    require(cwd.is_dir(), "cwd must be an existing directory")
    require(not out.is_relative_to(cwd), "Write snapshots outside the project so they are not reported as changes")
    protect = sorted({spec.rstrip("/") + ("/" if (cwd / spec).is_dir() else "") for spec in protect})
    head = subprocess.run(["git", "-C", str(cwd), "rev-parse", "HEAD"], capture_output=True, text=True)
    record = {"schema": 1, "cwd": str(cwd), "head": head.stdout.strip() or None, "protected": protect,
              "dirty": dirty_paths(cwd), "files": worktree_hashes(cwd, protect)}
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(record, indent=1) + "\n")
    return {"snapshot": str(out), "files": len(record["files"]), "dirty": record["dirty"], "protected": protect}


def owns(pattern, path):
    """A trailing slash owns a directory tree; otherwise fnmatch, where `*` also crosses `/`."""
    pattern = pattern[2:] if pattern.startswith("./") else pattern
    return path.startswith(pattern) if pattern.endswith("/") else fnmatchcase(path, pattern)


def check_ownership(snapshot_file, owners_file):
    """Pre-dispatch: overlapping or dirty-file ownership. Post-dispatch: changes outside every owner's Write list."""
    base = json.loads(Path(snapshot_file).read_text())
    require(base.get("schema") == 1, "Unsupported snapshot")
    owners = json.loads(Path(owners_file).read_text())
    require(isinstance(owners, dict) and owners and all(isinstance(pats, list) and pats and all(isinstance(p, str) and p for p in pats)
                                                         for pats in owners.values()),
            "Owners must map each worker to a non-empty list of path patterns")
    cwd = Path(base["cwd"])
    current = worktree_hashes(cwd, base["protected"])
    universe = sorted(set(base["files"]) | set(current))

    def owners_of(path):
        return sorted(worker for worker, patterns in owners.items() if any(owns(p, path) for p in patterns))

    names = sorted(owners)
    overlaps = []
    for index, first in enumerate(names):
        for second in names[index + 1:]:
            shared = [path for path in universe if {first, second} <= set(owners_of(path))]
            literal = [p for p in owners[first] for q in owners[second]
                       if p == q or owns(p, q.rstrip("/")) or owns(q, p.rstrip("/"))]
            if shared or literal:
                overlaps.append({"workers": [first, second], "files": shared, "patterns": sorted(set(literal))})
    changes = {"added": sorted(set(current) - set(base["files"])), "deleted": sorted(set(base["files"]) - set(current)),
               "modified": sorted(path for path in set(current) & set(base["files"]) if current[path] != base["files"][path])}
    changed = sorted(path for paths in changes.values() for path in paths)
    result = {
        "ok": True, "overlaps": overlaps,
        "owned_dirty": [{"file": path, "workers": owners_of(path)} for path in base["dirty"] if owners_of(path)],
        "changes": {path: owners_of(path) for path in changed},
        "unowned_changes": [path for path in changed if not owners_of(path)],
        "multiply_owned_changes": [path for path in changed if len(owners_of(path)) > 1],
        "protected_changes": [path for path in changed if any(owns(spec, path) for spec in base["protected"])],
        "notice": "Ignored files outside protected paths are not tracked. Cross-check each worker's reported touched files."}
    result["ok"] = not any(result[key] for key in ("overlaps", "owned_dirty", "unowned_changes", "multiply_owned_changes", "protected_changes"))
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["validate", "resolve", "claude-plan", "codex-plan", "plugin", "snapshot", "check-ownership"])
    parser.add_argument("--config", type=Path)
    parser.add_argument("--preset", action="append", default=[])
    parser.add_argument("--overlay", type=Path, action="append", default=[])
    parser.add_argument("--mode")
    parser.add_argument("--variant", help="Pool preference only, independent of controller design")
    parser.add_argument("--bias", choices=["low", "default", "high"], help="Selection preference, never a reasoning-effort override")
    parser.add_argument("--burn-account", help="Non-secret account identifier for the selected burn provider")
    parser.add_argument("--burn-endpoint", help="Identified reset/deadline or authorized queue endpoint")
    parser.add_argument("--profile")
    parser.add_argument("--slot", help="Stable job slot from the active mode's bindings")
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
    parser.add_argument("--check", action="store_true", help="plugin: verify the generated plugin copy without writing")
    parser.add_argument("--out", help="snapshot: JSON file outside the project")
    parser.add_argument("--protect", action="append", default=[], help="snapshot: path to watch even if ignored")
    parser.add_argument("--snapshot", help="check-ownership: snapshot JSON")
    parser.add_argument("--owners", help="check-ownership: JSON mapping each worker to its Write patterns")
    args = parser.parse_args(argv)
    try:
        config = load_config(args.config, args.preset, args.overlay)
        require(not args.direct or args.action == "claude-plan", "--direct applies only to claude-plan")
        if args.action == "plugin":
            require(not (args.config or args.preset or args.overlay), "The plugin copy is generated from the bundled configuration only")
            output = sync_plugin(config, args.check)
        elif args.action == "snapshot":
            require(args.cwd and args.out, "snapshot requires --cwd and --out")
            output = snapshot(args.cwd, args.out, args.protect)
        elif args.action == "check-ownership":
            require(args.snapshot and args.owners, "check-ownership requires --snapshot and --owners")
            output = check_ownership(args.snapshot, args.owners)
        elif args.action == "validate":
            output = {"valid": True, "profiles": len(config["profiles"]), "variant": args.variant or config.get("default_variant"),
                      "modes": list(mode_pools(config, args.variant))}
        else:
            role = args.role or ("qa" if args.action == "claude-plan" else "implementation")
            code = args.profile or (config["claude"]["default_profile"] if args.action == "claude-plan" and not args.slot else None)
            mode = args.mode
            claude_mode = args.claude_mode
            if args.direct:
                require(not mode, "Standalone --direct does not use a router --mode")
                config = deepcopy(config)
                config["modes"]["direct-claude"] = [{"profile": code}]
                mode = "direct-claude"
                if args.role is None and claude_mode is None:
                    claude_mode = config["claude"]["default_mode"]
            output = resolve(config, mode=mode, code=code, slot=args.slot, role=role, design=args.design,
                             assignment_kind=args.assignment_kind, ongoing=args.ongoing_thread, final=args.final_review,
                             allow_out_of_pool=args.allow_out_of_pool, role_override=args.role_override, claude_mode=claude_mode,
                             burn_account=args.burn_account, burn_endpoint=args.burn_endpoint, variant=args.variant, bias=args.bias)
            if args.action.endswith("-plan"):
                require(args.cwd and args.prompt_file and args.artifacts, "Launch planning requires --cwd, --prompt-file, and --artifacts")
                require(len(output["choices"]) == 1 and output["choices"][0]["provider"] == args.action.split("-")[0], "Profile provider does not match the requested adapter")
                output = launch_plan(output, args.cwd, args.prompt_file, args.artifacts, args.resume)
        print(json.dumps(output, indent=2))
        return 1 if output.get("ok") is False else 0
    except (KeyError, TypeError, ValueError, OSError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    sys.exit(main())
