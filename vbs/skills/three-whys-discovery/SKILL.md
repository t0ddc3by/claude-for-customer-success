---
name: three-whys-discovery
description: >
  Run or prepare Three Whys discovery (Why Change / Why Now / Why Us) for a
  prospect or account, and turn what is learned into a structured alignment
  record that lands in the deal's motivation fields. Use for discovery call
  planning, post-call synthesis, and re-validation when priorities may have
  shifted (renewal prep, stakeholder change, stalled deal). Produces the
  motivation record that downstream skills (good-sale-gate,
  value-commitment-builder, renewal influence) read; discovery that stays in
  prose notes does not survive the handoff.
argument-hint: "[--prep | --synthesize <notes> | --revalidate]"
version: "0.1.0"
deployment_target: plugin
---

# /vbs:three-whys-discovery

Discovery that produces an alignment record, not just notes. Anchor: VBS-103.

[PROPOSED]

ETM coordinates: pipeline 2 Qualified - 3 Discovery. Feeds value validation state 1 (Problem Evidenced) and readiness rung 1 (Pain Evidenced); record outputs via /vbs:deal-axes-reader.

---

## Use when

- Preparing discovery questions for a first or early-stage conversation (`--prep`)
- Synthesizing call notes or a transcript into the structured motivation record (`--synthesize`)
- Re-validating alignment before renewal, after a reorg or champion change, or when a deal stalls (`--revalidate`)
- The deal record's Why Change / Why Now / Why Us fields are empty or stale

## Do NOT use for

- Full call preparation with agenda and role framing (use `/vbs:consultative-call-prep`; it consumes this skill's output)
- Mapping discovered pains to catalog outcomes (use `/vbs:outcome-qualification`, the next step)

## Typical activation

"Prep discovery for the Alturo call" / "here are my notes, pull out the three whys" / "confirm the goals we set last quarter still hold before the renewal conversation"

---

## The framework

Three questions, each with a distinct job:

- **Why Change:** what is broken or costly enough in the current state that doing nothing is irrational? Seek the pain in the buyer's own words plus its business consequence. No credible Why Change means no deal, only a demo audience.
- **Why Now:** what trigger makes this quarter different (leadership change, retention miss, board mandate, growth strain)? No Why Now predicts a stalled deal or a Type 2 aware-inactive account; say so.
- **Why Us:** why this solution over alternatives and over internal build/do-nothing? Must connect to specific, catalog-deliverable differentiators, not generic strengths.

## Workflow

1. Read config (per plugin CLAUDE.md); read the deal record if one exists.
2. `--prep`: generate 3-5 open questions per Why, tailored to the persona and what is already known; include validation questions for anything previously assumed ("can you confirm the goals we set still reflect your priorities?"). One page maximum.
3. `--synthesize`: extract each Why with a verbatim supporting quote, a confidence read (stated directly / inferred / missing), and the business consequence. Missing Whys are named as gaps with the question that would close them, never backfilled with plausible guesses.
4. `--revalidate`: diff the recorded Whys against current evidence; flag drift explicitly ("Why Now was the Q3 board mandate; that passed: what is it now?").
5. Write the motivation record to the deal workspace (CRM motivation fields pattern, VBS-103 practice): `why_change`, `why_now`, `why_us`, each with quote, confidence, date, source.

## Output contract

A motivation record block (the three fields as above) plus a gaps list. Lead with the weakest Why; that is the deal's soft spot.

## Security & Permissions

Operates on user-supplied notes/transcripts and the local deal workspace; no network access; no CRM writes (the record is drafted locally; the user syncs it).

## Trust & Verification

Every Why cites a verbatim quote or is marked inferred/missing; no motivation is ever asserted without provenance. Anchors: VBS-103; Three Whys practices (CRM Motivation Fields, Connect to Achieved and Potential Value).
