---
name: renewal-influence-plan
description: >
  Build the value-based influence campaign for a renewal committee, starting
  90+ days out: the achieved-value summary assembled from registry evidence,
  the stakeholder-by-stakeholder message map for the renewal decision, risk
  and sentiment reads, and the sequenced touchpoints that land the case
  before the commercial conversation begins. Proactive by construction: if
  invoked inside 60 days, it says so and compresses honestly. Supplies the
  influence layer; the renewals plugin owns forecast, pricing, and the
  commercial negotiation itself.
argument-hint: "[--account <name> --renewal-date <date>]"
version: "0.1.0"
deployment_target: plugin
---

# /vbs:renewal-influence-plan

Renewals are won in the 90 days before the conversation, not in it. Anchors: VBS-111, VBS-113.

[PROPOSED]

---

## Use when

- A renewal is 90-180 days out and the influence campaign should start
- The renewal committee includes stakeholders who never saw the delivered value
- Sentiment is mixed and the case needs sequencing (who hears what, in what order)
- The achieved-value summary for the renewal needs assembling from the record

## Do NOT use for

- Renewal forecasting, risk tiers, or pricing strategy (renewals plugin: renewal-forecast, risk-assessment, negotiation-prep)
- Between-review value touchpoints outside a renewal window (use `/vbs:value-reinforcement`)
- Objection responses in the commercial meeting (use `/vbs:objection-reframe`, seeded from this plan)

## Typical activation

"Alturo renews in February, build the influence plan" / "assemble the achieved-value summary for the renewal" / "Priya sits on the renewal committee and never saw the results"

---

## Workflow

1. Read config, the account's registry entries, Value Map, EVB texts, touchpoint log, stakeholder map, and the original commitment language. Check runway: 90+ days is the design case; less gets the compression warning and a triaged plan.
2. **Achieved-value summary** (the VBS-101 practice: 90 days pre-renewal): per committed outcome, baseline → realized → recognized status, in their words with their numbers; open gaps stated honestly with the plan for each. Unrecognized achieved value is the priority workstream: recognition, not more delivery, is what is missing.
3. **Committee message map:** per stakeholder (from the influence plan pattern): the value framing in their metric, their likely concern, who delivers the message and when. New-to-the-story stakeholders get the narrative first, ask second.
4. **Validation pass:** explicitly re-confirm the Whys still hold ("can you confirm the goals we set still reflect your priorities?"); a drifted Why Change reframes the entire renewal from continuation to re-discovery, and the plan says so.
5. **Sequenced touchpoints:** dated, owner-assigned, ending before the commercial conversation opens; hand the completed case to the renewals plugin's motion.
6. Save to the account workspace.

## Output contract

Runway verdict first, then the achieved-value summary, message map, and dated sequence. Gaps and unrecognized value lead the workstream list.

## Security & Permissions

Local account workspace and configured reads; no sends, no CRM writes, no commercial terms.

## Trust & Verification

Every value claim traces to registry/Map evidence or is marked open; the validation pass is mandatory, not optional. Anchors: VBS-111 (value-based influence), VBS-113, Achieved Value Summaries for Renewal, Proactive Renewals Over Reactive.
