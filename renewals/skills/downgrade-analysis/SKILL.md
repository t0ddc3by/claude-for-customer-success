---
name: downgrade-analysis
description: "Analyzes customer contract downgrade requests (contraction only) and produces a value chain failure map, counter-proposal inputs, and recommended response strategy for CSM/AM negotiation. Scoped to contraction scenarios — full cancellation redirected to renewals:churn-rca."
version: "1.0.0"
metadata:
  author: "todd@successhacker.co"
  tags: "renewals downgrade contraction churn-prevention customer-success"
deployment_target: plugin
---

# /renewals:downgrade-analysis [VALIDATED]

## Overview

**Use when:**
- A customer has requested a contract reduction, tier downgrade, seat reduction, module removal, or ARR contraction
- A CSM or AM needs structured analysis of the downgrade driver before entering negotiation
- Preparing a counter-proposal or escalation brief for a renewal at risk of contracting

**Do NOT use for:**
- Full contract cancellations, terminations, or "cancel everything" requests → use `renewals:churn-rca`
- Expansion or upsell analysis
- Renewal risk scoring without a specific downgrade request in hand
- Post-mortem analysis after a downgrade has already closed

**Typical activation:**
> "Run downgrade analysis for Acme Corp — they want to cut from 500 to 200 seats, saying the team shrank."
> "Analyze this downgrade request: customer says they're switching to a cheaper tool."
> `/renewals:downgrade-analysis` — then provide operation inputs when prompted

**Churn boundary:**
If the request contains signals of full contract cancellation ("cancel everything," "terminate contract," "no longer proceeding," "shut down the account"), this skill redirects to `renewals:churn-rca`. Partial reduction of any kind — seats, modules, tier, spend — is in scope.

---

## Use When
- A customer has requested a contract reduction, tier downgrade, seat reduction, module removal, or ARR contraction
- A CSM or AM needs structured analysis of the downgrade driver before entering negotiation
- Preparing a counter-proposal or escalation brief for a renewal at risk of contracting

## Do NOT Use For
- Full contract cancellations, terminations, or "cancel everything" requests → use `renewals:churn-rca`
- Expansion or upsell analysis
- Renewal risk scoring without a specific downgrade request in hand
- Post-mortem analysis after a downgrade has already closed

## Typical Activation
> "Run downgrade analysis for Acme Corp — they want to cut from 500 to 200 seats, saying the team shrank."
> "Analyze this downgrade request: customer says they're switching to a cheaper tool."
> `/renewals:downgrade-analysis` — then provide operation inputs when prompted

---

## Pre-flight

- Confirm account context (company name, CSM/AM, current contract, renewal date)
- Identify the specific analysis goal (new analyze or update to existing DGA)
- Note any prior analysis or existing documentation to reference
- Check `~/.claude/plugins/config/claude-for-customer-success/company-profile.md` for company segment and escalation context (`company-profile.md` is a runtime config dependency, not a reference file)

**G-code dependency:** All G-code guardrails referenced in this skill (G1–G9) are defined in the CLAUDE.md config loaded above. If Pre-flight halts or config is missing, G-codes are undefined — do not proceed with partial config.
---

## Operations

This skill supports two operations: `analyze` and `update`.

---

### Operation: `analyze`

Creates a new downgrade analysis record and writes it to disk.

**Input fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| operation | string | Yes | Must be `"analyze"` |
| account_name | string | Yes | Account name — used for file path and display |
| csm_name | string | Yes | CSM or AM initiating the analysis |
| downgrade_request | string | Yes | Free-text description of what the customer wants to reduce |
| current_contract | string | No | Current tier, product name, or ARR |
| driver_category | string | No | One of: `budget_pressure`, `reduced_scope`, `feature_underutilization`, `competitive_pressure`, `dissatisfaction`. Inferred if omitted. |
| ocv_snapshot | string | No | OCV/outcome data snapshot — advisory signal for value delivery correlation |
| notes | string | No | Additional CSM/AM context |

