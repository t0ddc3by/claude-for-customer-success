---
name: icp-scorecard-builder
description: "Builds and scores an Ideal Customer Profile (ICP) fit+intent scorecard for B2B SaaS accounts/leads from CRM data, attribute lists, and closed-won/closed-lost history. Use when a user asks to build a lead/account scoring model, score a batch of leads against an ICP, define MQL thresholds, validate a scoring rubric against conversion outcomes, or explain why a specific account scored the way it did. Produces a weighted scorecard, tiered routing recommendations (A/B/C), and per-account explainability breakdowns."
license: MIT
metadata:
  author: icp-methodology-corpus
  version: '1.0'
  methodology_step: "Step 3 (Scorecard) and Step 7 (Operationalization) of ICP_Methodology.md"
---

# ICP Scorecard Builder

## When to Use This Skill

Use this skill when the user asks you to:

- Build a lead- or account-scoring model / rubric for a B2B SaaS ICP
- Score a batch of leads or accounts (CSV/CRM export) against an existing or newly-defined ICP
- Set or re-tune MQL/SQL score thresholds and tier bands (A/B/C)
- Explain, per-account, *why* a lead scored the way it did (explainability breakdown)
- Validate whether an existing scorecard actually discriminates buyers (top-tier vs. bottom-tier conversion comparison)
- Add or refine negative scoring / disqualification rules (negative ICP enforcement)

Do NOT use this skill for: win/loss qualitative interview analysis (use a win/loss pattern extractor instead), TAM/SAM/SOM market sizing, or long-term drift monitoring across quarters (use an ICP drift monitor instead).

## Conceptual Basis

This skill operationalizes a **hybrid fit + intent scoring architecture**: firmographic fit acts as a qualifying gate (a floor below which no behavioral signal can raise the score), and behavioral/intent signals occupy the top of the score range. This prevents highly-engaged-but-out-of-profile leads from being prioritized over accounts that are both a strong fit and actively buying. Scores must separate **fit** (does this account match the ICP: industry, size, role, geography, revenue) from **engagement/intent** (pricing-page visits, demo requests, ROI-calculator use, webinar attendance), include explicit **negative scoring** for disqualifiers, and **decay** over time to reflect that behavioral signals lose predictive value quickly.

## Instructions

### Step 1: Gather Inputs

Ask the user for (or infer from provided files):

1. **Attribute list** — the firmographic, technographic, behavioral, and situational attributes believed to predict fit (if none exists yet, help the user derive one from a sample of their best/worst customer accounts — ask for a CSV of top-quartile and bottom-quartile accounts by lifetime revenue/NRR, if available).
2. **Historical outcome data** — closed-won/closed-lost records (ideally 1,000+ records, minimum viable is 50–100 for a first pass) with the same attribute fields populated, plus the outcome label (won/lost, and at what stage).
3. **Current MQL/SQL definitions**, if they exist, so the scorecard aligns with existing sales process rather than inventing a parallel system.
4. **Deal-size / ACV context**, to calibrate whether this is an SMB high-velocity motion (lower thresholds, fewer criteria) or an enterprise motion (higher thresholds, more criteria, longer decay windows).

If historical outcome data is unavailable, proceed with a **hypothesis-driven scorecard** (Step 2) and flag to the user that it must be validated once 60–90 days of outcome data accumulate (Step 5).

### Step 2: Design the Scorecard

