"""Keep the two-document native routing path aligned with optional tooling."""

from copy import deepcopy
import importlib.util
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/agent-orch-router"
SPEC = importlib.util.spec_from_file_location("router_bundle", ROOT / "scripts/bundle.py")
bundle = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bundle)


def rows(path):
    return [[cell.strip() for cell in line.strip("|").split("|")]
            for line in path.read_text().splitlines()
            if line.startswith("| ") and not line.startswith("| ---")]


def documented_pool(path):
    pool = []
    flags = {"specialist": "specialist", "independent review": "independent_review",
             "escalation": "escalation", "one-off": "one_off_only",
             "ongoing thread": "ongoing_thread_only", "final review": "final_only",
             "verified adapter": "requires_verified_adapter"}
    for slot, exact, eligibility, task_fit in rows(path)[1:]:
        code = exact.split(": ", 1)[0]
        entry = {"slot": slot, "profile": code, "fit": task_fit}
        for part in eligibility.split("; "):
            if part in flags:
                entry[flags[part]] = True
            elif part != "general":
                entry["roles"] = part.split(", ")
        if not task_fit.strip():
            raise AssertionError("Missing concrete task fit for " + code)
        pool.append(entry)
    return pool


class RouterDocumentTests(unittest.TestCase):
    def setUp(self):
        self.config = bundle.load_config()

    def test_entrypoint_catalog_preserves_every_exact_model_and_effort(self):
        catalog = {row[0]: (row[1], row[2]) for row in rows(SKILL / "SKILL.md")
                   if row[0] in self.config["profiles"]}
        codes = self.config["catalogs"]["frontier"] + self.config["catalogs"]["specialists"]
        self.assertEqual(catalog, {code: (self.config["profiles"][code]["model"],
                                        self.config["profiles"][code]["effort"] or "unspecified") for code in codes})

    def test_selected_mode_pools_preserve_order_and_all_eligibility_fields(self):
        seen = set()
        for variant in self.config["variants"]:
            for mode, expected in bundle.mode_pools(self.config, variant).items():
                name = mode if mode in self.config["modes"] else variant + "-" + mode
                path = SKILL / "modes" / (name + ".md")
                self.assertEqual(documented_pool(path), expected, name)
                seen.add(path)
        self.assertEqual(seen, set((SKILL / "modes").glob("*.md")) - {SKILL / "modes/hiq.md"})

    def test_documented_fences_produce_identical_role_and_lifecycle_decisions(self):
        for variant in self.config["variants"]:
            for mode in bundle.mode_pools(self.config, variant):
                name = mode if mode in self.config["modes"] else variant + "-" + mode
                documented = deepcopy(self.config)
                pool = documented_pool(SKILL / "modes" / (name + ".md"))
                documented["bindings"]["shared"][mode] = {e["slot"]: e["profile"] for e in pool}
                documented["modes"][mode] = [{k: v for k, v in e.items() if k != "profile"} for e in pool]
                for role in self.config["roles"]:
                    for kind in ("bounded", "controller"):
                        for bias in self.config["selection"]["bias_options"]:
                            kwargs = dict(variant=variant, mode=mode, role=role, assignment_kind=kind, bias=bias)
                            if mode in bundle.BURN_PROVIDERS:
                                kwargs.update(burn_account="authorized", burn_endpoint="queue end")
                            try:
                                expected = bundle.resolve(self.config, **kwargs)
                            except ValueError as error:
                                with self.assertRaisesRegex(ValueError, re.escape(str(error))):
                                    bundle.resolve(documented, **kwargs)
                            else:
                                self.assertEqual(bundle.resolve(documented, **kwargs), expected)

    def test_required_native_path_is_entrypoint_and_one_self_contained_mode(self):
        entrypoint = (SKILL / "SKILL.md").read_text()
        targets = re.findall(r"\[[^\]]*\]\((modes/[^)]+)\)", entrypoint)
        expected = {"modes/" + path.name for path in (SKILL / "modes").glob("*.md") if path.name != "hiq.md"}
        self.assertEqual(set(targets), expected)
        self.assertEqual(len(targets), len(expected))
        for target in targets:
            mode = (SKILL / target).read_text()
            self.assertNotRegex(mode, r"\]\([^)]*modes/|\]\([^)]*routing\.json|references/(execution|routing-policy)")
            self.assertIn("Use native workers", mode)
            self.assertIn("installed Claude Delegation skill", mode)
            # Council's opening/critique/ratification protocol needs more than a routing pool.
            self.assertLess(len((entrypoint + mode).split()), 2100 if target == "modes/council.md" else 1750)

    def test_muse_task_fit_matches_catalog(self):
        fits = {slot: task_fit for slot, _, _, task_fit in rows(SKILL / "modes/amusing.md")[1:]}
        for slot in ("investigate", "investigate-deep"):
            entry = next(e for e in self.config["modes"]["amusing"] if e["slot"] == slot)
            self.assertEqual(fits[slot], entry["fit"])
            self.assertIn("Implement when the work order authorizes edits.", fits[slot])

    def test_fable_guidance_has_one_conditional_entrypoint_not_mode_preloads(self):
        target = "references/fable-prompting.md"
        entrypoint = (SKILL / "SKILL.md").read_text()
        links = re.findall(r"\[[^\]]*\]\(([^)]+)\)", entrypoint)
        self.assertEqual(links.count(target), 1)
        self.assertTrue((SKILL / target).is_file())
        # Conditional guidance must not become a required read for every mode worker.
        for mode in (SKILL / "modes").glob("*.md"):
            self.assertNotIn("fable-prompting.md", mode.read_text(), mode.name)
        fable_codes = {code for code, profile in self.config["profiles"].items()
                      if profile["model"] == "claude-fable-5-2"}
        link_paragraph = next(p for p in entrypoint.split("\n\n") if target in p)
        self.assertEqual(set(re.findall(r"\b(?:FM|FH|FX|FMAX)\b", link_paragraph)), fable_codes)

    def test_muse_checks_keep_permission_choice_separate_from_privacy(self):
        checks = (SKILL / "references/muse.md").read_text()
        self.assertIn("Honor the selected permission profile", checks)
        self.assertIn("No read-only or maximum-access profile is required.", checks)
        self.assertIn("verify effective Contributor mode is off", checks)
        self.assertIn("Stop confidential work if effective data handling remains unknown.", checks)


if __name__ == "__main__":
    unittest.main()
