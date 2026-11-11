#!/usr/bin/env python3
"""Render registry tables without replacing hand-written workflow instructions."""

import argparse
import importlib.util
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("router_bundle_render", Path(__file__).with_name("bundle.py"))
bundle = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bundle)
BLOCK = re.compile(r"<!-- BEGIN GENERATED:([^>]+) -->\n.*?<!-- END GENERATED:\1 -->", re.S)


def cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def table(headers, rows):
    return "\n".join("| " + " | ".join(map(cell, row)) + " |" for row in
                     [headers, ["---"] * len(headers), *rows])


def exact(item):
    return item.get("model") or item.get("label", "unverified ID")


def catalog_table(config, name):
    rows = []
    extended = name in {"specialists", "conditional"}
    for code in config.get("catalogs", {}).get(name, []):
        item = bundle.profile(config, code)
        row = [code, exact(item), item["effort"] or "unspecified"]
        if extended:
            row += [item.get("specialty", item.get("description", "")), item.get("access_mode", "verify route")]
        rows.append(row)
    return table(["Code", "Exact model", "Effort"] + (["Task exception", "Access"] if extended else []), rows)


def eligibility(entry):
    parts = [", ".join(entry["roles"])] if "roles" in entry else []
    for flag, label in (("specialist", "specialist"), ("independent_review", "independent review"),
                        ("escalation", "escalation"), ("one_off_only", "one-off"),
                        ("requires_verified_adapter", "verified adapter"),
                        ("ongoing_thread_only", "ongoing thread"), ("final_only", "final review")):
        if entry.get(flag):
            parts.append(label)
    return "; ".join(parts) or "general"


def pool_table(config, key):
    if "/" in key:
        variant, mode = key.split("/", 1)
    else:
        variant, mode = config.get("default_variant"), key
    # A private/document-only registry may supply the same pool shape directly.
    if "mode_entries" in config and not config.get("modes"):
        view = {**config, "modes": config["mode_entries"]}
    else:
        view = config
    pool = bundle.mode_pools(view, variant)[mode]
    rows = []
    for entry in pool:
        code = entry["profile"]
        item = bundle.profile(config, code)
        slot = entry.get("slot", "explicit profile")
        fit = entry.get("fit") or config.get("slots", {}).get(slot, {}).get("description") or item.get("description", "")
        rows.append([slot, f"{code}: {exact(item)} / {item['effort'] or 'unspecified'}", eligibility(entry), fit])
    return table(["Slot", "Exact profile", "Eligibility", "Task fit"], rows)


def render_documents(config, skill_root):
    """Return rendered Markdown. Read only the supplied registry and skill folder."""
    rendered = {}
    for path in sorted(Path(skill_root).rglob("*.md")):
        source = path.read_text(encoding="utf-8")
        if "<!-- BEGIN GENERATED:" not in source:
            continue
        def replace(match):
            name = match[1]
            if name.startswith("catalog-"):
                body = catalog_table(config, name[len("catalog-"):])
            elif name.startswith("pool:"):
                body = pool_table(config, name[len("pool:"):])
            else:
                raise ValueError("Unknown generated block: " + name)
            return f"<!-- BEGIN GENERATED:{name} -->\n{body}\n<!-- END GENERATED:{name} -->"
        updated = BLOCK.sub(replace, source)
        if updated.count("<!-- BEGIN GENERATED:") != len(BLOCK.findall(source)):
            raise ValueError("Unclosed generated block in " + str(path))
        rendered[path] = updated
    return rendered


def render(config, skill_root, check=False):
    changes = {path: text for path, text in render_documents(config, skill_root).items()
               if path.read_text(encoding="utf-8") != text}
    if check and changes:
        raise ValueError("Generated tables differ: " + ", ".join(str(path) for path in changes))
    for path, text in changes.items():
        path.write_text(text, encoding="utf-8")
    return list(changes)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--root", type=Path, default=ROOT, help="Configuration/preset root")
    parser.add_argument("--skill-root", type=Path, default=ROOT / "skills/agent-orch-router")
    parser.add_argument("--preset", action="append", default=[])
    parser.add_argument("--overlay", type=Path, action="append", default=[])
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    try:
        config = bundle.load_config(args.config, args.preset, args.overlay, root=args.root, validate_config=False)
        changed = render(config, args.skill_root, args.check)
        print("Generated tables match." if args.check else f"Updated {len(changed)} Markdown files.")
        return 0
    except (KeyError, TypeError, ValueError, OSError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    sys.exit(main())
