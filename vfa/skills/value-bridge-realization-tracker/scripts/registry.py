#!/usr/bin/env python3
"""Value Bridge Realization Tracker — the Value Registry's single-writer engine.

Operates the Registry entry lifecycle (Committed -> Baseline Captured -> Active ->
Value Bridge Executed -> Closed) and enforces the Bridge discipline rules:
verbatim Expected Value Baseline, customer-system Realized Value Indicator,
Finance-validated Business Impact Statement before customer exposure, formal
Value Recognition, and FM-A/B/C/D classification on every Not-Achieved close.
Computes portfolio aggregates (achievement rate by outcome and segment, FM
shares, pre-calibration flags) and the quarterly write-back payload (R1) plus
the R2/R3/R4 signal blocks.

Storage: append-only JSONL event log; entry state is derived by replay. This
skill's script is the ONLY writer of the registry file (single-writer rule,
registry-value-map-rollup-mapping.md).

Usage:
    registry.py ingest <commitment_draft.json> [--registry <path>]
    registry.py baseline <entry_id> --text "<verbatim>" --speaker <name> [--verbatim]
    registry.py activate <entry_id>
    registry.py realize <entry_id> --value "<measured>" --source <customer_system>
    registry.py impact <entry_id> --statement "<BIS>" [--finance-validated]
    registry.py recognize <entry_id> --mechanism <formal_mechanism> --by <role>
    registry.py close <entry_id> --result achieved|not_achieved [--fm A|B|C|D]
    registry.py report [--segment <s>] [--writeback]
    registry.py show <entry_id>
    registry.py --self-test

Stdlib only. Exit codes: 0 ok; 1 input error; 2 discipline violation; 3 self-test failure.
"""
from __future__ import annotations

import argparse
import json
import sys
import uuid
from datetime import date
from pathlib import Path
from typing import Any

SPEC = "phase0/registry-value-map-rollup-mapping.md + Value-Registry-Explainer-Playbook"
STATES = ["Committed", "Baseline Captured", "Active", "Value Bridge Executed", "Closed"]
FM = {"A": "healthy", "B": "delivery failure", "C": "sales over-commitment", "D": "discovery failure"}
PRECAL_THRESHOLD = 10
DEFAULT_REGISTRY = Path("value-registry.jsonl")


class Violation(Exception):
    """A Bridge discipline rule was violated; the write is refused."""


def _events(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]


def _append(path: Path, ev: dict[str, Any]) -> None:
    ev["ts"] = date.today().isoformat()
    with path.open("a") as f:
        f.write(json.dumps(ev) + "\n")


def _entries(path: Path) -> dict[str, dict[str, Any]]:
    """Replay the event log into current entry states."""
    out: dict[str, dict[str, Any]] = {}
    for ev in _events(path):
        e = out.setdefault(ev["entry_id"], {"entry_id": ev["entry_id"], "state": None, "history": []})
        e["history"].append(ev)
        kind = ev["event"]
        if kind == "ingest":
            e.update(ev["entry"])
            e["state"] = "Committed"
        elif kind == "baseline":
            e["evb"] = {"text": ev["text"], "speaker": ev["speaker"], "verbatim": True, "date": ev["ts"]}
            e["state"] = "Baseline Captured"
        elif kind == "activate":
            e["state"] = "Active"
        elif kind == "realize":
            e["rvi"] = {"value": ev["value"], "source": ev["source"], "date": ev["ts"]}
        elif kind == "impact":
            e["bis"] = {"statement": ev["statement"], "finance_validated": ev["finance_validated"], "date": ev["ts"]}
        elif kind == "recognize":
            e["vrm"] = {"mechanism": ev["mechanism"], "by": ev["by"], "date": ev["ts"]}
            e["state"] = "Value Bridge Executed"
        elif kind == "close":
            e["result"] = ev["result"]
            e["fm"] = ev.get("fm")
            e["state"] = "Closed"
    return out


def _get(path: Path, entry_id: str) -> dict[str, Any]:
    e = _entries(path).get(entry_id)
    if not e:
        raise Violation(f"no such entry: {entry_id}")
    return e


def _require_state(e: dict[str, Any], allowed: list[str], op: str) -> None:
    if e["state"] not in allowed:
        raise Violation(f"{op} requires state in {allowed}; entry is {e['state']}")


