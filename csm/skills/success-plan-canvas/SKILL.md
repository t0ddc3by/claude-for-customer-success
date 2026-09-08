---
name: success-plan-canvas
description: "Generates and refreshes structured Customer Success Plan canvas documents for a specific account and lifecycle stage. Supports three plan types: initial onboarding, pre-expansion, and pre-renewal review. OCV-aware: reads Outcome & Value Catalog snapshot data to surface gaps and delivered outcomes."
version: "1.0.0"
metadata:
  author: "todd@successhacker.co"
  tags: "csm success-plan canvas customer-success"
deployment_target: plugin
---

# csm:success-plan-canvas

[PROPOSED]

## Overview

`csm:success-plan-canvas` generates structured Customer Success Plan canvas documents tied to a specific account and lifecycle stage. The canvas is saved as a standalone exportable Markdown artifact and serves as the upstream input to `csm:success-plan-progress-review`.

Three plan types are supported, each producing a distinct document structure:

- **`initial`** — New customer onboarding plan; all 7 CCSM-104 components present; labeled "Initial Success Plan"
- **`expansion`** — Pre-expansion motion; labeled "Expansion Canvas" with explicit expansion framing; distinct from initial plan
- **`renewal-refresh`** — Pre-renewal review; includes OCV gap analysis surfacing committed-but-not-delivered outcomes

## Use When

- The organization uses the OCV (Outcome-to-Customer Value) system and a structured 7-component canvas format is required — if OCV is not in use, use `/csm:success-plan-builder` instead
- A CSM needs to generate a structured success plan canvas for a specific account at a lifecycle stage (initial onboarding, pre-expansion, pre-renewal review)
- An existing canvas needs to be refreshed with updated objectives, OCV data, or notes without generating a new dated artifact

## Do NOT Use For

- Progress tracking or scorecard generation — use `csm:success-plan-progress-review` instead
- Sending customer communications — use `csm:customer-comms` instead
- CRM integration or external system writes
- Multi-account batch generation
- Modifying OCV files (this skill is read-only with respect to OCV data)

## Typical Activation
"/csm:success-plan-canvas Acme Corp" (requires OCV system to be in use)
"/csm:success-plan-canvas Acme Corp --update"
"Create a success plan canvas for [account]" (OCV-aligned 7-component canvas format)
"Update the canvas for [customer]"

---

## Operations

### Operation: `generate`

Creates a new success plan canvas file for an account at a specified lifecycle stage.

**Input fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `operation` | string | Yes | Must be `"generate"` |
| `account_name` | string | Yes | Account name — used for file naming and canvas header |
| `plan_type` | string | Yes | One of: `initial`, `expansion`, `renewal-refresh` |
| `csm_name` | string | Yes | CSM who owns this plan |
| `account_stage` | string | No | Customer lifecycle stage (e.g., Onboarding, Adoption, Expansion, Renewal) |
| `ocv_snapshot` | object | No | Structured OCV data — list of outcomes: `{outcome_name, status, owner}` |
| `key_objectives` | list | No | CSM-provided list of key objectives to feature in the canvas |
| `notes` | string | No | Freeform CSM notes appended to canvas footer |

**Auto-generated fields (set at generate; immutable thereafter):**

- `plan_id`: `CANVAS-[ACCT]-[YYYYMMDD]` — ACCT = first 4 alpha chars of `account_name`, uppercased; non-alpha stripped
- `created_at`: ISO datetime of generation
- `created_by`: session user identity

**safe_account derivation (used for file path only):**
1. Lowercase `account_name`
2. Replace all non-alphanumeric characters with `-`
3. Collapse consecutive hyphens to single hyphen
4. Trim to 30 characters maximum

Examples:
- `"Acme Corp"` → `acme-corp`
- `"123 Widgets Inc."` → `123-widgets-inc-`  (trimmed if over 30 chars)
- `"TechCo Solutions LLC"` → `techco-solutions-llc`

**Plan-type behavior:**

