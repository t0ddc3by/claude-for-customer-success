---
name: icp-drift-monitor
description: "Detects and reports Ideal Customer Profile (ICP) drift and misfit in B2B SaaS using quantitative signals: segmented Net Revenue Retention (NRR) by ACV tier/vintage/product/vertical, sales-cycle length, win-rate variance by source, support/escalation load, and churn root-cause tagging. Use when a user asks whether their ICP is drifting, wants to prove ICP misfit to executives/the board with data, needs a quarterly bad-fit review, or wants an early-warning alert before a churn crisis. Produces a drift diagnosis, board-ready quantitative summary, and escalation recommendation."
license: MIT
metadata:
  author: icp-methodology-corpus
  version: '1.0'
  methodology_step: "Step 8 (Continuous Monitoring) and Step 9 (Closing the Loop) of ICP_Methodology.md"
---

# ICP Drift / Misfit Early-Warning Monitor

## When to Use This Skill

Use this skill when the user asks you to:

- Determine whether their ICP has drifted (i.e., the accounts being sold to no longer match the profile that predicts success)
- Segment NRR, churn, or retention data by cohort to find where a specific segment is underperforming
- Build a quantitative, board-ready case that a specific customer segment or sales motion is systematically low-fit
- Run a quarterly "bad-fit review" or churn root-cause pattern meeting
- Set up (or evaluate) an early-warning threshold that should trigger a formal ICP re-review

Do NOT use this skill for: initial ICP definition (use win/loss + best-customer cohort analysis first), or building the fit-scoring rubric itself (use the ICP scorecard builder skill) — this skill assumes an ICP and scorecard already exist and is checking whether reality still matches them.

## Conceptual Basis

ICP drift rarely announces itself directly — it shows up as **segment-specific degradation** in retention, expansion, cycle length, support load, and engagement, all of which are *lagging symptoms of an upstream qualification problem*, not something a Customer Success team can fix downstream. The core diagnostic principle: because Net Revenue Retention (NRR) excludes new logos, it is a pure cohort signal of how the *existing* book is performing — so segmenting NRR and finding a large gap between segments is a direct, quantitative proxy for whether Sales has been qualifying the right accounts. **A gap of 15+ percentage points in NRR between two comparable segments is treated as evidence of ICP drift in sales qualification, not a CS execution gap**, because a customer that was never a strong fit will not adopt the product at a rate that justifies renewal regardless of how well they are onboarded or managed.

## Instructions

### Step 1: Establish Data Prerequisites

Before running any analysis, confirm (or help the user establish) a credible data foundation:

1. **A clean subscription/billing data layer** — ARR by account, with start/end dates and cohort tags (ACV tier, acquisition vintage/quarter, product line, industry vertical).
2. **CRM-to-billing reconciliation** — flag to the user if NRR is being computed from CRM estimates only rather than billing actuals; billing-actuals-based NRR is the number that survives board scrutiny, CRM-only NRR is an estimate.
3. **Churn root-cause tagging** — check whether churn events are tagged by cause (e.g., Wrong ICP / Misaligned Use Case / Over-Promised / Price / Product Gap). If this field does not exist or is inconsistently populated, recommend making it a mandatory CRM field before proceeding, and note that historical analysis will be limited without it.
4. **Support/ticket volume and engagement/usage data by account**, if available, as a secondary corroborating signal.

If any prerequisite is missing, still proceed with best-available data, but explicitly flag data-quality limitations in the final output rather than presenting the diagnosis as more certain than the data supports.

### Step 2: Compute Segmented NRR

1. Compute NRR using: `NRR = (Starting ARR + Expansion − Contraction − Churned) / Starting ARR × 100`, over a consistent trailing period (typically trailing 12 months).
2. Segment this calculation across each of the following cuts independently:
   - **ACV tier** (e.g., SMB / mid-market / enterprise)
   - **Acquisition vintage** (the year/quarter the cohort was acquired)
   - **Product line** (if multi-product)
   - **Industry vertical**
3. Present results as a table showing the aggregate NRR alongside each segment's NRR, e.g.:

   | Segment | NRR | Gap vs. best segment |
   |---|---:|---:|
   | Company-wide (aggregate) | 105% | — |
   | Enterprise cohort | 118% | — |
   | Mid-market cohort | 108% | −10 pts |
   | SMB cohort | 85% | −33 pts |

4. **Flag any segment pair with a gap ≥ 15 percentage points** as a drift signal requiring escalation (Step 5).

### Step 3: Compute Vintage (Acquisition-Cohort) Trend

1. Compute NRR (or gross retention, if NRR is not yet reliable for young cohorts) separately for each acquisition vintage (e.g., cohort acquired in 2024-Q1, 2024-Q2, 2024-Q3...).
2. Plot/tabulate the trend across vintages. **A declining trend from earlier to later vintages is an early/leading indicator of ICP drift** — it means the profile of who is being sold to is deteriorating over time, even before it fully shows up in aggregate NRR.
3. If a decline is detected, cross-reference the vintage timeline against known changes in targeting, campaigns, comp-plan changes, or new sales hires to identify a candidate root cause.

