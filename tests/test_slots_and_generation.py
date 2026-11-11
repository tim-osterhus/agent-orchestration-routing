"""Behavioral invariants for registry bindings and generated native instructions."""

from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("render_router_tests", ROOT / "scripts/render_docs.py")
renderer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(renderer)
bundle = renderer.bundle


class SlotTests(unittest.TestCase):
    def setUp(self):
        self.config = bundle.load_config()

    def test_exact_frontier_and_disjoint_specialist_catalogs(self):
        self.assertEqual(self.config["catalogs"]["frontier"],
                         "LL LM HL TL EX EMAX TM TH SM SH SX SMAX AH AX FM OX GCM GCH FH FX FMAX".split())
        self.assertEqual(len(self.config["catalogs"]["specialists"]), 9)
        self.assertEqual(len(self.config["catalogs"]["conditional"]), 3)
        all_codes = [c for group in self.config["catalogs"].values() for c in group]
        self.assertEqual(len(all_codes), len(set(all_codes)))
        self.assertEqual(set(all_codes), set(self.config["profiles"]))

    def test_efficient_six_choices_and_cheap_slot_variants(self):
        for variant, cheap in (("codex-primary", "LM"), ("claude-primary", "HL")):
            pool = bundle.mode_pools(self.config, variant)["efficient"]
            self.assertEqual([e["profile"] for e in pool], [cheap, "TL", "EX", "TM", "TH", "SM"])
            unavailable = bundle.resolve(self.config, variant=variant, mode="efficient")
            self.assertNotIn("EX", [c["code"] for c in unavailable["choices"]])
            self.assertIn("EX", unavailable["unavailable_profiles"])
            verified = bundle.merge(self.config, {"adapters": {"muse:public_api_standard": {"verified": True}}})
            self.assertIn("EX", [c["code"] for c in bundle.resolve(verified, variant=variant, mode="efficient")["choices"]])

    def test_default_council_and_amusing_keep_known_code_routes_not_api_routes(self):
        for variant in self.config["variants"]:
            council = bundle.resolve(self.config, variant=variant, mode="council", role="research")
            self.assertEqual([c["code"] for c in council["choices"]], ["SMAX", "OX", "MFX", "AMAX", "FH"])
            amusing = bundle.resolve(self.config, variant=variant, mode="amusing", role="implementation")
            self.assertEqual([c["code"] for c in amusing["choices"]], ["SM", "SX", "OM", "MFH", "MFX"])
            for result in (council, amusing):
                self.assertNotIn("unavailable_profiles", result)
                for choice in result["choices"]:
                    if choice["provider"] == "muse":
                        self.assertTrue(choice["execution"]["adapter_route_available"])
                        self.assertFalse(choice["execution"]["account_access_verified"])
                        self.assertFalse(choice["execution"]["launch_plan_supported"])
            efficient = bundle.resolve(self.config, variant=variant, mode="efficient")
            self.assertEqual(efficient["unavailable_profiles"], ["EX"])

    def test_provider_flag_cannot_enable_or_substitute_a_different_access_route(self):
        broad = bundle.merge(self.config, {"adapters": {"muse": {"verified": True}}})
        self.assertFalse(bundle.adapter_available(broad, bundle.profile(broad, "EX")))
        self.assertTrue(bundle.adapter_available(broad, bundle.profile(broad, "MFX")))
        api_only = bundle.merge(broad, {"adapters": {"muse:public_api_standard": {"verified": True},
                                                     "muse:muse_code_subscription": {"verified": False}}})
        self.assertTrue(bundle.adapter_available(api_only, bundle.profile(api_only, "EX")))
        self.assertFalse(bundle.adapter_available(api_only, bundle.profile(api_only, "MFX")))
        council = bundle.resolve(api_only, mode="council", role="research")
        self.assertIn("MFX", council["unavailable_profiles"])
        self.assertNotIn("EX", [c["code"] for c in council["choices"]])
        exact = bundle.resolve(api_only, mode="council", code="MFX", role="research")["choices"][0]
        self.assertEqual(exact["model"], "muse-wonder-full-1.0")
        self.assertFalse(exact["execution"]["adapter_route_available"])

    def test_mode_specific_fit_preserves_review_scope_and_authority(self):
        cases = [
            ("claude-primary", "balanced", "SM", "qa", "not implementation"),
            ("claude-primary", "performance", "AMAX", "browser", "browser or computer-use"),
            ("codex-primary", "council", "OX", "planning", "simpler alternatives"),
            ("codex-primary", "council", "AMAX", "planning", "optional fourth perspective"),
            ("codex-primary", "amusing", "OX", "qa", "review maintainability and architecture"),
            ("codex-primary", "amusing", "AMAX", "qa", "without treating this route as clean-code authority"),
            ("codex-primary", "amusing", "FH", "spec-review", "without implementing fixes"),
        ]
        for variant, mode, code, role, scope in cases:
            entry = next(e for e in bundle.mode_pools(self.config, variant)[mode] if e["profile"] == code)
            self.assertIn(scope, entry["fit"])
            self.assertIn(role, entry["roles"])
            bundle.resolve(self.config, variant=variant, mode=mode, code=code, role=role)
            with self.assertRaisesRegex(ValueError, "role/lifecycle"):
                bundle.resolve(self.config, variant=variant, mode=mode, code=code, role="implementation")
        for code in ("MFH", "MFX"):
            entry = next(e for e in bundle.mode_pools(self.config)["amusing"] if e["profile"] == code)
            self.assertIn("Implement when the work order authorizes edits.", entry["fit"])
            self.assertIn("implementation", entry["roles"])
        burn = next(e for e in bundle.mode_pools(self.config)["claude-burn"] if e["profile"] == "OMAX")
        self.assertNotIn("escalation", burn)
        self.assertIn("not merely to consume allowance", burn["fit"])

    def test_cmax_migration_requires_explicit_effort_selection(self):
        with self.assertRaisesRegex(ValueError, "SNX \\(XHigh\\) or SNMAX \\(Max\\).*explicitly"):
            bundle.profile(self.config, "CMAX")
        self.assertEqual(bundle.profile(self.config, "SNX")["effort"], "xhigh")
        self.assertEqual(bundle.profile(self.config, "SNMAX")["effort"], "max")

    def test_rebinding_preserves_mode_fences_permissions_and_exact_requests(self):
        before = deepcopy(self.config)
        changed = bundle.merge(self.config, {"bindings": {"codex-primary": {"balanced": {"standard": "SX"}}}})
        bundle.validate(changed)
        selected = bundle.resolve(changed, slot="standard")["choices"][0]
        self.assertEqual((selected["code"], selected["effort"]), ("SX", "xhigh"))
        self.assertEqual(changed["variants"], before["variants"])
        self.assertEqual(changed["modes"], before["modes"])
        self.assertEqual(changed["codex"], before["codex"])
        self.assertEqual(changed["claude"], before["claude"])
        with self.assertRaisesRegex(ValueError, "outside"):
            bundle.resolve(changed, code="SM")
        exact = bundle.resolve(changed, code="SM", allow_out_of_pool=True, role_override=True)["choices"][0]
        self.assertEqual((exact["model"], exact["effort"]), ("gpt-6.1-sol", "medium"))

    def collision_config(self):
        c = deepcopy(self.config)
        c["slots"].update(author={"description": "Author a scoped change."}, reviewer={"description": "Review a completed candidate."})
        c["modes"]["collision"] = [{"slot": "author", "roles": ["implementation"]},
                                    {"slot": "reviewer", "roles": ["qa"], "one_off_only": True, "independent_review": True}]
        c["bindings"]["shared"]["collision"] = {"author": "SM", "reviewer": "SM"}
        return bundle.validate(c)

    def test_model_collision_does_not_merge_role_lifecycle_or_authority(self):
        c = self.collision_config()
        author = bundle.resolve(c, mode="collision", slot="author")["choices"][0]
        self.assertNotIn("independent_review", author)
        reviewer = bundle.resolve(c, mode="collision", slot="reviewer", role="qa")["choices"][0]
        self.assertTrue(reviewer["independent_review"])
        for kwargs in ({"slot": "reviewer", "role": "implementation"},
                       {"slot": "author", "role": "qa"},
                       {"slot": "reviewer", "role": "qa", "assignment_kind": "controller"}):
            with self.assertRaisesRegex(ValueError, "role/lifecycle"):
                bundle.resolve(c, mode="collision", **kwargs)
        for role, slot in (("implementation", "author"), ("qa", "reviewer")):
            choices = bundle.resolve(c, mode="collision", code="SM", role=role)["choices"]
            self.assertEqual(len(choices), 1)
            self.assertEqual(choices[0]["slot"], slot)

    def test_same_model_two_eligible_slots_keep_identity_but_exact_profile_is_one_target(self):
        c = self.collision_config()
        c["modes"]["collision"][1]["roles"] = ["implementation", "qa"]
        choices = bundle.resolve(c, mode="collision")["choices"]
        self.assertEqual([x["slot"] for x in choices], ["author", "reviewer"])
        exact = bundle.resolve(c, mode="collision", code="SM")["choices"]
        self.assertEqual(len(exact), 1)
        self.assertEqual(exact[0]["slot"], "author")
        self.assertNotIn("independent_review", exact[0])
        plan = bundle.launch_plan(bundle.resolve(c, mode="collision", code="SM", design="claude-first"), ROOT, __file__, ROOT / ".runs/test")
        self.assertEqual(plan["profile"]["effort"], "medium")

    def test_unknown_binding_duplicate_slot_and_unknown_slot_fail(self):
        for patch in ({"bindings": {"codex-primary": {"balanced": {"standard": "UNKNOWN"}}}},
                      {"bindings": {"codex-primary": {"balanced": {"UNKNOWN": "SM"}}}},
                      {"variants": {"codex-primary": {"modes": {"balanced": [{"slot": "standard"}, {"slot": "standard"}]}}}}):
            with self.assertRaises(ValueError):
                bundle.validate(bundle.merge(self.config, patch))
        with self.assertRaisesRegex(ValueError, "Unknown slot"):
            bundle.resolve(self.config, slot="unknown")
        with self.assertRaisesRegex(ValueError, "renamed.*amusing"):
            bundle.resolve(self.config, mode="hiq")

    def test_unsupported_providers_cannot_automatically_enter_through_legacy_pool(self):
        c = bundle.merge(self.config, {"modes": {"unverified": [{"profile": "GCM"}]}})
        with self.assertRaisesRegex(ValueError, "verified adapter"):
            bundle.resolve(c, mode="unverified")
        for code in ("GCM", "EX", "MFMAX", "KK31", "CYBER"):
            exact = bundle.resolve(self.config, code=code, allow_out_of_pool=True, role_override=True)
            self.assertEqual(exact["choices"][0]["code"], code)
            with self.assertRaisesRegex(ValueError, "adapter|Documentary"):
                bundle.launch_plan(exact, ROOT, __file__, ROOT / ".runs/test")