| Plan Type | Document Label | Section Structure | OCV Role |
|-----------|---------------|-------------------|----------|
| `initial` | Initial Success Plan | Goals, Onboarding Milestones, Responsibilities, Success Metrics, Timelines, Risks and Assumptions, Communication Strategy, Next Steps | OCV outcomes listed informally if provided |
| `expansion` | Expansion Canvas | Expansion Rationale, Current Outcomes, Expansion Opportunity, Proposed Outcomes, Responsibilities, Success Metrics, Risks and Assumptions, Communication Strategy, Next Steps | OCV outcomes mapped to expansion thesis |
| `renewal-refresh` | Renewal-Refresh Plan | Renewal Context, OCV Gap Analysis, Delivered Outcomes, At-Risk Outcomes, Renewal Objectives, Responsibilities, Communication Strategy, Next Steps | OCV gap analysis required when `ocv_snapshot` provided |

**Behavior:**
- Derives `safe_account` from `account_name` for all filesystem path construction
- `display_account` (original `account_name`) used only in document output
- Creates `context/success-plan-[safe_account]-[YYYY-MM-DD].md`
- If a canvas for the same account and date already exists, it is overwritten
- Returns console summary: `plan_id`, file path, plan type, and account name

**Output example (console summary):**
```
Canvas generated.
  plan_id:   CANVAS-ACME-20260517
  plan_type: initial
  account:   Acme Corp
  file:      context/success-plan-acme-corp-2026-05-17.md
```

---

### Operation: `refresh`

Updates an existing canvas in place without creating a new dated artifact.

**Input fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `operation` | string | Yes | Must be `"refresh"` |
| `account_name` | string | Yes | Account name — used to locate the existing canvas file |
| `canvas_date` | string | No | ISO date (YYYY-MM-DD) of canvas to refresh; defaults to most recent canvas for account |
| `key_objectives` | list | No | Replacement objectives list (replaces prior objectives section) |
| `ocv_snapshot` | object | No | Updated OCV data — replaces prior OCV section |
| `notes` | string | No | Appended to Notes section (append-only; prior notes are preserved) |

**Immutable fields — rejected if included in refresh payload:**

| Field | Error response |
|-------|---------------|
| `plan_id` | `Immutable field error: plan_id cannot be modified after generation.` |
| `created_at` | `Immutable field error: created_at cannot be modified after generation.` |
| `created_by` | `Immutable field error: created_by cannot be modified after generation.` |
| `plan_type` | `Immutable field error: plan_type cannot be modified after generation.` |
| `account_name` | `Immutable field error: account_name cannot be modified after generation.` |

**Canvas not found error:**
```
No success plan canvas found for [account_name]. Run generate first.
```

**Behavior:**
- Locates `context/success-plan-[safe_account]-[canvas_date].md`
- If `canvas_date` not provided, uses most recent canvas for account (by filename date)
- Updates mutable sections: `key_objectives`, `ocv_snapshot`, and appends to `notes`
- Sets `refreshed_at` to current ISO datetime
- Returns updated file path and refresh timestamp

**Output example (console summary):**
```
Canvas refreshed.
  plan_id:      CANVAS-ACME-20260517
  account:      Acme Corp
  file:         context/success-plan-acme-corp-2026-05-17.md
  refreshed_at: 2026-05-19T14:30:00Z
```

---

## Output Format

### File naming pattern

```
context/success-plan-[safe_account]-[YYYY-MM-DD].md
```

- `safe_account`: lowercase, alphanumeric + hyphens, max 30 chars (derived from `account_name`)
- `YYYY-MM-DD`: generation date (set at `generate`; preserved on `refresh`)
- One file per account per date

### YAML frontmatter fields

```yaml
---
plan_id: CANVAS-ACME-20260517
account_name: Acme Corp
plan_type: initial
csm_name: Jane Smith
account_stage: Onboarding
created_at: 2026-05-17T09:00:00Z
created_by: todd@successhacker.co
refreshed_at: null
---
```

### Document structure

```markdown
---
[YAML frontmatter as above]
---

# [Initial Success Plan | Expansion Canvas | Renewal-Refresh Plan]: [account_name]

**CSM:** [csm_name]
**Date:** [YYYY-MM-DD]
**Stage:** [account_stage]

---

## [Plan-type-specific sections — see plan-type-guide.md]

## OCV Outcomes

[Rendered OCV snapshot with status indicators — omitted if no ocv_snapshot provided]

## Notes

[CSM notes — append-only on refresh]
```

