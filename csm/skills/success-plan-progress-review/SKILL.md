---
name: success-plan-progress-review
description: "Reviews an existing success plan canvas and generates a structured progress review artifact with milestone scorecard, OCV outcome ratings, CSM action list, and optional customer-facing summary and QBR pre-work note."
version: "1.0.0"
metadata:
  author: "todd@successhacker.co"
  tags: "csm success-plan progress-review customer-success"
deployment_target: plugin
---

# /csm:success-plan-progress-review

[PROPOSED]

## Overview

`csm:success-plan-progress-review` generates a structured progress review artifact by reading an upstream success plan canvas and incorporating milestone and OCV updates provided by the CSM.

## Use When

- A CSM needs to generate a structured progress review against an existing success plan canvas
- Reviewing milestone status (On Track / At Risk / Missed) for a customer account
- Assessing OCV outcome progress (Delivered / In Progress / Not Started / Blocked)
- Evaluating success criteria met/not-met status against plan targets
- Preparing for a QBR and need a pre-work note or customer-facing summary
- Capturing a point-in-time progress snapshot for an account

## Do NOT Use For

- Generating or modifying success plan canvases — use `csm:success-plan-canvas [operation=generate]`
- Sending or drafting customer communications — use `csm:customer-comms`
- Health score calculation or portfolio-level reporting — use `rev-ops:portfolio-health-report`
- Automated milestone detection — the CSM provides milestone updates explicitly
- Writing to OCV files — this skill is read-only with respect to canvas and OCV files

## Typical Activation
"/csm:success-plan-progress-review Acme Corp"
"How is [account] tracking against their success plan?"
"Review progress on [customer]'s goals"
"Pull the success plan progress for [account] before my QBR"

**Inter-skill contract:**

```
csm:success-plan-canvas [operation=generate or refresh]
        ↓  emits context/success-plan-[safe_account]-[YYYY-MM-DD].md
csm:success-plan-progress-review [operation=review]
        ↓  reads canvas file → emits context/progress-review-[safe_account]-[YYYY-MM-DD].md
```

This skill is the downstream consumer. The upstream canvas must exist before a review can be generated.

---

## Operations

### operation: review

Reviews an existing success plan canvas and produces a dated progress review document.

**Upstream canvas file resolution:**

The skill locates the canvas at `context/success-plan-[safe_account]-[canvas_date].md`. If `canvas_date` is not provided, the skill scans for the most recent canvas file for the account using the `safe_account`-derived filename prefix.

If no canvas file is found, the skill returns the following error and produces no partial output:

```
Error: No success plan canvas found for [account_name].
Expected file: context/success-plan-[safe_account]-[YYYY-MM-DD].md
Run csm:success-plan-canvas [operation=generate] first.
```

**Inputs:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `operation` | string | Yes | Must be `"review"` |
| `account_name` | string | Yes | Account name — used to locate upstream canvas file and derive `safe_account` |
| `csm_name` | string | Yes | Name of CSM conducting the review — display-only |
| `review_date` | string | No | ISO date of review (defaults to today if not provided) |
| `canvas_date` | string | No | ISO date of canvas to review against (defaults to most recent canvas for account) |
| `milestone_updates` | list | Yes | List of milestone objects: `{milestone_name, status, notes}` where `status` is one of `On Track`, `At Risk`, `Missed` |
| `ocv_updates` | list | No | List of OCV outcome objects: `{outcome_name, status, notes}` where `status` is one of `Delivered`, `In Progress`, `Not Started`, `Blocked` |
| `key_benefits_realized` | list | No | CSM-provided list of concrete benefits the customer has already realized since the plan was created. When provided, rendered as a subsection of the Progress Scorecard and optionally surfaced in the customer-facing summary |
| `success_criteria_status` | list | No | List of success criteria assessment objects: `{criterion, met, notes}` where `met` is boolean. When provided, adds a Success Criteria Evaluation section |
| `include_customer_summary` | boolean | No | Default: `false`. When `true`, generates a customer-facing summary section using templates from `reference/customer-summary-templates.md` |
| `include_qbr_note` | boolean | No | Default: `false`. When `true`, generates a QBR pre-work note section |
| `notes` | string | No | CSM freeform notes — appended to the review document as display-only text |

**`safe_account` derivation:**

`account_name` → lowercase → replace all non-alphanumeric characters with `-` → collapse consecutive hyphens to a single `-` → trim to 30 characters.

