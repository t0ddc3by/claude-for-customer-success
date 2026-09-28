---
name: sales-cs-handoff-quality-scoring
version: 1.0.0
deployment_target: plugin
status: PROPOSED
description: "Scores each closed/won deal on five handoff dimensions (0–100). Pass threshold: 80. Below-threshold deals trigger a Linear issue assigned to the AE manager with 48-hour SLA. CS onboarding proceeds but CSM is notified of open issue. Dimensions: OCV entry referenced, trigger match, measurement source accessible, stakeholder map, risk flags documented. Triggers: 'handoff quality', 'handoff score', 'what's missing for [deal] handoff', 'CS handoff check', 'handoff completeness'."
---

[PROPOSED]

# Sales-CS Handoff Quality Scoring

Objective catalog alignment check — not subjective prose quality. The pass/fail
is binary per dimension, sourced from structured fields and OCV catalog, not
a judgment call on how good the rep's notes are.

**Reference:** Handoff quality scoring rubric → `../../../shared/revops-domain-model.md §10`
**Reference:** Governance tiers → `../../../shared/revops-domain-model.md §9`
**Config reads:** `ocv_catalog_path`, `linear_connected`

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/rev-ops/CLAUDE.md` and
`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/rev-ops:cold-start-interview`.

Note from config: `ocv_catalog_path`, `linear_connected`

**G-code dependency:** All G-code guardrails referenced in this skill (G1–G9) are defined in the CLAUDE.md config loaded above. If Pre-flight halts or config is missing, G-codes are undefined — do not proceed with partial config.
---

## Use when
- Closed deal is entering CS onboarding and handoff quality needs assessment
- Handoff package completeness needs scoring before CS assignment
- Handoff quality trending across reps or periods needs analysis

## Do NOT use for
- Deal desk routing (use deal-desk-workflow-management)
- Outcome tracing post-onboarding (use deal-to-outcome-tracing)
- CS capacity modeling (use closed-won-to-cs-capacity-modeling)

## Typical Activation
"Handoff quality score", "score the handoff for [account]", "sales to CS handoff quality", "handoff completeness check", "is this deal ready for CS"

---

## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of handoff quality request is this?
   - Single-deal scoring (one closed/won account — full five-dimension check)
   - Batch scoring (multiple recent closes — all scored, digest summary produced)
   - Trending analysis (handoff quality over time by rep or period)
   - Below-threshold remediation (deal already flagged — what's needed to resolve)

2. **CONSTRAINTS**: What limits the solution space?
   1. Confirm activation — user requesting handoff check for a specific deal or recent closes
   2. Read deal fields from HubSpot and OCV catalog; declare connector status
   3. Apply G8 — only Ratified OCV entries count toward D1; Draft entries do not satisfy
   4. Apply G6 — data-as-of timestamp required on all HubSpot and OCV reads
   5. Confirm Linear is connected before creating below-threshold issues; surface fallback if unavailable
   6. Apply G7 — every below-threshold flag includes named escalation path (AE manager) and 48h SLA
   7. CS onboarding proceeds regardless of score — flag is for the AE manager, not a CS blocker

3. **EXPERT CHECK**: What would a veteran RevOps handoff analyst verify before surfacing scores?
   - Is the OCV catalog path confirmed accessible? Scoring D1 without a live catalog read
     produces a false PASS if the deal field happens to contain any text — the check
     must verify the referenced entry is Ratified, not just present.
   - Is D3 (measurement source) evaluated from CS's access context, not Sales'? A measurement
     source accessible to the AE in Salesforce may be inaccessible to the CSM in Gainsight —
     the check is CS-context, not deal-context.
   - Is the Linear issue body specific enough to resolve in 48 hours? "D1 failed" is not
     actionable — the body must name what field needs populating and which OCV entry to reference.
   - Is the weekly digest compared to prior week? A 60% pass rate this week means nothing
     without trending context — if available, include WoW delta.

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Counting Draft OCV entries toward D1 (G8 violation — only Ratified entries count)
   - Creating Linear issues without confirming Linear connector is live (produces phantom issues)
   - Pulling HubSpot deal data without data-as-of timestamp (G6 violation)
   - Blocking CS onboarding pending handoff remediation — onboarding proceeds; remediation is parallel

**After execution**, verify:
- G6 data-as-of label applied to all HubSpot and OCV catalog reads
- G7 escalation path (AE manager, 48h SLA) present on all below-threshold flags
- G8 compliance confirmed — only Ratified OCV entries counted toward D1
- Linear issue body is specific and actionable, not just a dimension label
- Confidence: High when HubSpot and OCV catalog connected and current; Moderate when connector unavailable or OCV catalog path missing
    - Confidence: [High] when HubSpot and OCV catalog connected and current / [Medium] when connector unavailable or OCV catalog path missing / [Low] if all inputs are manual or unverified

---

## Five Dimensions `[revops-domain-model.md §10]`

```
D1: OCV entry referenced (20pts)
    PASS: ≥1 Ratified OCV entry linked to deal in HubSpot
    FAIL: No entry, or only Draft entries

