"""Offline configuration and launch-contract tests. No model subprocesses."""

from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import re
import shlex
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("bundle", ROOT / "scripts/bundle.py")
bundle = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bundle)


class RoutingTests(unittest.TestCase):
    def setUp(self):
        self.config = bundle.load_config()

    def resolve(self, **kwargs):
        return bundle.resolve(self.config, **kwargs)

    def test_default_config_and_standard_catalog(self):
        self.assertEqual(self.config["controller_design"], "codex-first")
        self.assertFalse(self.config["claude"]["modes"]["orchestration"]["enabled"])
        self.assertEqual(bundle.profile(self.config, "SNX")["effort"], "xhigh")
        self.assertEqual(bundle.profile(self.config, "SNX")["model"], "claude-sonnet-5-5")
        self.assertTrue(all(item["service_tier"] == "standard" for item in self.config["profiles"].values()
                            if item["provider"] == "codex"))
        self.assertEqual(self.resolve()["routing_variant"], "codex-primary")
        self.assertEqual([entry["profile"] for entry in bundle.mode_pools(self.config)["balanced"]],
                         ["SL", "TM", "TH", "SM", "SH", "SX", "SMAX", "AL", "OH"])

    def test_designs_invert_native_and_external_routes(self):
        for design, codex, claude in [("codex-first", "native-codex", "external-claude"),
                                       ("claude-first", "external-codex", "native-claude")]:
            self.assertEqual(self.resolve(code="SM", design=design)["choices"][0]["dispatch"], codex)
            self.assertEqual(self.resolve(code="OH", role="qa", design=design)["choices"][0]["dispatch"], claude)

    def test_role_boundary_is_not_waived_by_model_code(self):
        with self.assertRaisesRegex(ValueError, "role/lifecycle"):
            self.resolve(code="OH", role="implementation")
        allowed = self.resolve(code="OH", role="implementation", role_override=True)
        self.assertTrue(allowed["overrides"]["role_or_lifecycle"])

    def test_explicit_permission_role_is_independent_of_review_routing(self):
        result = self.resolve(code="OH", role="qa", claude_mode="implementation")
        self.assertEqual(result["choices"][0]["claude_mode"], "implementation")
        self.assertEqual(result["role"], "qa")

    def test_one_off_restriction(self):
        with self.assertRaisesRegex(ValueError, "role/lifecycle"):
            self.resolve(code="HM", variant="claude-primary", assignment_kind="controller")

    def test_ongoing_thread_and_final_review_are_separate(self):
        self.config["modes"]["restricted-review"] = [{"profile": "OX", "roles": ["qa", "spec-review"],
                                                     "ongoing_thread_only": True, "final_only": True}]
        for kwargs in ({}, {"ongoing": True}, {"final": True}):
            with self.assertRaisesRegex(ValueError, "role/lifecycle"):
                self.resolve(mode="restricted-review", code="OX", role="qa", **kwargs)
        result = self.resolve(mode="restricted-review", code="OX", role="qa", ongoing=True, final=True)
        self.assertEqual(result["choices"][0]["claude_mode"], "consultation")

    def test_browser_specialists(self):
        self.assertEqual(self.resolve(mode="balanced", role="browser")["choices"][0]["code"], "AL")
        self.assertEqual(self.resolve(mode="performance", role="browser")["choices"][0]["code"], "AH")
        self.assertEqual(self.resolve(mode="performance", role="browser", variant="claude-primary")["choices"][0]["code"], "AMAX")
        # Browser-specialist preference is not an assertion that other models lack browser capability.
        self.assertEqual(self.resolve(mode="balanced", role="browser", code="SM")["choices"][0]["code"], "SM")
        self.assertEqual(self.resolve(mode="codex-burn", role="browser", burn_account="codex-work",
                                      burn_endpoint="next reset")["choices"][0]["code"], "AL")

    def test_burn_modes_are_provider_exclusive_under_both_designs(self):
        for mode, provider, expected in [("codex-burn", "codex", ["AL", "SM", "SH", "SX", "AH", "AMAX"]),
                                          ("claude-burn", "claude", ["HMAX", "SNH", "OM", "OH", "OX", "OMAX"])]:
            self.assertEqual([entry["profile"] for entry in self.config["modes"][mode]], expected)
            for design in ("codex-first", "claude-first"):
                for role in self.config["roles"]:
                    result = self.resolve(mode=mode, design=design, role=role, burn_account="work-account", burn_endpoint="reset")
                    self.assertTrue(all(choice["provider"] == provider for choice in result["choices"]))
                    dispatch = ("native-" if design == provider + "-first" else "external-") + provider
                    self.assertTrue(all(choice["dispatch"] == dispatch for choice in result["choices"]))
                    self.assertEqual(result["burn"], {"provider": provider, "account": "work-account", "endpoint": "reset"})
            other = "OH" if provider == "codex" else "SM"
            with self.assertRaisesRegex(ValueError, "outside"):
                self.resolve(mode=mode, code=other, role="qa", burn_account="work-account", burn_endpoint="reset")
            exception = self.resolve(mode=mode, code=other, role="qa", allow_out_of_pool=True, role_override=True,
                                     burn_account="work-account", burn_endpoint="reset")
            self.assertTrue(exception["burn"]["out_of_provider_exception"])
            self.assertIn("does not apply", exception["notice"])
            self.assertTrue(exception["overrides"]["out_of_pool"])
            with self.assertRaisesRegex(ValueError, "profiles only"):
                bundle.validate(bundle.merge(self.config, {"modes": {mode: [{"profile": other}]}}))

    def test_burn_modes_require_explicit_invocation_account_and_endpoint(self):
        for mode in bundle.BURN_PROVIDERS:
            for kwargs in ({}, {"burn_account": "account"}, {"burn_endpoint": "reset"},
                           {"burn_account": " ", "burn_endpoint": "reset"}):
                with self.assertRaisesRegex(ValueError, "identified"):
                    self.resolve(mode=mode, **kwargs)
            self.config["default_mode"] = mode
            with self.assertRaisesRegex(ValueError, "explicit invocation"):
                self.resolve(burn_account="account", burn_endpoint="reset")
        with self.assertRaisesRegex(ValueError, "only to burn"):
            self.resolve(mode="balanced", burn_account="account", burn_endpoint="reset")

    def test_claude_burn_native_haiku_and_role_limits_remain_independent(self):
        kwargs = {"mode": "claude-burn", "burn_account": "claude-work", "burn_endpoint": "queue end"}
        haiku = self.resolve(code="HMAX", design="claude-first", **kwargs)["choices"][0]
        self.assertEqual(haiku["dispatch"], "native-claude")
        self.assertEqual(haiku["model"], "claude-haiku-5-5")
        self.assertEqual(haiku["claude_mode"], "implementation")
        for code, extra in [("HMAX", {"assignment_kind": "controller"})]:
            with self.assertRaisesRegex(ValueError, "role/lifecycle"):
                self.resolve(code=code, **kwargs, **extra)
        for code in ("OM", "OH", "OX", "OMAX"):
            self.assertEqual(self.resolve(code=code, **kwargs)["choices"][0]["claude_mode"], "implementation")
        result = self.resolve(code="SNH", role="qa", claude_mode="implementation", **kwargs)
        self.assertEqual(result["choices"][0]["claude_mode"], "implementation")
        self.assertEqual(result["role"], "qa")

    def test_retired_modes_and_codes_fail_without_fallback(self):
        for mode in ("fast", "tokenburn"):
            with self.assertRaisesRegex(ValueError, "retired.*explicitly"):
                self.resolve(mode=mode)
            with self.assertRaisesRegex(ValueError, "retired"):
                bundle.validate(bundle.merge(self.config, {"modes": {mode: [{"profile": "SM"}]}}))
        for code in bundle.RETIRED_PROFILES:
            self.assertNotIn(code, self.config["profiles"])
            with self.assertRaisesRegex(ValueError, "retired.*explicitly"):
                self.resolve(code=code, allow_out_of_pool=True, role_override=True)
            with self.assertRaisesRegex(ValueError, "retired"):
                bundle.validate(bundle.merge(self.config, {"profiles": {code: {"alias_of": "SM"}}}))
        with self.assertRaisesRegex(ValueError, "Standard"):
            bundle.validate(bundle.merge(self.config, {"profiles": {"SM": {"service_tier": "fast"}}}))
        with self.assertRaisesRegex(ValueError, "Sonnet Max"):
            bundle.validate(bundle.merge(self.config, {"profiles": {"SNX": {"effort": "max"}}}))

    def test_out_of_pool_requires_separate_pool_and_eligibility_overrides(self):
        for mode, code, role in [("balanced", "L", "implementation"), ("codex-burn", "OH", "qa"),
                                 ("codex-burn", "OX", "implementation"), ("claude-burn", "AM", "implementation")]:
            with self.subTest(mode=mode, code=code, role=role):
                kwargs = {"mode": mode, "code": code, "role": role}
                if mode in bundle.BURN_PROVIDERS:
                    kwargs.update(burn_account="work-account", burn_endpoint="queue end")
                for overrides in ({}, {"role_override": True}):
                    with self.assertRaisesRegex(ValueError, "outside"):
                        self.resolve(**kwargs, **overrides)
                with self.assertRaisesRegex(ValueError, "no role/lifecycle eligibility.*--role-override"):
                    self.resolve(**kwargs, allow_out_of_pool=True)
                result = self.resolve(**kwargs, allow_out_of_pool=True, role_override=True)
                self.assertEqual(result["choices"][0]["code"], code)
                self.assertEqual(result["overrides"], {"out_of_pool": True, "role_or_lifecycle": True})

    def test_pool_override_does_not_waive_in_pool_role_or_lifecycle_fences(self):
        for kwargs in ({"code": "OH", "role": "implementation"},
                       {"code": "HM", "variant": "claude-primary", "assignment_kind": "controller"},
                       {"code": "OX", "mode": "performance", "role": "implementation"}):
            with self.subTest(**kwargs):
                with self.assertRaisesRegex(ValueError, "role/lifecycle restrictions"):
                    self.resolve(**kwargs, allow_out_of_pool=True)
        allowed = self.resolve(code="OH", role="qa", allow_out_of_pool=True)
        self.assertFalse(allowed["overrides"]["role_or_lifecycle"])

    def test_invalid_mode_profile_role_and_alias_cycle(self):
        for kwargs in ({"mode": "missing"}, {"code": "missing"}, {"role": "missing"}):
            with self.assertRaises(ValueError):
                self.resolve(**kwargs)
        self.config["profiles"]["SM"] = {"alias_of": "SH"}
        self.config["profiles"]["SH"] = {"alias_of": "SM"}
        with self.assertRaisesRegex(ValueError, "cycle"):
            bundle.validate(self.config)

    def test_merge_replaces_arrays_and_preserves_other_settings(self):
        result = bundle.merge(self.config, {"modes": {"balanced": [{"profile": "SM"}]},
                                           "claude": {"modes": {"implementation": {"timeout_seconds": 42}}}})
        bundle.validate(result)
        self.assertEqual(len(result["modes"]["balanced"]), 1)
        self.assertEqual(result["claude"]["modes"]["implementation"]["timeout_seconds"], 42)
        self.assertIsNone(result["claude"]["modes"]["orchestration"]["timeout_seconds"])

    def test_permission_choices_are_configurable_not_role_locked(self):
        for patch in ({"consultation": {"tools": ["Read", "Bash"]}},
                      {"consultation": {"permission_mode": "auto"}},
                      {"implementation": {"permission_mode": "bypassPermissions"}}):
            bundle.validate(bundle.merge(self.config, {"claude": {"modes": patch}}))

    def test_validation_rejects_technical_conflicts_and_invalid_permissions(self):
        for patch in ({"consultation": {"restricted": True, "permission_mode": "bypassPermissions"}},
                      {"implementation": {"permission_mode": "invalid-mode"}},
                      {"implementation": {"tools": {"not": "a tool list"}}}):
            with self.assertRaises(ValueError):
                bundle.validate(bundle.merge(self.config, {"claude": {"modes": patch}}))

    def test_invalid_deadlines_and_concurrency(self):
        for value in (0, -1, True, "3600"):
            with self.assertRaises(ValueError):
                bundle.validate(bundle.merge(self.config, {"claude": {"modes": {"implementation": {"timeout_seconds": value}}}}))
        with self.assertRaises(ValueError):
            bundle.validate(bundle.merge(self.config, {"max_parallel_workers": 0}))

    def test_disabling_preset_with_later_local_policy(self):
        self.config = bundle.load_config(presets=["opus-haiku"])
        self.config["claude"]["modes"]["orchestration"]["enabled"] = False
        with self.assertRaisesRegex(ValueError, "disabled"):
            self.resolve(mode="opus-haiku", code="OH", claude_mode="orchestration")

    def test_no_silent_orchestration_or_model_substitution(self):
        with self.assertRaisesRegex(ValueError, "disabled"):
            self.resolve(code="OH", role_override=True, claude_mode="orchestration")
        result = self.resolve(code="OH", role="frontend", variant="claude-primary")
        self.assertEqual(result["choices"][0]["model"], "claude-opus-5-5")
        self.assertEqual(result["choices"][0]["claude_mode"], "implementation")