Examples:
- `"Acme Corp"` → `acme-corp`
- `"TechCo, Inc."` → `techco-inc`
- `"Global Health & Wellness Partners"` → `global-health-wellness-partners`

**Auto-ID generation:**

Format: `REVIEW-[ACCT]-[YYYYMMDD]`

- `ACCT`: first 4 alphabetic characters of `account_name`, uppercased, non-alpha characters stripped before extraction
  - `"Acme Corp"` → `ACME`
  - `"TechCo"` → `TECH`
  - `"123 Systems"` → `SYST`
- `YYYYMMDD`: review date

Example: `REVIEW-ACME-20260517`

**Output artifact structure:**

The review document contains up to 7 structured sections. Three are always present; four are conditional:

| Section | Always Present | Condition |
|---------|---------------|-----------|
| Progress Scorecard | Yes | Always; includes `### Key Benefits Already Realized` subsection when `key_benefits_realized` is provided |
| OCV Outcome Status | No | `ocv_updates` list provided and non-empty |
| Success Criteria Evaluation | No | `success_criteria_status` list provided |
| CSM Action List | Yes | Always (may note "No actions required — all milestones On Track" if applicable) |
| Customer-Facing Summary | No | `include_customer_summary: true`; includes benefits realized when `key_benefits_realized` provided |
| QBR Pre-Work Note | No | `include_qbr_note: true` |
| Notes | Yes | Always (rendered as empty section if no `notes` provided) |

Section assembly order in the output file is fixed: Progress Scorecard → OCV Outcome Status → Success Criteria Evaluation → CSM Action List → Customer-Facing Summary → QBR Pre-Work Note → Notes.

**Console summary returned after successful execution:**

```
Review generated.
  review_id:     REVIEW-[ACCT]-[YYYYMMDD]
  account:       [account_name]
  csm:           [csm_name]
  review_date:   [review_date]
  canvas_ref:    [plan_id from canvas frontmatter]
  at_risk:       [n]
  missed:        [n]
  file:          context/progress-review-[safe_account]-[YYYY-MM-DD].md
```

**Output file naming pattern:**

```
context/progress-review-[safe_account]-[YYYY-MM-DD].md
```

Multiple reviews on the same date for the same account overwrite the prior file (no versioning in v1.0.0).

---

## Output Format

**YAML frontmatter fields in the output file:**

```yaml
---
review_id: REVIEW-ACME-20260517
account_name: Acme Corp
canvas_reference: context/success-plan-acme-corp-2026-05-17.md
plan_id: CANVAS-ACME-20260517
review_date: 2026-05-17
csm_name: Jane Smith
created_at: 2026-05-17T14:00:00Z
created_by: todd@successhacker.co
milestone_summary:
  on_track: 3
  at_risk: 1
  missed: 0
includes_key_benefits_realized: true
includes_success_criteria_evaluation: false
includes_customer_summary: false
includes_qbr_note: true
---
```

**Immutable fields (set at creation; not modified in subsequent operations):**

| Field | Reason |
|-------|--------|
| `review_id` | Identity key |
| `created_at` | Audit timestamp |
| `created_by` | Audit identity |
| `canvas_reference` | Source artifact reference — must match upstream canvas used at review time |
| `account_name` | Account identity |

**Document body header:**

```markdown
# Progress Review: [account_name] — [review_date]

**CSM:** [csm_name]
**Review Date:** [review_date]
**Canvas Reference:** [plan_id]

---
```

**Progress Scorecard section format:**

```markdown
## Progress Scorecard

| Milestone | Status | Notes |
|-----------|--------|-------|
| [milestone_name] | On Track / At Risk / Missed | [notes] |

### Key Benefits Already Realized

(Conditional — present when key_benefits_realized provided)

- [benefit 1]
- [benefit 2]
```

**OCV Outcome Status section format (conditional):**

```markdown
## OCV Outcome Status

| Outcome | Status | Notes |
|---------|--------|-------|
| [outcome_name] | Delivered / In Progress / Not Started / Blocked | [notes] |
```

**Success Criteria Evaluation section format (conditional):**

```markdown
## Success Criteria Evaluation

| Criterion | Met | Notes |
|-----------|-----|-------|
| [criterion] | Yes / No | [notes] |
```

**CSM Action List section format:**

