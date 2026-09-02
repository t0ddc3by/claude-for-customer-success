---
name: value-reinforcement
description: >
  Make delivered value visible, relevant, and repeatable between formal
  reviews: compile usage, outcomes, and milestones into a value-delivered
  summary in the customer's language, tied back to their recorded Why Change
  and Expected Value Baseline. Produces the between-QBR touchpoints (a short
  note, a slide, a one-pager) that keep achieved value present in the
  customer's memory, because value that is achieved but not recognized does
  not drive retention. Reads the account's registry entries and Value Map
  evidence; never invents numbers.
argument-hint: "[--account <name> --format <note|slide|onepager>]"
version: "0.1.0"
deployment_target: plugin
---

# /vbs:value-reinforcement

Customers do not remember value they were never shown. Anchor: VBS-106.

[PROPOSED]

---

## Use when

- A quarter is passing without a formal review and achieved value should be surfaced anyway
- A registry entry just moved to a realized state and the moment deserves a touchpoint
- Renewal is 6+ months out and the value story needs regular deposits, not a lump sum at 90 days
- A champion needs fresh ammunition for an internal budget conversation

## Do NOT use for

- The 90-day pre-renewal achieved-value summary (use `/vbs:renewal-influence-plan`; it assembles the full case)
- QBR assembly (csm plugin's qbr-builder owns that; this skill feeds it)
- Claiming value with no evidence on record (the skill declines and says what evidence to capture first)

## Typical activation

"Send Northwind a value note, they hit the de-anon milestone" / "monthly value touchpoint for the top 10 accounts" / "give the champion a slide for her budget meeting"

---

## Workflow

1. Read config and the account's evidence: registry entries (states and realized values), Value Map items, usage milestones. No evidence, no touchpoint: instead output the two capture actions that would create evidence.
2. Frame each item as their outcome, their words: baseline (their EVB text) → what happened (measured, sourced) → what it maps to (their Why Change, their metric). The VBS-106 pattern: "in the past 6 months you've automated 3 processes, saving an estimated 120 hours; here's how that maps to your goals."
3. Render the requested format, short by design: note (5 sentences), slide (one visual claim + three proof lines), one-pager (forwardable, survives the reader who was not in the room).
4. Close every touchpoint with a forward hook: the next outcome in flight, not a sales ask.
5. Log the touchpoint to the account workspace so renewal-influence-plan can show the deposit history.

## Output contract

The artifact in the requested format, evidence-cited internally, customer-language externally. If evidence is thin, the capture actions lead instead.

## Security & Permissions

Local account workspace and configured registry/Value Map reads only; no sends (the user sends); no writes to shared state.

## Trust & Verification

Every number traces to a registry entry or sourced measurement; self-reported vendor numbers are labeled as such. Anchors: VBS-106 (Identify and Communicate Value Achieved), Value Bridge recognition thesis.
