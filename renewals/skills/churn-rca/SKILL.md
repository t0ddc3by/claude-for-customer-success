---
name: churn-rca
description: "Root cause analysis for individual customer churn events and cohort-level churn pattern analysis. Produces structured RCA with root cause taxonomy, contributing factors, timeline reconstruction, and remediation pathway. Scoped to full cancellation — contract contraction redirected to renewals:downgrade-analysis."
version: "1.0.0"
metadata:
  author: "todd@successhacker.co"
  tags: "renewals churn rca root-cause customer-success"
deployment_target: plugin
---

# /renewals:churn-rca [VALIDATED]

## Overview

`renewals:churn-rca` performs structured Root Cause Analysis on confirmed customer churn events (full contract cancellations). It supports three operations:

- **`analyze`** — individual account RCA; produces account-specific root cause findings, timeline reconstruction, OCV delivery analysis, win-back assessment, and remediation pathway
- **`cohort`** — multi-account pattern analysis; surfaces systemic drivers and generates portfolio-level escalation when churn rate meets or exceeds 25%
- **`export`** — retrieves and formats an existing RCA or cohort record for external use

**Use when:**
- A CSM or RevOps analyst needs to perform root cause analysis on a confirmed full contract cancellation
- Analyzing a batch of churned accounts to detect systemic drivers and portfolio-level patterns
- Exporting a completed RCA for stakeholder reporting or portfolio review

**Do NOT use for:**
- Contract downgrades, partial reductions, or contractions → use `renewals:downgrade-analysis`
- Active renewal negotiation or deal management
- Health score calculation or predictive churn scoring
- Real-time portfolio monitoring
- Win-back campaign execution (this skill recommends; it does not execute)

**Scope boundary — contraction redirect:**
If the scenario involves a customer reducing (not cancelling) their contract, respond with:

```
Scope redirect: This request describes a contract contraction, not full churn.
Please use renewals:downgrade-analysis for downgrade analysis.
```

Contraction signals: "reduce," "downgrade," "fewer seats," "smaller tier," "partial cancellation."

## Typical Activation
> `/renewals:churn-rca analyze "Acme Corp"` — full RCA on a single churned account with root cause taxonomy, timeline reconstruction, and win-back assessment
> `/renewals:churn-rca cohort` — multi-account pattern analysis to detect systemic churn drivers; triggers portfolio-level escalation if cohort churn rate ≥ 25%
> `/renewals:churn-rca export "Acme Corp"` — retrieve and format an existing RCA record for stakeholder reporting or portfolio review

---

## Use When
- A CSM or RevOps analyst needs to perform root cause analysis on a confirmed full contract cancellation
- Analyzing a batch of churned accounts to detect systemic drivers and portfolio-level patterns
- Exporting a completed RCA for stakeholder reporting or portfolio review

## Do NOT Use For
- Contract downgrades, partial reductions, or contractions → use `renewals:downgrade-analysis`
- Active renewal negotiation or deal management
- Health score calculation or predictive churn scoring
- Real-time portfolio monitoring
- Win-back campaign execution (this skill recommends; it does not execute)

## Typical Activation
> `/renewals:churn-rca analyze "Acme Corp"` — full RCA on a single churned account with root cause taxonomy, timeline reconstruction, and win-back assessment
> `/renewals:churn-rca cohort` — multi-account pattern analysis to detect systemic churn drivers; triggers portfolio-level escalation if cohort churn rate ≥ 25%
> `/renewals:churn-rca export "Acme Corp"` — retrieve and format an existing RCA record for stakeholder reporting or portfolio review

---

## Pre-flight

- Confirm account context (company name, CSM, churn date, ARR)
- Identify the specific analysis goal (individual RCA, cohort pattern, or export)
- Note any prior analysis or existing documentation to reference
- Check `~/.claude/plugins/config/claude-for-customer-success/company-profile.md` for company segment and escalation context

