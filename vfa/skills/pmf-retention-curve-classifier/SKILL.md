---
name: pmf-retention-curve-classifier
description: "Classifies SaaS cohort retention curves (decaying-to-zero, flattening/hook, or upward-smile) from raw cohort activity data, benchmarks them against category- and stage-specific PMF thresholds, and flags which customer segments show real Product-Market Fit versus which do not. Use when the user has cohort retention data (signups by period with active/churned status) and wants to know whether the shape indicates PMF, per Brian Balfour's and CRV's retention-curve methodology. Trigger phrases: 'cohort retention curve', 'retention curve shape', 'does this retention curve show PMF', 'flattening retention', 'retention benchmark', 'smile curve', 'logo retention analysis'."
license: MIT
metadata:
  author: pmf-methodology
  version: '1.0'
  based_on: "PMF_Methodology.md Step 5 (Cohort Retention Curve Analysis)"
---

# Cohort Retention Curve Classifier

## When to Use This Skill

Use this skill whenever the user provides cohort-level retention/activity data and wants to know:

- Whether the retention curve shape indicates Product-Market Fit (flattening above zero) or lack of it (decaying to zero)
- How their retention compares to category- and stage-specific benchmarks (consumer, SMB SaaS, enterprise SaaS, seed-stage B2B)
- Whether blended/aggregate retention is hiding a real-fit subsegment or a non-fit subsegment (segmentation analysis)
- Whether a poor retention curve is actually an onboarding/activation problem rather than a true PMF problem
- Whether the "trifecta" (growth + retention + usage depth) is present

Do NOT use this skill for computing NRR/GRR (revenue-based retention — use a dedicated NRR/GRR skill) or for survey-based PMF scoring (use the Sean Ellis survey analyzer skill). This skill is specifically for **behavioral cohort activity retention** — the "did they keep using it" signal, not the "did they keep paying, and how much" signal.

## Background: What This Skill Computes

A cohort retention curve plots, for a group of users/accounts who started in the same period ("cohort"), the percentage still active in each subsequent period. The three diagnostic shapes:

1. **Decaying to zero** — every cohort eventually fully churns out. No PMF signal.
2. **Flattening at a non-zero plateau** (the "smile" or "hook") — a durable retained base exists. PMF signal for at least that segment; the plateau height indicates strength.
3. **Curving upward over time** (true "smile") — the surviving cohort's engagement or revenue grows over time (expansion/negative-churn dynamics). Strongest possible signal.

**Time unit convention:** Use days for B2C consumer products (messaging, gaming, photos — fast signal); use months for B2B SaaS (slower signal, typically read on monthly churn).

## Instructions

### Step 1: Validate and structure the input data

1. Required fields per row, at minimum: `cohort_id` (or cohort start period), `period_number` (0, 1, 2, 3... periods since cohort start), and either `active_count` (count still active that period) or `active_flag` per individual account/user with a `cohort_start_date`.
2. If data is at the individual-account level, aggregate into cohort × period tables: `retention_pct = active_count_at_period_n / initial_cohort_size * 100`.
3. Require at least 3 periods of data for a directional read, and ideally 6+ periods (6 months for B2B SaaS) for a benchmark-comparable read. If fewer than 3 periods exist, report the result as "too early to classify shape — insufficient periods" rather than forcing a classification.
4. If segment fields are available (industry, company size, acquisition source, plan tier, signup cohort quarter), always compute retention **both blended and segmented**. Never report only the blended number — per methodology, blended metrics can hide both a real-fit subsegment and a non-fit majority.

### Step 2: Classify the curve shape

For each cohort/segment series:

1. Compute period-over-period deltas: `delta_n = retention_pct[n] - retention_pct[n-1]`.
2. Apply this classification logic:
   - If retention_pct is trending toward 0 with no deceleration in the decline rate over the last 2+ periods → **"Decaying to zero — no PMF signal."**
   - If the decline rate decelerates and the last 2+ periods show retention_pct changing by less than ~3 percentage points period-over-period, holding above 0 → **"Flattening/hook — PMF signal present."** Report the plateau level (average of the last 2–3 stable periods).
   - If retention_pct is flat or rising over the last 2+ periods (delta_n ≥ 0 sustained) → **"Upward smile — expansion dynamics, strongest signal."**
   - If the series is too short or too noisy to fit any pattern confidently → **"Indeterminate — collect more periods."**
3. Always run this classification per segment, not just blended.

### Step 3: Benchmark against category/stage tables

Compare the plateau (or latest available period, if not yet flattened) against these reference tables and report which band the result falls into.

**6-month retention by category (consumer/SaaS products with meaningful history):**