**Auto-generated fields (immutable after creation):**
- `dga_id`: `DGA-[ACCT]-[YYYYMMDD]-[SEQ]` — ACCT is first 8 chars of safe_account uppercased, SEQ is 3-digit sequence starting 001
- `created_at`: ISO 8601 datetime
- `created_by`: session user

**Scope redirect — full churn detection:**
If `downgrade_request` contains any of the following signals, return the redirect message and do not create a file:
- "cancel everything" / "cancel the contract" / "cancel our subscription"
- "terminate contract" / "terminate the agreement"
- "no longer proceeding" / "shutting down" / "going out of business"
- "end our relationship" / "close the account"

Redirect message (exact):
```
Scope redirect: This request describes full contract cancellation, not a downgrade.
Please use renewals:churn-rca for churn analysis.
```

**Driver category inference (when `driver_category` not provided):**

| Signal vocabulary in request | Inferred category |
|------------------------------|-------------------|
| cost, price, budget, expensive, afford, overpaying, ROI, justify spend | `budget_pressure` |
| fewer users, less volume, smaller team, headcount, reduced seats, team shrank | `reduced_scope` |
| not using, don't need all features, too complex, not adopted, only using part | `feature_underutilization` |
| competitor, alternative, switching, vendor, cheaper tool, evaluating others | `competitive_pressure` |
| problems, unhappy, support, broken, frustrated, disappointed, not working | `dissatisfaction` |

Mixed-signal handling: if two or more categories are signaled, identify the primary (strongest/most explicit signal) and note secondary signals in the analysis. Load `references/downgrade-driver-taxonomy.md` for full heuristics.

**Analysis output structure:**

```
## Downgrade Analysis: [Account Name]
### Analysis ID: [DGA-ID]
### Driver Category: [category] ([inferred|provided])

## Value Chain Failure Map
### Failure Classification: [Missing link | Broken link | Non-value-chain driver]
[Narrative: what failed, where in the value chain, evidence from request and OCV]

## Counter-Proposal Inputs (CSM/AM Internal Use)
### Retention Levers Available
[Structured inputs: concessions, alternatives, commitment asks]
### Negotiation Anchors
[Key facts and positions CSM/AM can reference]

## Recommended Response Strategy
### Primary Action
[Highest-priority response action for this driver category]
### Supporting Actions
[Ordered list of supporting moves]
### Escalation Trigger
[Condition under which this should escalate beyond CSM/AM]
```

**Output file path:** `context/downgrade-analysis-[safe_account]-[YYYY-MM-DD].md`

---

### Operation: `update`

Appends new information to an existing downgrade analysis. Never overwrites prior content.

**Input fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| operation | string | Yes | Must be `"update"` |
| dga_id | string | Yes | Target analysis ID (e.g., `DGA-ACMECORP-20260517-001`) |
| additional_context | string | Yes | New information to append |
| revised_driver_category | string | No | If new info changes driver classification — one of the 5 valid categories |
| ocv_snapshot | string | No | Updated OCV data — appended alongside prior snapshot |
| notes | string | No | Additional notes |

**Immutable fields — update rejected if provided as modifications:**
`dga_id`, `created_at`, `created_by`, `account_name`

Error message format:
```
Immutable field error: [field_name] cannot be modified after analysis creation.
```

**Update block format (appended to file):**
```
## Update Log

### Update [N] — [YYYY-MM-DDTHH:MM:SSZ]
**Added by:** [csm_name or session user]
**Additional context:** [additional_context content]
**Driver reclassification:** [if applicable — from X to Y, rationale]
**OCV update:** [if provided]
**Notes:** [notes if provided]
```

---

## Output Format

### File naming convention
`context/downgrade-analysis-[safe_account]-[YYYY-MM-DD].md`

### safe_account derivation (file paths only — never used for display)
1. Lowercase the full `account_name`
2. Replace all non-alphanumeric characters with `-`
3. Collapse consecutive hyphens to a single hyphen
4. Trim to 30 characters maximum

