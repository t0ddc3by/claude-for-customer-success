---
name: value-bridge-realization-tracker
description: >
  Operate the Value Registry, the portfolio-wide repository of the OC/VR pair:
  ingest commitment drafts from the vbs value-commitment-builder, walk each
  entry through the lifecycle (Committed, Baseline Captured, Active, Value
  Bridge Executed, Closed) enforcing the Bridge discipline rules (verbatim
  EVB, customer-system RVI, Finance-validated BIS, formal recognition, FM
  classification on every not-achieved close), and produce portfolio
  aggregates plus the quarterly write-back payload feeding all four loop
  edges (R1 catalog, R2 ICVP, R3 ICP, R4 PMF). This skill's engine is the
  Registry's designated single writer; everything else reads.
argument-hint: "[ingest <draft> | baseline|realize|impact|recognize|close <entry> | report --writeback]"
version: "0.1.0"
deployment_target: plugin
---

# /vfa:value-bridge-realization-tracker

Value that is achieved but not recognized does not drive retention; value that is recognized but not recorded cannot train the gates.

[PROPOSED]

---

## Use when

- A closed deal's commitment drafts arrive from `/vbs:value-commitment-builder` (ingest)
- An account milestone produces baseline, realization, impact, or recognition evidence to record
- An outcome cycle ends, achieved or not (close, with FM classification when not)
- The quarterly loop needs the aggregates and write-back payload (`report --writeback`)
- Leadership asks the only question that validates the whole system: do we deliver what we promise, for whom, at what rate?

## Do NOT use for

- Per-account value management and next-step control (the Value Map and its VMB agent own the per-account control plane; Map evidence rolls up here, per the roll-up mapping)
- Writing the Outcome Catalog (the R1 payload is delivered to `rev-ops.outcome-statement-builder`; this engine never touches the catalog)
- Drafting commitments (vbs owns the drafting; this skill enforces and records)

## Typical activation

"Ingest the Summit commitment entries" / "record the baseline from the kickoff call" / "close OC-W004 for Northwind, not achieved" / "run the quarterly registry report"

---

## The discipline rules (enforced by the engine, not by intention)

1. Ingest refuses drafts violating the sales-eligibility rule (non-eligible tier or roadmap-dependent) and drafts whose evidence plan lacks a customer-side source system.
2. The Expected Value Baseline is recorded only with a verbatim attestation, text, and speaker; catalog-language baselines are rejected at the API, with the fix stated.
3. The Realized Value Indicator must cite a customer-system source; vendor self-report is rejected.
4. The Business Impact Statement requires the finance-validated flag before it exists on the record.
5. Recognition requires a formal mechanism (co-authored summary, signed acknowledgment); informal thanks is disqualified as evidence.
6. An achieved close requires the full Bridge executed; a not-achieved close requires an FM class: A healthy, B delivery failure, C sales over-commitment, D discovery failure.

## Workflow

1. Read config (registry path from the vfa config; default per deployment). All operations run through `scripts/registry.py`; never hand-edit the registry file, and never re-derive aggregates in-context.
2. For each user request, map to the engine command, run it, and present the result. A discipline violation (exit 2) is presented as what the rule is, why it exists, and exactly what evidence would satisfy it; never worked around.
3. `report --writeback` each quarter: present achievement rate (overall, per outcome, per segment), FM counts with the FM-C/FM-D share called out as the drift dashboard, pre-calibration flags, and the four-edge payload with its delivery instructions (R1 to the catalog writer; R2 as a proposed weights re-fit via `/vfa:customize --propose-weights`, human-approved; R3 to `icp-drift-monitor`; R4 as the PMF decay check).

## Output contract

Engine output first, interpretation second. Quarterly reports lead with achievement rate and FM-C/FM-D share; pre-calibration segments are always labeled.

## Security & Permissions

Writes only the configured registry JSONL through the bundled stdlib script (append-only event log; state derived by replay); no network access; no catalog, Value Map, CRM, or Linear writes. The single-writer designation is load-bearing: report any second writer as an architecture defect.

## Trust & Verification

Structural validation: `scripts/registry.py --self-test` (14 checks including the vbs-draft round-trip and every discipline refusal). The event log is the audit trail; any entry's full history is `show <entry_id>`. Anchors: Value-Registry-Explainer-Playbook, Value-Catalog-Explainer-Playbook-v2, NRR-Unified-Framework (FM taxonomy), registry-value-map-rollup-mapping.md (single-writer designation).
