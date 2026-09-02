---
name: pmf-sean-ellis-survey-analyzer
description: "Analyzes Sean Ellis / Superhuman-style Product-Market Fit survey data (the 'How would you feel if you could no longer use [Product]?' question) and produces a scored PMF verdict. Use when the user has raw PMF survey responses (CSV, JSON, or spreadsheet) and wants the 'very disappointed' percentage calculated, segmented into High-Expectation-Customer (HXC) cohorts, and turned into a prioritized love/blockers product roadmap. Trigger phrases: 'Sean Ellis survey', 'PMF survey', 'very disappointed percentage', 'product-market fit score', '40% test', 'Superhuman PMF engine', 'HXC analysis'."
license: MIT
metadata:
  author: pmf-methodology
  version: '1.0'
  based_on: "PMF_Methodology.md Step 4 (Sean Ellis Survey with HXC Segmentation)"
---

# Sean Ellis PMF Survey Analyzer

## When to Use This Skill

Use this skill whenever the user provides (or asks you to help design/run) a Product-Market Fit survey based on Sean Ellis's canonical instrument, and wants any of the following:

- The core PMF score (% "very disappointed") calculated from raw responses
- A pass/fail read against the 40% benchmark, with the correct scoring band
- Segmentation of respondents into High-Expectation Customers (HXC), on-the-fence users, and lost causes, following Rahul Vohra's Superhuman method
- A prioritized "love vs. blockers" product roadmap derived from open-ended survey answers
- Guidance on designing or timing a new PMF survey (sample size, respondent gating, question wording)
- Tracking the score over multiple survey rounds (quarterly cadence) to see if it's trending toward or away from 40%

Do NOT use this skill for NPS analysis, general customer satisfaction surveys, or churn surveys — those are different instruments (see the companion NRR/GRR and retention-curve skills for economic/behavioral PMF signals). This skill covers only the leading-indicator survey signal.

## Background: The Instrument This Skill Analyzes

The canonical question, exactly as used by Sean Ellis and Rahul Vohra (Superhuman):

> **"How would you feel if you could no longer use [Product]?"**

with answer options:

1. Very disappointed
2. Somewhat disappointed
3. Not disappointed
4. (Optional 4th option) N/A — I no longer use it

