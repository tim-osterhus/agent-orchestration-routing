"""Keep progressive routing documents aligned with executable contracts."""

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
             "verified adapter": "requires_verified_adapter", "explicit selection": "explicit_only"}
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

    def test_full_catalog_and_compact_index_preserve_every_exact_model_and_effort(self):
        catalog = {row[0]: (row[1], row[2]) for row in rows(SKILL / "references/catalog.md")
                   if row[0] in self.config["profiles"]}
        codes = self.config["catalogs"]["frontier"] + self.config["catalogs"]["specialists"]
        expected = {code: (self.config["profiles"][code]["model"],
                           self.config["profiles"][code]["effort"] or "unspecified") for code in codes}
        self.assertEqual(catalog, expected)
        efforts = {"l": "low", "m": "medium", "h": "high", "x": "xhigh",
                   "max": "max", "unspecified": "unspecified"}
        compact = {}
        models = {profile["model"] for profile in self.config["profiles"].values()}
        for row in rows(SKILL / "SKILL.md"):
            if len(row) != 2 or row[0] not in models or " → " not in row[1]:
                continue
            aliases, levels = row[1].split(" → ")
            aliases, levels = aliases.split("/"), levels.split("/")
            self.assertEqual(len(aliases), len(levels))
            for code, level in zip(aliases, levels):
                self.assertNotIn(code, compact)
                compact[code] = (row[0], efforts[level])
        self.assertEqual(compact, expected)

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

    def test_native_path_reaches_shared_dispatch_and_exactly_one_selected_mode(self):
        entrypoint = (SKILL / "SKILL.md").read_text()
        self.assertLessEqual(len(entrypoint.split()), 400)
        targets = re.findall(r"\[[^\]]*\]\((modes/[^)]+)\)", entrypoint)
        expected = {"modes/" + path.name for path in (SKILL / "modes").glob("*.md") if path.name != "hiq.md"}
        self.assertEqual(set(targets), expected)
        self.assertEqual(len(targets), len(expected))
        self.assertIn("](references/dispatch.md)", entrypoint)
        shared = (SKILL / "references/dispatch.md").read_text()
        self.assertIn("Use native workers", shared)
        self.assertIn("Native Codex workers remain leaves", shared)
        self.assertIn("Null/omitted caps", shared)
        self.assertIn("external-session cap does not gate uncapped native workers", shared)
        self.assertIn("Reviewers need reassignment to fix", shared)
        # Execution mechanics are authoritative in shared dispatch, not copied
        # into every mode. Mode-specific launch designs remain local.
        for target in targets:
            mode = (SKILL / target).read_text()
            # Count the complete required native read, not conditional provider references.
            budget = 2100 if target in {"modes/council.md", "modes/ui-pro.md"} else 1750
            self.assertLessEqual(len((entrypoint + shared + mode).split()), budget, target)
            self.assertIn("](../references/dispatch.md)", mode)
            self.assertNotRegex(mode, r"\]\([^)]*modes/|\]\([^)]*routing\.json|references/(execution|routing-policy)")
            if target != "modes/browser-3d.md":
                self.assertNotIn("installed Claude Delegation skill", mode)

    def test_skill_markdown_links_resolve(self):
        for source in SKILL.rglob("*.md"):
            for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", source.read_text()):
                if "://" in target or target.startswith("#"):
                    continue
                self.assertTrue((source.parent / target.split("#", 1)[0]).is_file(),
                                f"{source.relative_to(SKILL)}: {target}")

    def test_coding_acceptance_is_conditional_and_complete_paths_remain_bounded(self):
        entrypoint = (SKILL / "SKILL.md").read_text()
        shared = (SKILL / "references/dispatch.md").read_text()
        acceptance = (SKILL / "references/coding-acceptance.md").read_text()
        self.assertNotIn("coding-acceptance.md", entrypoint)
        links = re.findall(r"\[[^\]]*\]\(([^)]+)\)", shared)
        self.assertEqual(links.count("coding-acceptance.md"), 1)
        for mode in (SKILL / "modes").glob("*.md"):
            if mode.name == "hiq.md":
                continue
            with self.subTest(mode=mode.name):
                # Count the conditional document once, including when the mode
                # also links it. Ordinary research paths retain the old budgets.
                path = entrypoint + shared + mode.read_text() + acceptance
                budget = 2650 if mode.name in {"council.md", "ui-pro.md"} else 2300
                self.assertLessEqual(len(path.split()), budget)

    def test_provider_defaults_and_mode_specific_controller_contracts_remain_distinct(self):
        shared = (SKILL / "references/dispatch.md").read_text()
        self.assertIn("](claude-execution.md)", shared)
        self.assertIn("](muse.md)", shared)
        claude = (SKILL / "references/claude-execution.md").read_text()
        self.assertIn("installed Claude Delegation skill", claude)
        self.assertIn("QA/spec review defaults to Consultation", claude)
        self.assertIn("Frontier Research research/review", claude)
        self.assertIn("Authored work defaults to Implementation", claude)
        browser = (SKILL / "modes/browser-3d.md").read_text()
        self.assertIn("existing Claude Code **FH:", browser)
        self.assertIn("`--design claude-first`", browser)
        self.assertIn("not replacement of this running FH parent", browser)
        research = (SKILL / "modes/frontier-research.md").read_text()
        self.assertIn("reviewer's blind failure modes before revealing the proposal", research)
        self.assertIn("Two same-model runs do not establish model diversity", research)
        council = (SKILL / "modes/council.md").read_text()
        self.assertIn("every required member to endorse the same final proposal", council)
        self.assertIn("Never combine mixed-version endorsements", council)
        ui = (SKILL / "modes/ui-pro.md").read_text()
        self.assertIn("identical final revision/build", ui)
        self.assertIn("same-build evidence", ui)

    def test_muse_task_fit_matches_catalog(self):
        fits = {slot: task_fit for slot, _, _, task_fit in rows(SKILL / "modes/amusing.md")[1:]}
        for slot in ("investigate", "investigate-deep"):
            entry = next(e for e in self.config["modes"]["amusing"] if e["slot"] == slot)
            self.assertEqual(fits[slot], entry["fit"])
            self.assertIn("Implement when the work order authorizes edits.", fits[slot])

    def test_fable_guidance_has_one_conditional_entrypoint_not_mode_preloads(self):
        target = "references/fable-prompting.md"
        shared = (SKILL / "references/dispatch.md").read_text()
        links = re.findall(r"\[[^\]]*\]\(([^)]+)\)", shared)
        self.assertEqual(links.count("fable-prompting.md"), 1)
        self.assertTrue((SKILL / target).is_file())
        # Conditional guidance must not become a required read for every mode worker.
        for mode in (SKILL / "modes").glob("*.md"):
            self.assertNotIn("fable-prompting.md", mode.read_text(), mode.name)
        fable_codes = {code for code, profile in self.config["profiles"].items()
                      if profile["model"] == "claude-fable-5-2"}
        link_paragraph = next(p for p in shared.splitlines() if "](fable-prompting.md)" in p)
        self.assertEqual(set(re.findall(r"\b(?:FM|FH|FX|FMAX)\b", link_paragraph)), fable_codes)

    def test_muse_checks_keep_permission_choice_separate_from_privacy(self):
        checks = (SKILL / "references/muse.md").read_text()
        self.assertIn("Honor the selected permission profile", checks)
        self.assertIn("No read-only or maximum-access profile is required.", checks)
        self.assertIn("verify effective Contributor mode is off", checks)
        self.assertIn("Stop confidential work if effective data handling remains unknown.", checks)


if __name__ == "__main__":
    unittest.main()