# ------------------------------------------------------------------ commands --
def cmd_ingest(path: Path, draft_file: Path) -> str:
    d = json.loads(draft_file.read_text())
    if d.get("entry_type") != "commitment_draft":
        raise Violation("input is not a vbs commitment_draft")
    tier = d.get("deliverability_tier", "")
    if tier not in ("Fully Deliverable", "Partially Deliverable", "Conditionally Deliverable") or d.get("roadmap_dependent"):
        raise Violation(f"sales-eligibility rule: tier {tier!r} / roadmap_dependent={d.get('roadmap_dependent')} is not committable")
    for k in ("account", "outcome_id", "commitment_language", "evidence_plan"):
        if not d.get(k):
            raise Violation(f"commitment draft missing required field: {k}")
    if not d["evidence_plan"].get("source_system"):
        raise Violation("evidence_plan must name the customer-side source_system (Bridge rule: no vendor self-report)")
    entry_id = f"{d['account']}::{d['outcome_id']}::{uuid.uuid4().hex[:8]}"
    _append(path, {"event": "ingest", "entry_id": entry_id, "entry": {
        "account": d["account"], "outcome_id": d["outcome_id"], "segment": d.get("segment", "unsegmented"),
        "tier": tier, "commitment_language": d["commitment_language"], "evidence_plan": d["evidence_plan"],
    }})
    return entry_id


def cmd_baseline(path: Path, entry_id: str, text: str, speaker: str, verbatim: bool) -> None:
    e = _get(path, entry_id)
    _require_state(e, ["Committed"], "baseline")
    if not verbatim:
        raise Violation("EVB must be attested verbatim (--verbatim): the customer's words, not catalog language")
    if not text.strip() or not speaker.strip():
        raise Violation("EVB requires non-empty text and speaker")
    _append(path, {"event": "baseline", "entry_id": entry_id, "text": text, "speaker": speaker})


def cmd_realize(path: Path, entry_id: str, value: str, source: str) -> None:
    e = _get(path, entry_id)
    _require_state(e, ["Active", "Baseline Captured"], "realize")
    if not source.strip():
        raise Violation("RVI must cite a customer-system source (Bridge rule: vendor self-report rejected)")
    _append(path, {"event": "realize", "entry_id": entry_id, "value": value, "source": source})


def cmd_impact(path: Path, entry_id: str, statement: str, finance_validated: bool) -> None:
    e = _get(path, entry_id)
    if "rvi" not in e:
        raise Violation("BIS requires a recorded RVI first")
    if not finance_validated:
        raise Violation("BIS must carry --finance-validated before customer exposure (Bridge rule)")
    _append(path, {"event": "impact", "entry_id": entry_id, "statement": statement, "finance_validated": True})


def cmd_recognize(path: Path, entry_id: str, mechanism: str, by: str) -> None:
    e = _get(path, entry_id)
    if "bis" not in e:
        raise Violation("recognition requires a Finance-validated BIS on record")
    if mechanism.lower() in ("verbal", "informal", "email-thanks", ""):
        raise Violation("informal acknowledgment is disqualified as evidence; use a formal Value Recognition Mechanism")
    _append(path, {"event": "recognize", "entry_id": entry_id, "mechanism": mechanism, "by": by})


def cmd_close(path: Path, entry_id: str, result: str, fm: str | None) -> None:
    e = _get(path, entry_id)
    if result == "achieved" and e["state"] != "Value Bridge Executed":
        raise Violation("achieved close requires the full Bridge executed (EVB -> RVI -> BIS -> VRM)")
    if result == "not_achieved" and fm not in FM:
        raise Violation("not_achieved close requires an FM classification (A/B/C/D)")
    _append(path, {"event": "close", "entry_id": entry_id, "result": result, "fm": fm})