```markdown
## CSM Action List

(Actions generated from At Risk and Missed milestones per milestone-rating-guide.md)

| Milestone | Status | Recommended Action |
|-----------|--------|--------------------|
| [milestone_name] | At Risk / Missed | [action] |

(When all milestones are On Track: "No immediate actions required — continue monitoring.")
```

**Customer-Facing Summary section format (conditional):**

```markdown
## Customer-Facing Summary

(Tone determined by milestone mix per customer-summary-templates.md)

[Customer-facing narrative paragraph(s)]

**Key Benefits Realized** (conditional — when key_benefits_realized provided)

[Benefits realized in customer-facing language]
```

**QBR Pre-Work Note section format (conditional):**

```markdown
## QBR Pre-Work Note

**Milestone Summary:** [on_track] on track, [at_risk] at risk, [missed] missed
**Key Wins:** [list]
**Open Risks:** [list]
**Suggested Discussion Agenda:**
- [item]
```

**Notes section format:**

```markdown
## Notes

[CSM freeform notes, or empty]
```

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md` and
`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/csm:cold-start-interview`.

Note from config:
- CS motion — shapes how directive vs. collaborative the progress review framing is
- Health model — provides context for milestone status interpretation and escalation thresholds
- Escalation matrix — required if milestone ratings trigger escalation routing
- Integrations — determines which data sources are available for canvas and OCV resolution

**`context/` path resolution:** Inter-skill artifacts (`context/success-plan-*` and `context/progress-review-*`) resolve relative to the session working directory at runtime. In a Claude Code plugin deployment, this is the directory from which Claude Code is launched. Both this skill and `csm:success-plan-canvas` must operate from the same working directory for the inter-skill contract to hold.

**G-code dependency:** All G-code guardrails referenced in this skill (G1–G9) are defined in the CLAUDE.md config loaded above. If Pre-flight halts or config is missing, G-codes are undefined — do not proceed with partial config.
---

## Reasoning Protocol

> Blueprint: `references/reasoning-blueprint.md` (on-demand only)

Before generating output, apply these primers:

1. **CLASSIFY** — Determine operation validity and data completeness before proceeding:
   - Is `operation` present and equal to `"review"`? If absent or any other value → return an error and halt before any output.
   - Is `account_name` non-empty? If not → reject immediately with a clear error; do not attempt canvas resolution.
   - Does an upstream canvas file exist for this account (located via `canvas_date` or most-recent scan)? If not → return the canonical canvas-not-found error and halt; produce no partial output.
   - Are `milestone_updates` provided and non-empty? If absent → halt with a missing-required-input error; the progress scorecard cannot be generated without milestone data.
   - CLASSIFY is complete when: operation confirmed as `"review"`, `account_name` validated, canvas file located and readable, `milestone_updates` present.

2. **CONSTRAINTS** — Apply before generating any output (blocking before non-blocking):
   - **C-1 BLOCKING**: `account_name` must be non-empty — reject all operations if absent; `safe_account` derivation cannot proceed.
   - **C-2 BLOCKING**: Canvas file must exist for the target account before any review output is generated — return the canonical error message exactly as specified; do not generate partial output.
   - **C-3 BLOCKING**: `milestone_updates` must be provided and non-empty — the Progress Scorecard is always-present and cannot be built without milestone data.
   - **C-4 BLOCKING**: Each `milestone_updates[].status` value must be one of `On Track`, `At Risk`, `Missed` — halt with a validation error on any invalid value; do not process the remaining list.
   - **C-5 BLOCKING**: Each `ocv_updates[].status` value (when provided) must be one of `Delivered`, `In Progress`, `Not Started`, `Blocked` — halt with a validation error on any invalid value.
   - **C-6 Non-blocking**: `safe_account` derivation (lowercase → replace non-alphanumeric with `-` → collapse hyphens → trim to 30 chars) must be applied before any file path construction — never use raw `account_name` in a path.
   - **C-7 Non-blocking**: Canvas content is read-only; this skill never writes to canvas files or OCV files under any condition — write scope is `context/progress-review-*` only.
   - G5: Internal data (health scores, ARR, expansion signals) must never appear in customer-facing output
   - G7: Flag any data older than 30 days with source date and staleness indicator

3. **EXPERT CHECK** — What a veteran CSM verifies before generating a progress review:
   - Do the `milestone_updates` statuses reflect the current state rather than the planned state? A CSM who copies milestone names from the canvas without providing actual status assessments produces a review that adds no signal. Flag if all milestones are listed as `On Track` with no notes — this pattern often signals incomplete input rather than genuine account health.
   - For `At Risk` milestones: does each entry include a `notes` field with a specific reason? A bare `At Risk` status without a root cause observation produces a CSM Action List with generic recommendations — flag for input enrichment.
   - For `Missed` milestones: has the escalation threshold check (Step 8, `reference/milestone-rating-guide.md` § 2) been applied? A missed milestone on a high-ARR account or near-renewal account may trigger escalation — this check must not be skipped.
   - If `include_customer_summary: true`: does the milestone mix support the tone selected from the template? A cautionary summary generated from an all-`On Track` milestone set is misaligned — verify tone selection against the actual milestone_summary counts.
   - If `include_qbr_note: true`: are `key_benefits_realized` entries present? A QBR Pre-Work Note without Key Wins forces the template to fall back to `On Track` milestones — this produces weaker pre-work material; prompt the CSM to provide explicit benefits if absent.

4. **ANTI-PATTERNS** — Mistakes to catch before generating output:
   - **AP-1 Partial output on canvas-not-found**: beginning any section generation before the canvas file has been confirmed readable — the error path must halt all output, not produce a partial review with a warning appended.
   - **AP-2 Invalid status values silently coerced**: accepting a `milestone_updates[].status` of `"Delayed"` or `"Complete"` and mapping it to a valid enum value — invalid values must surface as validation errors, not be silently normalized.
   - **AP-3 Customer-facing summary with internal language**: allowing health tier labels (`Red`, `Yellow`, `Green`), escalation routing details, ARR values, or internal action items to appear in the Customer-Facing Summary section — customer output is firewalled from internal language.
   - **AP-4 Notes field overwrite**: if a prior review file exists for the same account and date, overwriting prior notes without surfacing the conflict — v1.0.0 behavior is overwrite, but the CSM should be aware.
   - **AP-5 QBR note without risk acknowledgment**: generating a QBR Pre-Work Note that lists only Key Wins when At Risk or Missed milestones are present — the Open Risks section must reflect the milestone mix, not be omitted for tone reasons.

**After execution**, verify:
- Does the output file contain all required sections in fixed order (Progress Scorecard → OCV Outcome Status → Success Criteria Evaluation → CSM Action List → Customer-Facing Summary → QBR Pre-Work Note → Notes)? Are conditional sections present only when their conditions were met?
- Is the YAML frontmatter complete? Are `review_id`, `canvas_reference`, `plan_id`, `milestone_summary` counts, and all `includes_*` boolean flags correctly populated?
- For any `At Risk` or `Missed` milestones: does the CSM Action List contain specific actions (not generic "monitor closely" entries)?
- Is the `safe_account` derivation applied correctly in the output file path? Does `canvas_reference` point to the exact canvas file that was read?
- Is the customer-facing language firewall intact? No health scores, escalation identifiers, ARR values, or internal routing language in the Customer-Facing Summary or QBR Pre-Work Note.
- Confidence: [High] if canvas file confirmed readable with complete frontmatter, all milestone statuses are valid enum values, and `milestone_updates` entries include notes / [Medium] if canvas file located but some frontmatter fields missing, or milestone entries lack notes for At Risk/Missed statuses / [Low] if canvas file not found and operating on CSM-provided description only, or if `milestone_updates` statuses are unvalidated — state which.

Execute the following steps in order for every `review` operation. Do not skip steps or reorder them.

**Step 1 — Resolve `safe_account`**

Derive `safe_account` from `account_name`: lowercase → replace all non-alphanumeric characters with `-` → collapse consecutive hyphens → trim leading/trailing hyphens → truncate to 30 characters. Store as the path-construction token. The original `account_name` is `display_account` — used only in document content.

**Step 2 — Locate upstream canvas file**

If `canvas_date` is provided, attempt to read `context/success-plan-[safe_account]-[canvas_date].md`. If `canvas_date` is not provided, scan `context/success-plan-[safe_account]-*.md` for the most recent file by date suffix. If no matching canvas file is found, return the error message exactly as specified and halt — produce no partial output:

```
Error: No success plan canvas found for [account_name].
Expected file: context/success-plan-[safe_account]-[YYYY-MM-DD].md
Run csm:success-plan-canvas [operation=generate] first.
```

**Step 3 — Read canvas frontmatter**

From the located canvas file, extract: `plan_id`, `plan_type`, `csm_name` (if `csm_name` input is not provided), and `account_stage`. These values populate the review document frontmatter and inform section structure expectations based on `plan_type` (initial vs expansion vs renewal-refresh).

**Step 4 — Generate `review_id`**

Format: `REVIEW-[ACCT]-[YYYYMMDD]`. Derive `ACCT`: strip all non-alphabetic characters from `account_name`, take the first 4 characters, uppercase. Derive `YYYYMMDD` from `review_date` (or today if not provided) with hyphens removed.

**Step 5 — Build Progress Scorecard**

Iterate `milestone_updates`. Validate each `status` value against the allowed enum (`On Track`, `At Risk`, `Missed`); halt with validation error on any invalid value. Count on_track, at_risk, and missed totals for `milestone_summary`. Render the milestone status table. If `key_benefits_realized` is provided and non-empty, append the `### Key Benefits Already Realized` subsection and set `includes_key_benefits_realized: true`.