**G-code dependency:** All G-code guardrails referenced in this skill (G1–G9) are defined in the CLAUDE.md config loaded above. If Pre-flight halts or config is missing, G-codes are undefined — do not proceed with partial config.
---

## Operations

### Operation: `analyze` — Individual Churn RCA

Performs root cause analysis on a single churned account. Produces a structured RCA document written to `context/rca-[safe_account]-[YYYY-MM-DD].md`.

**Inputs:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `operation` | string | Yes | `"analyze"` |
| `account_name` | string | Yes | Account name |
| `csm_name` | string | Yes | CSM who owned the account |
| `churn_reason` | string | Yes | Customer-stated or CSM-assessed churn reason |
| `churn_date` | string | No | ISO date of confirmed churn (YYYY-MM-DD); defaults to today |
| `account_stage` | string | No | Lifecycle stage at time of churn |
| `contract_value` | string | No | ARR or contract value for impact sizing |
| `tenure_months` | integer | No | Months as customer |
| `ocv_snapshot` | string | No | OCV outcome data — advisory signal for value delivery analysis |
| `early_warning_signals` | list | No | List of pre-churn signals observed |
| `notes` | string | No | CSM freeform notes |

**Scope redirect — check first:**
Before any analysis, scan `churn_reason` and `notes` for contraction signals ("reduce," "downgrade," "fewer seats," "smaller tier"). If found, return the scope redirect message and stop.

**Auto-generated fields (immutable after creation):**
- `rca_id`: `RCA-[ACCT]-[YYYYMMDD]-[SEQ]`
  - `ACCT`: first 4 alphabetic characters of `account_name`, uppercased, non-alpha stripped
  - `SEQ`: 3-digit sequence starting at `001`; scan `context/rca-[safe_account]-*.md` for the same date and increment from the highest found
- `created_at`: ISO datetime of operation
- `created_by`: session user

**safe_account derivation (for file path only):**
1. Lowercase `account_name`
2. Replace all non-alphanumeric characters with `-`
3. Collapse consecutive hyphens to a single hyphen
4. Trim to 30 characters maximum

**Output file:** `context/rca-[safe_account]-[YYYY-MM-DD].md`

**Output structure:**

```markdown
---
rca_id: [RCA-ID]
account_name: [account_name]
churn_date: [churn_date]
csm_name: [csm_name]
created_at: [ISO datetime]
created_by: [session user]
---

## Churn RCA: [Account Name]
### RCA ID: [RCA-ID]
### Churn Date: [date]
### Contract Value: [if provided; omit section if not]

## Root Cause Classification
### Primary Root Cause: [taxonomy category from the 7-category taxonomy]
### Contributing Factors: [list of secondary factors from available signals]
### Value Chain Position: [where in the value delivery chain the failure occurred]

## Timeline Reconstruction
[Key events and signals leading to churn, synthesized from: early_warning_signals,
account_stage, tenure_months, churn_date, and churn_reason. State assumptions when
fields are absent.]

## OCV Delivery Analysis
[If ocv_snapshot provided: analysis of outcome delivery status and gaps correlated
with churn timing. If not provided: omit this section entirely.]

## Remediation Pathway
### Preventable: [Yes / Possibly / No]
### Primary Prevention Lever: [what should have been done differently]
### Systemic Recommendation: [pattern recommendation for future accounts at similar stage/profile]

## Win-Back Assessment
### Win-Back Viability: [High / Medium / Low / Not viable]
### Recommended Timing: [when to re-engage]
### Win-Back Approach: [summary of recommended approach]
```

---

### Operation: `cohort` — Cohort Churn Pattern Analysis

Analyzes a batch of churn events for pattern identification and systemic root cause. Writes to `context/rca-cohort-[YYYYMMDD]-[SEQ].md`.

