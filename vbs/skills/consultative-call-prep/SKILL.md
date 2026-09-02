---
name: consultative-call-prep
description: >
  Prepare a customer-facing call the consultative way: oriented to the buyer's
  outcomes and current motivation record, not to product positioning. Produces
  a one-page prep sheet with the call's single objective, the questions to ask
  (curious guide, not pushy seller), the relevant insight to bring, anticipated
  concerns, and the agreed next step to propose. Works for discovery,
  demo-stage, proposal, and renewal-adjacent calls; consumes three-whys and
  outcome-qualification outputs when present.
argument-hint: "[--call-type <discovery|demo|proposal|renewal> --attendees <roles>]"
version: "0.1.0"
deployment_target: plugin
---

# /vbs:consultative-call-prep

Walk in as the most prepared person in the room, prepared about them, not about the deck. Anchor: VBS-104, the Consultative Approach framework.

[PROPOSED]

ETM coordinates: pipeline 3 Discovery - 4 Demo/Evaluation. Prep questions are designed to elicit buyer-verifiable evidence for validation states 1-2.

---

## Use when

- Any customer-facing call in an active deal or expansion motion needs prep
- Attendees include a new stakeholder whose priorities are unmapped
- A previous call ran feature-first and the account is cooling

## Do NOT use for

- Extracting discovery findings after the call (use `/vbs:three-whys-discovery --synthesize`)
- Building the value story artifact itself (use `/vbs:value-narrative`)
- Negotiation-stage sessions where terms are on the table (use `/vbs:negotiation-prep`)

## Typical activation

"Prep me for tomorrow's call with the VP CS and their RevOps lead" / "demo-stage prep for Alturo, Priya is skeptical"

---

## Workflow

1. Read config, the deal's motivation record, qualified promise set, and stakeholder plan. Name what is missing rather than improvising around it.
2. Set one call objective stated as a buyer outcome ("agree how they will measure onboarding time-to-value"), never as a seller activity ("show the dashboard module").
3. Build the sheet, one page: **Opening frame** (their situation in their words, one sentence); **Questions** (5-7, open, sequenced from their world toward the gap, per persona; the consultative rule is questions before assertions); **Insight to bring** (one relevant, non-pitch observation from their industry or data that earns partner status); **Likely concerns** per attendee with a value-anchored response each (pull from `objection-reframe` patterns when config exists); **Proposed next step** (specific, dated, low-friction).
4. Every product claim on the sheet cites the qualified promise set; anything not in it is cut or flagged provisional.
5. Save to the deal workspace; after the call, route notes to `three-whys-discovery --synthesize`.

## Output contract

The one-page sheet, opening frame first. If the motivation record is empty, the sheet becomes discovery prep and says so.

## Security & Permissions

Local deal workspace and configured catalog only; no network access.

## Trust & Verification

Claims trace to the qualified promise set; concerns and personas trace to the stakeholder plan; the sheet never introduces an unqualified promise. Anchors: VBS-104; Consultative Approach framework; Show Up as Partner Every Day practice.