def cmd_report(path: Path, segment: str | None, writeback: bool) -> dict[str, Any]:
    ents = list(_entries(path).values())
    if segment:
        ents = [e for e in ents if e.get("segment") == segment]
    closed = [e for e in ents if e["state"] == "Closed"]
    achieved = [e for e in closed if e.get("result") == "achieved"]
    fms = {k: sum(1 for e in closed if e.get("fm") == k) for k in FM}
    by_seg: dict[str, list[dict[str, Any]]] = {}
    for e in ents:
        by_seg.setdefault(e.get("segment", "unsegmented"), []).append(e)
    precal = {s: len(v) < PRECAL_THRESHOLD for s, v in by_seg.items()}
    rep: dict[str, Any] = {
        "entries_total": len(ents),
        "closed": len(closed),
        "achievement_rate": round(len(achieved) / len(closed), 3) if closed else None,
        "fm_counts": fms,
        "fm_cd_share": round((fms["C"] + fms["D"]) / len(closed), 3) if closed else None,
        "pre_calibration_segments": [s for s, flag in precal.items() if flag],
        "note": "[Pre-calibration] applies to any segment under 10 entries (VFAS gap 4.2)",
    }
    if writeback:
        rep["writeback_payload"] = {
            "R1_catalog": {
                "per_outcome": {
                    oc: {
                        "achievement_rate": round(
                            sum(1 for e in closed if e["outcome_id"] == oc and e.get("result") == "achieved")
                            / max(1, sum(1 for e in closed if e["outcome_id"] == oc)), 3),
                        "n": sum(1 for e in closed if e["outcome_id"] == oc),
                    }
                    for oc in sorted({e["outcome_id"] for e in closed})
                },
                "deliver_to": "rev-ops.outcome-statement-builder (Portfolio Intelligence Block); this engine never writes the catalog",
            },
            "R2_icvp": {"signal": "achievement rate by ICVP score band", "action": "propose weights.json re-fit via /vfa:customize --propose-weights; human-approved"},
            "R3_icp": {"signal": "realized-value distribution by segment", "action": "feed icp-drift-monitor"},
            "R4_pmf": {"signal": "outcome achievement rate trend as leading NRR indicator", "action": "PMF decay tripwire on sustained decline"},
        }
    return rep