**Inputs:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `operation` | string | Yes | `"cohort"` |
| `cohort_name` | string | Yes | Descriptive name (e.g., "Q1-2026 Enterprise Churn") |
| `csm_name` | string | Yes | CSM or analyst running the cohort analysis |
| `rca_ids` | list | No | List of existing RCA IDs to include (prior individual RCAs) |
| `churn_events` | list | No | Inline churn event objects: `{account_name, churn_reason, churn_date, contract_value, account_stage}` — for events without prior individual RCAs |
| `analysis_period` | string | No | ISO date range `YYYY-MM-DD/YYYY-MM-DD` |
| `portfolio_size` | integer | No | Total accounts in the defined portfolio. Must be a positive integer > 0 |
| `notes` | string | No | Additional context |

**Validation — enforce before any analysis or file write:**

portfolio_size = 0 or negative:
```
Validation error: portfolio_size must be a positive integer greater than zero. Received: [value]. Provide the total number of accounts in the defined portfolio.
```

**Churn rate calculation (when portfolio_size provided):**
```
churn_rate = count(churn_events + rca_ids) / portfolio_size × 100
systemic_threshold_met = churn_rate >= 25.0
```

**Auto-generated fields (immutable after creation):**
- `cohort_id`: `RCA-COHORT-[YYYYMMDD]-[SEQ]`
  - `SEQ`: 3-digit sequence; scan `context/rca-cohort-*.md` for the same date and increment from highest found; default `001`
- `created_at`: ISO datetime
- `created_by`: session user

**Output file:** `context/rca-cohort-[YYYYMMDD]-[SEQ].md`

**Output structure:**

```markdown
---
cohort_id: [cohort_id]
cohort_name: [cohort_name]
portfolio_size: [N or "not provided"]
churn_rate: [X.X% or "not calculated — portfolio_size not provided"]
analysis_period: [period or "not specified"]
created_at: [ISO datetime]
created_by: [session user]
---

## Cohort Churn Analysis: [cohort_name]
### Cohort ID: [cohort_id]
### Analysis Period: [period]
### Churn Rate: [N/portfolio_size]% [⚠ Above threshold — systemic pattern] if >= 25%

## Pattern Analysis
### Primary Churn Drivers (ranked by frequency)
| Driver Category | Count | % of Cohort |
|----------------|-------|-------------|
| [category]     | [N]   | [%]         |

### Common Contributing Factors
[Cross-account themes identified from churn_reason signals]

### Lifecycle Stage Concentration
[Which stages have highest churn concentration; any stage-specific patterns]

## Systemic Recommendations
[Portfolio-level interventions based on pattern analysis. Produced for all cohorts;
escalation intensity increases when churn_rate >= 25%.]
[If churn_rate >= 25%: prefix section with ⚠ and address to CS Leadership and Product.]
```

---

### Operation: `export`

Retrieves and formats an existing RCA or cohort record for external use. Does not write to the filesystem — content returned in response only.

**Inputs:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `operation` | string | Yes | `"export"` |
| `rca_id` | string | No | Single RCA ID to export |
| `cohort_id` | string | No | Cohort ID to export |
| `format` | string | No | `"markdown"` (default) or `"summary"` |

**Validation:**
- At least one of `rca_id` or `cohort_id` must be provided:
  ```
  Export error: At least one of rca_id or cohort_id is required.
  ```

**Not-found errors:**
```
Export error: RCA record not found for rca_id [rca_id]. Verify the ID is correct and confirm the rca operation completed successfully.
```
```
Export error: RCA record not found for cohort_id [cohort_id]. Verify the ID is correct and confirm the cohort operation completed successfully.
```

**Locate source file:** Scan `context/rca-*` for a file whose frontmatter `rca_id` or `cohort_id` matches the provided value. The identifier is a match predicate against file frontmatter — never interpolated into a file path.

**Format behavior:**
- `markdown` (default): return the full document as written
- `summary`: return only the Root Cause Classification, Remediation Pathway, and Win-Back Assessment sections (or the Pattern Analysis and Systemic Recommendations for cohorts)

---

## Output Format

**Individual RCA file naming:**
```
context/rca-[safe_account]-[YYYY-MM-DD].md
```
Examples:
- `context/rca-acme-corp-2026-05-17.md`
- `context/rca-meridian-health-2026-05-01.md`

