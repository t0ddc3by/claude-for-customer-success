---
name: sale-quality-review
description: >
  Post-close review of a won deal's quality as a sale: were the promises
  deliverable, the motivation validated, the committee durable, the economics
  written, and the commitment entries complete? Re-runs the good-sale-gate
  rubric against the closed record, classifies any weakness by the failure
  mode it predicts (FM-C sales over-commitment, FM-D discovery failure), and
  produces the quality verdict that feeds Gate 0 alongside the rev-ops
  handoff completeness score. Also runs in batch for cohort trending: rising
  FM-C/FM-D share at close time is the earliest drift signal the system has.
argument-hint: "[--deal <name> | --cohort <quarter>]"
version: "0.1.0"
deployment_target: plugin
---

# /vbs:sale-quality-review

Handoff scoring asks "is the record complete?" This skill asks "was the sale good?" Gate 0 needs both answers.

[PROPOSED]

ETM coordinates: post-seam for won deals; at close for lost and no-decision (both frozen axis readings are the win-loss record separating never-real deals from genuinely lost ones).

---

## Use when

- A deal closed and Gate 0 review is imminent
- The commitment drafts exist and the sale's quality should be scored before onboarding inherits it
- Quarterly cohort review: FM-C/FM-D share trending across closed deals (`--cohort`)
- A closed deal later churned and the review record is needed for the FM classification comparison
- A deal closed lost or no-decision: the frozen deal-axes readings (from `/vbs:deal-axes-reader close`) are reviewed as the win-loss record; a loss at readiness rung 1 was never real and is classified as an acquisition-gate miss, not a sales-execution loss

## Do NOT use for

- Pre-close strengthening (use `/vbs:good-sale-gate`; same rubric, different moment, fix list still actionable there)
- Handoff record completeness (rev-ops `sales-cs-handoff-quality-scoring` owns that; this skill complements it)
- Churn root-cause analysis after a loss (renewals `churn-analysis`; this skill's records are its input)

## Typical activation

"Review the Summit close" / "quality-score last quarter's closed-won cohort" / "did we sell that one well?"

---

## Workflow

1. Read config, the deal's closed record: motivation record, qualified promise set, gate history, commitment drafts, and the handoff score if present.
2. Re-score the five gate dimensions against the record as-closed (not as-hoped): unqualified promises that made it into the contract, Whys never validated, single-threaded closes, unwritten economics, missing or non-verbatim EVB plans.
3. Classify: clean (no dimension ≤2), **FM-C exposure** (promises beyond sales-eligible tiers or beyond the qualified set reached the customer), **FM-D exposure** (motivation or economics never validated). Exposure is a prediction, recorded now so the eventual outcome can confirm or refute it; that comparison is how the gate itself gets validated.
4. Emit the review record to the deal workspace: verdict, dimension scores, FM exposure with the specific evidence, and the remediation actions onboarding should take early (a missing EVB is fixable in week one; it is not fixable at renewal).
5. `--cohort`: aggregate review records; report FM-C/FM-D share, trend against prior cohorts, and the reps/segments where exposure concentrates. This is the drift dashboard's close-time feed.

## Output contract

Single deal: verdict line, dimension table, FM exposure with evidence, early-remediation list. Cohort: share, trend, concentration. Framing stays constructive: the unit of accountability is the system, and the review names process fixes before it names people.

## Security & Permissions

Local deal workspace and configured records only; no network access; no writes to Registry, CRM, or Linear (routing recommendations are surfaced, not executed).

## Trust & Verification

Every score cites the closed record; FM exposure predictions are dated so later outcomes can score the reviewer. Anchors: good-sale-gate rubric, FM taxonomy (NRR-Unified-Framework), VFAS §3.3 (FM-C/FM-D as the smoking guns of drift).
