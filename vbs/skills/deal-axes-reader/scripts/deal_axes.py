#!/usr/bin/env python3
"""Deal Axes Engine — the ETM's two pre-sale instruments at deal grain.

Implements the Expanded Triaxial Model's value-validation parallel state (five
states) and buying-readiness inferred ladder (seven rungs, first-missing-rung
governs) over an append-only evidence-event log per deal. Core rules enforced:
only buyer-verifiable evidence moves an instrument; readiness is computed,
never declared; assertions are recorded with names and staleness windows;
declared pipeline stage vs. computed validation state produces the divergence
read; every close (won / lost / no_decision) freezes both readings, with
validation_shortfall_flag on wins below Business Case Accepted.

Usage:
    deal_axes.py evidence <deal.jsonl> --kind <evidence_kind> --ref "<artifact>" [--buyer-verifiable] [--by <who>]
    deal_axes.py invalidate <deal.jsonl> --ref "<artifact>" --reason "<why>"
    deal_axes.py assert <deal.jsonl> --rung <1-7> --by <rep> --claim "<text>"
    deal_axes.py declare-stage <deal.jsonl> --stage <1-7> --by <who>
    deal_axes.py read <deal.jsonl> [--stale-days N]
    deal_axes.py close <deal.jsonl> --outcome won|lost|no_decision
    deal_axes.py --self-test

Stdlib only. Exit: 0 ok; 1 input error; 2 rule violation; 3 self-test failure.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

VALIDATION_STATES = [
    "Problem Evidenced", "Success Criteria Agreed", "Value Quantified",
    "Proof Demonstrated", "Business Case Accepted",
]
RUNGS = [
    "Pain Evidenced", "Power Engaged", "Vision Aligned", "Impact Quantified",
    "Decision Process Mapped", "Paper Process Known", "Commitment Evidenced",
]
# Evidence kinds -> (validation state index or None, rung index or None)
EVIDENCE_MAP: dict[str, tuple[int | None, int | None]] = {
    "problem_statement_confirmed": (0, 0),
    "recorded_pain_call": (0, 0),
    "success_criteria_signed": (1, None),
    "buyer_value_inputs_confirmed": (2, 3),
    "pilot_reviewed_against_criteria": (3, None),
    "demo_buyer_verdict": (3, None),
    "business_case_eb_response": (4, None),
    "economic_buyer_meeting": (None, 1),
    "champion_internal_action": (None, 1),
    "decision_criteria_documented": (None, 2),
    "buyer_fit_confirmation": (None, 2),
    "decision_process_map_confirmed": (None, 4),
    "procurement_requirements_named": (None, 5),
    "security_questionnaire_received": (None, 5),
    "map_buyer_tasks_completing": (None, 6),
    "buyer_initiated_procurement": (None, 6),
    "seller_sent_artifact": (None, None),  # recordable; moves nothing
}
PIPELINE_STAGES = ["Prospecting", "Qualified", "Discovery", "Demo/Evaluation", "Proposal", "Negotiation/Commit", "Closed"]
# Validation state typically travels with pipeline stages (index ranges, 1-based stages)
TRAVELS_WITH = {0: (2, 3), 1: (3, 4), 2: (4, 5), 3: (4, 5), 4: (5, 6)}
DEFAULT_STALE_DAYS = 21


class RuleViolation(Exception):
    pass


def _events(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]


def _append(path: Path, ev: dict[str, Any]) -> None:
    ev.setdefault("ts", date.today().isoformat())
    with path.open("a") as f:
        f.write(json.dumps(ev) + "\n")


def add_evidence(path: Path, kind: str, ref: str, buyer_verifiable: bool, by: str) -> None:
    if kind not in EVIDENCE_MAP:
        raise RuleViolation(f"unknown evidence kind {kind!r}; admissible kinds: {sorted(EVIDENCE_MAP)}")
    if _closed(path):
        raise RuleViolation("deal is closed; readings are frozen")
    _append(path, {"event": "evidence", "kind": kind, "ref": ref, "buyer_verifiable": buyer_verifiable, "by": by})


def invalidate(path: Path, ref: str, reason: str) -> None:
    if not any(e.get("ref") == ref for e in _events(path) if e["event"] == "evidence"):
        raise RuleViolation(f"no evidence with ref {ref!r} to invalidate")
    _append(path, {"event": "invalidate", "ref": ref, "reason": reason})


def add_assertion(path: Path, rung: int, by: str, claim: str) -> None:
    if not 1 <= rung <= 7:
        raise RuleViolation("rung must be 1-7")
    if not by.strip():
        raise RuleViolation("assertions carry the asserter's name; anonymous assertions are refused")
    _append(path, {"event": "assertion", "rung": rung, "by": by, "claim": claim})


def declare_stage(path: Path, stage: int, by: str) -> None:
    if not 1 <= stage <= 7:
        raise RuleViolation("pipeline stage must be 1-7")
    _append(path, {"event": "declare_stage", "stage": stage, "by": by})


def _closed(path: Path) -> dict[str, Any] | None:
    for e in reversed(_events(path)):
        if e["event"] == "close":
            return e
    return None


def read(path: Path, stale_days: int = DEFAULT_STALE_DAYS) -> dict[str, Any]:
    evs = _events(path)
    dead = {e["ref"] for e in evs if e["event"] == "invalidate"}
    live = [e for e in evs if e["event"] == "evidence" and e["ref"] not in dead]
    verifiable = [e for e in live if e.get("buyer_verifiable")]
    ignored_non_verifiable = [e["ref"] for e in live if not e.get("buyer_verifiable")]

    # Validation state: highest contiguous... ETM defines states as evidence-supported individually;
    # the recorded state is the highest state with verifiable evidence, and gaps below are reported.
    v_supported = sorted({EVIDENCE_MAP[e["kind"]][0] for e in verifiable if EVIDENCE_MAP[e["kind"]][0] is not None})
    v_state = VALIDATION_STATES[max(v_supported)] if v_supported else None
    v_gaps = [VALIDATION_STATES[i] for i in range(max(v_supported) + 1) if i not in v_supported] if v_supported else []

    # Readiness ladder: first missing rung governs, strictly.
    r_supported = {EVIDENCE_MAP[e["kind"]][1] for e in verifiable if EVIDENCE_MAP[e["kind"]][1] is not None}
    governing = 0
    while governing in r_supported:
        governing += 1
    rung_read = governing  # number of contiguous rungs established (0..7)
    above_gap = sorted(r for r in r_supported if r > governing)

    # Assertions: uncorroborated past staleness become warnings.
    warnings: list[str] = []
    today = date.today()
    for a in (e for e in evs if e["event"] == "assertion"):
        rung_idx = a["rung"] - 1
        if rung_idx not in r_supported:
            age = (today - datetime.strptime(a["ts"], "%Y-%m-%d").date()).days
            if age > stale_days:
                warnings.append(
                    f"stale assertion: rung {a['rung']} ({RUNGS[rung_idx]}) asserted by {a['by']} "
                    f"{age}d ago, never corroborated by buyer-verifiable evidence"
                )

    # Divergence: declared stage vs validation expectation.
    declared = next((e["stage"] for e in reversed(evs) if e["event"] == "declare_stage"), None)
    divergence = None
    if declared and v_state:
        lo, hi = TRAVELS_WITH[VALIDATION_STATES.index(v_state)]
        if declared > hi:
            divergence = f"SLIPPING: declared stage {declared} ({PIPELINE_STAGES[declared-1]}) is ahead of validation ({v_state} typically travels with stages {lo}-{hi}); paperwork is outrunning the value case"
        elif declared < lo:
            divergence = f"AHEAD: validation ({v_state}) is ahead of declared stage {declared}; positive signal"
    elif declared and not v_state:
        divergence = f"SLIPPING: declared stage {declared} with no buyer-verifiable validation evidence at all"

    return {
        "validation_state": v_state,
        "validation_gaps_below": v_gaps,
        "readiness_rungs_established": rung_read,
        "readiness_governing_gap": RUNGS[governing] if governing < 7 else None,
        "readiness_evidence_above_gap": [RUNGS[r] for r in above_gap],
        "declared_stage": PIPELINE_STAGES[declared - 1] if declared else None,
        "divergence": divergence,
        "stale_assertion_warnings": warnings,
        "non_verifiable_ignored": ignored_non_verifiable,
        "closed": _closed(path),
    }


def close(path: Path, outcome: str) -> dict[str, Any]:
    if outcome not in ("won", "lost", "no_decision"):
        raise RuleViolation("outcome must be won | lost | no_decision")
    if _closed(path):
        raise RuleViolation("deal already closed")
    final = read(path)
    shortfall = outcome == "won" and final["validation_state"] != "Business Case Accepted"
    record = {
        "event": "close", "outcome": outcome,
        "final_validation_state": final["validation_state"],
        "final_readiness_rungs": final["readiness_rungs_established"],
        "final_governing_gap": final["readiness_governing_gap"],
        "validation_shortfall_flag": shortfall,
    }
    _append(path, record)
    return record


# ------------------------------------------------------------------ self-test
def self_test() -> int:
    import tempfile
    ok: list[tuple[str, bool]] = []
    with tempfile.TemporaryDirectory() as td:
        d = Path(td) / "deal.jsonl"
        # seller-sent artifacts move nothing
        add_evidence(d, "seller_sent_artifact", "value-deck-v1", buyer_verifiable=False, by="rep")
        r = read(d)
        ok.append(("seller-sent moves nothing", r["validation_state"] is None and r["readiness_rungs_established"] == 0))
        ok.append(("non-verifiable listed as ignored", "value-deck-v1" in r["non_verifiable_ignored"]))

        add_evidence(d, "recorded_pain_call", "call-2026-08-01", buyer_verifiable=True, by="rep")
        r = read(d)
        ok.append(("pain evidence -> state 1 + rung 1", r["validation_state"] == "Problem Evidenced" and r["readiness_rungs_established"] == 1))

        # MAP evidence (rung 7) with no rung 2: first missing rung governs
        add_evidence(d, "map_buyer_tasks_completing", "map-v2", buyer_verifiable=True, by="rep")
        r = read(d)
        ok.append(("first-missing-rung governs (happy ears)", r["readiness_rungs_established"] == 1
                   and r["readiness_governing_gap"] == "Power Engaged"
                   and "Commitment Evidenced" in r["readiness_evidence_above_gap"]))

        # stale assertion warning
        _append(d, {"event": "assertion", "rung": 2, "by": "rep", "claim": "champion exists",
                    "ts": (date.today() - timedelta(days=40)).isoformat()})
        r = read(d)
        ok.append(("stale uncorroborated assertion warns", len(r["stale_assertion_warnings"]) == 1))

        # divergence: declared Proposal (5) with validation at Problem Evidenced (travels 2-3)
        declare_stage(d, 5, by="rep")
        r = read(d)
        ok.append(("slipping-deal divergence caught", r["divergence"] is not None and r["divergence"].startswith("SLIPPING")))

        # evidence invalidation (champion leaves)
        add_evidence(d, "success_criteria_signed", "criteria-doc", buyer_verifiable=True, by="rep")
        r = read(d)
        ok.append(("criteria signed -> state 2", r["validation_state"] == "Success Criteria Agreed"))
        invalidate(d, "criteria-doc", "champion departed; sign-off no longer stands")
        r = read(d)
        ok.append(("state falls back on invalidation", r["validation_state"] == "Problem Evidenced"))

        # ahead-of-stage positive divergence
        d2 = Path(td) / "deal2.jsonl"
        add_evidence(d2, "recorded_pain_call", "c1", buyer_verifiable=True, by="rep")
        add_evidence(d2, "buyer_value_inputs_confirmed", "model-v1", buyer_verifiable=True, by="rep")
        declare_stage(d2, 3, by="rep")
        r2 = read(d2)
        ok.append(("ahead-of-stage positive signal", r2["divergence"] is not None and r2["divergence"].startswith("AHEAD")))

        # close: won below Business Case Accepted -> shortfall flag
        rec = close(d2, "won")
        ok.append(("won below BCA sets validation_shortfall_flag", rec["validation_shortfall_flag"] is True))
        try:
            add_evidence(d2, "recorded_pain_call", "late", buyer_verifiable=True, by="rep")
            ok.append(("closed deal frozen", False))
        except RuleViolation:
            ok.append(("closed deal frozen", True))

        # lost close records readings too
        d3 = Path(td) / "deal3.jsonl"
        add_evidence(d3, "recorded_pain_call", "c1", buyer_verifiable=True, by="rep")
        rec3 = close(d3, "no_decision")
        ok.append(("no-decision close freezes readings for win-loss", rec3["final_validation_state"] == "Problem Evidenced"
                   and rec3["validation_shortfall_flag"] is False))

        # governance refusals
        try:
            add_assertion(d3, 2, by="", claim="x")
            ok.append(("anonymous assertion refused", False))
        except RuleViolation:
            ok.append(("anonymous assertion refused", True))
        try:
            add_evidence(Path(td) / "d4.jsonl", "vibes", "x", buyer_verifiable=True, by="rep")
            ok.append(("unknown evidence kind refused", False))
        except RuleViolation:
            ok.append(("unknown evidence kind refused", True))

    fails = [n for n, v in ok if not v]
    for n, v in ok:
        print(("PASS " if v else "FAIL ") + n)
    print(f"\n{len(ok) - len(fails)}/{len(ok)} checks passed")
    return 3 if fails else 0


def main() -> int:
    ap = argparse.ArgumentParser(description="ETM deal-axes engine (validation state + readiness ladder)")
    ap.add_argument("command", nargs="?", choices=["evidence", "invalidate", "assert", "declare-stage", "read", "close"])
    ap.add_argument("deal", nargs="?")
    ap.add_argument("--kind"); ap.add_argument("--ref"); ap.add_argument("--buyer-verifiable", action="store_true")
    ap.add_argument("--by", default=""); ap.add_argument("--claim", default=""); ap.add_argument("--reason", default="")
    ap.add_argument("--rung", type=int); ap.add_argument("--stage", type=int)
    ap.add_argument("--outcome"); ap.add_argument("--stale-days", type=int, default=DEFAULT_STALE_DAYS)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    try:
        if a.self_test:
            return self_test()
        if not a.command or not a.deal:
            ap.print_help(); return 1
        p = Path(a.deal)
        if a.command == "evidence":
            add_evidence(p, a.kind or "", a.ref or "", a.buyer_verifiable, a.by); print("ok")
        elif a.command == "invalidate":
            invalidate(p, a.ref or "", a.reason); print("ok")
        elif a.command == "assert":
            add_assertion(p, a.rung or 0, a.by, a.claim); print("recorded as assertion (moves nothing until corroborated)")
        elif a.command == "declare-stage":
            declare_stage(p, a.stage or 0, a.by); print("declared (claims are recorded; evidence is the truth-check)")
        elif a.command == "read":
            print(json.dumps(read(p, a.stale_days), indent=2))
        elif a.command == "close":
            print(json.dumps(close(p, a.outcome or ""), indent=2))
        return 0
    except RuleViolation as v:
        print(f"rule violation: {v}", file=sys.stderr); return 2
    except (OSError, json.JSONDecodeError) as e:
        print(f"error: {e}", file=sys.stderr); return 1


if __name__ == "__main__":
    sys.exit(main())
