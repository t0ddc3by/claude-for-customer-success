#!/usr/bin/env python3
"""Deliverability Taxonomy Reconciler — executable form of the Phase 0 crosswalk.

Scans an artifact (markdown or JSON) for deliverability-tier vocabulary,
detects which system it uses (canonical 7-tier "C", Product Spec governance
4-tier "A", entry-builder subset "B", or historical v1.0), maps every legacy
value to the canonical two-axis model (evidence tier + roadmap-dependent
boolean), and validates the single sales-eligibility rule. Pre-flight for any
claim gate or deliverability-multiplier computation.

Usage:
    taxonomy_reconcile.py <artifact> [--json]
    taxonomy_reconcile.py --check-tier "<tier>" [--roadmap-dependent]
    taxonomy_reconcile.py --self-test

Stdlib only. Exit codes: 0 canonical/clean; 1 input error; 2 pre-canonical
vocabulary found (report emitted); 3 self-test failure.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

CANONICAL = [
    "Fully Deliverable", "Partially Deliverable", "Conditionally Deliverable",
    "Aspirational", "Requires Investigation", "Provisional", "Not Supported",
]
SALES_ELIGIBLE = {"Fully Deliverable", "Partially Deliverable", "Conditionally Deliverable"}
# Legacy value -> (canonical evidence tier, roadmap_dependent, source system)
CROSSWALK: dict[str, tuple[str, bool, str]] = {
    "Roadmap Dependent": ("(any evidence tier)", True, "A"),
    "Gap Under Investigation": ("Requires Investigation", False, "A"),
    "Always Deliverable": ("Fully Deliverable", False, "v1.0"),
}
A_ONLY = {"Roadmap Dependent", "Gap Under Investigation"}
C_ONLY = {"Partially Deliverable", "Requires Investigation", "Not Supported"}


def scan(text: str) -> dict[str, Any]:
    found: dict[str, int] = {}
    for term in list(CROSSWALK) + CANONICAL:
        n = len(re.findall(re.escape(term), text))
        if n:
            found[term] = n
    legacy = {t: n for t, n in found.items() if t in CROSSWALK}
    c_marks = {t: n for t, n in found.items() if t in C_ONLY}
    if legacy and not c_marks:
        system = "A/v1.0 (pre-canonical)"
    elif legacy:
        system = "mixed (pre-canonical values present alongside canonical)"
    elif found:
        system = "C (canonical 7-tier)" if c_marks else "B-compatible subset (labels shared with canonical; verify authoring tool offers all 7)"
    else:
        system = "none (no deliverability vocabulary found)"
    mappings = [
        {"legacy": t, "canonical_tier": CROSSWALK[t][0], "roadmap_dependent": CROSSWALK[t][1], "occurrences": n}
        for t, n in legacy.items()
    ]
    return {"system_detected": system, "found": found, "pre_canonical": bool(legacy), "mappings": mappings}


def check_tier(tier: str, roadmap_dependent: bool) -> dict[str, Any]:
    canon, rd = tier, roadmap_dependent
    note = None
    if tier in CROSSWALK:
        canon, rd_flag, src = CROSSWALK[tier]
        rd = rd or rd_flag
        note = f"legacy value from system {src}; mapped via crosswalk"
    elif tier not in CANONICAL:
        return {"tier": tier, "error": "unknown tier: not canonical and not in the crosswalk", "sales_committable": False}
    committable = (canon in SALES_ELIGIBLE) and not rd
    guidance = None
    if committable and canon == "Partially Deliverable":
        guidance = "commitment must state the subset boundary"
    elif committable and canon == "Conditionally Deliverable":
        guidance = "commitment must state the verifiable conditions"
    elif not committable and canon in ("Aspirational", "Requires Investigation"):
        guidance = "route to the Roadmap Demand Register; do not silently drop or sell"
    elif rd:
        guidance = "blocked until graduation trigger: GA release + joint CS/Product review"
    return {"tier_input": tier, "canonical_tier": canon, "roadmap_dependent": rd,
            "sales_committable": committable, "guidance": guidance, "note": note}


def self_test() -> int:
    checks: list[tuple[str, bool]] = []
    r = check_tier("Fully Deliverable", False)
    checks.append(("Fully Deliverable committable", r["sales_committable"]))
    r = check_tier("Partially Deliverable", False)
    checks.append(("Partially committable with subset guidance", r["sales_committable"] and "subset" in r["guidance"]))
    r = check_tier("Aspirational", False)
    checks.append(("Aspirational not committable, Register routing", not r["sales_committable"] and "Register" in r["guidance"]))
    r = check_tier("Fully Deliverable", True)
    checks.append(("roadmap-dependent blocks even Fully", not r["sales_committable"]))
    r = check_tier("Roadmap Dependent", False)
    checks.append(("legacy Roadmap Dependent maps to rd=true, blocked", r["roadmap_dependent"] and not r["sales_committable"]))
    r = check_tier("Gap Under Investigation", False)
    checks.append(("legacy Gap maps to Requires Investigation", r["canonical_tier"] == "Requires Investigation"))
    r = check_tier("Always Deliverable", False)
    checks.append(("v1.0 Always maps to Fully", r["canonical_tier"] == "Fully Deliverable" and r["sales_committable"]))
    r = check_tier("Sort Of Deliverable", False)
    checks.append(("unknown tier rejected", "error" in r))
    s = scan("Deliverability Rating: Partially Deliverable ... another: Requires Investigation")
    checks.append(("canonical doc detected", s["system_detected"].startswith("C") and not s["pre_canonical"]))
    s = scan("gapStatus: Roadmap Dependent; also Gap Under Investigation")
    checks.append(("pre-canonical doc flagged with mappings", s["pre_canonical"] and len(s["mappings"]) == 2))
    failures = [n for n, ok in checks if not ok]
    for n, ok in checks:
        print(("PASS " if ok else "FAIL ") + n)
    print(f"\n{len(checks) - len(failures)}/{len(checks)} checks passed")
    return 3 if failures else 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Deliverability taxonomy reconciler")
    ap.add_argument("artifact", nargs="?")
    ap.add_argument("--check-tier")
    ap.add_argument("--roadmap-dependent", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    try:
        if a.self_test:
            return self_test()
        if a.check_tier:
            print(json.dumps(check_tier(a.check_tier, a.roadmap_dependent), indent=2))
            return 0
        if not a.artifact:
            ap.print_help()
            return 1
        result = scan(Path(a.artifact).read_text())
        print(json.dumps(result, indent=2) if a.json else
              f"system: {result['system_detected']}\nfound: {result['found']}\nmappings: {result['mappings']}")
        return 2 if result["pre_canonical"] else 0
    except OSError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
