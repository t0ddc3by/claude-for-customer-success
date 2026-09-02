---
name: value-commitment-builder
description: >
  At close (or just before), draft the Value Registry Commitment entries for a
  won deal: one entry per committed outcome, each linked to its catalog OC-ID
  at a sales-eligible tier, with the agreed evidence plan and the Expected
  Value Baseline capture scheduled or recorded in the customer's verbatim
  words. The artifact that crosses the sale boundary: handoff validates it at
  Gate 0, onboarding derives success criteria from it, the Value Registry
  tracks it, and renewals negotiates from it. Drafts only; commitment into the
  Registry is executed by the vfa realization tracker (the designated single
  writer), never by this skill.
argument-hint: "[--deal <name> | --capture-evb <entry-id>]"
version: "0.1.0"
deployment_target: plugin
---

# /vbs:value-commitment-builder

The sale is not done when the signature lands; it is done when the promises are on the record in a form the next three years can be measured against.

[PROPOSED]

ETM coordinates: pipeline 7 Closed (won) / the seam (HC-3). The drafts plus the etm_final_readings block constitute the AX-1.5.1 payload delta.

---

## Use when

- A deal reaches verbal or signed close and the commitment record must be drafted while context is fresh
- The onboarding intake call is scheduled and the Expected Value Baseline capture needs preparing (`--capture-evb`)
- A gate review flagged dimension 5 (value-evidence plan) and the fix is drafting the actual entries

## Do NOT use for

- Qualifying which outcomes may be committed (already done in `/vbs:outcome-qualification`; this skill consumes the qualified promise set and refuses anything outside it)
- Writing to the Value Registry or Value Map (single-writer rule: the `vfa` realization tracker commits entries; this skill hands off drafts)
- Post-baseline tracking (that is the tracker's lifecycle)

## Typical activation

"Summit signed, draft the commitment entries" / "prep the EVB capture for the kickoff call" / "turn the promise set into registry drafts"

---

## The entry (draft schema)

One per committed outcome, JSON, to the deal workspace:

```json
{
  "entry_type": "commitment_draft",
  "account": "...",
  "outcome_id": "OC-...",
  "deliverability_tier": "Partially Deliverable",
  "commitment_language": "the exact sentence sold, subset/conditions included",
  "roadmap_dependent": false,
  "evidence_plan": {"metric": "...", "source_system": "customer's system name", "cadence": "...", "acknowledger_role": "..."},
  "evb": {"status": "scheduled|captured", "verbatim_text": null, "speaker": null, "capture_date": null},
  "provenance": {"why_change_ref": true, "gate_verdict": "Fixable", "drafted_by": "...", "date": "..."},
  "etm_final_readings": {"validation_state": "Value Quantified", "readiness_rungs": 5, "governing_gap": "Paper Process Known", "validation_shortfall_flag": true}
}
```

## Workflow

1. Read config, the qualified promise set, motivation record, and gate result. A promise not in the qualified set is refused with the reason; a Fragile gate verdict is surfaced before drafting proceeds.
2. Draft one entry per committed outcome. Commitment language is copied from the promise set's drafted sentences (subset boundaries and conditions intact), never re-improvised. The evidence plan names the customer-side source system, per the Bridge discipline the tracker will enforce.
3. `--capture-evb`: prepare the intake questions that elicit the baseline in the customer's own words ("what does success look like by when, in your terms?"); on capture, record the text verbatim with speaker and date, and set `verbatim: true` only if it is actually their words. Seller-authored catalog language in the EVB field is a defect the tracker will reject; this skill says so at capture time.
4. Attach the ETM payload delta (AX-1.5.1): run `/vbs:deal-axes-reader close won` and embed the frozen final readings (validation state, readiness rungs, governing gap) and the `validation_shortfall_flag` in every entry. A win below Business Case Accepted is not blocked, but it crosses the seam flagged, so onboarding starts with eyes open instead of discovering the unfinished value case months later.
5. Hand off: write the drafts to the deal workspace and notify the handoff flow; the drafts are inputs to `sales-cs-handoff-quality-scoring` (dimension 6) and to `/vfa:value-bridge-realization-tracker ingest`.

## Output contract

The draft entries plus a one-line handoff summary: N outcomes committed, tiers, EVB status, and anything refused with the reason. Refusals lead.

## Security & Permissions

Local deal workspace only; no Registry, Value Map, catalog, or CRM writes; no network access.

## Trust & Verification

Every entry traces to a qualified promise and a catalog OC-ID; EVB verbatim discipline is stated at capture and enforced downstream by the tracker. Anchors: VBS-107/108, Value-Registry-Explainer-Playbook §4, registry-value-map-rollup-mapping.md.