Examples:
- `Acme Corp` → `acme-corp`
- `O'Brien & Associates, LLC` → `o-brien-associates-llc` (trimmed if over 30 chars)

### Output file YAML frontmatter
```yaml
---
dga_id: DGA-[ACCT]-[YYYYMMDD]-[SEQ]
account_name: [original account_name verbatim]
safe_account: [derived safe_account]
csm_name: [csm_name]
driver_category: [category]
driver_source: inferred | provided
created_at: [ISO 8601 datetime]
created_by: [session user]
updated_at: [ISO 8601 datetime — set on each update]
current_contract: [value or omitted if not provided]
---
```

---

## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of downgrade analysis request is this?
   - **New Analysis** (`analyze`): New downgrade request — driver classification, value chain failure map, counter-proposal inputs, response strategy.
   - **Update** (`update`): Append new context to an existing DGA record — preserve prior analysis verbatim, append as numbered update block.

2. **CONSTRAINTS**: What limits the solution space?
   - G4: Escalation triggers must be specific and actionable — not generic "escalate to your manager."
   - G5: Counter-proposal inputs (walk-away figures, concession authority, competitive analysis) are CSM/AM internal use only — never include in customer-facing output.
   - Never infer driver category from a single ambiguous signal — require clear signal vocabulary match or flag as mixed-signal.

3. **EXPERT CHECK**: What would a veteran renewals specialist verify first?
   - Is the value chain failure classification (Missing link / Broken link / Non-value-chain) correctly matched to the driver category and OCV data?
   - Does the recommended response strategy address the actual driver — not the surface objection?

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Accepting the stated downgrade reason as the root driver without checking for secondary signals in the vocabulary.
   - Classifying a budget cut as a value chain failure when it is a non-value-chain driver (external mandate).
   - Generating escalation triggers that are time-based but not tied to a specific outcome or escalation owner.
   - Proceeding to counter-proposal without first checking for full-churn signals — always run the redirect check first.
   - Modifying immutable fields (dga_id, created_at, created_by, account_name) in update operations — these are locked at creation.

**After execution**, verify:
- Did the full-churn signal check run before any analysis?
- Is the value chain failure classification consistent with the driver category and OCV evidence?
- Are escalation triggers specific (condition, owner, timeframe)?
- Confidence: [High] when account data is complete and driver vocabulary is unambiguous / [Medium] when partial data or mixed signals / [Low] if inputs are manual or inferred

---

### For `analyze` operations

**Step 1 — Full-churn signal check**
Scan `downgrade_request` for cancellation vocabulary. If found, return scope redirect message and stop. Do not create a file.

**Step 2 — Derive safe_account**
Apply the 4-step derivation: lowercase → replace non-alphanumeric with `-` → collapse hyphens → trim to 30 chars. Confirm derivation before using in file path.

**Step 3 — Driver category resolution**
If `driver_category` is provided: validate against the 5-category enum. If invalid, return error and stop.
If `driver_category` is not provided: scan `downgrade_request` for signal vocabulary per inference table. Identify primary category. Note secondary signals. Set `driver_source` to `inferred`.

**Step 4 — Value chain failure classification**
Apply the three-way classification (load `references/value-chain-failure-map.md`):
- **Missing link**: Outcome committed but not delivered. OCV shows gap between expected and actual outcome delivery. Root cause: CSM/delivery failure.
- **Broken link**: Outcome delivered but customer has not recognized or adopted it. Low usage despite feature availability. Root cause: adoption/change management failure.
- **Non-value-chain driver**: Budget cuts, reorg, market conditions, headcount reduction, competitive pricing. Value delivery is not the root cause.

Classification heuristics:
- `budget_pressure` without dissatisfaction signals → Non-value-chain driver (unless OCV shows delivery gap)
- `reduced_scope` (team shrank, fewer users) → Non-value-chain driver
- `feature_underutilization` → Broken link (delivered but not adopted) or Missing link (never onboarded)
- `competitive_pressure` → Non-value-chain driver unless price objection masks dissatisfaction
- `dissatisfaction` → Missing link (failed delivery) — corroborate with OCV if provided