See `references/success-plan-canvas-schema.md` for complete field definitions and section structure per plan type.

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md` and
`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/csm:cold-start-interview`.

Note from config:
- CS motion — shapes how directive vs. collaborative the canvas framing is
- Health model — determines context for lifecycle stage assessment
- Integrations — determines which data sources are available for OCV snapshot

**G-code dependency:** All G-code guardrails referenced in this skill (G1–G9) are defined in the CLAUDE.md config loaded above. If Pre-flight halts or config is missing, G-codes are undefined — do not proceed with partial config.
---

## Reasoning Protocol

> Blueprint: `references/reasoning-blueprint.md` (on-demand only)

Before generating output, apply these primers:

1. **CLASSIFY** — Determine operation and validate inputs before proceeding:
   - Is `operation` present and one of `generate` or `refresh`? If absent or invalid → AskUserQuestion before proceeding.
   - Is `account_name` non-empty? If not → reject immediately with a clear error before any output.
   - For `generate`: is `plan_type` one of `initial`, `expansion`, or `renewal-refresh`? If not → return `Invalid plan_type` error.
   - For `refresh`: does a canvas file exist for this account? If not → return `No success plan canvas found` error before attempting any update.
   - CLASSIFY is complete when: operation confirmed, `account_name` validated, operation-specific preconditions pass.

2. **CONSTRAINTS** — Apply before generating any output (blocking before non-blocking):
   - **C-1 BLOCKING**: `account_name` must be non-empty — reject all operations if absent.
   - **C-2 BLOCKING (generate)**: `plan_type` must be one of `initial`, `expansion`, `renewal-refresh` — return `Invalid plan_type` error immediately; do not attempt to infer or default.
   - **C-3 BLOCKING (refresh)**: canvas file must exist for the target account before applying any mutable updates — return `No success plan canvas found` before attempting any field write.
   - **C-4 BLOCKING (refresh)**: if the refresh payload includes any immutable field (`plan_id`, `created_at`, `created_by`, `plan_type`, `account_name`) → return immutable field error for that specific field; do not apply partial updates.
   - **C-5 Non-blocking**: `safe_account` derivation (lowercase → replace non-alphanumeric with `-` → collapse hyphens → trim to 30 chars) must be applied before any file path construction — never use raw `account_name` in a path.
   - G5: Internal data (health scores, ARR, expansion signals) must never appear in customer-facing output
   - G7: Flag any data older than 30 days with source date and staleness indicator

3. **EXPERT CHECK** — What a veteran CSM verifies before generating or refreshing a success plan canvas:
   - Does the `plan_type` match the account's current lifecycle stage? An `initial` canvas for an account in active renewal review, or a `renewal-refresh` canvas for a brand-new onboarding, signals a misconfiguration — flag it.
   - For `initial` plans: are all 7 required CCSM-104 components present (Goals, Onboarding Milestones, Responsibilities, Success Metrics, Timelines, Risks and Assumptions, Communication Strategy)? An initial canvas missing structural sections is incomplete before it's shared.
   - For `renewal-refresh` with `ocv_snapshot`: does the OCV data contain enough outcome detail to drive meaningful gap analysis? An empty or single-outcome snapshot produces a shallow renewal canvas — flag the data gap.
   - For `refresh` with `notes` append: are prior notes preserved? Append-only discipline on notes is critical — replacing prior notes destroys the account narrative history.
   - Is the `key_objectives` content customer-sourced? Objectives written by the CSM without customer language anchor produce plans that get ignored at QBR.

4. **ANTI-PATTERNS** — Mistakes to catch before generating output:
   - **AP-1 Missing key_objectives on initial generate**: producing an initial plan without `key_objectives` — creates a canvas with no outcome anchor; the plan cannot be meaningfully reviewed.
   - **AP-2 renewal-refresh without ocv_snapshot**: generating a renewal-refresh canvas without OCV data — skips gap analysis entirely, which is the primary value of the renewal-refresh plan type.
   - **AP-3 Refresh targeting immutable fields**: attempting to update `plan_type`, `account_name`, `plan_id`, `created_at`, or `created_by` — these define plan identity; changing them corrupts the record.
   - **AP-4 Wrong plan_type for lifecycle stage**: generating an `initial` canvas for an account in renewal, or `expansion` for a net-new account — the section structure will be wrong and the CSM context misaligned.
   - **AP-5 Notes replacement instead of append**: overwriting prior notes content on a refresh — destroys the longitudinal account narrative; notes are always append-only.

**After execution**, verify:
- Does the output match the classified operation (`generate` or `refresh`) and apply the correct plan-type section structure?
- For `generate`: are all plan-type-specific sections present (e.g., all 8 sections for `initial`, all 9 for `expansion`, all 8 for `renewal-refresh`)?
- For `renewal-refresh` with `ocv_snapshot`: is the OCV Gap Analysis section populated and are outcomes correctly split between gap and delivered tables?
- For `refresh`: are all immutable field constraints (C-4) confirmed clear? Are prior notes preserved if `notes` was in the payload?
- Is the `safe_account` derivation applied correctly before the file path is constructed?
- Confidence: [High] if `ocv_snapshot` provided with full outcome data and plan_type matches confirmed account lifecycle stage / [Medium] if plan_type or account stage is CSM-provided without system confirmation / [Low] if operating without OCV data on a renewal-refresh or without key_objectives on an initial — state which.

### When operation = `generate`

1. **Validate `plan_type`** — confirm value is one of `[initial, expansion, renewal-refresh]`. If not, return: `Invalid plan_type: [value]. Must be one of: initial, expansion, renewal-refresh.`
2. **Derive `safe_account`** — apply the four-step derivation: lowercase → replace non-alphanumeric with `-` → collapse consecutive hyphens → trim to 30 chars. If trimming occurs, proceed silently (no error). If `safe_account` after trim ends with a hyphen, that is acceptable.
3. **Generate `plan_id`** — extract first 4 alpha characters from `account_name`, strip non-alpha, uppercase; format as `CANVAS-[ACCT]-[YYYYMMDD]` using today's date.
4. **Select section structure** from plan type:
   - `initial` → Goals, Onboarding Milestones, Responsibilities, Success Metrics, Timelines, Risks and Assumptions, Communication Strategy, Next Steps
   - `expansion` → Expansion Rationale, Current Outcomes, Expansion Opportunity, Proposed Outcomes, Responsibilities, Success Metrics, Risks and Assumptions, Communication Strategy, Next Steps
   - `renewal-refresh` → Renewal Context, OCV Gap Analysis, Delivered Outcomes, At-Risk Outcomes, Renewal Objectives, Responsibilities, Communication Strategy, Next Steps
5. **Render OCV outcomes** if `ocv_snapshot` is provided — render per plan type rules in `reference/plan-type-guide.md`.
6. **For `renewal-refresh` with `ocv_snapshot`** — classify all outcomes with `status != "delivered"` as gaps; render gap table in OCV Gap Analysis section; render delivered outcomes separately in Delivered Outcomes section.
7. **Write file** to `context/success-plan-[safe_account]-[YYYY-MM-DD].md` with YAML frontmatter and full document body.
8. **Return console summary** with `plan_id`, `plan_type`, `account`, and `file` path.

### When operation = `refresh`

1. **Derive `safe_account`** from `account_name` using the same four-step derivation as generate.
2. **Locate canvas file** — resolve `context/success-plan-[safe_account]-[canvas_date].md`; if `canvas_date` is omitted, select the most recent canvas for the account by filename date sort.
3. **If file not found** — return: `No success plan canvas found for [account_name]. Run generate first.`
4. **Check for immutable field violations first** — if the refresh payload includes any of `plan_id`, `created_at`, `created_by`, `plan_type`, or `account_name`, return the corresponding immutable field error immediately before making any changes.
5. **Apply mutable updates:**
   - `key_objectives` — replace existing objectives section if provided
   - `ocv_snapshot` — replace existing OCV section if provided
   - `notes` — append to Notes section (never replace; prior notes are preserved)
6. **Set `refreshed_at`** to current ISO datetime.
7. **Return console summary** with `plan_id`, `account`, `file` path, and `refreshed_at`.

### For `renewal-refresh` with `ocv_snapshot`

- Iterate all outcomes in `ocv_snapshot.outcomes`
- Outcomes with `status != "delivered"` → classified as gap, rendered in OCV Gap Analysis table with Gap Risk = `⚠ Gap`
- Outcomes with `status == "delivered"` → rendered in Delivered Outcomes table only, not in gap table
- At-risk classification detail: `at_risk` status outcomes appear in both the gap table and the At-Risk Outcomes section

### Escalation rules

- If `account_name` produces a `safe_account` that exceeds 30 chars after trim: truncate at char 30 without error or warning
- If no `account_stage` is provided: omit Stage line from canvas header (do not substitute a default)
- If `ocv_snapshot` is provided but `outcomes` array is empty: render OCV section with note `No outcomes recorded in this snapshot.`

---

## Reviewer note

> **⚠️ Reviewer note**
> - **Sources:** [CRM ✓ live — contract terms, stakeholder contacts | CRM [configured but unverified] | document storage: existing canvas or kickoff notes | user provided | not connected — conversation context only]
> - **Data as of:** [timestamp per source]
> - **Flagged for your judgment:** [N items marked `[review]` inline | none]
> - **Before sending:** Verify success criteria in the canvas have been reviewed and agreed with the customer sponsor before treating as a mutual plan. Canvas contains no internal health scores or expansion signals.

---

## Security & Permissions

- **Network access:** none
- **Filesystem read scope:** `context/success-plan-*` only (for refresh file lookup); OCV data is passed as the `ocv_snapshot` input parameter — it is NOT read from the filesystem by this skill
- **Filesystem write scope:** `context/success-plan-*` only
- **Subprocess execution:** none
- **Dynamic code execution:** none
- **OCV files:** this skill NEVER writes to OCV files or any context file type other than `context/success-plan-*`
- **External integrations:** none

---

## Trust & Verification

**Path construction:**
- `account_name` is always sanitized via the `safe_account` function (lowercase, alphanumeric + hyphen, max 30 chars) before use in any filesystem path
- `display_account` (the original, unsanitized `account_name`) is used only in document content — never in filesystem path construction

**Display-only fields (never used in path construction or skill logic):**
- `ocv_snapshot` content is stored as advisory display data — it is rendered into the canvas document but never executed or interpolated into skill logic
- `notes` and `key_objectives` are treated as display-only freetext — sanitized for path use only if they were referenced in naming (they are not)
- `csm_name` is display-only — never used in filesystem path construction

**Immutable field enforcement:**
- Fields `plan_id`, `created_at`, `created_by`, `plan_type`, and `account_name` are set at `generate` and rejected at `refresh` with an explicit error message
- No silent overwrites of immutable fields

**OCV advisory contract:**
- OCV data received via `ocv_snapshot` parameter is rendered for human review only
- This skill NEVER writes to OCV files under any condition
- OCV gap analysis (for `renewal-refresh`) is computed and displayed — not stored back to any OCV source

---

## Reference Files

The following reference files govern this skill's detailed behavior. They are loaded on-demand when the relevant behavior is being applied — they are not front-loaded into every response.

| File | Purpose |
|------|---------|
| `references/success-plan-canvas-schema.md` | Canonical canvas record format, complete YAML frontmatter field list with types and validation rules, section structure per plan type, auto-ID generation rules, immutable field list and enforcement behavior |
| `references/plan-type-guide.md` | CCSM-104 7-component framework definition, per-plan-type section templates with placeholder content guidance, OCV integration rules by plan type, expansion canvas distinction rules (header branding and framing language), renewal-refresh OCV gap detection logic, component presence rules (required vs optional per plan type) |
| `references/ocv-integration-contract.md` | OCV snapshot input format spec, valid status values, field mappings (`outcome_name`, `status`, `owner`), rendering format for OCV outcomes in canvas sections per plan type, gap detection logic for renewal-refresh, advisory-only contract (skill NEVER writes to OCV files) |
| `references/reasoning-blueprint.md` | Problem classification taxonomy, domain heuristics, common failure modes, and expert judgment patterns for this skill |

---

## Examples

### Example 1: Generate an initial success plan

**Input:**
```json
{
  "operation": "generate",
  "account_name": "Acme Corp",
  "plan_type": "initial",
  "csm_name": "Jane Smith",
  "account_stage": "Onboarding",
  "key_objectives": [
    "Complete technical onboarding within 30 days",
    "Achieve first value milestone by day 45",
    "Establish executive sponsor alignment"
  ],
  "ocv_snapshot": {
    "outcomes": [
      {"outcome_name": "Reduce manual reporting time", "status": "committed", "owner": "Jane Smith"},
      {"outcome_name": "Improve team visibility into pipeline", "status": "not_started", "owner": "Jane Smith"}
    ]
  },
  "notes": "Champion is Sarah Lee (VP Operations). Executive sponsor is Mark Torres (CFO). Kickoff completed 2026-05-15."
}
```

**Output (console summary):**
```
Canvas generated.
  plan_id:   CANVAS-ACME-20260517
  plan_type: initial
  account:   Acme Corp
  file:      context/success-plan-acme-corp-2026-05-17.md