class VariantTests(unittest.TestCase):
    def setUp(self):
        self.config = bundle.load_config()

    def test_exact_bundled_pools_and_counts(self):
        expected = {
            "codex-primary": {
                "efficient": ["LM", "TL", "SL", "TM", "TH", "SM", "SH"],
                "balanced": ["SL", "TM", "TH", "SM", "SH", "SX", "SMAX", "AL", "OH"],
                "performance": ["SH", "SX", "SMAX", "AMAX", "AH", "OX", "OMAX"]},
            "claude-primary": {
                "efficient": ["HMED", "HH", "HM", "HMAX", "SNH", "OM", "OH"],
                "balanced": ["HH", "HM", "HMAX", "SNH", "OM", "OH", "OX", "SM", "SMAX"],
                "performance": ["OM", "OH", "OX", "OMAX", "SMAX", "AMAX"]}}
        for variant, modes in expected.items():
            actual = bundle.mode_pools(self.config, variant)
            self.assertEqual(set(actual), {"efficient", "balanced", "performance", "high-qual", "codex-burn", "claude-burn"})
            for mode, codes in modes.items():
                self.assertEqual([entry["profile"] for entry in actual[mode]], codes)
        for mode in bundle.BURN_PROVIDERS:
            self.assertEqual(bundle.mode_pools(self.config, "codex-primary")[mode],
                             bundle.mode_pools(self.config, "claude-primary")[mode])
            self.assertTrue(all(mode not in variant["modes"] for variant in self.config["variants"].values()))

    def test_exact_catalog_ids_efforts_and_retained_meanings(self):
        families = {
            "gpt-6-luna": {"LM": "medium", "L": "max"},
            "gpt-6.1-terra": {"TL": "low", "TM": "medium", "TH": "high"},
            "gpt-6.1-sol": {"SL": "low", "SM": "medium", "SH": "high", "SX": "xhigh", "SMAX": "max"},
            "gpt-6-astra": {"AL": "low", "AM": "medium", "AH": "high", "AX": "xhigh", "AMAX": "max", "AU": "ultra"},
            "claude-haiku-5-5": {"HMED": "medium", "HH": "high", "HM": "xhigh", "HK": "xhigh", "HMAX": "max"},
            "claude-sonnet-5-5": {"SNH": "high", "SNX": "xhigh"},
            "claude-opus-5-5": {"OM": "medium", "OH": "high", "OX": "xhigh", "OMAX": "max"},
            "claude-fable-5-1": {"FH": "high", "FX": "xhigh"},
            "muse-wonder-full-1.0": {"MFH": "high", "MFX": "xhigh"}}
        self.assertEqual(set(self.config["profiles"]), {code for efforts in families.values() for code in efforts})
        for model, efforts in families.items():
            for code, effort in efforts.items():
                item = bundle.profile(self.config, code)
                self.assertEqual((item["model"], item["effort"]), (model, effort))
                expected_provider = "codex" if model.startswith("gpt-") else "muse" if model.startswith("muse-") else "claude"
                self.assertEqual(item["provider"], expected_provider)
                self.assertTrue(item["description"].strip())
        self.assertEqual(bundle.profile(self.config, "HK")["context_target_tokens"], 100000)
        self.assertIsNone(bundle.profile(self.config, "HM")["context_target_tokens"])

    def test_variants_all_modes_roles_and_designs_have_eligible_workers(self):
        for variant in self.config["variants"]:
            for mode in bundle.mode_pools(self.config, variant):
                for role in self.config["roles"]:
                    for design in self.config["designs"]:
                        kwargs = {"burn_account": "work", "burn_endpoint": "queue end"} if mode in bundle.BURN_PROVIDERS else {}
                        result = bundle.resolve(self.config, variant=variant, mode=mode, role=role, design=design, **kwargs)
                        self.assertTrue(result["choices"])
                        self.assertEqual(result["routing_variant"], variant)
                        for item in result["choices"]:
                            expected = ("native-" if item["provider"] == result["controller"] else "external-") + item["provider"]
                            self.assertEqual(item["dispatch"], expected)
                            if mode in bundle.BURN_PROVIDERS:
                                self.assertEqual(item["provider"], bundle.BURN_PROVIDERS[mode])

    def test_variant_does_not_change_controller_permissions_or_effort(self):
        for variant in self.config["variants"]:
            for bias in ("low", "default", "high"):
                result = bundle.resolve(self.config, variant=variant, bias=bias)
                self.assertEqual(result["controller_design"], "codex-first")
                self.assertEqual(result["selection_bias"], bias)
                for item in result["choices"]:
                    self.assertEqual(item["effort"], bundle.profile(self.config, item["code"])["effort"])
                if bias == "low":
                    baseline = [(item["code"], item["effort"]) for item in result["choices"]]
                self.assertEqual([(item["code"], item["effort"]) for item in result["choices"]], baseline)
        native = bundle.resolve(self.config, variant="claude-primary", design="claude-first", code="OH")
        self.assertEqual(native["choices"][0]["dispatch"], "native-claude")
        self.assertEqual(native["choices"][0]["execution"], self.config["claude"]["modes"]["implementation"])

    def test_general_opus_implementation_and_optional_review(self):
        for mode, codes in [("efficient", ["OM", "OH"]), ("balanced", ["OM", "OH", "OX"]),
                            ("performance", ["OM", "OH", "OX", "OMAX"])]:
            for code in codes:
                result = bundle.resolve(self.config, variant="claude-primary", mode=mode, code=code)
                self.assertEqual(result["choices"][0]["claude_mode"], "implementation")
                self.assertFalse(result["overrides"]["role_or_lifecycle"])
        review = bundle.resolve(self.config, variant="claude-primary", code="SM", role="qa")
        self.assertTrue(review["choices"][0]["independent_review"])
        with self.assertRaisesRegex(ValueError, "role/lifecycle"):
            bundle.resolve(self.config, variant="claude-primary", code="SM", role="implementation")
        authored = bundle.resolve(self.config, variant="claude-primary", code="OH")
        self.assertNotIn("independent_review", authored["choices"][0])
        escalation = bundle.resolve(self.config, mode="performance", code="OMAX")
        self.assertTrue(escalation["choices"][0]["escalation"])

    def test_custom_variant_overlays_legacy_modes_and_presets(self):
        config = bundle.merge(self.config, {"variants": {"claude-primary": {"modes": {"balanced": [{"profile": "OM"}]}}}})
        bundle.validate(config)
        self.assertEqual([item["code"] for item in bundle.resolve(config, variant="claude-primary")["choices"]], ["OM"])
        config = bundle.merge(config, {"modes": {"balanced": [{"profile": "SH"}]}})
        bundle.validate(config)
        for variant in config["variants"]:
            self.assertEqual([item["code"] for item in bundle.resolve(config, variant=variant)["choices"]], ["SH"])
        legacy = deepcopy(config)
        del legacy["variants"], legacy["default_variant"]
        bundle.validate(legacy)
        self.assertIsNone(bundle.resolve(legacy)["routing_variant"])
        for variant in self.config["variants"]:
            config = bundle.load_config(presets=["opus-haiku"])
            bundle.validate(config)
            result = bundle.resolve(config, variant=variant, mode="opus-haiku", code="OH", claude_mode="orchestration")
            self.assertIsNone(result["choices"][0]["execution"]["timeout_seconds"])
        with self.assertRaisesRegex(ValueError, "Unknown routing variant"):
            bundle.resolve(self.config, variant="missing")
        with self.assertRaisesRegex(ValueError, "shared top-level"):
            bundle.validate(bundle.merge(self.config, {"variants": {"codex-primary": {"modes": {"codex-burn": [{"profile": "SH"}]}}}}))

    def test_fable_outside_other_pools_and_preset(self):
        config = bundle.load_config(presets=["opus-haiku"])
        for variant in config["variants"]:
            for mode, pool in bundle.mode_pools(config, variant).items():
                self.assertEqual({"FH", "FX"} & {entry["profile"] for entry in pool},
                                 {"FX"} if mode == "high-qual" else set())
            for code in ("FH", "FX"):
                with self.assertRaisesRegex(ValueError, "outside"):
                    bundle.resolve(config, variant=variant, code=code)
                with self.assertRaisesRegex(ValueError, "--role-override"):
                    bundle.resolve(config, variant=variant, code=code, allow_out_of_pool=True)
                result = bundle.resolve(config, variant=variant, code=code, allow_out_of_pool=True, role_override=True)
                self.assertEqual(result["choices"][0]["model"], "claude-fable-5-1")

    def test_high_qual_is_shared_non_burn_with_nonpreemptive_role_fences(self):
        expected = ["SM", "SX", "OM", "OX", "AX", "FX", "MFH", "MFX"]
        for variant in self.config["variants"]:
            pool = bundle.mode_pools(self.config, variant)["high-qual"]
            self.assertEqual([entry["profile"] for entry in pool], expected)
            self.assertNotIn("high-qual", self.config["variants"][variant]["modes"])
            self.assertFalse(any(entry.get("specialist") for entry in pool))
            for role, codes in {
                "implementation": ["SM", "SX", "OM"],
                "research": ["SM", "SX", "OM", "MFH", "MFX"],
                "planning": ["SM", "SX", "OM", "OX", "MFH", "MFX"],
                "qa": ["SM", "SX", "OM", "OX", "AX", "MFH", "MFX"],
                "spec-review": ["SM", "SX", "OM", "OX", "FX"],
                "browser": ["SM", "SX", "OM", "AX"]}.items():
                result = bundle.resolve(self.config, mode="high-qual", variant=variant, role=role)
                self.assertEqual([choice["code"] for choice in result["choices"]], codes)
                self.assertNotIn("burn", result)
        for code in ("OX", "AX", "FX", "MFH", "MFX"):
            with self.assertRaisesRegex(ValueError, "role/lifecycle"):
                bundle.resolve(self.config, mode="high-qual", code=code, role="implementation")
        with self.assertRaisesRegex(ValueError, "only to burn"):
            bundle.resolve(self.config, mode="high-qual", burn_account="work", burn_endpoint="reset")

    def test_muse_is_external_without_codex_or_claude_execution_settings(self):
        for code, effort in (("MFH", "high"), ("MFX", "xhigh")):
            for design in self.config["designs"]:
                choice = bundle.resolve(self.config, mode="high-qual", code=code, role="research", design=design)["choices"][0]
                self.assertEqual((choice["provider"], choice["model"], choice["effort"], choice["dispatch"]),
                                 ("muse", "muse-wonder-full-1.0", effort, "external-muse"))
                self.assertEqual(set(choice["execution"]), {"launch_plan_supported", "adapter_required", "notice"})
                self.assertFalse(choice["execution"]["launch_plan_supported"])
                self.assertTrue(choice["execution"]["adapter_required"])
                self.assertNotIn("claude_mode", choice)
        with self.assertRaisesRegex(ValueError, "Unknown provider"):
            bundle.validate(bundle.merge(self.config, {"profiles": {"MFH": {"provider": "unknown"}}}))