When `ocv_snapshot` is provided: OCV gap between committed and actual outcomes strengthens Missing link; strong outcome delivery + low adoption strengthens Broken link.

**Step 5 — Counter-proposal inputs**
Generate retention levers and negotiation anchors per driver category. Load `references/counter-proposal-framework.md` for the full lever catalog. Mark all counter-proposal inputs as CSM/AM internal use only.

**Step 6 — Recommended response strategy**
Generate primary action, supporting actions (ordered by priority), and escalation trigger. Escalation trigger must be specific and actionable, not generic.

**Step 7 — DGA-ID derivation**
Construct candidate ID: `DGA-[ACCT]-[YYYYMMDD]-001` where ACCT = first 8 chars of safe_account uppercased, with hyphens removed. Check `context/` for existing `downgrade-analysis-[safe_account]-[YYYY-MM-DD].md` files. If one exists, scan frontmatter for the highest existing SEQ with matching ACCT+date prefix and increment by 1. If no match, SEQ = 001.

**Step 8 — Write output file**
Write complete file to `context/downgrade-analysis-[safe_account]-[YYYY-MM-DD].md` with YAML frontmatter followed by full analysis content. Confirm write succeeded. Return file path and DGA-ID.

---

### For `update` operations

**Step 1 — Immutable field check**
If input attempts to modify `dga_id`, `created_at`, `created_by`, or `account_name`, return immutable field error and stop. (`dga_id` as lookup key is valid; providing it as a modification is not.)

**Step 2 — Locate target file**
Parse `dga_id` to extract date component. Search `context/downgrade-analysis-*` for file whose frontmatter contains the exact `dga_id`. If not found, return: `Analysis not found: no file with dga_id [dga_id] in context/downgrade-analysis-*.`

**Step 3 — Validate revised_driver_category (if provided)**
Validate against 5-category enum. Return error if invalid.

**Step 4 — Count existing updates**
Scan file for `### Update [N]` pattern. Set next N = count + 1.

**Step 5 — Append update block**
Append update block. Omit lines for absent optional fields. Set `updated_at` in YAML frontmatter to current ISO 8601 datetime.

**Step 6 — Confirm and return**
Return: updated file path, update number, timestamp.

---

## Security & Permissions

```
network:        none — no external API calls, no web fetch
read_scope:     context/downgrade-analysis-* only
write_scope:    context/downgrade-analysis-* only
ocv_data:       read from ocv_snapshot input parameter only — never from filesystem
subprocess:     none
dynamic_code:   none — no eval, no exec, no runtime code execution
```

This skill operates exclusively within the `context/` directory on files matching the `downgrade-analysis-*` prefix. It does not read from, write to, or reference any other path.

---

## Trust & Verification

**safe_account sanitization:**
`safe_account` is derived deterministically from `account_name` using the 4-step normalization. It is used exclusively in file paths. The original `account_name` is preserved verbatim in frontmatter and all display contexts. `safe_account` is never shown to users as an account identifier.

**Free-text field handling:**
`downgrade_request`, `notes`, and `additional_context` are stored verbatim as display data. They are not executed, evaluated, or used to derive file paths. Prompt injection via free-text fields cannot affect file paths, IDs, or system behavior.

**driver_category validation:**
When provided, `driver_category` is validated against the 5-item enum before use. Values outside this set return an error and halt execution. Inferred categories are constrained to the same enum.

**Immutable field enforcement:**
After a downgrade analysis is created, `dga_id`, `created_at`, `created_by`, and `account_name` cannot be modified. Update operations attempting to change these fields are rejected before any file write occurs.

**Update operations are append-only:**
No update operation modifies existing content. All updates are written as new numbered blocks. Prior analysis sections are preserved verbatim.

**ocv_snapshot integrity:**
OCV data is accepted only through the `ocv_snapshot` input parameter. This skill never reads OCV data from the filesystem, from external sources, or from prior session context not provided in the current input.

---

