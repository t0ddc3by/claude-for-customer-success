---
name: stakeholder-influence-plan
description: >
  Map the buying committee (champions, blockers, skeptics, economic buyer,
  operational users) and produce a per-stakeholder influence strategy using
  the Stakeholder Engagement Ladder and SIMAC-based recommendations tailored
  to what each stakeholder values and fears. Tracks stakeholder movement
  (blocker to neutral to champion) across the deal and flags single-threaded
  deals as a durability risk feeding the good-sale-gate. For complex,
  multi-stakeholder deals and renewal committees.
argument-hint: "[--map | --strategy <stakeholder> | --movement-check]"
version: "0.1.0"
deployment_target: plugin
---

# /vbs:stakeholder-influence-plan

Champions, blockers, and skeptics coexist in every complex deal; influence each on their own terms. Anchor: VBS-110.

[PROPOSED]

ETM coordinates: pipeline 2 Qualified - 6 Negotiation/Commit. Feeds readiness rungs 2 (Power Engaged) and 5 (Decision Process Mapped).

---

## Use when

- A deal involves 3+ stakeholders or any known blocker
- Building or refreshing the committee map after a reorg or new attendee
- Designing the influence approach for one difficult stakeholder (`--strategy`)
- Checking movement before the gate or a committee moment (`--movement-check`)

## Do NOT use for

- Single-call preparation (use `/vbs:consultative-call-prep`, which reads this plan)
- Renewal committee execution inside the renewals commercial motion (renewals plugin owns that; this skill can seed its stakeholder view)

## Typical activation

"Map the Alturo buying committee" / "Priya blocks on client-facing complexity, build me an approach" / "who moved since last month?"

---

## Workflow

1. Read config and the deal record. Inventory stakeholders: role, stance (champion / neutral / skeptic / blocker), what they measurably care about, what they fear, influence weight, and relationship owner. Unknown stances are unknowns.
2. Per stakeholder, build the influence line: frame the value in their metric (from the qualified promise set), address their specific fear with evidence or risk mitigation, and name the ask sized to their stance. SIMAC pattern for recommendations to decision-makers; risk-mitigation-first for blockers (a blocker moved to neutral is a win; do not oversell for champion conversion); air cover and enablement for operational users.
3. Check threading: champion-only deals get the durability warning verbatim ("assuming the champion is still the champion after a reorg can be fatal"); name the second and third threads to open and who opens them.
4. `--movement-check`: diff stances against the last dated map; movement is the metric (VBS-110 practice), stalls are findings.
5. Save the dated map to the deal workspace; the gate reads dimension 3 from it.

## Output contract

The committee table, then per-stakeholder strategies ordered by influence weight, then the threading verdict. Lead with the most dangerous stakeholder, not the friendliest.

## Security & Permissions

Local deal workspace only; no network access; no enrichment lookups in this version.

## Trust & Verification

Stances cite observed evidence (quotes, behaviors, meeting patterns), never vibes; movement is tracked against dated maps. Anchors: VBS-110 (Influence Complex Stakeholders), Stakeholder Engagement Ladder framework.
