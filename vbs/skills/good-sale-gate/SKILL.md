---
name: good-sale-gate
description: >
  Score an active deal's keepability before close: will the revenue this sale
  creates survive its first renewal? Reviews outcome deliverability, motivation
  strength, stakeholder durability, economic alignment, and the value-evidence
  plan, then returns a keepability verdict (Keep-Ready / Fixable / Fragile)
  with a prioritized fix list and a pre-classification of the failure mode a
  bad close would produce (FM-C sales over-commitment, FM-D discovery failure).
  A deal-strengthening tool, not a deal-killing one: the output is what to fix
  before close, framed for the seller. The signature skill of the vbs plugin.
argument-hint: "[--deal <name> | --scan (late-stage list)]"
version: "0.1.0"
deployment_target: plugin
---

# /vbs:good-sale-gate

The question Claudeforce never asks: not "will this close?" but "will this stay closed?"

[PROPOSED]

ETM coordinates: pipeline 5 Proposal - 7 Closed (pre-close). Consumes both pre-sale instruments per the conformance crosswalk (dimensions 2/3/4 cite readiness rungs 1/2+5/4; dimensions 1/5 cite validation artifacts); where /vbs:deal-axes-reader has computed readings, cite them rather than re-deriving.

---

## Use when

- A deal is entering late stage and the close plan is being written
- Before commercial terms are drafted, so fixes are still cheap
- A renewal-minded leader asks which closing deals are keepable, not just winnable (`--scan`)
- A deal feels winnable but something is off and the seller wants the soft spot named

## Do NOT use for

- Account-level value-fit gating pre-pipeline (that is `/vfa:icvp-composite-scorer`; different altitude, and this skill reads its output when present)
- Post-close handoff quality scoring (Phase 3 `sale-quality-review`, which inherits this rubric)
- Win-probability forecasting; keepability and win probability are deliberately different questions

## Typical activation

"Run the good-sale gate on Summit Learning" / "is this a good sale or just a closeable one?" / "gate check the Q4 commit list"

---

## The five dimensions

Each scored 1-5 with evidence cited from the deal record; unknowns score as unknowns, never as middles:

1. **Outcome deliverability.** Every promise in the qualified promise set commits at a sales-eligible tier with conditions/subsets stated (from `outcome-qualification`). Un-qualified promises in the deal cap this dimension at 2.
2. **Motivation strength.** Why Change / Why Now / Why Us each present with verbatim provenance (from `three-whys-discovery`). A missing Why Now caps at 3: the deal may close on discounting pressure and churn on indifference.
3. **Stakeholder durability.** Does the deal survive the champion leaving? Multi-threaded, economic buyer engaged, blockers addressed rather than avoided (from `stakeholder-influence-plan`).
4. **Economic alignment.** Cost of inaction is written, dollar-quantified, confidence-tiered, and exceeds cost credibly (ICVP arbitrage when available). "The ROI is obvious" written nowhere scores 1.
5. **Value-evidence plan.** It is agreed with the buyer how delivered value will be measured, from whose systems, on what cadence, and who acknowledges it: the Expected Value Baseline conversation is scheduled or done. This dimension is the sale's renewal insurance and the most commonly empty.

## Verdict

- **Keep-Ready (each dimension ≥4):** close with confidence; note residual risks.
- **Fixable (no dimension ≤2, average ≥3):** close is plausible but list the fixes in priority order, each with the concrete action and who runs it. This is the normal, useful verdict.
- **Fragile (any dimension ≤2):** name what a close today would likely become: FM-C if dimension 1 is the failure (we promised beyond the catalog), FM-D if dimensions 2/4 are (we never validated the problem). State the churn horizon honestly (typically 9-18 months, silent). Still produce the fix list; Fragile plus fixes executed becomes Fixable.

## Workflow

1. Read config; load the deal's motivation record, qualified promise set, and stakeholder plan; note any ICVP score on the account. Missing inputs are scored as gaps and the prerequisite skill is named.
2. Score the five dimensions with cited evidence; no dimension scores above 3 on assertion alone.
3. Render the verdict, the fix list (priority order, concrete actions), and the FM pre-classification if Fragile.
4. Write the gate result to the deal workspace, dated, so `--scan` and the Phase 3 `sale-quality-review` can trend it.

## Output contract

Verdict first, one line. Then the five-dimension table (score, evidence, gap). Then the fix list. Never a naked kill: every Fragile verdict ships with the path to Fixable.

## Security & Permissions

Reads local deal workspace artifacts and configured catalog only; no network access; no CRM writes.

## Trust & Verification

Every score cites deal-record evidence; unknowns are visible; verdicts are reproducible from the written record. Anchors: VBS-100/115 (Validate Alignment Instead of Assuming; Customer Simulation Circle), FM taxonomy (NRR-Unified-Framework), Retention Reckoning, VFAS §1.
