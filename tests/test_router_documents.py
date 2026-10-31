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
    for code, eligibility, task_fit in rows(path)[1:]:
        entry = {"profile": code}
        if eligibility == "one-off":
            entry["one_off_only"] = True
        elif eligibility == "escalation":
            entry["escalation"] = True
        elif "; " in eligibility:
            roles, marker = eligibility.split("; ")
            entry["roles"] = roles.split(", ")
            entry[{"specialist": "specialist", "independent review": "independent_review"}[marker]] = True
        elif ", " in eligibility:
            entry["roles"] = eligibility.split(", ")
        elif eligibility != "general":
            raise AssertionError("Unknown eligibility: " + eligibility)
        if len(task_fit.split()) < 8:
            raise AssertionError("Missing concrete task fit for " + code)
        pool.append(entry)
    return pool


class RouterDocumentTests(unittest.TestCase):
    def setUp(self):
        self.config = bundle.load_config()

    def test_entrypoint_catalog_preserves_every_exact_model_and_effort(self):
        catalog = {row[0]: (row[1], row[2]) for row in rows(SKILL / "SKILL.md")
                   if row[0] in self.config["profiles"]}
        self.assertEqual(catalog, {code: (p["model"], p["effort"])
                                   for code, p in self.config["profiles"].items()})

    def test_selected_mode_pools_preserve_order_and_all_eligibility_fields(self):
        seen = set()
        for variant in self.config["variants"]:
            for mode, expected in bundle.mode_pools(self.config, variant).items():
                name = mode if mode in self.config["modes"] else variant + "-" + mode
                path = SKILL / "modes" / (name + ".md")
                self.assertEqual(documented_pool(path), expected, name)
                seen.add(path)
        self.assertEqual(seen, set((SKILL / "modes").glob("*.md")))

    def test_documented_fences_produce_identical_role_and_lifecycle_decisions(self):
        for variant in self.config["variants"]:
            for mode in bundle.mode_pools(self.config, variant):
                name = mode if mode in self.config["modes"] else variant + "-" + mode
                documented = deepcopy(self.config)
                documented["modes"][mode] = documented_pool(SKILL / "modes" / (name + ".md"))
                for role in self.config["roles"]:
                    for kind in ("bounded", "controller"):
                        for bias in self.config["selection"]["bias_options"]:
                            kwargs = dict(variant=variant, mode=mode, role=role, assignment_kind=kind, bias=bias)
                            if mode in bundle.BURN_PROVIDERS:
                                kwargs.update(burn_account="authorized", burn_endpoint="queue end")
                            self.assertEqual(bundle.resolve(documented, **kwargs), bundle.resolve(self.config, **kwargs))

    def test_required_native_path_is_entrypoint_and_one_self_contained_mode(self):
        entrypoint = (SKILL / "SKILL.md").read_text()
        targets = re.findall(r"\[[^\]]*\]\((modes/[^)]+)\)", entrypoint)
        self.assertEqual(len(targets), 9)
        for target in targets:
            mode = (SKILL / target).read_text()
            self.assertNotRegex(mode, r"\]\([^)]*modes/|\]\([^)]*routing\.json|references/(execution|routing-policy)")
            self.assertIn("Use native workers", mode)
            self.assertIn("installed Claude Delegation skill", mode)
            self.assertLess(len((entrypoint + mode).split()), 1200)


if __name__ == "__main__":
    unittest.main()
