#!/usr/bin/env python3
"""ICVP Composite Scorer — executable implementation of ICVP Composite Score Spec v1.0.

Implements the 100-point, 8-component additive model with readiness routing,
value arbitrage, governance flags, and a full audit trail. Resolves verification
findings F1 (one Signal Density formula), F2 (one score name), and W2
(contact-quality cap = 13).

Usage:
    python3 icvp_score.py <prospect.json> [--config <weights.json>] [--pretty]
    python3 icvp_score.py --batch <prospects.jsonl> [--config <weights.json>]
    python3 icvp_score.py --self-test

Stdlib only. Exit codes: 0 scored; 1 input/config error; 2 self-test failure.
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

SPEC_VERSION = "1.0"
DEFAULT_CONFIG = Path(__file__).resolve().parent.parent / "config" / "weights.json"


class SpecError(ValueError):
    """Raised when input or configuration violates the spec contract."""


@dataclass
class Result:
    """Scoring outcome with full audit trail."""

    composite_score: float = 0.0
    tier: str = "No Fit"
    readiness: str = "unknown"
    advance: bool = False
    routing: str = ""
    arbitrage_ratio: float | None = None
    net_value_ratio: float | None = None
    arbitrage_class: str = "Insufficient"
    flags: dict[str, Any] = field(default_factory=dict)
    components: dict[str, float] = field(default_factory=dict)
    audit: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "spec_version": SPEC_VERSION,
            "composite_score": round(self.composite_score, 2),
            "tier": self.tier,
            "readiness": self.readiness,
            "advance": self.advance,
            "routing": self.routing,
            "arbitrage_ratio": self.arbitrage_ratio,
            "net_value_ratio": self.net_value_ratio,
            "arbitrage_class": self.arbitrage_class,
            "flags": self.flags,
            "components": {k: round(v, 2) for k, v in self.components.items()},
            "audit": self.audit,
        }


def load_config(path: Path) -> dict[str, Any]:
    cfg = json.loads(path.read_text())
    if str(cfg.get("spec_version", "")).split(".")[0] != SPEC_VERSION.split(".")[0]:
        raise SpecError(
            f"config spec_version {cfg.get('spec_version')!r} incompatible with engine spec {SPEC_VERSION}"
        )
    return cfg


def classify_readiness(p: dict[str, Any], r: Result) -> str:
    """Spec §3: hard router, evaluated before any scoring."""
    readiness = p.get("readiness", {})
    rtype = readiness.get("type", "unknown")
    if rtype == "aware_inactive" and readiness.get("new_leadership_signals"):
        r.audit.append("readiness: aware_inactive + new-leadership signals -> reclassified constrained_believer")
        rtype = "constrained_believer"
    r.audit.append(f"readiness classification: {rtype}")
    return rtype


def score_firmographic(p: dict[str, Any], cfg: dict[str, Any], r: Result) -> float:
    fp = cfg["firmographic_points"]
    f = p.get("firmographic", {})
    if f.get("hard_fail"):
        r.flags["s1_hard_fail"] = f.get("hard_fail_reason", "unspecified criterion")
        r.audit.append(f"S1 HARD_FAIL: {r.flags['s1_hard_fail']} -> scoring ends, composite 0")
        return 0.0
    if f.get("soft_fail_overridden"):
        pts = fp["soft_fail_overridden"]
    elif f.get("modifier_below_threshold"):
        pts = fp["all_pass_modifier_below_threshold"]
    else:
        pts = fp["all_pass"]
    r.audit.append(f"S1 firmographic: {pts}/{cfg['components']['firmographic_gate']}")
    return float(pts)


def signal_density(p: dict[str, Any], cfg: dict[str, Any], r: Result) -> float:
    """Spec §2 canonical Signal Density formula (F1 resolution)."""
    mults = cfg["signal_deliverability_multipliers"]
    rec = cfg["recency"]
    total = 0.0
    for s in p.get("signals", []):
        w = float(s["weight"])
        age = float(s.get("age_over_half_life", 0.0))  # age expressed as multiples of half-life
        recency = rec["fresh"] if age <= 0 else rec["at_half_life"] if age <= 1 else (
            rec["floor_beyond_2x_half_life"] if age > 2 else rec["at_half_life"] * (2 - age)
        )
        recency = max(recency, rec["floor_beyond_2x_half_life"])
        dm = mults.get(s.get("mapped_deliverability", "Provisional"), 0.0)
        contrib = w * recency * dm
        total += contrib
        r.audit.append(
            f"S2 signal '{s.get('name', '?')}': w={w} x recency={recency:.2f} x deliverability={dm} = {contrib:.2f}"
        )
    r.audit.append(f"S2 signal density total: {total:.2f} (gate {cfg['s2_gate_min_density']})")
    return total


def score_triggers(density: float, cfg: dict[str, Any]) -> float:
    cap = cfg["components"]["organizational_triggers"]
    return min(cap, density * cap / (cfg["s2_gate_min_density"] * 2))  # density 2x gate saturates the component


def score_value_alignment(p: dict[str, Any], cfg: dict[str, Any], r: Result) -> float:
    cap = cfg["components"]["value_alignment"]
    mults = cfg["signal_deliverability_multipliers"]
    total = 0.0
    for m in p.get("pain_outcome_mappings", []):
        contrib = float(m["mapping_confidence"]) * mults.get(m.get("deliverability", "Provisional"), 0.0)
        total += contrib
        r.audit.append(
            f"S3 mapping '{m.get('outcome_id', '?')}': confidence={m['mapping_confidence']} x "
            f"{m.get('deliverability')} -> {contrib:.2f}"
        )
        if m.get("deliverability") in ("Aspirational", "Requires Investigation"):
            r.flags.setdefault("roadmap_demand_register", []).append(m.get("outcome_id", "?"))
    return min(cap, total)


def arbitrage(p: dict[str, Any], cfg: dict[str, Any], r: Result) -> tuple[float | None, float | None, str]:
    econ = p.get("economics", {})
    vendor = float(econ.get("vendor_annual_cost", 0) or 0)
    pains = p.get("pains", [])
    if not pains or vendor <= 0:
        r.audit.append("S3 arbitrage: insufficient economics (no pains or no vendor cost)")
        return None, None, "Insufficient"
    cm = cfg["confidence_multipliers"]
    coi = sum(float(x["annual_cost"]) * cm.get(x.get("confidence", "Directional"), 0.25) for x in pains)
    ratio = coi / vendor
    mod = cfg["cost_to_serve_modifiers"].get(econ.get("cost_to_serve", "Standard"), 1.0)
    net = ratio * mod
    bands = cfg["arbitrage_bands"]
    cls = (
        "Strong" if ratio >= bands["strong_min"]
        else "Standard" if ratio >= bands["standard_min"]
        else "Marginal" if ratio >= bands["marginal_min"]
        else "Insufficient"
    )
    r.audit.append(
        f"S3 arbitrage: risk-adjusted COI ${coi:,.0f} / vendor ${vendor:,.0f} = {ratio:.2f}x; "
        f"cost-to-serve {econ.get('cost_to_serve', 'Standard')} ({mod}) -> net {net:.2f}x [{cls}]"
    )
    non_directional = [x for x in pains if x.get("confidence", "Directional") != "Directional"]
    if not non_directional:
        r.flags["cold_start_provisional"] = True
        r.audit.append("flag: cold_start_provisional (advancement rests on Directional-confidence pains only)")
    return ratio, net, cls


def score_industry(p: dict[str, Any], cfg: dict[str, Any], va: float, net: float | None, r: Result) -> float:
    tier = p.get("industry_tier", "other")
    pts = float(cfg["industry_points"].get(tier, cfg["industry_points"]["other"]))
    ov = cfg["industry_override"]
    if tier == "deprioritized" and va >= ov["min_value_alignment"] and (net or 0) >= ov["min_net_value_ratio"]:
        pts = float(ov["override_points"])
        r.flags["shadow_icp_flag"] = True
        r.audit.append(
            f"industry override: deprioritized -> {pts} pts (VA {va:.1f} >= {ov['min_value_alignment']}, "
            f"net {net:.2f}x >= {ov['min_net_value_ratio']}x); shadow_icp_flag emitted"
        )
    else:
        r.audit.append(f"industry fit: tier {tier} -> {pts}")
    return pts


def score_deep_intelligence(p: dict[str, Any], cfg: dict[str, Any], r: Result) -> float:
    cap = cfg["components"]["deep_intelligence"]
    cq = cfg["contact_quality_points"].get(p.get("contact_quality", "none"), 0)
    research = float(p.get("deep_intelligence_score", 0))  # 0..cap from research completeness
    pts = min(cap, max(float(cq), research))  # W2: capped at 13, DM verified alone reaches the cap
    r.audit.append(f"S4 deep intelligence: contact_quality={cq}, research={research} -> {pts}/{cap} (W2 cap enforced)")
    return pts


def score_simple(p: dict[str, Any], cfg: dict[str, Any], key: str, table: str, r: Result, label: str) -> float:
    pts = float(cfg[table].get(p.get(key, "none"), 0))
    r.audit.append(f"{label}: {p.get(key, 'none')} -> {pts}")
    return pts


def tier_for(score: float, cfg: dict[str, Any]) -> str:
    for t in cfg["tiers"]:
        if score >= t["min"]:
            return t["name"]
    return "No Fit"


def score_prospect(p: dict[str, Any], cfg: dict[str, Any]) -> Result:
    r = Result()
    r.readiness = classify_readiness(p, r)

    if r.readiness == "oblivious":
        r.routing = "archive"
        r.audit.append("routing: Type 1 oblivious -> archive; no composite score can advance this prospect")
        return r
    if r.readiness == "aware_inactive":
        r.routing = "nurture"
        r.audit.append("routing: Type 2 aware_inactive -> nurture; watch for trigger events")
        return r

    c = r.components
    c["firmographic_gate"] = score_firmographic(p, cfg, r)
    if "s1_hard_fail" in r.flags:
        r.routing = "disqualified"
        return r

    density = signal_density(p, cfg, r)
    nominated = bool(p.get("nominated"))
    if nominated:
        r.flags["quiet_account_nomination"] = True
        r.audit.append("S2 gate skipped: quiet-account nomination lane (must still clear S3)")
    elif density < cfg["s2_gate_min_density"]:
        r.routing = "defer_research"
        r.audit.append("S2 gate: below density threshold -> research deferred (never a standalone disqualifier)")
    c["organizational_triggers"] = score_triggers(density, cfg)

    c["value_alignment"] = score_value_alignment(p, cfg, r)
    r.arbitrage_ratio, r.net_value_ratio, r.arbitrage_class = arbitrage(p, cfg, r)
    c["industry_fit"] = score_industry(p, cfg, c["value_alignment"], r.net_value_ratio, r)
    c["deep_intelligence"] = score_deep_intelligence(p, cfg, r)
    c["deal_size"] = score_simple(p, cfg, "deal_size_tier", "deal_size_points", r, "deal size")
    c["playbook_readiness"] = min(cfg["components"]["playbook_readiness"], float(p.get("playbook_readiness", 0)))
    r.audit.append(f"S5 playbook readiness: {c['playbook_readiness']}")
    c["buying_signals"] = score_simple(p, cfg, "buying_signal", "buying_signal_points", r, "S6 buying signals")

    r.composite_score = sum(c.values())
    r.tier = tier_for(r.composite_score, cfg)
    r.advance = (
        r.readiness in ("constrained_believer", "unknown")
        and r.tier in ("Prime", "Strong")
        and r.arbitrage_class in ("Strong", "Standard")
        and r.routing != "defer_research"
    )
    if not r.routing:
        r.routing = "advance" if r.advance else "hold"

    ov = p.get("override")
    if ov and not r.advance:
        if not (ov.get("owner") and ov.get("value_hypothesis")):
            raise SpecError("override requires owner and written value_hypothesis (VFAS gap 4.6)")
        r.flags["override"] = {"owner": ov["owner"], "value_hypothesis": ov["value_hypothesis"], "loop3_review": True}
        r.routing = "advance_by_override"
        r.audit.append(f"override recorded by {ov['owner']} -> tagged for Loop 3 override-cohort review")

    r.audit.append(f"composite: {r.composite_score:.2f}/100 -> {r.tier}; routing: {r.routing}")
    return r


# ---------------------------------------------------------------- self-test --
def _fixture(**over: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "readiness": {"type": "constrained_believer"},
        "firmographic": {},
        "signals": [
            {"name": "cs-leader-hire", "weight": 9, "age_over_half_life": 0, "mapped_deliverability": "Fully Deliverable"},
            {"name": "g2-pain-review", "weight": 8, "age_over_half_life": 0.5, "mapped_deliverability": "Fully Deliverable"},
            {"name": "funding", "weight": 5, "age_over_half_life": 0, "mapped_deliverability": "Partially Deliverable"},
            {"name": "tech-stack", "weight": 6, "age_over_half_life": 0, "mapped_deliverability": "Fully Deliverable"},
        ],
        "pain_outcome_mappings": [
            {"outcome_id": "OC-1", "mapping_confidence": 9, "deliverability": "Fully Deliverable"},
            {"outcome_id": "OC-2", "mapping_confidence": 8, "deliverability": "Fully Deliverable"},
            {"outcome_id": "OC-3", "mapping_confidence": 7, "deliverability": "Partially Deliverable"},
        ],
        "pains": [
            {"annual_cost": 2_800_000, "confidence": "Quantified"},
            {"annual_cost": 900_000, "confidence": "Benchmarked"},
        ],
        "economics": {"vendor_annual_cost": 60_000, "cost_to_serve": "Standard"},
        "industry_tier": "primary",
        "contact_quality": "dm_verified",
        "deep_intelligence_score": 10,
        "deal_size_tier": "mid_market",
        "playbook_readiness": 6,
        "buying_signal": "active_engagement",
    }
    base.update(over)
    return base


def self_test(cfg: dict[str, Any]) -> int:
    checks: list[tuple[str, bool]] = []
    strong = score_prospect(_fixture(), cfg)
    checks.append(("strong prospect reaches Prime/Strong", strong.tier in ("Prime", "Strong")))
    checks.append(("strong prospect advances", strong.advance))
    checks.append(("arbitrage Strong at ~58x", strong.arbitrage_class == "Strong"))
    checks.append(("W2 cap: deep intelligence <= 13", strong.components["deep_intelligence"] <= 13))

    obl = score_prospect(_fixture(readiness={"type": "oblivious"}), cfg)
    checks.append(("oblivious archives with zero score", obl.routing == "archive" and obl.composite_score == 0))

    hf = score_prospect(_fixture(firmographic={"hard_fail": True, "hard_fail_reason": "B2C"}), cfg)
    checks.append(("S1 HARD_FAIL disqualifies", hf.routing == "disqualified" and hf.composite_score == 0))

    quiet = score_prospect(_fixture(signals=[], nominated=True), cfg)
    checks.append(("nominated quiet account skips S2 gate", quiet.flags.get("quiet_account_nomination") is True))
    checks.append(("quiet account still scored on S3", quiet.components["value_alignment"] > 0))

    lowsig = score_prospect(_fixture(signals=[]), cfg)
    checks.append(("low signal defers, never disqualifies", lowsig.routing == "defer_research"))

    cold = score_prospect(
        _fixture(pains=[{"annual_cost": 500_000, "confidence": "Directional"}]), cfg
    )
    checks.append(("Directional-only pains flag cold_start_provisional", cold.flags.get("cold_start_provisional") is True))

    shadow = score_prospect(
        _fixture(
            industry_tier="deprioritized",
            pain_outcome_mappings=[
                {"outcome_id": f"OC-{i}", "mapping_confidence": 9, "deliverability": "Fully Deliverable"}
                for i in range(4)
            ],
        ),
        cfg,
    )
    checks.append(("deprioritized-industry override emits shadow_icp_flag", shadow.flags.get("shadow_icp_flag") is True))

    weak = score_prospect(
        _fixture(
            pains=[{"annual_cost": 80_000, "confidence": "Directional"}],
            pain_outcome_mappings=[{"outcome_id": "OC-1", "mapping_confidence": 3, "deliverability": "Aspirational"}],
            industry_tier="other",
            contact_quality="none",
            deep_intelligence_score=2,
            deal_size_tier="standard",
            playbook_readiness=0,
            buying_signal="none",
        ),
        cfg,
    )
    checks.append(("weak prospect does not advance", not weak.advance))
    checks.append(("aspirational pain routed to Roadmap Demand Register", "roadmap_demand_register" in weak.flags))
    gap = strong.composite_score - weak.composite_score
    checks.append((f"discriminative gap strong-weak >= 25 pts (got {gap:.1f})", gap >= 25))

    try:
        score_prospect(_fixture(buying_signal="none", playbook_readiness=0, pains=[], override={"owner": "x"}), cfg)
        checks.append(("override without hypothesis rejected", False))
    except SpecError:
        checks.append(("override without hypothesis rejected", True))

    failures = [name for name, ok in checks if not ok]
    for name, ok in checks:
        print(("PASS " if ok else "FAIL ") + name)
    print(f"\n{len(checks) - len(failures)}/{len(checks)} checks passed")
    return 2 if failures else 0


def main() -> int:
    ap = argparse.ArgumentParser(description="ICVP Composite Scorer (spec v1.0)")
    ap.add_argument("prospect", nargs="?", help="prospect JSON file")
    ap.add_argument("--batch", help="JSONL file of prospects (one per line)")
    ap.add_argument("--config", default=str(DEFAULT_CONFIG))
    ap.add_argument("--pretty", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    try:
        cfg = load_config(Path(args.config))
        if args.self_test:
            return self_test(cfg)
        if args.batch:
            for line in Path(args.batch).read_text().splitlines():
                if line.strip():
                    print(json.dumps(score_prospect(json.loads(line), cfg).to_dict()))
            return 0
        if not args.prospect:
            ap.print_help()
            return 1
        out = score_prospect(json.loads(Path(args.prospect).read_text()), cfg).to_dict()
        print(json.dumps(out, indent=2 if args.pretty else None))
        return 0
    except (SpecError, OSError, json.JSONDecodeError, KeyError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