# ----------------------------------------------------------------- self-test --
def self_test() -> int:
    import tempfile
    checks: list[tuple[str, bool]] = []
    with tempfile.TemporaryDirectory() as td:
        reg = Path(td) / "reg.jsonl"
        draft = Path(td) / "draft.json"
        good = {
            "entry_type": "commitment_draft", "account": "Northwind", "outcome_id": "OC-W001",
            "segment": "mid-market", "deliverability_tier": "Fully Deliverable", "roadmap_dependent": False,
            "commitment_language": "De-anonymize 200+ in-market ICP accounts/month in Q1",
            "evidence_plan": {"metric": "accounts/month", "source_system": "HubSpot", "cadence": "monthly", "acknowledger_role": "Head of RevOps"},
        }
        draft.write_text(json.dumps(good))
        eid = cmd_ingest(reg, draft)
        checks.append(("round-trip: vbs draft ingests to Committed", _get(reg, eid)["state"] == "Committed"))

        bad = dict(good, deliverability_tier="Aspirational")
        draft.write_text(json.dumps(bad))
        try:
            cmd_ingest(reg, draft)
            checks.append(("aspirational draft refused", False))
        except Violation:
            checks.append(("aspirational draft refused", True))

        try:
            cmd_baseline(reg, eid, "catalog-style baseline", "CSM", verbatim=False)
            checks.append(("non-verbatim EVB refused", False))
        except Violation:
            checks.append(("non-verbatim EVB refused", True))

        cmd_baseline(reg, eid, "We need 200 in-market accounts a month and a third less cold-outreach time", "Dana (Head of RevOps)", verbatim=True)
        checks.append(("verbatim EVB -> Baseline Captured", _get(reg, eid)["state"] == "Baseline Captured"))

        cmd_realize(reg, eid, "260 accounts/month by month 3", "Northwind HubSpot")
        try:
            cmd_impact(reg, eid, "~$310K annualized productivity", finance_validated=False)
            checks.append(("un-validated BIS refused", False))
        except Violation:
            checks.append(("un-validated BIS refused", True))
        cmd_impact(reg, eid, "~$310K annualized productivity", finance_validated=True)

        try:
            cmd_recognize(reg, eid, "informal", "champion")
            checks.append(("informal recognition refused", False))
        except Violation:
            checks.append(("informal recognition refused", True))
        cmd_recognize(reg, eid, "co-authored Value Realization Summary", "Head of RevOps")
        checks.append(("full Bridge -> Value Bridge Executed", _get(reg, eid)["state"] == "Value Bridge Executed"))

        cmd_close(reg, eid, "achieved", None)
        checks.append(("achieved close after full Bridge", _get(reg, eid)["result"] == "achieved"))

        # second entry: not-achieved path requires FM
        draft.write_text(json.dumps(dict(good, outcome_id="OC-W004", deliverability_tier="Conditionally Deliverable")))
        e2 = cmd_ingest(reg, draft)
        cmd_baseline(reg, e2, "We want autonomous outbound live by Q2", "Dana", verbatim=True)
        try:
            cmd_close(reg, e2, "not_achieved", None)
            checks.append(("not-achieved without FM refused", False))
        except Violation:
            checks.append(("not-achieved without FM refused", True))
        cmd_close(reg, e2, "not_achieved", "C")

        rep = cmd_report(reg, None, writeback=True)
        checks.append(("achievement rate computed", rep["achievement_rate"] == 0.5))
        checks.append(("FM-C counted", rep["fm_counts"]["C"] == 1))
        checks.append(("pre-calibration flagged under threshold", "mid-market" in rep["pre_calibration_segments"]))
        checks.append(("writeback payload has all four edges", all(k in rep["writeback_payload"] for k in ("R1_catalog", "R2_icvp", "R3_icp", "R4_pmf"))))
        checks.append(("R1 per-outcome rates present", rep["writeback_payload"]["R1_catalog"]["per_outcome"]["OC-W001"]["achievement_rate"] == 1.0))

    failures = [n for n, ok in checks if not ok]
    for n, ok in checks:
        print(("PASS " if ok else "FAIL ") + n)
    print(f"\n{len(checks) - len(failures)}/{len(checks)} checks passed")
    return 3 if failures else 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Value Registry engine (single writer)")
    ap.add_argument("command", nargs="?", choices=["ingest", "baseline", "activate", "realize", "impact", "recognize", "close", "report", "show"])
    ap.add_argument("target", nargs="?")
    ap.add_argument("--registry", default=str(DEFAULT_REGISTRY))
    ap.add_argument("--text"); ap.add_argument("--speaker"); ap.add_argument("--verbatim", action="store_true")
    ap.add_argument("--value"); ap.add_argument("--source"); ap.add_argument("--statement")
    ap.add_argument("--finance-validated", action="store_true"); ap.add_argument("--mechanism"); ap.add_argument("--by")
    ap.add_argument("--result", choices=["achieved", "not_achieved"]); ap.add_argument("--fm", choices=list(FM))
    ap.add_argument("--segment"); ap.add_argument("--writeback", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    path = Path(a.registry)
    try:
        if a.self_test:
            return self_test()
        if a.command == "ingest":
            print(json.dumps({"entry_id": cmd_ingest(path, Path(a.target))}))
        elif a.command == "baseline":
            cmd_baseline(path, a.target, a.text or "", a.speaker or "", a.verbatim); print("ok")
        elif a.command == "activate":
            _require_state(_get(path, a.target), ["Baseline Captured"], "activate")
            _append(path, {"event": "activate", "entry_id": a.target}); print("ok")
        elif a.command == "realize":
            cmd_realize(path, a.target, a.value or "", a.source or ""); print("ok")
        elif a.command == "impact":
            cmd_impact(path, a.target, a.statement or "", a.finance_validated); print("ok")
        elif a.command == "recognize":
            cmd_recognize(path, a.target, a.mechanism or "", a.by or ""); print("ok")
        elif a.command == "close":
            cmd_close(path, a.target, a.result, a.fm); print("ok")
        elif a.command == "report":
            print(json.dumps(cmd_report(path, a.segment, a.writeback), indent=2))
        elif a.command == "show":
            print(json.dumps(_get(path, a.target), indent=2))
        else:
            ap.print_help(); return 1
        return 0
    except Violation as v:
        print(f"discipline violation: {v}", file=sys.stderr); return 2
    except (OSError, json.JSONDecodeError, KeyError) as e:
        print(f"error: {e}", file=sys.stderr); return 1


if __name__ == "__main__":
    sys.exit(main())
