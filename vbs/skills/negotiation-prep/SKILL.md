---
name: negotiation-prep
description: >
  Prepare a value-led negotiation: BATNA analysis for both sides, the value
  exchange map (what each side gives and gets beyond price), calibrated
  questions to surface constraints, anchor and concession planning with
  non-price levers first, and the walk-away line. Leads every move with
  delivered and deliverable value rather than discount; stops at the
  configured commercial boundary (pricing and discount authority belong to
  whoever owns them, typically the renewals plugin or deal desk).
argument-hint: "[--deal <name> --moment <initial|renewal-adjacent|expansion>]"
version: "0.1.0"
deployment_target: plugin
---

# /vbs:negotiation-prep

Negotiation is alignment on value with terms attached, not a discount schedule with a meeting attached. Anchor: VBS-112.

[PROPOSED]

ETM coordinates: pipeline 6 Negotiation/Commit. Draws on validation state 5 (Business Case Accepted) and readiness rungs 6-7; a Business Case not yet accepted is surfaced as the negotiation risk it is.

---

## Use when

- Commercial conversation is imminent on a new deal or expansion
- The buyer has signaled price pressure and the seller needs the value-led response ready
- Preparing the concession plan before pressure exists, which is the only time it can be planned

## Do NOT use for

- Setting price, discount floors, or approving terms (commercial boundary; route to the configured owner)
- Renewal negotiation execution (renewals plugin's negotiation-prep owns that motion; this skill covers the methodology and pre-renewal moments)
- Objection handling outside a terms context (use `/vbs:objection-reframe`)

## Typical activation

"Prep the commercial conversation for Alturo" / "they asked for 20 percent off, get me ready" / "map our BATNA before Thursday"

---

## Workflow

1. Read config (including the commercial boundary), the gate result, qualified promise set, arbitrage math, and stakeholder plan. A Fragile gate verdict gets surfaced first: negotiating a fragile deal harder does not make it keepable.
2. **BATNA, both sides:** yours (pipeline strength, this deal's real alternatives) and theirs (status quo cost from the motivation record, competitor fit, internal build). Their BATNA analysis is where the cost-of-inaction number does its work.
3. **Value exchange map:** levers beyond price on both sides: scope phasing, term length, payment timing, reference/advocacy participation, evidence-plan commitments, rollout support. Ordered by cost-to-you versus value-to-them asymmetry; best levers are cheap for you and valuable for them.
4. **Calibrated questions** (open, "how/what" form) to surface the real constraint behind a demand: "what does your approval process need to see?" / "how would you use the difference if we met that number?"
5. **Anchor and concession plan:** the value anchor restated before any number moves (achieved plus deliverable value against their cost of inaction); concessions sequenced non-price-first, each traded never given, each paired with a get.
6. **Walk-away line:** the terms under which this becomes a bad sale (promises beyond the catalog, economics below credible arbitrage) stated before the meeting, because it cannot be found during one.
7. Save the prep sheet to the deal workspace.

## Output contract

One sheet: BATNA summary, exchange map, five calibrated questions, concession sequence, walk-away line. The value anchor paragraph is written out verbatim, ready to say.

## Security & Permissions

Local deal workspace and config only; no network access; produces no terms, offers, or approvals.

## Trust & Verification

Every number traces to the deal record's arbitrage math; every lever respects the configured commercial boundary; the walk-away line is explicit. Anchors: VBS-112 (BATNA, value exchange, calibrated questions), Value-Focused Negotiation practice.