**Step 6 — Build OCV Outcome Status section (conditional)**

If `ocv_updates` is provided and non-empty, validate each `status` value against the OCV enum (`Delivered`, `In Progress`, `Not Started`, `Blocked`). Render the OCV outcome status table. If `ocv_updates` is absent or an empty list, omit this section entirely.

**Step 7 — Build Success Criteria Evaluation section (conditional)**

If `success_criteria_status` is provided, render the success criteria table with `met` displayed as `Yes` / `No`. Set `includes_success_criteria_evaluation: true`. Apply evaluation logic from `reference/milestone-rating-guide.md` § 4 — flag unmet criteria with no corresponding At Risk or Missed milestone for additional CSM action items.

**Step 8 — Build CSM Action List**

Apply action generation logic from `references/milestone-rating-guide.md` § 3. For each `At Risk` milestone, generate investigation and intervention actions. For each `Missed` milestone, generate recovery and escalation actions. Apply escalation threshold logic from § 2. If all milestones are `On Track`, render: "No immediate actions required — continue standard monitoring cadence."

**Step 9 — Build Customer-Facing Summary (conditional)**

If `include_customer_summary: true`, select the appropriate tone template from `reference/customer-summary-templates.md` based on the milestone mix (positive / cautionary / escalation). Incorporate `key_benefits_realized` using customer-facing language guidance from that file. Set `includes_customer_summary: true`.