**Cohort RCA file naming:**
```
context/rca-cohort-[YYYYMMDD]-[SEQ].md
```
Examples:
- `context/rca-cohort-20260517-001.md`
- `context/rca-cohort-20260517-002.md`

**Auto-ID examples:**
- Individual: `RCA-ACME-20260517-001`, `RCA-MERI-20260501-001`
- Cohort: `RCA-COHORT-20260517-001`

**Date in filename:** Date of the operation (creation date). Never updated.

**YAML frontmatter fields — individual RCA:**
```yaml
rca_id: [RCA-ID]
account_name: [verbatim from input]
churn_date: [YYYY-MM-DD]
csm_name: [verbatim from input]
created_at: [ISO datetime]
created_by: [session user email]
```

**YAML frontmatter fields — cohort RCA:**
```yaml
cohort_id: [RCA-COHORT-ID]
cohort_name: [verbatim from input]
portfolio_size: [integer or "not provided"]
churn_rate: [decimal or "not calculated"]
analysis_period: [range or "not specified"]
created_at: [ISO datetime]
created_by: [session user email]
```

**Export output:** Returned in response only. No file written.

---

## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of churn analysis request is this?
   - **Individual RCA** (`analyze`): Single churned account — root cause taxonomy, timeline reconstruction, win-back assessment.
   - **Cohort Pattern Analysis** (`cohort`): Multi-account batch — systemic driver identification, frequency ranking, portfolio-level escalation if churn rate ≥ 25%.
   - **Export** (`export`): Retrieval and formatting of an existing RCA or cohort record for stakeholder distribution.

2. **CONSTRAINTS**: What limits the solution space?
   - G4: Escalation guidance must reference the configured escalation matrix — no generic "escalate to leadership."
   - G5: RCA files containing ARR, health data, and stakeholder details are internal-only — confirm recipient authorization before distribution.
   - Never assign root cause without named evidence; never treat stated close reason as root cause without corroboration.

3. **EXPERT CHECK**: What would a veteran CS analyst verify first?
   - Is the root cause assignment based on the earliest signal in the timeline, or the most recent/dramatic one?
   - Does the cohort frequency table rank by count descending? Are systemic recommendations scaled to the churn rate severity?

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Accepting the stated churn reason as root cause without independent corroboration — stated reasons and actual root causes diverge frequently.
   - Assigning root cause to the last signal before churn rather than the first — recency bias is the most common analytical error.
   - Including force majeure losses in process-improvement conclusions — uncontrollable losses should not drive response process changes.
   - Generating portfolio escalation from a cohort without validating the churn_rate calculation against portfolio_size.
   - Running export without validating the ID against frontmatter — never interpolate IDs into file paths.

**After execution**, verify:
- Does the root cause assignment cite specific, named evidence?
- Is the cohort churn rate calculation correct (count / portfolio_size × 100)?
- Are escalation references specific (owner, channel, SLA) — not generic?
- Confidence: [High] when data is complete and multi-signal / [Medium] when partial data available / [Low] if single-signal or inferred

---

Execute in this order for each operation:

**For `analyze`:**
1. Check `churn_reason` and `notes` for contraction signals — if found, return scope redirect and stop
2. Derive `safe_account` from `account_name` (lowercase → replace non-alphanumeric with `-` → collapse hyphens → trim to 30 chars)
3. Derive `churn_date`: use provided value or today's date in ISO format
4. Classify primary root cause from `churn_reason` using the 7-category taxonomy in `reference/churn-rca-taxonomy.md` — load on demand
5. Identify contributing factors from secondary signals in `churn_reason`, `early_warning_signals`, `notes`, and `ocv_snapshot`
6. Reconstruct timeline from `early_warning_signals`, `account_stage`, `tenure_months`, and `churn_date`; state assumptions for absent fields
7. Render OCV Delivery Analysis only if `ocv_snapshot` is provided; omit the section entirely if not
8. Assess win-back viability per root cause category using `reference/remediation-playbook.md` — load on demand
9. Derive `rca_id`: scan `context/rca-[safe_account]-*.md` for same date; set SEQ to highest found + 1, defaulting to `001`
10. Write the RCA file to `context/rca-[safe_account]-[churn_date].md`