## Reference Files

> **Lifecycle alignment:** This analysis supports G4.1 (Retention/Renewal) and G5.1 (Recovery) stages.

| File | Path | Purpose |
|------|------|---------|
| Reasoning Blueprint | `references/reasoning-blueprint.md` | Reasoning framework for this skill — D1 cognitive stance, constraints, and expert orientation |
| Downgrade Driver Taxonomy | `references/downgrade-driver-taxonomy.md` | Full definitions, signal vocabulary, diagnostic questions, and mixed-signal handling for all 5 driver categories |
| Value Chain Failure Map | `references/value-chain-failure-map.md` | Missing link / Broken link / Non-value-chain definitions, detection patterns, remediation pathways, and escalation guidance |
| Counter-Proposal Framework | `references/counter-proposal-framework.md` | Retention levers per driver category, negotiation anchors, concession guidance, and escalation trigger conditions |

Reference files are loaded on demand during analysis generation — not front-loaded into every response.

---

## Examples

### Example 1 — `analyze` with driver inference

**Input:**
```
operation: analyze
account_name: Meridian Health Group
csm_name: Jordan Reyes
downgrade_request: "Customer says they're cutting software spend across the board — CFO mandate. They want to drop from the Enterprise tier to the Professional tier."
current_contract: Enterprise tier, $84,000 ARR
ocv_snapshot: "QBR outcomes delivered: 3/5. Two outcome areas (reporting automation, manager dashboards) not yet adopted. Usage at 34% of licensed seats."
```

**Skill behavior:**
1. Churn signal check: No cancellation vocabulary — proceed.
2. safe_account: `meridian-health-group` → trimmed to `meridian-health-group` (21 chars, under limit).
3. Driver inference: "cutting software spend," "CFO mandate" → primary `budget_pressure`. OCV shows low adoption (34% seats, 2 undelivered outcomes) → secondary `feature_underutilization` noted.
4. Value chain failure: Non-value-chain driver (CFO mandate) with Broken link as contributing factor (low adoption gives the CFO justification).
5. DGA-ID: No existing file — `DGA-MERIDIANHEAL-20260517-001`.

**Output file:** `context/downgrade-analysis-meridian-health-group-2026-05-17.md`

**Recommended response strategy excerpt:**
```
### Primary Action
Secure CFO-level engagement to present ROI data before the tier change is finalized.
This is a CFO mandate — not negotiable at CSM/AM level.

### Escalation Trigger
If CSM/AM cannot access CFO or VP-level sponsor within 5 business days,
escalate to Customer Success leadership for exec-to-exec outreach.
```

---

### Example 2 — `update` operation

**Input:**
```
operation: update
dga_id: DGA-MERIDIANHEAL-20260517-001
additional_context: "Spoke with champion Sarah Kim — confirmed CFO mandate is a 90-day cost reduction cycle, not permanent. Budget expected to normalize Q3. She's open to a temporary downgrade with re-expansion commitment clause."
revised_driver_category: budget_pressure
notes: "Consider 90-day bridge pricing offer rather than full tier downgrade."
```

**Appended block:**
```
## Update Log

### Update 1 — 2026-05-17T14:32:00Z
**Added by:** Jordan Reyes
**Additional context:** Spoke with champion Sarah Kim — confirmed CFO mandate is a
90-day cost reduction cycle, not permanent. Budget expected to normalize Q3.
She's open to a temporary downgrade with re-expansion commitment clause.
**Driver reclassification:** budget_pressure (confirmed — no change to prior classification)
**Notes:** Consider 90-day bridge pricing offer rather than full tier downgrade.
```

---

### Example 3 — scope redirect

**Input:**
```
operation: analyze
account_name: Pinnacle Dynamics
csm_name: Alex Torres
downgrade_request: "Customer wants to terminate the contract entirely — they're shutting down their CS department."
```

**Skill response:**
```
Scope redirect: This request describes full contract cancellation, not a downgrade.
Please use renewals:churn-rca for churn analysis.
```

No file is written.