```

**Output (canvas document excerpt):**
```markdown
---
plan_id: CANVAS-ACME-20260517
account_name: Acme Corp
plan_type: initial
csm_name: Jane Smith
account_stage: Onboarding
created_at: 2026-05-17T09:00:00Z
created_by: todd@successhacker.co
refreshed_at: null
---

# Initial Success Plan: Acme Corp

**CSM:** Jane Smith
**Date:** 2026-05-17
**Stage:** Onboarding

---

## Goals

- Complete technical onboarding within 30 days
- Achieve first value milestone by day 45
- Establish executive sponsor alignment

## Onboarding Milestones

| Milestone | Target Date | Owner | Status |
|-----------|-------------|-------|--------|
| [Add milestone] | [Date] | [Owner] | Not Started |

## Responsibilities
...
```

---

### Example 2: Generate a renewal-refresh canvas with OCV gap analysis

**Input:**
```json
{
  "operation": "generate",
  "account_name": "Globex Inc",
  "plan_type": "renewal-refresh",
  "csm_name": "Carlos Rivera",
  "account_stage": "Renewal",
  "ocv_snapshot": {
    "outcomes": [
      {"outcome_name": "Automate monthly close reporting", "status": "delivered", "owner": "Carlos Rivera"},
      {"outcome_name": "Reduce onboarding time by 30%", "status": "committed", "owner": "Carlos Rivera"},
      {"outcome_name": "Expand usage to 3 new departments", "status": "in_progress", "owner": "Carlos Rivera"}
    ]
  },
  "key_objectives": [
    "Demonstrate ROI ahead of renewal conversation",
    "Close outstanding OCV gaps before renewal date"
  ]
}
```

**Output (console summary):**
```
Canvas generated.
  plan_id:   CANVAS-GLOB-20260517
  plan_type: renewal-refresh
  account:   Globex Inc
  file:      context/success-plan-globex-inc-2026-05-17.md