Recommended follow-up questions (Superhuman's exact set — include these if available, since they drive the HXC/roadmap steps below):

- Q2: "What type of people do you think would most benefit from [Product]?"
- Q3: "What is the main benefit you receive from [Product]?"
- Q4: "How can we improve [Product] for you?"

**Sampling requirement to validate before scoring:** respondents should have used the product's core functionality at least twice in the last two weeks. If the dataset includes users who signed up but never activated, or who used the product only once, flag this as a sampling-gate violation before reporting the score — the score will read artificially low and the diagnosis will be wrong (an activation problem, not a PMF problem).

## Instructions

### Step 1: Validate and clean the input data

1. Confirm the dataset contains at minimum: a respondent ID, the Q1 (disappointment) answer, and ideally Q2–Q4 free-text answers.
2. Confirm sample size. If n < 40, report the result as "directionally suggestive only, not statistically reliable" per the 40-respondent minimum threshold. If n is between 40 and 100, note it as adequate but note ideal range is 100–200.
3. Check for and flag duplicate respondents (the same user should never be surveyed twice in the same measurement window — if duplicates exist, deduplicate to the most recent response only).
4. If an engagement/activation flag is available (e.g., "sessions in last 14 days"), filter out respondents who don't meet the ≥2-uses-in-14-days gate and report both the gated and ungated scores side by side, flagging any material difference as an activation-vs-PMF issue.

### Step 2: Compute the core PMF score

1. Tally responses into the three (or four) buckets.
2. Compute: `PMF_score = count("Very disappointed") / total_valid_responses * 100`. Exclude "N/A — no longer use it" responses from the denominator, but report their count and rate separately as an implicit-churn signal.
3. Classify the score into a band:

   | Score | Band |
   |---|---|
   | ≥ 40% | Strong PMF signal |
   | 25% – 39% | Promising — iterate and narrow focus |
   | < 25% | Not achieved — pivot or iterate before scaling |

4. If historical survey rounds are available, compute the trend (e.g., 22% → 33% → 58%) and report direction and rate of change per round.

### Step 3: Build the High-Expectation-Customer (HXC) segment

1. Filter to respondents who answered "Very disappointed."
2. From this subset's answers to Q2 ("What type of people would most benefit?"), extract recurring role/persona descriptors (job titles, company types, use-case descriptions, behavioral traits). Cluster into 1–3 candidate HXC profiles. Write each as a short persona paragraph (name, role, defining behavior/need) — modeled on Superhuman's "Nicole" persona (a heavy-email professional who prioritizes responsiveness).
3. From the same subset's answers to Q3 ("main benefit"), extract and rank the top 3–5 recurring value themes — this is the "love" list.
4. Re-score the PMF percentage restricted to respondents whose profile matches the dominant HXC cluster (if role/firmographic data is available to make this cut). Report this HXC-adjusted score alongside the blended score — expect it to be higher, mirroring the Superhuman pattern (22% blended → 33% after segmentation).

### Step 4: Extract the "somewhat disappointed" opportunity set

1. Filter to respondents who answered "Somewhat disappointed."
2. Cross-reference their Q3 answers against the "love" list from Step 3. Split this group into:
   - **Near-miss users**: cite the same core benefit as the HXC — these are convertible.
   - **Mismatched users**: cite a different benefit or use case — treat as lower priority (likely a different segment/job entirely, not a near-term conversion target).
3. From near-miss users' Q4 answers ("How can we improve?"), extract and rank the top 3–5 recurring blockers. This is the "blockers" list.
4. Explicitly disregard "Not disappointed" respondents from roadmap prioritization — per the methodology, these are not a near-term conversion opportunity; note their count/share for reference only.

### Step 5: Produce the prioritized roadmap

1. Combine the Step 3 "love" list and Step 4 "blockers" list.
2. For each item, assign a Cost (Low/Medium/High) and Impact (Low/Medium/High) estimate — ask the user for input if you cannot infer this from context, or flag as "needs cost/impact estimate from the team."
3. Rank items so the roadmap allocates roughly 50% of near-term effort to deepening "love" items and 50% to resolving "blocker" items — never 100% to either side (over-indexing on love stalls the score; over-indexing on blockers cedes ground to competition).
4. Sequence within each half by Low-cost/High-impact first.

### Step 6: Produce the final report

Output a structured report with these sections, in this order:

1. **Headline score**: blended % very disappointed, band classification, sample size and validity note.
2. **HXC-adjusted score**: segmented %, and the HXC persona(s) identified.
3. **Trend** (if historical data exists): table of round-over-round scores with direction.
4. **Love list**: ranked themes with supporting quote excerpts.
5. **Blockers list**: ranked themes with supporting quote excerpts, split by near-miss vs. mismatched origin.
6. **Roadmap**: the 50/50 prioritized list with cost/impact tags.
7. **Data quality flags**: any sampling gate violations, duplicate respondents, or n<40 warnings.
8. **Recommended next action**: one of:
   - Score ≥40% and HXC-adjusted ≥40%: "Survey signal supports PMF for this segment — proceed to cross-check with cohort retention curve and NRR/GRR before scaling (do not scale on survey alone)."
   - Score 25–39%: "Promising but not sufficient — execute the roadmap above, re-survey next quarter against freshly-engaged users."
   - Score <25%: "Signal does not support PMF — revisit ICP and value proposition before further product investment; re-run qualitative discovery interviews."

## Output Format

Present results as a markdown report with a summary table at the top:

```
| Metric | Value |
|---|---|
| Total valid responses | n |
| Very disappointed % (blended) | x% |
| Band | Strong / Promising / Not achieved |
| HXC-adjusted % | y% |
| Sample adequacy | Adequate (100-200) / Minimum (40-99) / Below minimum (<40) |
```

Followed by the Love List, Blockers List, Roadmap, and Recommendation sections as narrative + tables.

## Important Caveats to Always Include in Output

- This survey measures **stated intent**, not behavior. Always note: "This score should be triangulated with cohort retention data and NRR/GRR before making scaling decisions — surveys alone carry the highest risk of false positives."
- Never resurvey the same respondent in a way that double-counts them in the same measurement window; this artificially distorts the 40% benchmark.
- If the respondent population is drawn from a narrow early-adopter cohort (e.g., only beta testers or only design partners), explicitly flag the risk that a high score reflects "product-user fit" rather than "product-market fit" — recommend testing with a broader/more representative population before concluding market-wide fit.

## Example Walkthrough

Given 165 survey responses: 54 "very disappointed" (32.7%), 79 "somewhat disappointed," 32 "not disappointed." Band = Promising. Analyzing Q2 answers from the 54 very-disappointed respondents reveals 41 describe themselves as "solo/small firm owners serving many clients" — this is the HXC cluster. Re-scoring within that cluster (41 of 118 total respondents matching that profile) yields 34.7% — still promising but improved. Mining Q4 answers from near-miss "somewhat disappointed" respondents who cited the same core benefit reveals "lack of mobile app" as the top blocker (cited by 38 of 62 relevant respondents). The roadmap allocates 50% of next-quarter engineering time to deepening the core workflow and 50% to shipping the mobile app.
