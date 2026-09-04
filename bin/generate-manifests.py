#!/usr/bin/env python3
"""
generate-manifests.py — write every <plugin>/.claude-plugin/plugin.json from
the tracked canonical source at bin/manifests.yaml.

`.claude-plugin/` is gitignored, so plugin.json exists only in a working tree.
Without a tracked source, version bumps evaporate on a fresh clone. This script
makes bin/manifests.yaml the source of truth and plugin.json a build artifact.

Usage:
    generate-manifests.py                 # write all manifests
    generate-manifests.py --check         # verify on-disk == expected (CI)
    generate-manifests.py --list          # print name/version table
    generate-manifests.py --only csm vbs  # restrict to named plugins

Exit codes:
    0 — success (or --check found no drift)
    1 — validation failure, or --check found drift / missing files
    2 — usage error (missing manifests.yaml, unknown plugin, bad repo root)

Dependencies: Python 3.7+, PyYAML (`pip install pyyaml`).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

try:
    import yaml  # PyYAML
except ImportError:
    sys.stderr.write("ERROR: PyYAML is required. Install with: pip install pyyaml\n")
    sys.exit(2)

# CHECK 6 — empirical Cowork backend ceiling for plugin.json description.
# See skills/plugin-preflight-validator/references/known-constraints.md.
PLUGIN_DESC_CEILING = 388
PLUGIN_DESC_SAFE_TARGET = 300
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
KEY_ORDER = ("name", "version", "description", "author")

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFESTS_YAML = REPO_ROOT / "bin" / "manifests.yaml"


def load_manifests() -> Dict[str, Dict[str, Any]]:
    if not MANIFESTS_YAML.exists():
        sys.stderr.write(f"ERROR: canonical source not found: {MANIFESTS_YAML}\n")
        sys.exit(2)
    try:
        doc = yaml.safe_load(MANIFESTS_YAML.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as e:
        sys.stderr.write(f"ERROR: could not parse {MANIFESTS_YAML}: {e}\n")
        sys.exit(2)
    plugins = doc.get("plugins")
    if not isinstance(plugins, dict) or not plugins:
        sys.stderr.write(f"ERROR: {MANIFESTS_YAML} has no 'plugins:' mapping\n")
        sys.exit(2)
    return plugins


def build_manifest(name: str, spec: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
    """Return (manifest_dict, errors). Key order normalized to KEY_ORDER."""
    errors: List[str] = []

    version = spec.get("version")
    if not isinstance(version, str) or not SEMVER_RE.match(version):
        errors.append(f"{name}: version {version!r} is not N.N.N")

    desc = spec.get("description")
    if not isinstance(desc, str) or not desc.strip():
        errors.append(f"{name}: description missing or empty")
        desc = ""
    else:
        # YAML folded scalars (>-) leave a single space between lines; normalize
        # any stray whitespace so the char count matches what ships.
        desc = " ".join(desc.split())
        if len(desc) > PLUGIN_DESC_CEILING:
            errors.append(
                f"{name}: description is {len(desc)} chars, over the CHECK 6 "
                f"ceiling of {PLUGIN_DESC_CEILING} by "
                f"{len(desc) - PLUGIN_DESC_CEILING}. Shorten to "
                f"<= {PLUGIN_DESC_SAFE_TARGET} for margin."
            )

    author = spec.get("author")
    if not isinstance(author, dict) or not author.get("name"):
        errors.append(f"{name}: author.name missing")

    plugin_dir = REPO_ROOT / name
    if not plugin_dir.is_dir():
        errors.append(f"{name}: no directory {plugin_dir} — name must match the folder")

    manifest = {"name": name, "version": version, "description": desc, "author": author}
    return {k: manifest[k] for k in KEY_ORDER}, errors


def render(manifest: Dict[str, Any]) -> str:
    return json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Generate .claude-plugin/plugin.json from bin/manifests.yaml."
    )
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true",
                      help="verify on-disk manifests match the source; write nothing")
    mode.add_argument("--list", action="store_true",
                      help="print the name/version/description-length table")
    ap.add_argument("--only", nargs="+", metavar="PLUGIN",
                    help="restrict to the named plugins")
    args = ap.parse_args()

    plugins = load_manifests()

    if args.only:
        unknown = [p for p in args.only if p not in plugins]
        if unknown:
            sys.stderr.write(
                f"ERROR: not in manifests.yaml: {', '.join(unknown)}\n"
                f"Known: {', '.join(sorted(plugins))}\n"
            )
            return 2
        plugins = {k: v for k, v in plugins.items() if k in args.only}

    built: Dict[str, Dict[str, Any]] = {}
    all_errors: List[str] = []
    for name, spec in sorted(plugins.items()):
        manifest, errors = build_manifest(name, spec or {})
        all_errors.extend(errors)
        if not errors:
            built[name] = manifest

    if all_errors:
        sys.stderr.write("VALIDATION FAILED — nothing written:\n")
        for e in all_errors:
            sys.stderr.write(f"  ✗ {e}\n")
        return 1

    if args.list:
        print(f"{'PLUGIN':32} {'VERSION':10} DESC")
        for name, m in built.items():
            print(f"{name:32} {m['version']:10} {len(m['description'])}")
        return 0

    if args.check:
        drift: List[str] = []
        for name, m in built.items():
            pj = REPO_ROOT / name / ".claude-plugin" / "plugin.json"
            if not pj.exists():
                drift.append(f"{name}: {pj.relative_to(REPO_ROOT)} missing "
                             f"(run generate-manifests.py)")
                continue
            try:
                on_disk = json.loads(pj.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as e:
                drift.append(f"{name}: could not read/parse plugin.json: {e}")
                continue
            if on_disk != m:
                drift.append(
                    f"{name}: on-disk plugin.json differs from manifests.yaml "
                    f"(disk v{on_disk.get('version')} vs source v{m['version']})"
                )
        if drift:
            sys.stderr.write("DRIFT DETECTED:\n")
            for d in drift:
                sys.stderr.write(f"  ✗ {d}\n")
            sys.stderr.write(
                "\nmanifests.yaml is the source of truth. Either run "
                "`python3 bin/generate-manifests.py` to regenerate, or update "
                "manifests.yaml if the on-disk value is the intended one.\n"
            )
            return 1
        print(f"✓ no drift — {len(built)} manifest(s) match bin/manifests.yaml")
        return 0

    written = 0
    for name, m in built.items():
        pj_dir = REPO_ROOT / name / ".claude-plugin"
        pj_dir.mkdir(parents=True, exist_ok=True)
        pj = pj_dir / "plugin.json"
        new = render(m)
        old = pj.read_text(encoding="utf-8") if pj.exists() else None
        if old != new:
            pj.write_text(new, encoding="utf-8")
            print(f"  wrote {pj.relative_to(REPO_ROOT)}  (v{m['version']})")
            written += 1
    print(f"✓ {len(built)} manifest(s) generated — {written} changed, "
          f"{len(built) - written} already current")
    return 0


if __name__ == "__main__":
    sys.exit(main())