### Step 4: Compute Secondary Corroborating Signals

1. **Sales-cycle length and win-rate by source**: compute average days-to-close and win rate, segmented by lead source and by the same cohort cuts as Step 2. Wildly varying win rates by source (e.g., 12% vs. 34%) indicate that acquisition sources are not calibrated to the ICP.
2. **Support/escalation load per account**, segmented by the same cuts — elevated load in a specific segment corroborates a structural (not merely operational) misfit.
3. **Product engagement depth** (feature adoption, login frequency, or an equivalent usage metric) by segment — shallow engagement in a specific segment is the behavioral signature of accounts that were never a strong fit.

### Step 5: Diagnose and Escalate

1. If any segment-pair NRR gap is ≥ 15 points, or vintage NRR is declining, classify this as an **active drift signal**.
2. Cross-tabulate churn root-cause tags (if available) against the flagged segment. If ≥ 25% of churned accounts in the flagged segment/cohort quarter are tagged "Wrong ICP," this **crosses the escalation threshold** and should trigger a recommendation for a formal ICP review within 30 days (do not recommend waiting for an annual cycle — that cadence is explicitly too infrequent to catch drift before it compounds).
3. Produce a **quarterly bad-fit pattern-meeting readout**: which segment is flagged, the magnitude of the gap, the corroborating secondary signals, and a recommended owner (typically RevOps + Sales leadership, with Customer Success as the signal-source, not the fix-owner — cohort composition is a lever CS investment alone cannot fix).

### Step 6: Produce the Board-Ready Summary

When the audience is executive/board-level, structure the output as:

1. **Headline finding** in one sentence (e.g., "SMB cohort NRR (85%) is 33 points below enterprise cohort NRR (118%), consistent with ICP drift in SMB sales qualification, not a CS execution gap.")
2. **The segmented NRR table** (Step 2).
3. **The vintage trend** (Step 3), if relevant.
4. **Dollar translation**: estimate the revenue impact — e.g., translate the NRR gap into dollars of ARR at risk for the flagged cohort, and note comparable industry costs of misalignment (wrong-segment targeting inflating CAC 30–50%; a 24-point revenue-growth gap between aligned and misaligned GTM orgs) as context, clearly labeled as general industry benchmarks rather than this company's own measured figures unless the user has verified their own CAC/growth data.
5. **Data-quality caveat**, if CRM-to-billing reconciliation was not confirmed in Step 1.
6. **Recommended action and owner** (e.g., "Recommend RevOps + Sales leadership review SMB qualification criteria within 30 days; CS to supply churn root-cause detail as input, not as the accountable owner of the fix.")

### Step 7: Set Up Recurring Monitoring (if requested)

If the user wants this to run on a recurring basis rather than as a one-time analysis:

1. Recommend a **quarterly cadence** as the default for the full segmented review (Step 2–4), with an **immediate ad hoc re-run** any time the 15-point NRR gap or 25% Wrong-ICP-churn threshold is crossed mid-quarter.
2. Recommend the same cadence be used to refresh the TAM/SAM/SOM sizing and the ICP scorecard rubric if drift is confirmed and the ICP definition is subsequently revised.

## Example

**Input:** "Our board thinks our CS team is underperforming because overall NRR is only 98%. Here's our billing data by segment."

**Output:**

> Headline: Aggregate NRR of 98% masks a 34-point gap between segments — this is an acquisition/ICP problem, not a CS execution problem.
>
> | Segment | NRR |
> |---|---:|
> | Company-wide | 98% |
> | Enterprise | 121% |
> | Mid-market | 104% |
> | SMB | 87% |
>
> The SMB cohort (87% NRR) is 34 points below Enterprise (121%), exceeding the 15-point drift threshold. Vintage analysis shows SMB NRR has declined each quarter for the last 4 quarters (91% → 89% → 88% → 87%), indicating the SMB acquisition profile has been deteriorating, not stabilizing. Churn tags show 41% of SMB churn this quarter was root-caused "Wrong ICP" — above the 25% escalation threshold. **Recommendation: trigger a formal SMB ICP qualification review within 30 days; this is a RevOps/Sales-owned fix, not a CS staffing issue.**

## Notes and Limitations

- This skill diagnoses *where* drift is occurring and provides the quantitative case; it does not itself redefine the ICP. Once drift is confirmed, hand off to the win/loss + best-customer cohort re-analysis (initial ICP definition steps) to determine the corrected profile.
- Segment sample size matters — flag to the user if any segment has fewer than ~20–30 accounts, since NRR at small sample sizes is noisy and a 15-point gap may not be statistically meaningful.
- Always distinguish **leading indicators** (vintage NRR trend, cycle length) from **lagging indicators** (aggregate churn, support load) in the output — leading indicators justify earlier action even before lagging ones move.
- Do not present industry benchmark figures (e.g., "30-50% CAC inflation," "24-point growth gap") as this-company's own measured results — always label them as external context unless the user's own data has been used to compute the equivalent figure.
