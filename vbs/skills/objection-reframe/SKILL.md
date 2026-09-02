---
name: objection-reframe
description: >
  Handle objections with value-focused reframes: prepare the objection map for
  a deal (price, timing, competition, status quo, internal build, past failed
  initiative) with a value-anchored response for each, or work one live
  objection into an honest, non-defensive reframe. Responses lead with ROI,
  outcomes, and partnership rather than discounts or feature rebuttals, and
  they concede what is true: an objection grounded in a real catalog gap gets
  honesty and the Roadmap Demand Register, not spin.
argument-hint: "[--map | --handle <objection text>]"
version: "0.1.0"
deployment_target: plugin
---

# /vbs:objection-reframe

Reframe around value; never around the customer's judgment. Anchor: VBS-115 practices.

[PROPOSED]

ETM coordinates: pipeline 3-6 (any stage). Responses preserve evidence integrity; no instrument moves on seller output.

---

## Use when

- Building the deal's objection map before proposal or committee moments (`--map`)
- A specific objection just landed and the response needs crafting (`--handle`)
- The same objection keeps recurring across deals and needs a canonical response for the team

## Do NOT use for

- Terms-and-price negotiation sessions (use `/vbs:negotiation-prep`; it consumes this map)
- Objections that are really discovery gaps (a buyer who cannot articulate Why Change has no objection to reframe; route to `/vbs:three-whys-discovery`)

## Typical activation

"Map the objections for Summit before the committee readout" / "they said it's too expensive, help me respond" / "Priya keeps raising client-facing complexity"

---

## The pattern

Acknowledge honestly → anchor to value ("here is what you have achieved, or what is at risk if nothing changes, against this investment") → address the specific concern with evidence, a condition, or a mitigation → advance with a question that moves the conversation, not a rebuttal that ends it. The VBS-115 template for price: "let's look at what you've achieved and what's at risk if we don't continue; how does that compare to the investment?"

## Workflow

1. Read config, motivation record, qualified promise set, arbitrage math, and stakeholder plan.
2. `--map`: for each standard category (price, timing, competitor, status quo, internal build, scar tissue from a failed past initiative) plus any stakeholder-specific concerns from the influence plan: write the objection as the buyer would say it, the honest kernel in it, and the reframe per the pattern. Scar-tissue objections get respect and a de-risked path, never dismissal.
3. `--handle`: classify the live objection; check whether it is actually true (a real gap, a real risk); if true, the response concedes it, states the subset or condition from the promise set, or routes the demand to the Register, and reframes around what is deliverable. If misinformed, correct gently with evidence.
4. Every response passes two checks: it cites only qualified promises, and it would survive being read back by the buyer's most skeptical stakeholder.
5. Save the map to the deal workspace; recurring objections get flagged for the team's canonical library.

## Output contract

`--map`: the objection table (objection, honest kernel, reframe, advancing question). `--handle`: the spoken-form response, three sentences maximum, plus the advancing question. Lead with the honest kernel; that is what makes the reframe credible.

## Security & Permissions

Local deal workspace and config only; no network access.

## Trust & Verification

Reframes cite the promise set and arbitrage math; conceded gaps are logged, never buried; no response contradicts the catalog. Anchors: VBS-115 (Value-Focused Objection Handling, Challenging the "Selling Is Bad" Narrative).
