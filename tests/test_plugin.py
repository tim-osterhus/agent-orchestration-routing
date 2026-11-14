"""Offline checks for the Claude Code plugin, its generated agents, vendored runtime, and ownership tools."""

from copy import deepcopy
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/agent-orch"
RUNTIME = PLUGIN / "runtime/codex"
SPEC = importlib.util.spec_from_file_location("plugin_bundle", ROOT / "scripts/bundle.py")
bundle = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bundle)
NODE = shutil.which("node")


def fields(text):
    header = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    return dict(line.split(": ", 1) for line in header[1].splitlines())


class PluginPackageTests(unittest.TestCase):
    def setUp(self):
        self.config = bundle.load_config()

    def test_marketplace_and_manifest_name_one_plugin_matching_the_design(self):
        market = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
        manifest = json.loads((PLUGIN / ".claude-plugin/plugin.json").read_text())
        self.assertTrue(market["name"] and market["owner"]["name"])
        self.assertEqual([(p["name"], p["source"]) for p in market["plugins"]], [(manifest["name"], "./plugins/agent-orch")])
        self.assertEqual(self.config["designs"]["claude-plugin"]["plugin_agents"], manifest["name"])
        self.assertFalse((ROOT / ".claude-plugin/plugin.json").exists(), "The repository root must not be a plugin")

    def test_generated_copy_is_in_sync(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/bundle.py"), "plugin", "--check"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)["in_sync"])

    def test_plugin_loads_only_the_router_skill(self):
        self.assertEqual([path.name for path in (PLUGIN / "skills").iterdir()], ["agent-orch-router"])
        names = {path.name for path in PLUGIN.rglob("*")}
        for excluded in ("claude-delegation", "codex-plus-efficiency", "test_plus_skill.py", "local.json", "stop-review-gate-hook.mjs"):
            self.assertNotIn(excluded, names)

    def test_router_copy_is_canonical_plus_flag_and_plugin_pointer(self):
        canonical = (ROOT / "skills/agent-orch-router/SKILL.md").read_text()
        copy = (PLUGIN / "skills/agent-orch-router/SKILL.md").read_text()
        self.assertEqual(fields(copy), {**fields(canonical), "disable-model-invocation": "true"})
        expected = canonical.replace("description: " + fields(canonical)["description"] + "\n",
                                     "description: " + fields(canonical)["description"] + "\ndisable-model-invocation: true\n")
        self.assertEqual(copy, expected.replace("\nOptional: ", "\n" + bundle.PLUGIN_POINTER + "Optional: "))
        self.assertNotIn("claude-plugin.md", canonical)
        self.assertTrue((PLUGIN / "skills/agent-orch-router/references/claude-plugin.md").is_file())

    def test_one_pinned_agent_per_codex_and_claude_profile(self):
        pinned = {code: p for code, p in self.config["profiles"].items()
                  if p["provider"] in {"codex", "claude"} and p.get("executable", True)}
        self.assertTrue(any(not p.get("executable", True) for p in self.config["profiles"].values()),
                        "Expected at least one documentary profile to exercise the exclusion")
        expected = {f"{p['provider']}-{code.lower()}.md" for code, p in pinned.items()}
        self.assertEqual({path.name for path in (PLUGIN / "agents").glob("*.md")}, expected)
        write_roles = bundle.codex_write_roles(self.config)
        self.assertEqual(write_roles, ["implementation", "frontend", "integration", "browser"])
        for code, item in pinned.items():
            text = (PLUGIN / "agents" / f"{item['provider']}-{code.lower()}.md").read_text()
            meta = fields(text)
            self.assertEqual(meta["name"], f"{item['provider']}-{code.lower()}")
            if item["provider"] == "codex":
                self.assertEqual((meta["model"], meta["effort"], meta["tools"]), ("haiku", "low", "Bash"))
                command = re.search(r"```bash\n(.+)\n```", text)[1]
                self.assertEqual(command, 'node "${CLAUDE_PLUGIN_ROOT}/runtime/codex/scripts/codex-companion.mjs" task --json --detach '
                                          f'--model {item["model"]} --effort {item["effort"]} [--write] [--resume-thread <id>] '
                                          '--prompt-file "<work order file>"')
                # One call per Codex turn was moved to the background at Claude Code's 2-minute Bash timeout.
                self.assertIn("run the identical command again, unchanged", text)
                # Claude Code shows each Bash description as the subagent's activity.
                self.assertIn("set that Bash call's description to the JSON's `description` value, copied exactly", text)
                self.assertIn("Do not run it in the background", text)
                self.assertIn("Roles " + ", ".join(write_roles) + " add `--write`", text)
                self.assertNotIn("<<", text, "Work orders travel by file, never through a heredoc")
                self.assertIn("stdout, character for character", text, "A live relay paraphrased the JSON")
            else:
                self.assertEqual((meta["model"], meta["effort"]), (item["model"], item["effort"]))
                self.assertNotIn("tools", meta)
                self.assertEqual(meta.get("autoCompactWindow"), str(item["context_target_tokens"]) if item.get("context_target_tokens") else None)

    def test_plugin_agents_reject_unattended_codex_settings_they_cannot_honor(self):
        for change, message in [({"sandbox_by_role": {"default": "danger-full-access"}}, "read-only and workspace-write"),
                                ({"approval_policy": "on-request"}, "approval_policy must be never"),
                                ({"bypass_approvals_and_sandbox": True}, "bypass disabled")]:
            config = deepcopy(self.config)
            config["codex"].update(change)
            with self.assertRaisesRegex(ValueError, message):
                bundle.resolve(config, code="SM", design="claude-plugin")
            with self.assertRaisesRegex(ValueError, message):
                bundle.plugin_files(config)
            bundle.resolve(config, code="SM", design="claude-first")

    def test_plugin_design_resolves_pinned_agents_and_refuses_cli_plans(self):
        codex = bundle.resolve(self.config, code="SM", design="claude-plugin")["choices"][0]
        self.assertEqual((codex["dispatch"], codex["agent"]), ("native-codex", "agent-orch:codex-sm"))
        claude = bundle.resolve(self.config, code="OH", role="qa", design="claude-plugin")["choices"][0]
        self.assertEqual((claude["dispatch"], claude["agent"]), ("native-claude", "agent-orch:claude-oh"))
        muse = bundle.resolve(self.config, mode="amusing", code="MFH", role="research", design="claude-plugin")["choices"][0]
        self.assertEqual(muse["dispatch"], "external-muse")
        self.assertNotIn("agent", muse)
        documentary = bundle.resolve(self.config, code="CYBER", design="claude-plugin",
                                     allow_out_of_pool=True, role_override=True)["choices"][0]
        self.assertNotIn("agent", documentary, "Documentary profiles have no pinned agent")
        with tempfile.TemporaryDirectory() as directory:
            prompt = Path(directory) / "task.txt"
            prompt.write_text("Bounded task.")
            resolved = bundle.resolve(self.config, code="SM", design="claude-plugin")
            with self.assertRaisesRegex(ValueError, "Native routes require"):
                bundle.launch_plan(resolved, directory, str(prompt), str(Path(directory) / "runs"))
        bulk = bundle.resolve(self.config, mode="bulk", design="claude-plugin")
        self.assertEqual([c["code"] for c in bulk["choices"]], ["SL", "TM", "TH", "SM", "SH", "SX", "SMAX", "AL", "OX", "FH"])
        self.assertIsNone(bulk["limits"]["max_parallel_workers"])

    def test_plugin_settings_only_supply_the_codex_status_line(self):
        # Claude Code 2.1.322 accepts only these keys from a plugin's settings.json.
        settings = json.loads((PLUGIN / "settings.json").read_text())
        self.assertLessEqual(set(settings), {"agent", "subagentStatusLine"})
        status = settings["subagentStatusLine"]
        self.assertEqual(status["type"], "command")
        self.assertEqual(status["command"], 'node "${CLAUDE_PLUGIN_ROOT}/runtime/codex/scripts/subagent-status.mjs"')
        self.assertTrue((RUNTIME / "scripts/subagent-status.mjs").is_file())

    def test_hooks_only_manage_session_state(self):
        hooks = json.loads((PLUGIN / "hooks/hooks.json").read_text())["hooks"]
        self.assertEqual(set(hooks), {"SessionStart", "SessionEnd"})
        for event, groups in hooks.items():
            command = groups[0]["hooks"][0]["command"]
            self.assertIn("runtime/codex/scripts/session-lifecycle-hook.mjs", command)
            self.assertTrue(command.endswith(event))
        self.assertTrue((RUNTIME / "scripts/session-lifecycle-hook.mjs").is_file())


class VendoredRuntimeTests(unittest.TestCase):
    PATCHED = {"codex-companion.mjs", "app-server-broker.mjs", "session-lifecycle-hook.mjs", "lib/codex.mjs", "lib/app-server.mjs",
               "lib/state.mjs", "lib/broker-lifecycle.mjs", "lib/claude-session-transfer.mjs", "lib/tracked-jobs.mjs"}

    def test_license_notice_provenance_and_change_notices(self):
        for name in ("LICENSE", "NOTICE", "VENDORED.md"):
            self.assertTrue((RUNTIME / name).is_file(), name)
        self.assertIn("db52e28f4d9ded852ab3942cea316258ae4ef346", (RUNTIME / "VENDORED.md").read_text())
        scripts = RUNTIME / "scripts"
        noticed = {path.relative_to(scripts).as_posix() for path in scripts.rglob("*.mjs")
                   if "// Modified by Tim Osterhus for agent-orch" in path.read_text()}
        self.assertEqual(noticed, self.PATCHED)

    def test_names_and_paths_are_separate_from_the_official_plugin(self):
        text = "\n".join(path.read_text() for path in (RUNTIME / "scripts").rglob("*.mjs"))
        self.assertNotIn("CODEX_COMPANION_", text)
        self.assertNotIn("claude_code_codex_plugin", text)
        self.assertIn('"AGENT_ORCH_CODEX_DATA"', (RUNTIME / "scripts/lib/state.mjs").read_text())
        manifest = re.search(r'new URL\("([^"]+plugin\.json)"', (RUNTIME / "scripts/lib/app-server.mjs").read_text())[1]
        self.assertEqual((RUNTIME / "scripts/lib" / manifest).resolve(), (PLUGIN / ".claude-plugin/plugin.json").resolve())

    @unittest.skipUnless(NODE, "node is required")
    def test_runtime_node_suites(self):
        result = subprocess.run([NODE, "--test", *map(str, sorted((RUNTIME / "tests").glob("*.test.mjs")))],
                                cwd=ROOT, capture_output=True, text=True, timeout=120, env=bundle.git_env())
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    @unittest.skipUnless(NODE, "node is required")
    def test_modules_parse_and_task_arguments_fail_before_codex_starts(self):
        for module in (RUNTIME / "scripts").rglob("*.mjs"):
            result = subprocess.run([NODE, "--check", str(module)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, f"{module}: {result.stderr}")
        companion = str(RUNTIME / "scripts/codex-companion.mjs")
        with tempfile.TemporaryDirectory() as directory:
            for args, message in [(["--effort", "ultra"], "none, minimal, low, medium, high, xhigh, max."),
                                  (["--resume-thread", "thread-1", "--fresh"], "Choose only one of --resume-thread"),
                                  (["--resume-thread", "thread-1", "--resume-last"], "Choose only one of --resume-thread")]:
                result = subprocess.run([NODE, companion, "task", *args, "Bounded task."], cwd=directory, input="",
                                        capture_output=True, text=True, timeout=30, env=bundle.git_env())
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(message, result.stderr)

    @unittest.skipUnless(NODE, "node is required")
    def test_task_result_file_never_carries_a_stale_result(self):
        # Live Haiku relays sometimes paraphrased the JSON, so controllers read <work order>.result.json instead.
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            (base / "bin").mkdir()
            (base / "bin/codex").write_text('#!/bin/sh\necho "fake codex failure" >&2\nexit 1\n')
            (base / "bin/codex").chmod(0o755)
            order = base / "order.md"
            order.write_text("Role: research\n")
            stale = base / "order.md.result.json"
            stale.write_text('{"stale": true}\n')
            env = {**bundle.git_env(), "PATH": f"{base / 'bin'}:/usr/bin:/bin", "AGENT_ORCH_CODEX_DATA": str(base / "state")}
            result = subprocess.run([NODE, str(RUNTIME / "scripts/codex-companion.mjs"), "task", "--json", "--prompt-file", str(order)],
                                    cwd=directory, input="", capture_output=True, text=True, timeout=30, env=env)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(stale.exists(), "A run that produced no result must not leave an older result behind")
        source = (RUNTIME / "scripts/codex-companion.mjs").read_text()
        self.assertIn('`${path.resolve(cwd, options["prompt-file"])}.result.json`', source)
        self.assertIn("fs.renameSync(temporary, file)", source)


class OwnershipTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        base = Path(self.directory.name)
        self.repo, self.runs = base / "repo", base / "runs"
        self.repo.mkdir()
        for rel, text in {"src/a.py": "a\n", "src/b.py": "b\n", "docs/guide.md": "g\n", ".gitignore": "/private/\n"}.items():
            (self.repo / rel).parent.mkdir(parents=True, exist_ok=True)
            (self.repo / rel).write_text(text)
        (self.repo / "private").mkdir()
        (self.repo / "private/bench.json").write_text("{}\n")
        for command in (["init", "-q"], ["add", "."], ["-c", "user.name=t", "-c", "user.email=t@example.invalid", "commit", "-qm", "base"]):
            subprocess.run(["git", "-C", str(self.repo), *command], check=True, capture_output=True, env=bundle.git_env())
        (self.repo / "docs/guide.md").write_text("user edit\n")  # Pre-existing uncommitted change.

    def snapshot(self):
        return bundle.snapshot(self.repo, self.runs / "baseline.json", ["private"])

    def check(self, owners):
        path = self.runs / "owners.json"
        path.write_text(json.dumps(owners))
        return bundle.check_ownership(self.runs / "baseline.json", path)

    def test_inherited_git_repository_variables_cannot_redirect_git(self):
        # Git hooks and `git rebase --exec` export GIT_DIR. Inherited, it once sent these fixtures' commits into the real checkout.
        decoy = self.runs / "decoy"
        decoy.mkdir(parents=True)
        subprocess.run(["git", "-C", str(decoy), "init", "-q"], check=True, capture_output=True, env=bundle.git_env())
        before = (decoy / ".git/config").read_bytes()
        hostile = {"GIT_DIR": str(decoy / ".git"), "GIT_WORK_TREE": str(decoy), "GIT_INDEX_FILE": str(decoy / ".git/index")}
        with mock.patch.dict(os.environ, hostile):
            self.assertEqual(self.snapshot()["dirty"], ["docs/guide.md"])
            self.assertTrue(set(hostile) <= set(os.environ) and not set(hostile) & set(bundle.git_env()))
        self.assertEqual((decoy / ".git/config").read_bytes(), before)
        self.assertFalse((decoy / ".git/index").exists())

    def test_snapshot_records_dirty_and_protected_files_outside_the_project(self):
        result = self.snapshot()
        self.assertEqual(result["dirty"], ["docs/guide.md"])
        self.assertEqual(result["protected"], ["private/"])
        recorded = json.loads((self.runs / "baseline.json").read_text())["files"]
        self.assertIn("private/bench.json", recorded)
        with self.assertRaisesRegex(ValueError, "outside the project"):
            bundle.snapshot(self.repo, self.repo / "baseline.json")

    def test_pre_dispatch_overlap_and_dirty_ownership_block_parallel_dispatch(self):
        self.snapshot()
        self.assertTrue(self.check({"one": ["src/a.py"], "two": ["src/b.py"]})["ok"])
        overlap = self.check({"one": ["src/"], "two": ["src/b.py"]})
        self.assertFalse(overlap["ok"])
        self.assertEqual(overlap["overlaps"][0]["workers"], ["one", "two"])
        self.assertEqual(overlap["overlaps"][0]["files"], ["src/b.py"])
        new_file = self.check({"one": ["src/new.py"], "two": ["src/*.py"]})
        self.assertEqual(new_file["overlaps"][0]["patterns"], ["src/new.py"])
        dirty = self.check({"one": ["docs/"]})
        self.assertEqual(dirty["owned_dirty"], [{"file": "docs/guide.md", "workers": ["one"]}])

    def test_post_dispatch_changes_are_attributed_or_flagged(self):
        self.snapshot()
        (self.repo / "src/a.py").write_text("a2\n")
        (self.repo / "src/new.py").write_text("n\n")
        owners = {"one": ["src/a.py", "src/new.py"], "two": ["src/b.py"]}
        result = self.check(owners)
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["changes"], {"src/a.py": ["one"], "src/new.py": ["one"]})
        (self.repo / "src/b.py").unlink()
        (self.repo / "README.md").write_text("stray\n")
        (self.repo / "private/bench.json").write_text('{"changed": true}\n')
        result = self.check(owners)
        self.assertFalse(result["ok"])
        self.assertEqual(result["changes"]["src/b.py"], ["two"])
        self.assertEqual(result["unowned_changes"], ["README.md", "private/bench.json"])
        self.assertEqual(result["protected_changes"], ["private/bench.json"])

    def test_cli_exit_status_reflects_violations(self):
        command = [sys.executable, str(ROOT / "scripts/bundle.py")]
        result = subprocess.run(command + ["snapshot", "--cwd", str(self.repo), "--out", str(self.runs / "baseline.json")],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        (self.runs / "owners.json").write_text(json.dumps({"one": ["src/a.py"]}))
        check = command + ["check-ownership", "--snapshot", str(self.runs / "baseline.json"), "--owners", str(self.runs / "owners.json")]
        self.assertEqual(subprocess.run(check, capture_output=True).returncode, 0)
        (self.repo / "src/b.py").write_text("unowned\n")
        result = subprocess.run(check, capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)["unowned_changes"], ["src/b.py"])


if __name__ == "__main__":
    unittest.main()