**Step 10 — Build QBR Pre-Work Note (conditional)**

If `include_qbr_note: true`, generate the QBR Pre-Work Note using the template from `reference/customer-summary-templates.md` § 5. Populate Key Wins from `key_benefits_realized` (or On Track milestones if key_benefits_realized is absent). Populate Open Risks from At Risk and Missed milestones. Set `includes_qbr_note: true`.

**Step 11 — Assemble and write output file**

Construct the YAML frontmatter block with all required fields. Assemble document sections in fixed order: Progress Scorecard → OCV Outcome Status → Success Criteria Evaluation → CSM Action List → Customer-Facing Summary → QBR Pre-Work Note → Notes. Write the complete document to `context/progress-review-[safe_account]-[review_date].md`. Return the console summary.

---

## Reviewer note

> **⚠️ Reviewer note**
> - **Sources:** [CS Platform ✓ live — usage, milestone data | CS Platform [configured but unverified] | CRM ✓ live — account context | CRM [configured but unverified] | document storage: canvas from [date] | user provided | not connected — conversation context only]
> - **Data as of:** [timestamp per source]
> - **Flagged for your judgment:** [N items marked `[review]` inline | none]
> - **Before sending:** Confirm progress data is current (CS Platform data >30 days old is directional only). Do not share internal health score components in customer-facing progress summary.

---

## Security & Permissions

- **Network access:** none
- **Filesystem read scope:** `context/success-plan-*` (upstream canvas files — read-only); `context/progress-review-*` (own output files — read for conflict detection)
- **Filesystem write scope:** `context/progress-review-*` only
- **Subprocess execution:** none
- **Dynamic code execution:** none

This skill does not read, write, or modify any file outside the `context/` directory. It does not write to canvas files or OCV files under any condition.

---

## Trust & Verification