class PlanTests(unittest.TestCase):
    def setUp(self):
        self.config = bundle.load_config()
        self.cwd = str(ROOT)
        self.prompt = str(Path(__file__))
        self.artifacts = str(ROOT / ".runs/test")

    def plan(self, *, config=None, resume=None, **kwargs):
        resolved = bundle.resolve(config or self.config, **kwargs)
        return bundle.launch_plan(resolved, self.cwd, self.prompt, self.artifacts, resume)

    @staticmethod
    def value(args, flag):
        return args[args.index(flag) + 1]

    def test_consultation_tools_and_spawn_restrictions(self):
        plan = self.plan(code="OH", role="qa")
        args = plan["argv"]
        definitions = json.loads(self.value(args, "--agents"))
        self.assertEqual(definitions["review-worker"]["tools"], ["Read", "Glob", "Grep"])
        self.assertEqual(definitions["consultation-controller"]["tools"][-1], "Agent(review-worker)")
        self.assertNotIn("Agent", definitions["review-worker"]["tools"])
        self.assertIn("--restricted", args)
        self.assertNotIn("--safe-mode", args)
        self.assertNotIn("maxTurns", definitions["review-worker"])
        self.assertEqual(plan["timeout_seconds"], 3600)

    def test_consultation_can_disable_reviewers(self):
        config = bundle.merge(self.config, {"claude": {"modes": {"consultation": {"reviewer": {"enabled": False}}}}})
        plan = self.plan(config=config, code="OH", role="qa")
        self.assertNotIn("--agents", plan["argv"])
        self.assertEqual(self.value(plan["argv"], "--tools"), "Read,Glob,Grep")

    def test_implementation_is_full_tool_auto_without_bypass(self):
        plan = self.plan(code="HM", variant="claude-primary")
        self.assertEqual(self.value(plan["argv"], "--permission-mode"), "auto")
        self.assertEqual(self.value(plan["argv"], "--tools"), "default")
        self.assertNotIn("--restricted", plan["argv"])
        self.assertNotIn("--dangerously-skip-permissions", plan["argv"])
        self.assertNotIn("--max-turns", plan["argv"])
        self.assertEqual(plan["timeout_seconds"], 3600)

    def test_custom_consultation_approvals_and_reviewer_tools(self):
        config = bundle.merge(self.config, {"claude": {"modes": {"consultation": {
            "permission_mode": "auto", "tools": "default", "restricted": False,
            "allowed_tools": ["Bash(python -m pytest *)"], "disallowed_tools": ["Write"],
            "permission_prompts": "host", "reviewer": {"tools": ["Read", "Bash"], "permission_mode": "manual"}
        }}}})
        bundle.validate(config)
        plan = self.plan(config=config, code="OH", role="qa")
        args = plan["argv"]
        definitions = json.loads(self.value(args, "--agents"))
        self.assertEqual(self.value(args, "--tools"), "default")
        self.assertEqual(self.value(args, "--permission-mode"), "auto")
        self.assertEqual(definitions["review-worker"]["tools"], ["Read", "Bash"])
        self.assertEqual(definitions["review-worker"]["permissionMode"], "manual")
        self.assertIn("--disallowedTools", args)
        self.assertIn("Bash(python -m pytest *)", args)
        self.assertNotIn("--restricted", args)
        self.assertIn("configured host permission responder is available", plan["required_checks"])

    def test_configured_implementation_bypass_needs_explicit_authorization(self):
        config = bundle.merge(self.config, {"claude": {"modes": {"implementation": {"permission_mode": "bypassPermissions"}}}})
        plan = self.plan(config=config, code="HM", variant="claude-primary")
        self.assertIn("--dangerously-skip-permissions", plan["argv"])
        self.assertIn("explicit assignment-level permission-bypass authorization", plan["required_checks"])

    def test_codex_permissions_and_deadline_are_independent_configuration(self):
        config = bundle.merge(self.config, {"codex": {"sandbox_by_role": {"qa": "workspace-write"}, "approval_policy": "on-request", "timeout_seconds": 88}})
        plan = self.plan(config=config, code="SM", role="qa", design="claude-first")
        self.assertEqual(self.value(plan["argv"], "--sandbox"), "workspace-write")
        self.assertIn('approval_policy="on-request"', plan["argv"])
        self.assertEqual(plan["timeout_seconds"], 88)
        config["codex"]["bypass_approvals_and_sandbox"] = True
        bypass = self.plan(config=config, code="SM", role="qa", design="claude-first")
        self.assertIn("--dangerously-bypass-approvals-and-sandbox", bypass["argv"])
        self.assertNotIn("--sandbox", bypass["argv"])

    def test_preset_has_no_timeout_or_turn_cap_and_exact_worker(self):
        config = bundle.load_config(presets=["opus-haiku"])
        plan = self.plan(config=config, mode="opus-haiku", code="OH", claude_mode="orchestration")
        definitions = json.loads(self.value(plan["argv"], "--agents"))
        worker = definitions["haiku-worker"]
        self.assertEqual((worker["model"], worker["effort"]), ("claude-haiku-5-5", "xhigh"))
        self.assertNotIn("tools", worker)
        self.assertNotIn("maxTurns", worker)
        self.assertIsNone(plan["timeout_seconds"])
        self.assertIn("--dangerously-skip-permissions", plan["argv"])
        self.assertNotIn("--restricted", plan["argv"])
        self.assertIn("explicit assignment-level permission-bypass authorization", plan["required_checks"])

    def test_explicit_turn_limit_and_leaf_worker_setting(self):
        config = bundle.load_config(presets=["opus-haiku"])
        settings = config["claude"]["modes"]["orchestration"]
        settings.update(max_turns=12, timeout_seconds=120, nested_delegation=False)
        plan = self.plan(config=config, mode="opus-haiku", code="OH", claude_mode="orchestration")
        worker = json.loads(self.value(plan["argv"], "--agents"))["haiku-worker"]
        self.assertEqual(worker["disallowedTools"], ["Agent"])
        self.assertEqual(worker["maxTurns"], 12)
        self.assertEqual(self.value(plan["argv"], "--max-turns"), "12")
        self.assertEqual(plan["timeout_seconds"], 120)

    def test_resume_is_exact_and_keeps_mode_flags(self):
        session_id = "12345678-1234-4234-8234-123456789abc"
        plan = self.plan(code="OH", role="qa", resume=session_id)
        self.assertEqual(self.value(plan["argv"], "--resume"), session_id)
        self.assertNotIn("--session-id", plan["argv"])
        self.assertNotIn("--continue", plan["argv"])
        self.assertIn("--restricted", plan["argv"])
        with self.assertRaises(ValueError):
            self.plan(code="OH", role="qa", resume="latest")

    def test_external_codex_is_workspace_scoped_without_bypass(self):
        plan = self.plan(code="SM", design="claude-first")
        self.assertEqual(plan["argv"][:2], ["codex", "exec"])
        self.assertEqual(self.value(plan["argv"], "--sandbox"), "workspace-write")
        self.assertNotIn("--dangerously-bypass-approvals-and-sandbox", plan["argv"])
        self.assertTrue(plan["stdout_file"].endswith("events.jsonl"))
        readonly = self.plan(code="SM", role="qa", design="claude-first")
        self.assertEqual(self.value(readonly["argv"], "--sandbox"), "read-only")

    def test_retired_codex_and_codex_resume_fail_without_fake_support(self):
        with self.assertRaisesRegex(ValueError, "retired"):
            self.plan(code="SMF", design="claude-first")
        with self.assertRaisesRegex(ValueError, "resume"):
            self.plan(code="SM", design="claude-first", resume="12345678-1234-4234-8234-123456789abc")

    def test_standard_launch_plans_preserve_exact_codex_model_effort(self):
        for code, item in self.config["profiles"].items():
            if item["provider"] != "codex":
                continue
            plan = self.plan(code=code, allow_out_of_pool=True, role_override=True, design="claude-first")
            self.assertEqual(self.value(plan["argv"], "--model"), item["model"])
            self.assertIn("model_reasoning_effort=" + json.dumps(item["effort"]), plan["argv"])
            self.assertEqual(plan["profile"]["service_tier"], "standard")
            self.assertIn("Standard service tier on the actual route", plan["required_checks"])
            self.assertNotIn("--fast", plan["argv"])

    def test_burn_plan_retains_scope_and_preset_compatibility(self):
        for mode, code, design in [("codex-burn", "SH", "claude-first"), ("claude-burn", "SNH", "codex-first")]:
            plan = self.plan(mode=mode, code=code, design=design, burn_account="work-account", burn_endpoint="reset")
            self.assertEqual(plan["burn"]["provider"], "codex" if code == "SH" else "claude")
            self.assertEqual(plan["burn"]["endpoint"], "reset")
        exception = self.plan(mode="codex-burn", code="OH", role="qa", allow_out_of_pool=True, role_override=True,
                              burn_account="codex-work", burn_endpoint="reset")
        self.assertTrue(exception["burn"]["out_of_provider_exception"])
        self.assertIn("explicit cross-provider exception uses a separate account route, not the selected burn account",
                      exception["required_checks"])
        config = bundle.load_config(presets=["opus-haiku"])
        plan = self.plan(config=config, mode="claude-burn", code="OH", role="qa", claude_mode="orchestration",
                         burn_account="claude-work", burn_endpoint="queue end")
        self.assertIsNone(plan["timeout_seconds"])
        self.assertEqual(json.loads(self.value(plan["argv"], "--agents"))["haiku-worker"]["effort"], "xhigh")
        with self.assertRaisesRegex(ValueError, "cannot control"):
            self.plan(config=config, mode="claude-burn", code="SNH", claude_mode="orchestration",
                      burn_account="claude-work", burn_endpoint="queue end")

    def test_cli_burn_requirements_and_migration_errors(self):
        command = [sys.executable, str(ROOT / "scripts/bundle.py"), "resolve"]
        for extra, message in [(["--mode", "fast"], "retired"), (["--mode", "tokenburn"], "retired"),
                               (["--profile", "CMAX"], "retired"), (["--mode", "codex-burn"], "burn-account")]:
            result = subprocess.run(command + extra, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(message, result.stderr)
        for mode in ("codex-burn", "claude-burn"):
            result = subprocess.run(command + ["--mode", mode, "--burn-account", "work", "--burn-endpoint", "queue end"],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["burn"]["account"], "work")

    def test_cli_requires_both_out_of_pool_exception_flags(self):
        command = [sys.executable, str(ROOT / "scripts/bundle.py"), "resolve", "--mode", "codex-burn",
                   "--profile", "OH", "--role", "qa", "--burn-account", "work", "--burn-endpoint", "queue end"]
        for flags, message in [(["--allow-out-of-pool"], "--role-override"), (["--role-override"], "outside")]:
            result = subprocess.run(command + flags, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(message, result.stderr)
        result = subprocess.run(command + ["--allow-out-of-pool", "--role-override"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        resolved = json.loads(result.stdout)
        self.assertEqual(resolved["overrides"], {"out_of_pool": True, "role_or_lifecycle": True})
        self.assertTrue(resolved["burn"]["out_of_provider_exception"])

    def test_missing_paths_and_multiple_choices_fail(self):
        resolved = bundle.resolve(self.config, code="OH", role="qa")
        with self.assertRaises(ValueError):
            bundle.launch_plan(resolved, self.cwd, "/nonexistent-prompt", self.artifacts)
        with self.assertRaises(ValueError):
            bundle.launch_plan(bundle.resolve(self.config), self.cwd, self.prompt, self.artifacts)

    def test_planning_does_not_create_artifacts(self):
        with tempfile.TemporaryDirectory() as directory:
            artifacts = Path(directory) / "not-created"
            resolved = bundle.resolve(self.config, code="OH", role="qa")
            plan = bundle.launch_plan(resolved, self.cwd, self.prompt, str(artifacts))
            self.assertFalse(plan["executes"])
            self.assertFalse(artifacts.exists())

    def test_cli_is_offline_json(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/bundle.py"), "validate"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)["valid"])

    def test_native_routes_never_generate_external_cli_plans(self):
        for variant, design, code in [("codex-primary", "codex-first", "SM"),
                                       ("claude-primary", "claude-first", "OH")]:
            with self.assertRaisesRegex(ValueError, "Native routes require"):
                self.plan(variant=variant, design=design, code=code)

    def test_muse_launch_plans_fail_closed_for_both_controller_designs(self):
        for code in ("MFH", "MFX"):
            for design in self.config["designs"]:
                with self.assertRaisesRegex(ValueError, "No bundled launch adapter for provider muse"):
                    self.plan(mode="high-qual", code=code, role="research", design=design)
        for action in ("codex-plan", "claude-plan"):
            result = subprocess.run([sys.executable, str(ROOT / "scripts/bundle.py"), action,
                                     "--mode", "high-qual", "--profile", "MFH", "--role", "research",
                                     "--cwd", self.cwd, "--prompt-file", self.prompt, "--artifacts", self.artifacts],
                                    capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Profile provider does not match", result.stderr)
            self.assertEqual(result.stdout, "")

    def test_fable_explicit_launch_uses_exact_profile_and_existing_permissions(self):
        for variant in self.config["variants"]:
            for code, effort in [("FH", "high"), ("FX", "xhigh")]:
                plan = self.plan(variant=variant, code=code, role="frontend", allow_out_of_pool=True, role_override=True)
                self.assertEqual(self.value(plan["argv"], "--model"), "claude-fable-5-1")
                self.assertEqual(self.value(plan["argv"], "--effort"), effort)
                self.assertEqual(self.value(plan["argv"], "--permission-mode"), "auto")
                self.assertEqual(plan["timeout_seconds"], 3600)
                self.assertNotIn("--dangerously-skip-permissions", plan["argv"])

    def test_cli_variant_bias_and_preset_combinations(self):
        command = [sys.executable, str(ROOT / "scripts/bundle.py")]
        for variant in self.config["variants"]:
            for preset in ([], ["--preset", "opus-haiku"]):
                result = subprocess.run(command + ["validate", "--variant", variant, *preset], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(result.stdout)["variant"], variant)
        result = subprocess.run(command + ["resolve", "--variant", "claude-primary", "--design", "claude-first",
                                           "--profile", "OH", "--bias", "high"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        resolved = json.loads(result.stdout)
        self.assertEqual(resolved["choices"][0]["dispatch"], "native-claude")
        self.assertEqual(resolved["choices"][0]["effort"], "high")
        self.assertEqual(resolved["selection_bias"], "high")

    def test_local_markdown_links_resolve(self):
        for source in ROOT.rglob("*.md"):
            for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", source.read_text()):
                if target.startswith(("https://", "http://", "#")):
                    continue
                target = target.split("#", 1)[0]
                self.assertTrue((source.parent / target).exists(), f"Broken link in {source.relative_to(ROOT)}: {target}")

    def test_documented_bundle_commands_are_valid_offline(self):
        for source in ROOT.rglob("*.md"):
            for line in source.read_text().splitlines():
                if not line.startswith("python3 scripts/bundle.py "):
                    continue
                args = shlex.split(line)
                args[0] = sys.executable
                args = [self.prompt if arg == "task.txt" else arg for arg in args]
                result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, f"{source.relative_to(ROOT)}: {line}\n{result.stderr}")
                output = json.loads(result.stdout)
                if args[2].endswith("-plan"):
                    self.assertFalse(output["executes"])

    def test_direct_companion_defaults_and_explicit_implementation(self):
        for extra, expected_mode in [([], "consultation"), (["--role", "implementation"], "implementation")]:
            command = [sys.executable, str(ROOT / "scripts/bundle.py"), "claude-plan", "--direct",
                       "--cwd", self.cwd, "--prompt-file", self.prompt, "--artifacts", self.artifacts, *extra]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            plan = json.loads(result.stdout)
            self.assertEqual(plan["profile"]["model"], "claude-opus-5-5")
            self.assertEqual(plan["profile"]["claude_mode"], expected_mode)
            self.assertFalse(plan["executes"])

    def test_direct_cannot_be_combined_with_an_active_router_mode(self):
        command = [sys.executable, str(ROOT / "scripts/bundle.py"), "claude-plan", "--direct", "--mode", "balanced"]
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("does not use a router", result.stderr)


if __name__ == "__main__":
    unittest.main()