class GenerationTests(unittest.TestCase):
    def test_committed_generated_blocks_match_registry(self):
        self.assertEqual(renderer.render(bundle.load_config(), ROOT / "skills/agent-orch-router", check=True), [])

    def test_overlay_drives_generation_and_drift_check(self):
        config = bundle.merge(bundle.load_config(), {"bindings": {"codex-primary": {"balanced": {"standard": "SX"}}}})
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "mode.md"
            target.write_text("Workflow stays.\n<!-- BEGIN GENERATED:pool:codex-primary/balanced -->\nstale\n<!-- END GENERATED:pool:codex-primary/balanced -->\n")
            with self.assertRaisesRegex(ValueError, "differ"):
                renderer.render(config, root, check=True)
            renderer.render(config, root)
            self.assertIn("standard | SX: gpt-6.1-sol / xhigh", target.read_text())
            self.assertTrue(target.read_text().startswith("Workflow stays."))
            self.assertEqual(renderer.render(config, root, check=True), [])
            target.write_text(target.read_text().replace("SX: gpt-6.1-sol", "SM: gpt-6.1-sol", 1))
            with self.assertRaisesRegex(ValueError, "differ"):
                renderer.render(config, root, check=True)

    def test_explicit_private_registry_does_not_read_public_defaults(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            registry = root / "private.json"
            registry.write_text(json.dumps({"profiles": {"PRIVATE": {"provider": "codex", "model": "private-only", "effort": "low"}},
                                            "catalogs": {"frontier": ["PRIVATE"]}}))
            target = root / "SKILL.md"
            target.write_text("<!-- BEGIN GENERATED:catalog-frontier -->\nstale\n<!-- END GENERATED:catalog-frontier -->\n")
            command = [sys.executable, str(ROOT / "scripts/render_docs.py"), "--config", str(registry), "--root", str(root), "--skill-root", str(root)]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("private-only", target.read_text())
            self.assertNotIn("gpt-6", target.read_text())


if __name__ == "__main__":
    unittest.main()
