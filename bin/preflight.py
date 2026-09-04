#!/usr/bin/env python3
"""
Plugin preflight validator — 8 known Cowork backend constraint checks.

Runs against a plugin directory (containing .claude-plugin/plugin.json) and
exits non-zero if any BLOCK-level finding is detected. Prevents the opaque
"Plugin validation failed" backend error by catching known issues before
packaging.

Usage:
    preflight.py <plugin_dir> [<plugin_dir> ...]
    preflight.py --all [<parent_dir>]              # auto-detect plugins
    preflight.py --help

Exit codes:
    0 — all plugins pass
    1 — one or more BLOCK findings
    2 — usage error or no plugins found

Constraint reference: skills/plugin-preflight-validator/references/known-constraints.md
Encodes CHECKs 1-8 from plugin-validation-toolkit v1.3.0 (2026-05-25).

Dependencies: Python 3.7+, PyYAML (`pip install pyyaml`).
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys
from pathlib import Path
from typing import List, Tuple

try:
    import yaml  # PyYAML
except ImportError:
    sys.stderr.write(
        "ERROR: PyYAML is required. Install with: pip install pyyaml\n"
    )
    sys.exit(2)

# --- Constants derived from plugin-validation-toolkit v1.3.0 ---
NAME_RE = re.compile(r"^([a-z][a-z0-9-]*:)?[a-z][a-z0-9-]*$")
SKILL_DESC_LIMIT = 1024            # CHECK 2
PLUGIN_DESC_CEILING = 388          # CHECK 6 (empirical; safe target ≤300)
VAR_INTERPOLATION_RE = re.compile(r"\$\{[^}]+\}")   # CHECK 7
DOT_DOT_TRAVERSAL_RE = re.compile(r"\.\./")          # CHECK 8b
HOOK_SCRIPT_EXTS = {".sh", ".bash", ".py"}           # CHECK 8b


class Finding:
    __slots__ = ("severity", "check", "path", "message", "remediation")

    def __init__(self, severity: str, check: str, path: str,
                 message: str, remediation: str) -> None:
        self.severity = severity
        self.check = check
        self.path = path
        self.message = message
        self.remediation = remediation

    def render(self) -> str:
        return (
            f"  [{self.severity}] {self.check}\n"
            f"    file: {self.path}\n"
            f"    {self.message}\n"
            f"    → {self.remediation}"
        )


def parse_frontmatter(content: str) -> Tuple[dict | None, str | None]:
    if not content.startswith("---"):
        return None, "no frontmatter block"
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None, "malformed frontmatter (missing closing ---)"
    try:
        return (yaml.safe_load(parts[1]) or {}), None
    except yaml.YAMLError as e:
        return None, f"YAML parse error: {e}"


def check_skill_md(skill_path: Path, plugin_root: Path) -> List[Finding]:
    rel = skill_path.relative_to(plugin_root)
    findings: List[Finding] = []
    try:
        content = skill_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        findings.append(Finding(
            "BLOCK", "skill_read_error", str(rel),
            f"could not read: {e}", "Ensure file is UTF-8 encoded and readable"
        ))
        return findings

    fm, err = parse_frontmatter(content)
    if err:
        findings.append(Finding(
            "BLOCK", "frontmatter_parse", str(rel),
            err, "Add valid --- delimited YAML frontmatter"
        ))
        return findings

    # CHECK 1 — security: block in frontmatter (plugin deployment forbidden)
    if "security" in fm:
        findings.append(Finding(
            "BLOCK", "CHECK 1: security_block_in_frontmatter", str(rel),
            "security: block present in frontmatter",
            "Remove security: block. Move contract to ## Security & Permissions "
            "and ## Trust & Verification body sections."
        ))

    # CHECK 2 — description length
    desc = fm.get("description", "")
    if isinstance(desc, str) and len(desc) > SKILL_DESC_LIMIT:
        findings.append(Finding(
            "BLOCK", "CHECK 2: description_too_long", str(rel),
            f"description is {len(desc)} chars "
            f"(limit: {SKILL_DESC_LIMIT}, over by {len(desc) - SKILL_DESC_LIMIT})",
            f"Reduce description by at least {len(desc) - SKILL_DESC_LIMIT} chars. "
            f"Target ≤ 900 chars for 12% safety margin."
        ))

    # CHECK 3 — name format (kebab-case, optional plugin: namespace prefix)
    name = fm.get("name", "")
    if not (isinstance(name, str) and NAME_RE.match(name)):
        findings.append(Finding(
            "BLOCK", "CHECK 3: name_format_invalid", str(rel),
            f"name {name!r} is not valid kebab-case",
            "Use ^([a-z][a-z0-9-]*:)?[a-z][a-z0-9-]*$ — lowercase letters/digits/"
            "hyphens, with an optional 'plugin-name:' prefix. Empirically confirmed: "
            "the Cowork validator accepts namespaced names (e.g., 'rev-ops:csql-tracking')."
        ))

    # CHECKs 4/5 — nested inside security block (informational if CHECK 1 fires)
    sec = fm.get("security")
    if isinstance(sec, dict):
        if sec.get("dynamic_code_execution") is True:
            findings.append(Finding(
                "BLOCK", "CHECK 4: dynamic_code_execution_true", str(rel),
                "security.dynamic_code_execution: true",
                "Remove or set to false. Prohibited capability."
            ))
        if sec.get("requires_elevated") is True:
            findings.append(Finding(
                "BLOCK", "CHECK 5: requires_elevated_true", str(rel),
                "security.requires_elevated: true",
                "Remove or set to false. Elevated permissions require catalog review."
            ))

    return findings


def check_plugin_json(plugin_root: Path) -> List[Finding]:
    """CHECK 6 — plugin.json description length ≤ 388 chars."""
    pj_path = plugin_root / ".claude-plugin" / "plugin.json"
    if not pj_path.exists():
        return [Finding(
            "BLOCK", "plugin_json_missing", ".claude-plugin/plugin.json",
            f"plugin manifest not found at {pj_path.relative_to(plugin_root)}",
            "Create .claude-plugin/plugin.json with at minimum name + version."
        )]
    try:
        pj = json.loads(pj_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        return [Finding(
            "BLOCK", "plugin_json_parse", ".claude-plugin/plugin.json",
            f"could not parse: {e}", "Fix JSON syntax."
        )]

    findings: List[Finding] = []
    desc = pj.get("description", "")
    if isinstance(desc, str) and len(desc) > PLUGIN_DESC_CEILING:
        findings.append(Finding(
            "BLOCK", "CHECK 6: plugin_json_description_too_long",
            ".claude-plugin/plugin.json",
            f"description is {len(desc)} chars "
            f"(empirical ceiling: {PLUGIN_DESC_CEILING}, "
            f"over by {len(desc) - PLUGIN_DESC_CEILING})",
            f"Shorten to ≤ 300 chars (safe target). Move detail into SKILL.md "
            f"descriptions (separate ≤ 1024 ceiling per CHECK 2) or README."
        ))
    return findings


def check_mcp_json(plugin_root: Path) -> List[Finding]:
    """CHECK 7 — .mcp.json URL fields must not contain ${VAR} interpolation."""
    mcp_path = plugin_root / ".mcp.json"
    if not mcp_path.exists():
        return []  # optional file; absence is fine

    try:
        mcp = json.loads(mcp_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        return [Finding(
            "BLOCK", "mcp_json_parse", ".mcp.json",
            f"could not parse: {e}", "Fix JSON syntax."
        )]

    findings: List[Finding] = []
    servers = mcp.get("mcpServers", {})
    if not isinstance(servers, dict):
        return findings

    for server_name, cfg in servers.items():
        if not isinstance(cfg, dict):
            continue
        url = cfg.get("url", "")
        if isinstance(url, str) and VAR_INTERPOLATION_RE.search(url):
            findings.append(Finding(
                "BLOCK", "CHECK 7: mcp_json_url_has_var_interpolation",
                ".mcp.json",
                f'server "{server_name}" URL contains ${{VAR}}: {url!r}',
                "Replace with literal placeholder URL "
                "(e.g., 'https://<name>-mcp.example.com/mcp'). "
                "${VAR:-default} fallback syntax is also rejected. "
                "Document URL replacement in README."
            ))
    return findings


def check_hooks(plugin_root: Path) -> List[Finding]:
    """CHECK 8 — hooks/hooks.json nested schema + no '..' in hook scripts."""
    hooks_dir = plugin_root / "hooks"
    if not hooks_dir.is_dir():
        return []  # optional directory; absence is fine

    findings: List[Finding] = []

    # CHECK 8a — hooks.json schema
    hooks_json = hooks_dir / "hooks.json"
    if hooks_json.exists():
        try:
            h = json.loads(hooks_json.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            findings.append(Finding(
                "BLOCK", "hooks_json_parse", "hooks/hooks.json",
                f"could not parse: {e}", "Fix JSON syntax."
            ))
        else:
            hooks_val = h.get("hooks")
            if isinstance(hooks_val, list):
                findings.append(Finding(
                    "BLOCK", "CHECK 8a: hooks_json_flat_schema",
                    "hooks/hooks.json",
                    'hooks.json uses flat schema {"hooks": [...]}',
                    'Convert to nested {"hooks": {"EventName": '
                    '[{"matcher": ..., "hooks": [{"type": "command", "command": ...}]}]}}. '
                    "Use ${CLAUDE_PLUGIN_ROOT}/hooks/... for plugin-relative paths."
                ))

    # CHECK 8b — no '..' path traversal in any shell/python script under hooks/
    for script_path in hooks_dir.rglob("*"):
        if not script_path.is_file() or script_path.suffix not in HOOK_SCRIPT_EXTS:
            continue
        try:
            content = script_path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if DOT_DOT_TRAVERSAL_RE.search(content):
            findings.append(Finding(
                "BLOCK", "CHECK 8b: hooks_script_path_traversal",
                str(script_path.relative_to(plugin_root)),
                "contains '..' cross-plugin path reference",
                "Remove any '../' path defaults. Use ${CLAUDE_PLUGIN_ROOT}/... "
                "for plugin-relative paths or an absolute path from env var "
                "with /dev/null fallback for graceful no-op."
            ))
    return findings


def validate_plugin(plugin_root: Path) -> Tuple[int, int, List[Finding]]:
    """Run all 8 checks against a single plugin directory.

    Returns: (num_skills_scanned, num_blocks, findings)
    """
    all_findings: List[Finding] = []

    # CHECKs 1-5 per SKILL.md
    skill_files = sorted(plugin_root.glob("skills/*/SKILL.md"))
    for sp in skill_files:
        all_findings.extend(check_skill_md(sp, plugin_root))

    # CHECK 6 — plugin.json once per plugin
    all_findings.extend(check_plugin_json(plugin_root))
    # CHECK 7 — .mcp.json once per plugin (skips if absent)
    all_findings.extend(check_mcp_json(plugin_root))
    # CHECK 8 — hooks/ once per plugin (skips if absent)
    all_findings.extend(check_hooks(plugin_root))

    blocks = sum(1 for f in all_findings if f.severity == "BLOCK")
    return len(skill_files), blocks, all_findings


def is_plugin_dir(path: Path) -> bool:
    return (path / ".claude-plugin" / "plugin.json").is_file()


def discover_plugins(parent: Path) -> List[Path]:
    return sorted(
        p for p in parent.iterdir()
        if p.is_dir() and is_plugin_dir(p)
    )


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Preflight validator for Cowork plugins (CHECKs 1-8).",
        epilog="Exit codes: 0 = all pass, 1 = BLOCK findings, 2 = usage error"
    )
    parser.add_argument(
        "plugin_dirs", nargs="*",
        help="One or more plugin directories to validate"
    )
    parser.add_argument(
        "--all", action="store_true",
        help="Auto-detect all plugins under the given parent directory (default: cwd)"
    )
    parser.add_argument(
        "--parent", default=".",
        help="Parent directory for --all discovery (default: current directory)"
    )
    parser.add_argument(
        "--quiet", "-q", action="store_true",
        help="Suppress the per-plugin PASS lines; only print failures"
    )
    args = parser.parse_args(argv)

    # Resolve plugin dirs to scan
    if args.all:
        parent = Path(args.parent).resolve()
        if not parent.is_dir():
            sys.stderr.write(f"ERROR: parent directory not found: {parent}\n")
            return 2
        plugins = discover_plugins(parent)
        if not plugins:
            sys.stderr.write(
                f"ERROR: no plugins found under {parent} "
                f"(no subdirectory contains .claude-plugin/plugin.json)\n"
            )
            return 2
    elif args.plugin_dirs:
        plugins = [Path(p).resolve() for p in args.plugin_dirs]
        for p in plugins:
            if not is_plugin_dir(p):
                sys.stderr.write(
                    f"ERROR: {p} is not a plugin directory "
                    f"(missing .claude-plugin/plugin.json)\n"
                )
                return 2
    else:
        parser.print_help(sys.stderr)
        return 2

    print(f"PLUGIN PREFLIGHT — validating {len(plugins)} plugin(s)")
    print(f"Checks: CHECKs 1-8 per plugin-validation-toolkit v1.3.1")
    print()

    total_blocks = 0
    failed_plugins = 0

    for plugin_root in plugins:
        name = plugin_root.name
        skills_n, blocks, findings = validate_plugin(plugin_root)
        total_blocks += blocks

        if blocks:
            failed_plugins += 1
            print(f"✗ FAIL: {name}  ({skills_n} skill(s) scanned, {blocks} BLOCK(s))")
            for f in findings:
                if f.severity == "BLOCK":
                    print(f.render())
            print()
        else:
            if not args.quiet:
                print(f"✓ PASS: {name}  ({skills_n} skill(s) scanned, 0 BLOCK(s))")

    print()
    print("=" * 60)
    if total_blocks:
        print(
            f"RESULT: FAIL — {failed_plugins}/{len(plugins)} plugin(s) failed, "
            f"{total_blocks} total BLOCK finding(s)"
        )
        return 1
    print(f"RESULT: PASS — {len(plugins)}/{len(plugins)} plugin(s) clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
