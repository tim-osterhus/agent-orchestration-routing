"""Offline configuration and launch-contract tests. No model subprocesses."""

from copy import deepcopy
import importlib.util
import json
from pathlib import Path
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

    def test_default_config_and_alias(self):
        self.assertEqual(bundle.profile(self.config, "SF"), bundle.profile(self.config, "SMF"))
        self.assertEqual(self.config["controller_design"], "codex-first")
        self.assertFalse(self.config["claude"]["modes"]["orchestration"]["enabled"])

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
            self.resolve(code="HM", assignment_kind="controller")

    def test_ongoing_thread_and_final_review_are_separate(self):
        for kwargs in ({}, {"ongoing": True}, {"final": True}):
            with self.assertRaises(ValueError):
                self.resolve(mode="fast", code="OX", role="qa", **kwargs)
        result = self.resolve(mode="fast", code="OX", role="qa", ongoing=True, final=True)
        self.assertEqual(result["choices"][0]["claude_mode"], "consultation")

    def test_browser_specialists(self):
        self.assertEqual(self.resolve(mode="performance", role="browser")["choices"][0]["code"], "ALF")
        self.assertEqual(self.resolve(mode="tokenburn", role="browser")["choices"][0]["code"], "AMF")

    def test_out_of_pool_requires_recorded_override(self):
        with self.assertRaisesRegex(ValueError, "outside"):
            self.resolve(code="L")
        result = self.resolve(code="L", allow_out_of_pool=True)
        self.assertEqual(result["choices"][0]["code"], "L")

    def test_invalid_mode_profile_role_and_alias_cycle(self):
        for kwargs in ({"mode": "missing"}, {"code": "missing"}, {"role": "missing"}):
            with self.assertRaises(ValueError):
                self.resolve(**kwargs)
        self.config["profiles"]["SM"] = {"alias_of": "SF"}
        self.config["profiles"]["SMF"] = {"alias_of": "SM"}
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
        result = self.resolve(code="OH", role="frontend")
        self.assertEqual(result["choices"][0]["model"], "claude-opus-5-5")
        self.assertEqual(result["choices"][0]["claude_mode"], "implementation")


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
        plan = self.plan(code="HM")
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
        plan = self.plan(config=config, code="HM")
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

    def test_fast_codex_and_codex_resume_fail_without_fake_support(self):
        with self.assertRaisesRegex(ValueError, "Fast"):
            self.plan(code="SMF", design="claude-first")
        with self.assertRaisesRegex(ValueError, "resume"):
            self.plan(code="SM", design="claude-first", resume="12345678-1234-4234-8234-123456789abc")

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