1. **Separate the criteria into four buckets**: Firmographic Fit, Technographic Fit, Behavioral/Intent, Negative/Disqualifying.
2. **Assign point weights** using this reference schema (adjust magnitudes to the user's context, but preserve the relative ordering — intent signals should generally out-weight static firmographic fit at the top of the range):

   | Signal type | Example | Typical weight |
   |---|---|---|
   | High-intent behavioral | Pricing page visit, demo request, ROI calculator completion | 15–25 pts |
   | Mid-intent behavioral | Blog visits, email clicks, webinar attendance | 5–10 pts |
   | Firmographic fit | ICP industry match, title/seniority match, company size band | 5–20 pts |
   | Technographic fit | Compatible/complementary tech stack detected | 10–20 pts |
   | Situational/trigger | Recent funding round, new relevant executive hire, hiring surge | 10–20 pts (apply shorter decay window — see Step 4) |
   | Negative/disqualifying | Below company-size floor, incompatible tech stack, competitor domain, personal email, inactivity | −10 to −25 pts |

3. **Set a firmographic/technographic gate.** Define a floor threshold below which no behavioral score can push a lead above disqualification (e.g., "any lead scoring below 0 net firmographic+technographic points is capped at 'nurture' regardless of behavioral score"). This is the single most important design choice — it prevents highly-engaged-but-wrong-fit leads from consuming sales capacity.
4. **List explicit negative/disqualifying criteria** (pull directly from the user's negative ICP if one exists): company-size floor, industry exclusion, tech-stack incompatibility, absence of identifiable budget authority, inactivity thresholds (typically 30 and 45+ days).
5. **Keep the rubric to fewer than ~10–12 total criteria** for a first version — simpler rubrics are easier to validate and explain to sales.

### Step 3: Set Thresholds and Tiers

Default starting bands (adjust based on deal size/ACV — enterprise motions should generally use the higher end):

| Score band | Tier | Action |
|---|---|---|
| 80+ | A — Highest priority | Route to senior AE, same-day outreach |
| 60–79 | B — MQL | Route to SDR, work within minutes/hours |
| 40–59 | C — Nurture | Automated nurture sequence |
| Below 40 | D — Deprioritized | Suppress or long-cycle nurture only |

For enterprise motions (deal sizes >$150K ACV), shift all thresholds up by roughly 15–20 points, since longer cycles and more stakeholders require higher-confidence signal before committing AE time.

### Step 4: Implement Decay

Apply decay to prevent stale signals from over-inflating scores:

- **Behavioral signals**: decay starting at 30 days of inactivity (e.g., −5 to −10 pts), accelerating at 45–60 days.
- **Situational/trigger-event signals**: these decay much more slowly than behavioral signals — maintain elevated scoring for 30–90 days post-event, then decay sharply, since trigger events (funding, exec hires) create a bounded buying window rather than an ongoing intent signal.
- Document the decay schedule explicitly in the rubric output so it is auditable.

### Step 5: Score a Batch and Produce Explainability Output

When given a batch of leads/accounts (CSV or CRM export):

1. Compute the total score for each record by summing applicable criteria.
2. Apply the firmographic/technographic gate from Step 2.
3. Assign the tier from Step 3.
4. For each scored record, output the **top 3 contributing factors** in plain language, e.g.: `"Industry: SaaS (+10) / Employee count 200-500 (+15) / Pricing page visited 3x in 14 days (+20)"`. This explainability layer is mandatory — a bare numeric score without a breakdown is an incomplete deliverable.
5. Sort the output by tier, then by score descending, and present as a table.

### Step 6: Validate Against Outcomes (once data is available)

1. Establish baseline metrics before the scorecard goes live: current MQL-to-SQL conversion rate, average deal size by lead source, SDR connect rate by segment.
2. After 60–90 days of live scoring, compare conversion rates for the top score tier (A) vs. the bottom score tier (D).
3. **The scorecard is working if the conversion gap between top and bottom tiers widens over time.** If the gap is flat or narrow, the weighting is miscalibrated — return to Step 2 and re-examine which criteria actually differ between historical closed-won and closed-lost records.
4. Recommend re-tuning the rubric quarterly, or immediately if win rate shifts by more than 10 percentage points.

### Step 7: Deliver Outputs

Always produce, as applicable to the request:

1. **The documented rubric** (criteria, weights, gate, decay schedule, thresholds) as a markdown table.
2. **The scored batch output** (if a lead list was provided) with tier and explainability breakdown.
3. **A validation plan or validation result** (baseline metrics + comparison, if outcome data exists).
4. **Explicit flags** for: (a) any criteria that could not be scored due to missing data, (b) any lead/account that trips a negative/disqualifying rule, and (c) a recommendation to review the rubric if fewer than 50 historical outcome records were available to inform weighting.

## Example

**Input:** "Score these 40 leads against our ICP. We sell accounting automation software to mid-market companies. Best customers are 150-500 employees, run NetSuite or Sage Intacct, and the buyer is a Controller or VP Finance."

**Output rubric produced:**

| Criterion | Points |
|---|---:|
| Controller/VP Finance title or above | +25 |
| 150–500 employees | +20 |
| NetSuite/Sage Intacct detected | +20 |
| Pricing page visited 2+ times in 14 days | +15 |
| ROI calculator completed | +20 |
| Under 50 employees | −20 |
| No ERP detected | −15 |
| 30+ days no engagement | −10 |

**Output for one scored lead:** `Jane Doe, VP Finance, Acme Corp (300 employees, NetSuite) — Score: 65 (Tier B, MQL) — Top factors: VP Finance title (+25), NetSuite detected (+20), 300 employees (+20)`

## Notes and Limitations

- This skill produces a *rules-based* scorecard by default. If the user wants a trained statistical/ML model, treat this skill's output as the feature-engineering and labeling step, then hand off to a modeling process — do not silently swap in a black-box model without telling the user.
- Always ask whether a negative ICP / exclusion list already exists before inventing disqualifying criteria from scratch; reuse the user's existing definitions where available.
- Scorecards must be re-validated whenever the underlying ICP changes (new segment, new product, upmarket move) — do not assume a rubric built for one ICP tier applies unchanged to another.
