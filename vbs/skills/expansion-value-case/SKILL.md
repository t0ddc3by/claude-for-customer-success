---
name: expansion-value-case
description: >
  Frame an expansion opportunity as next-outcome delivery: start from the
  account's realized value and unmet outcomes (Roadmap Demand Register
  entries, deferred catalog mappings, new Whys), run the GROWTH sequence
  (Gather, Review, Outline, Win, Tailor, Handle) to structure the expansion
  conversation, and produce the value case that composes into the csm
  plugin's expansion-business-case for commercial packaging. Expansion sold
  as the continuation of proven value, not as a new product pitch to a
  captive audience.
argument-hint: "[--account <name> --trigger <signal>]"
version: "0.1.0"
deployment_target: plugin
---

# /vbs:expansion-value-case

The best expansion evidence is the value already delivered; the best expansion timing is a fresh Why Now. Anchors: VBS-114, GROWTH framework.

[PROPOSED]

---

## Use when

- Realized value on record creates standing for a next-outcome conversation
- A Roadmap Demand Register entry for this account graduated to a sales-eligible tier
- A trigger (new leader, new team, new use case, growth strain) opens a fresh Why Now
- The csm expansion-business-case needs its value-methodology core supplied

## Do NOT use for

- Commercial packaging, pricing, and CSQL mechanics (csm `expansion-business-case` + rev-ops `csql-tracking` own those; this skill feeds them)
- Expansion pushed onto an account with unrecognized or unachieved core value (the skill flags this as trust-damaging and routes to `/vbs:value-reinforcement` first, per the upsell-without-trust-damage practice)

## Typical activation

"Northwind hit their outcomes, what's the expansion case?" / "the register entry for autonomous outbound just graduated, build the case" / "new CRO at Alturo, frame the expansion"

---

## The GROWTH sequence (from the framework)

**G**ather: realized value, unmet outcomes, new triggers from the record. **R**eview: with the champion, confirm the reading. **O**utline: the next outcome, its catalog anchor and tier, the arbitrage estimate at this account's actual data. **W**in: the stakeholder who owns the new outcome's metric (often not the current champion). **T**ailor: the case in that owner's language, achieved value as the proof layer. **H**andle: the expansion-specific objections ("we haven't finished absorbing phase one") with honest sequencing answers.

## Workflow

1. Read config, registry entries, Value Map, Register entries for the account, stakeholder map, and the current motivation record. Gate check: core committed outcomes unachieved or unrecognized triggers the trust warning and the reinforcement-first routing.
2. Run GROWTH; each step's output is a section. New promises go through `/vbs:outcome-qualification` like any promise: expansion earns no exemption from the catalog rule.
3. Compute the expansion arbitrage using this account's own realized numbers as the evidence base (stronger than any benchmark: their data, their proof).
4. Emit the value case to the account workspace and hand off to csm `expansion-business-case` for packaging; note the CSQL handoff point.

## Output contract

The GROWTH-structured case, qualified promises only, this-account evidence cited. If the gate check failed, the reinforcement plan leads instead of the case.

## Security & Permissions

Local account workspace and configured reads; no CRM writes; no pricing.

## Trust & Verification

Realized-value claims trace to registry entries; new promises carry OC-IDs and tiers; the trust gate is non-skippable. Anchors: VBS-114, GROWTH framework, Upselling Without Damaging Customer Trust.
