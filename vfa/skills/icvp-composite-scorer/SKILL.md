---
name: icvp-composite-scorer
description: >
  Score a prospect (or batch) on the ICVP Composite Score: the 100-point,
  8-component value-fit gate that upgrades ICP "could this company buy?" to
  "how much would solving their problems be worth to them, and can we prove
  it?". Classifies account readiness (ICVP classification: oblivious / aware_inactive / constrained_believer; distinct from the ETM deal-level buying-readiness ladder),
  computes confidence-weighted value arbitrage and net value ratio, assigns a
  Prime/Strong/Conditional/Watch/No Fit tier, and emits a full audit trail with
  governance flags (override tagging, cold-start, quiet-account nomination,
  Shadow ICP). Implements ICVP Composite Score Spec v1.0; scoring math runs in
  the bundled script, never re-derived in-context.
argument-hint: "[prospect.json | --batch prospects.jsonl | --self-test]"
version: "0.1.0"
deployment_target: plugin
---

# /vfa:icvp-composite-scorer

The value-fit gate. Answers "should this prospect want to buy, at a provable ratio?" and refuses to confuse that with "can we reach them?"

[PROPOSED]

---

## Use when

- Qualifying a prospect list beyond the firmographic ICP gate (post `icp-scorecard-builder`)
- Prioritizing which prospects earn deep research and role-targeted playbooks
- A rep nominates a quiet, low-signal account with a written value hypothesis
- Re-scoring after new signals, deepened value-alignment research, or a catalog update
- Running the quarterly batch for the Loop 3 review (`--batch`)
- Validating the score against historical win/loss data (`--batch` on closed outcomes)

## Do NOT use for

- Firmographic-only lead scoring or MQL thresholds (use `/vfa:icp-scorecard-builder`)
- Deal-level keepability review of an active opportunity (that is `vbs.good-sale-gate`, Phase 2)
- Editing scoring weights in conversation (weights change only via a proposed new `config/weights.json` version, human-approved; see Governance)

## Typical activation

"Score these 40 accounts through the ICVP gate" / "is this prospect actually worth pursuing?" / "run the value-fit filter on the ICP-qualified list" / "a rep wants to nominate a quiet account"

---

## How it works

1. **Read config.** Company profile + vfa config (per plugin CLAUDE.md). STOP and route to `/vfa:cold-start-interview` if placeholders remain. The scorer needs: the Outcome Catalog location, the vendor annual cost model, and signal half-life defaults.
2. **Assemble the prospect record** as JSON matching the input contract below. Pain-outcome mappings MUST cite catalog entry IDs and their canonical 7-tier deliverability; every pain carries a dollar annual cost and a confidence tier (Quantified/Benchmarked/Estimated/Directional). If the user cannot supply a dollar figure, help triangulate one and tag it Directional; never omit it (non-negotiable core, VFAS §4.8).
3. **Run the engine:** `python3 scripts/icvp_score.py <prospect.json> --pretty`. Never re-derive the math in-context; the script is the spec's executable form.
4. **Present the verdict:** tier, routing, arbitrage story (risk-adjusted cost of inaction vs. vendor cost), and the top audit lines. Lead with the routing decision.
5. **Honor the flags:** `roadmap_demand_register` entries go to the register, not the trash; `shadow_icp_flag` is surfaced for the drift review; `cold_start_provisional` is stated plainly; an `override` is recorded with owner + hypothesis and counted against the override budget.

## Input contract (per prospect)

```json
{
  "readiness": {"type": "constrained_believer", "new_leadership_signals": false},
  "firmographic": {"hard_fail": false, "soft_fail_overridden": false, "modifier_below_threshold": false},
  "signals": [{"name": "...", "weight": 9, "age_over_half_life": 0.5, "mapped_deliverability": "Fully Deliverable"}],
  "pain_outcome_mappings": [{"outcome_id": "OC-...", "mapping_confidence": 8, "deliverability": "Fully Deliverable"}],
  "pains": [{"annual_cost": 2800000, "confidence": "Quantified"}],
  "economics": {"vendor_annual_cost": 60000, "cost_to_serve": "Standard"},
  "industry_tier": "primary",
  "contact_quality": "dm_verified",
  "deep_intelligence_score": 10,
  "deal_size_tier": "mid_market",
  "playbook_readiness": 6,
  "buying_signal": "active_engagement",
  "nominated": false,
  "override": null
}
```

## Naming note (ETM alignment ruling)

"Readiness" here is always the ICVP account readiness classification: is the account ready to be sold to at all. The ETM's deal-level buying-readiness ladder (seven rungs, first-missing-rung, `/vbs:deal-axes-reader`) is a different instrument at a different grain; the conformance audit (etm-conformance-audit-and-crosswalk.md §3) governs the vocabulary.

## Governance (enforced by the engine, restated for the operator)

Readiness is a hard router: no score advances a Type 1/2 prospect. Low signal density defers research and never disqualifies alone; nominated accounts skip the S2 gate but must clear S3. Overrides require owner + written value hypothesis and are tagged for the Loop 3 cohort review. Weight changes are proposed config versions (R2 feedback), human-approved, never auto-applied, never code edits.

## Security & Permissions

Runs locally on user-supplied JSON; stdlib-only Python; no network access; no subprocess beyond the bundled script; writes nothing outside the conversation workspace. External-signal ingestion (CRM/enrichment feeds) is out of scope for this version; when added, every ingesting step carries an output schema with injection-prevention constraints.

## Trust & Verification

Spec: `icvp-composite-score-spec-v1.0.md` (value-based-acquisition/docs/specs/). Structural validation: `scripts/icvp_score.py --self-test` (15 checks: gates, caps, flags, tier discrimination). Discriminative validation against real win/loss data is REQUIRED before [VALIDATED]; run `--batch` on closed outcomes and compare tier distributions.