| Category | Good | Great |
|---|---:|---:|
| Consumer social | 25% | 45% |
| Consumer transactional | 30% | 50% |
| Consumer SaaS | 40% | 70% |
| SMB/mid-market SaaS | 60% | 80% |
| Enterprise SaaS | 70% | 90% |

**Seed-stage B2B (3-month retention, more forgiving early benchmark):**

| Percentile | 3-month retention |
|---|---:|
| Top performers | 15.6% |
| Median | 2.5% |

**Logo retention sanity anchors (12-month, mature public SaaS comps):** Atlassian ~98%, Salesforce ~90%, Workday ~95%, Slack ~90–95%, QuickBooks ~79%, Dropbox ~80%.

Ask the user which category/stage applies (consumer vs. SMB SaaS vs. enterprise SaaS; seed vs. later-stage) if not specified, and select the correct table accordingly — do not apply a mature-company benchmark to an early-stage cohort or vice versa.

### Step 4: Diagnose activation contamination

Before concluding "no PMF" from a decaying curve, check for onboarding/activation contamination:

1. If activation-event data is available (did the user reach the defined "aha moment"?), split the cohort into "activated" vs. "never activated" sub-cohorts and re-run Step 2 classification on each separately.
2. If the "activated" sub-cohort flattens well above zero while "never activated" users drag down the blended curve, report this explicitly: **"This looks like an onboarding/time-to-value problem, not a PMF problem. Fix activation before concluding lack of fit."**
3. If activation data isn't available, note this as a data-quality gap and recommend instrumenting an activation event before drawing firm PMF conclusions from a weak blended curve.

### Step 5: Check for the "trifecta" (optional, if growth and usage-depth data are available)

If top-line growth data (new cohort size trend) and usage-depth data (actions per active user per period) are also available, report whether all three signals — growth, retention, and usage depth — are simultaneously positive. Per Balfour's methodology, only when all three agree can PMF be asserted "with close to 100% certainty" for that segment.

### Step 6: Produce the final report

Output a structured report with:

1. **Shape classification** per segment (table: segment | shape | plateau/latest value | trend).
2. **Benchmark comparison** per segment (table: segment | value | category benchmark band | verdict: below good / good / great).
3. **Segmentation insight**: explicitly call out any case where blended and segmented reads disagree materially (e.g., blended 62% masking an 81%-retaining fit segment and a 28%-retaining non-fit segment).
4. **Activation contamination check**: flag if applicable.
5. **Trifecta check**: report if applicable data exists.
6. **Recommendation**, one of:
   - Flattening/upward-smile at or above "Good" band for the relevant category: "Retention supports a PMF verdict for this segment. Cross-check with the Sean Ellis survey score and NRR/GRR before scaling GTM investment in this segment."
   - Flattening but below "Good" band: "Weak/fragile fit signal. Do not scale this segment yet; prioritize product work informed by survey blockers before increasing acquisition spend."
   - Decaying to zero: "No PMF signal for this segment. Do not scale. Return to qualitative discovery (customer interviews) for this segment before further investment — check first for activation contamination."
   - Indeterminate: "Insufficient data — re-run this analysis after collecting at least 3-6 more periods of cohort data."

## Output Format

Lead with a summary table:

```
| Segment | Periods observed | Shape | Plateau/Latest value | Benchmark band | Verdict |
|---|---|---|---|---|---|
```

Followed by narrative sections for Segmentation Insight, Activation Contamination Check, Trifecta Check, and Recommendation.

## Example Walkthrough

Given a 6-month B2B SaaS cohort of 38 accounts with monthly retention 100%, 84%, 74%, 68%, 65%, 63%, 62%: the decline decelerates sharply after month 3 and flattens near 62-63% — classified as "Flattening/hook." Benchmarked against SMB/mid-market SaaS (Good=60%, Great=80%), 62% lands just above "Good." Splitting the same cohort by firmographic segment reveals a "solo/small firm" sub-segment retaining at 81% by month 6 (crossing into "Great") and a "large multi-entity firm" sub-segment decaying to 28% (heading toward zero). The report flags this divergence explicitly and recommends treating these as two different PMF verdicts: confirmed for the solo/small-firm segment, not present for the multi-entity segment — do not scale GTM spend targeting the latter.

## Important Caveats to Always Include in Output

- A retention curve alone is a behavioral signal, not an economic one — always recommend cross-checking with NRR/GRR (revenue retention) before declaring durable, monetizable PMF.
- Never classify a shape from fewer than 3 periods of data; label it "Indeterminate" instead of guessing.
- Always segment before concluding "no PMF" — a decaying blended curve very often hides a flattening subsegment, and vice versa.