**For `cohort`:**
1. Validate `portfolio_size` > 0 if provided; return validation error and stop if zero or negative
2. Collect all churn events: combine inline `churn_events` entries with any `rca_ids` references
3. Calculate `churn_rate` if `portfolio_size` provided: `count(events) / portfolio_size × 100`; flag systemic pattern if `churn_rate >= 25.0`
4. Load `reference/churn-rca-taxonomy.md` — classify each event's primary root cause
5. Build frequency table: rank drivers by count descending; alpha-sort ties
6. Identify cross-account themes from signal language in `churn_reason` fields
7. Identify lifecycle stage concentration from `account_stage` fields
8. Load `reference/cohort-analysis-framework.md` for pattern interpretation guidance — load on demand
9. Generate systemic recommendations scaled to churn rate severity; use `reference/remediation-playbook.md` — load on demand
10. Derive `cohort_id`: scan `context/rca-cohort-*.md` for same date; set SEQ to highest found + 1, defaulting to `001`
11. Write cohort file to `context/rca-cohort-[YYYYMMDD]-[SEQ].md`

**For `export`:**
1. Validate that at least one of `rca_id` or `cohort_id` is provided; return error if neither
2. Scan `context/rca-*` for a file whose frontmatter `rca_id` or `cohort_id` matches the provided value
3. If not found, return the not-found error message; stop
4. Apply format: `markdown` = return full document; `summary` = return key sections only
5. Return content in response; do not write any file

---

## Security & Permissions

- **Network access:** none
- **Filesystem read scope:** `context/rca-*` only
- **Filesystem write scope:** `context/rca-*` only (individual and cohort RCA files)
- **Subprocess execution:** none
- **Dynamic code execution:** none
- **External API calls:** none
- **Export operation:** no filesystem write — content returned in response only
- **OCV data:** read from `ocv_snapshot` input parameter only; skill never reads OCV data from the filesystem

---

## Trust & Verification

**Input sanitization:**
- `account_name` sanitized to `safe_account` (lowercase, alphanumeric + hyphens only, max 30 chars) for all filesystem path construction
- `safe_account` is derived once and used for both the filename and the `rca_id` ACCT segment
- Display names (unsanitized `account_name`) used only in document body output — never in path construction
- `churn_reason`, `notes`, `ocv_snapshot`, and all free-text fields stored verbatim in document body — never executed, interpolated into skill logic, or used in path construction

**Validation — portfolio_size:**
- Must be a positive integer greater than zero
- If `portfolio_size = 0` or negative:
  ```
  Validation error: portfolio_size must be a positive integer greater than zero. Received: [value]. Provide the total number of accounts in the defined portfolio.
  ```

**Immutable fields — locked at creation; no update operation exists:**
- Individual: `rca_id`, `created_at`, `created_by`, `account_name`, `churn_date`
- Cohort: `cohort_id`, `created_at`, `created_by`, `cohort_name`, `churn_rate`
- If revised analysis is needed, initiate a new operation — a new ID is generated

**Root cause taxonomy validation:**
- Primary root cause must be one of the 7 taxonomy categories defined in `reference/churn-rca-taxonomy.md`
- If `churn_reason` is ambiguous, apply the classification heuristics in the taxonomy file; document the rationale

**Export ID resolution:**
- File scan against `context/rca-*` for matching frontmatter value — the ID is a match predicate, never a path component
- If not found: return the not-found error message verbatim

**Display-only fields:**
- `ocv_snapshot` content and all free-text inputs are display-only — they inform the analysis narrative but are never used in logic, path construction, or calculation

---

## Reference Files

The following reference files are loaded on-demand. They are not front-loaded.