```

**OCV Gap Analysis section in canvas:**
```markdown
## OCV Gap Analysis

The following outcomes are committed or in progress with no delivered resolution.
These represent renewal-risk gaps requiring attention before the renewal conversation.

| Outcome | Status | Owner | Gap Risk |
|---------|--------|-------|----------|
| Reduce onboarding time by 30% | committed | Carlos Rivera | ⚠ Gap |
| Expand usage to 3 new departments | in_progress | Carlos Rivera | ⚠ Gap |

**Delivered Outcomes**

| Outcome | Status | Owner |
|---------|--------|-------|
| Automate monthly close reporting | delivered | Carlos Rivera |
```

---

### Example 3: Refresh an existing canvas with updated notes

**Input:**
```json
{
  "operation": "refresh",
  "account_name": "Acme Corp",
  "canvas_date": "2026-05-17",
  "notes": "QBR scheduled for 2026-06-01. Champion confirmed renewal intent pending gap closure."
}
```

**Output (console summary):**
```
Canvas refreshed.
  plan_id:      CANVAS-ACME-20260517
  account:      Acme Corp
  file:         context/success-plan-acme-corp-2026-05-17.md
  refreshed_at: 2026-05-19T14:30:00Z
```

---

### Example 4: Refresh error — canvas not found

**Input:**
```json
{
  "operation": "refresh",
  "account_name": "Unknown Customer",
  "notes": "Some update"
}
```

**Output:**
```
No success plan canvas found for Unknown Customer. Run generate first.
```