- `account_name` is sanitized via the `safe_account` function (alphanumeric + hyphen, max 30 chars) for all filesystem path construction. The unsanitized value (`display_account`) is used only in document content — never in path construction.
- `milestone_updates` and `ocv_updates` list items (including `milestone_name`, `outcome_name`, and `notes` fields) are treated as display-only. They are never used in filesystem path construction, logic branching, or code execution.
- `notes` input is treated as display-only freetext. It is rendered into the Notes section of the output document without interpretation.
- `csm_name` is treated as display-only. It is never used in filesystem path construction.
- Canvas content loaded from the upstream file is rendered into the review document as display content. It is never executed, evaluated, or interpolated into skill logic.
- All path construction uses only `safe_account` (derived from `account_name`) and `review_date` (ISO date). No other user input reaches path construction.

---

## Reference Files

The following reference files are loaded on-demand during skill execution:

| File | Purpose | Loaded When |
|------|---------|-------------|
| `references/progress-review-schema.md` | Canonical review record format, YAML frontmatter field definitions, section assembly order, field validation rules, auto-ID generation rules | Every `review` operation |
| `references/milestone-rating-guide.md` | Rating criteria for On Track / At Risk / Missed; escalation thresholds; CSM action generation logic per rating; Success Criteria evaluation logic; Measures of Success assessment; Key Benefits Already Realized guidance | Every `review` operation |
| `references/customer-summary-templates.md` | Customer-facing language templates by milestone status (positive, cautionary, escalation tones); QBR pre-work note structure and language guidance | When `include_customer_summary: true` or `include_qbr_note: true` |
| `references/reasoning-blueprint.md` | Problem classification taxonomy, domain heuristics, common failure modes, and expert judgment patterns for this skill | On-demand per Reasoning Protocol |

---

## Examples

### Example 1 — Basic progress review

```
csm:success-plan-progress-review
  operation: review
  account_name: Acme Corp
  csm_name: Jane Smith
  milestone_updates:
    - milestone_name: "Complete onboarding for 3 admin users"
      status: On Track
      notes: "All 3 admins completed training last week"
    - milestone_name: "Achieve 80% DAU adoption in core module"
      status: At Risk
      notes: "Currently at 52% DAU; adoption stalled in ops team"
    - milestone_name: "Complete integration with Salesforce"
      status: Missed
      notes: "IT resourcing delayed; now targeting Q3"
```

**What this produces:**
- Reads `context/success-plan-acme-corp-[most-recent-date].md`
- Creates `context/progress-review-acme-corp-2026-05-17.md`
- Output includes: Progress Scorecard, CSM Action List, Notes
- Console summary: 1 At Risk, 1 Missed

---

### Example 2 — Full review with OCV updates, success criteria, customer summary, and QBR note

```
csm:success-plan-progress-review
  operation: review
  account_name: Acme Corp
  csm_name: Jane Smith
  review_date: 2026-05-17
  canvas_date: 2026-03-01
  milestone_updates:
    - milestone_name: "Complete onboarding for 3 admin users"
      status: On Track
      notes: "All 3 admins certified"
    - milestone_name: "Achieve 80% DAU adoption in core module"
      status: At Risk
      notes: "52% DAU — ops team lagging"
  ocv_updates:
    - outcome_name: "Reduce manual reporting time by 40%"
      status: In Progress
      notes: "Reporting automation deployed; measuring impact"
    - outcome_name: "Enable real-time pipeline visibility"
      status: Delivered
      notes: "Live dashboards confirmed by VP Sales"
  key_benefits_realized:
    - "Admin team onboarded and self-sufficient — no support tickets in 30 days"
    - "Real-time pipeline dashboard live — VP Sales confirmed visibility improvement"
  success_criteria_status:
    - criterion: "3 admin users certified"
      met: true
      notes: "All 3 completed certification 2026-04-15"
    - criterion: "80% DAU in core module"
      met: false
      notes: "Currently 52%; ops team adoption lagging"
  include_customer_summary: true
  include_qbr_note: true
  notes: "QBR scheduled for 2026-06-01. Ops team adoption is the key risk to address."
```

**What this produces:**
- Reads `context/success-plan-acme-corp-2026-03-01.md` (explicit canvas_date)
- Creates `context/progress-review-acme-corp-2026-05-17.md`
- Output includes all 7 sections: Progress Scorecard (with Key Benefits Already Realized subsection), OCV Outcome Status, Success Criteria Evaluation, CSM Action List, Customer-Facing Summary (with benefits realized), QBR Pre-Work Note, Notes
- Console summary: 1 At Risk, 0 Missed