| File | Purpose |
|------|---------|
| `reference/reasoning-blueprint.md` | Reasoning framework for this skill — D1 cognitive stance, constraints, and expert orientation |
| `reference/churn-rca-taxonomy.md` | 7-category root cause taxonomy with definitions, signal vocabulary, classification heuristics, value chain position mapping, and win-back viability assessment rules per category |
| `reference/cohort-analysis-framework.md` | Cohort construction methods, pattern identification algorithm, churn rate threshold logic, lifecycle stage concentration analysis, systemic recommendation generation, and portfolio_size validation |
| `reference/remediation-playbook.md` | Prevention lever per root cause category, systemic recommendation templates, win-back timing guidance and approach templates per root cause, and escalation guidance |

Load `reference/churn-rca-taxonomy.md` when classifying root causes during `analyze` or `cohort`.
Load `reference/cohort-analysis-framework.md` when executing `cohort` pattern analysis.
Load `reference/remediation-playbook.md` when generating remediation recommendations or win-back assessments.

---

## Examples

### Example 1 — Individual Analyze

**Input:**
```json
{
  "operation": "analyze",
  "account_name": "Meridian Health",
  "csm_name": "Sarah Chen",
  "churn_reason": "The product never integrated with their EHR system. IT gave up after 4 months of failed attempts. Exec sponsor left and no champion replaced her.",
  "churn_date": "2026-05-01",
  "account_stage": "adoption",
  "contract_value": "$48,000 ARR",
  "tenure_months": 8,
  "ocv_snapshot": "3 of 5 target outcomes partially met; integration milestone never completed; last active session 2026-03-15",
  "early_warning_signals": ["no login activity for 45 days", "IT escalation ticket opened 2026-02-01", "champion Sarah Torres promoted to new division 2026-03-01"]
}
```

**Behavior:**
- No contraction signals in `churn_reason` — proceed
- `safe_account`: `meridian-health`
- `rca_id`: `RCA-MERI-20260501-001`
- Output file: `context/rca-meridian-health-2026-05-01.md`
- Primary root cause: `product_fit_failure` (integration failure as dominant signal)
- Contributing factors: `champion_departure` (exec sponsor left, no replacement)
- OCV Delivery Analysis rendered: integration milestone never completed; 3/5 outcomes stalled
- Timeline: IT escalation at month 6, champion departure at month 7, activity gap last 45 days
- Win-Back Viability: Medium — contingent on integration resolution and new champion identification
- Preventable: Possibly — integration validation gate at 30 days would have surfaced the blocker earlier

---

### Example 2 — Cohort Analysis (Systemic Threshold Met)

**Input:**
```json
{
  "operation": "cohort",
  "cohort_name": "Q1-2026 Enterprise Churn",
  "csm_name": "Tom Liu",
  "churn_events": [
    {"account_name": "Acme Corp", "churn_reason": "ROI not demonstrated to CFO", "churn_date": "2026-01-15", "account_stage": "renewal"},
    {"account_name": "Beta Solutions", "churn_reason": "Value unclear after renewal conversation", "churn_date": "2026-02-01", "account_stage": "renewal"},
    {"account_name": "Gamma Industries", "churn_reason": "Could not show business impact to board", "churn_date": "2026-03-10", "account_stage": "maturity"}
  ],
  "portfolio_size": 10,
  "analysis_period": "2026-01-01/2026-03-31"
}
```

**Behavior:**
- `portfolio_size = 10` — positive integer, validation passes
- 3 events collected from `churn_events`
- `churn_rate = 3 / 10 × 100 = 30.0%`
- `systemic_threshold_met = true` (30.0% >= 25.0%)
- `cohort_id`: `RCA-COHORT-20260517-001`
- Output file: `context/rca-cohort-20260517-001.md`
- Primary driver: `value_not_realized` (all 3 accounts: ROI articulation failure at renewal stage)
- Stage concentration: 2/3 at renewal stage — value story not built before renewal conversation
- Systemic recommendations prefixed with ⚠, addressed to CS Leadership and Product
- Recommendation: implement 60-day pre-renewal value review as standard; build ROI case study library