D2: Trigger condition match (20pts)
    PASS: OCV trigger condition confirmed present in account context
    FAIL: Trigger condition not present, or not verifiable from deal data

D3: Measurement source accessible (20pts)
    PASS: The measurement source in the OCV entry is accessible to CS post-close
    FAIL: Source requires system CS doesn't have access to

D4: Stakeholder map transferred (20pts)
    PASS: Economic buyer + champion + technical contact all named and tagged
    FAIL: One or more roles missing

D5: Risk flags documented (20pts)
    PASS: Deal notes include risk flags OR explicit "none identified"
    FAIL: Field empty or not populated
```

---

## Below-Threshold Action (score < 80)

```
1. Create Linear issue:
   Title: "Handoff quality below threshold — [Account Name]"
   Assigned to: [AE manager]
   SLA: 48 hours
   Body:
     Deal: [link]  ACV: $XXXk  Close date: [date]
     Failed dimensions: [list]
     What's needed: [specific fields/actions per dimension]

2. Notify CSM:
   "Handoff for [Account] is below threshold (score: [N]/100).
   Missing: [dimensions]. Linear issue [#N] assigned to [AE manager].
   Onboarding proceeds — please flag if blockers surface."

3. Log in audit trail:
   timestamp, deal ID, score, failed dimensions, issue number, CSM notified
```

---

## Output

```
HANDOFF QUALITY SCORING — [Deal / Week]
[HubSpot ✓ live — as of YYYY-MM-DD] [Confidence: High]

[Account A]  $XXXk  Score: 100/100  ✓ PASS
[Account B]  $XXXk  Score: 60/100   ✗ BELOW THRESHOLD
  Failed: D1 (no Ratified OCV entry), D4 (technical contact not tagged)
  Linear issue created: #[N] → [AE manager], 48h SLA
  CSM [name] notified

Weekly digest:
  Deals closed this week: [N]
  Pass (≥80): [N] (XX%)
  Below threshold: [N] (XX%)
  Avg score: [N]/100

[G7: Below-threshold escalation path: AE manager via Linear within 48h]
[G8: Only Ratified OCV entries counted toward D1]
```

---

## Reference Files

| File | Purpose |
|------|---------|
| `references/reasoning-blueprint.md` | Problem classification taxonomy, domain heuristics, common failure modes, and expert judgment patterns for this skill |

## Security & Permissions

**Network access:** None direct — all external data access is mediated by host-provided MCP connector tools (HubSpot, CS platform, Slack, Linear). This skill makes no direct outbound HTTP calls.
**Filesystem scope:** None — this skill does not read or write local files. All data is provided at runtime via parameters or MCP connector responses.
**Subprocess execution:** None.
**Dynamic code execution:** None — pseudocode in this skill represents the logic contract and is not executed at runtime.
**Data sensitivity:** Inputs may contain confidential customer, deal, and operational data. Handle with RevOps-level confidentiality.

## Trust & Verification

**Input trust model:** All user-provided parameters are treated as untrusted at intake. Numeric inputs are validated for plausible range before use in calculations. String inputs are not evaluated as code.
**Output trust model:** All outputs are proposals or analytical inputs — no outputs constitute approved decisions, revenue commitments, or system actions without explicit human confirmation.
**Connector data:** Data retrieved via MCP connectors is treated as read-only observed state. Timestamps and data-as-of labels are applied to all connector-sourced values per G6.
**Write-tier confirmation:** Any proposed write to HubSpot, Linear, or Slack is surfaced as a draft requiring explicit user confirmation before execution.

## Guardrails

- G7: Every below-threshold flag includes named escalation path and owner
- G8: Draft OCV entries do not satisfy D1
- G6: Data-as-of required on all reads
