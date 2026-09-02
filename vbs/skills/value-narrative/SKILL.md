---
name: value-narrative
description: >
  Build a value story from deal evidence using the Story Spine structure
  (setup, challenge, resolution, future vision) in the customer's language,
  linking past or comparable value to the buyer's specific future
  possibilities. Produces narrative variants sized to the moment: a 60-second
  spoken version, a proposal paragraph, and a one-page leave-behind designed
  to survive forwarding to someone who was not in the meeting. Every claim in
  the narrative traces to the qualified promise set or to real evidence.
argument-hint: "[--audience <role> --moment <call|proposal|exec-readout>]"
version: "0.1.0"
deployment_target: plugin
---

# /vbs:value-narrative

Structure prevents rambling; evidence prevents fiction. Anchor: VBS-105, Story Spine.

[PROPOSED]

ETM coordinates: pipeline 4 Demo/Evaluation - 5 Proposal. Supports validation states 3-4 (Value Quantified, Proof Demonstrated); the narrative moves nothing until the buyer verifies its numbers.

---

## Use when

- A proposal, exec readout, or committee moment needs the value story told, not listed
- Translating the qualified promise set and arbitrage math into something a human repeats internally
- A champion needs a forwardable one-pager to sell for you when you are not in the room

## Do NOT use for

- Qualifying which claims may appear (that already happened in `/vbs:outcome-qualification`; this skill consumes its output and adds nothing to it)
- Renewal-specific value summaries with achieved-value evidence (Phase 3 `value-reinforcement` and `renewal-influence-plan` own that moment)

## Typical activation

"Build the value story for the Summit proposal" / "give me the 60-second version for the CFO" / "make a leave-behind Talia can forward"

---

## The structure

Story Spine, from the VBS-105 practice: *Once upon a time* (their current state, their words) → *Then* (the change: what the qualified outcomes make possible) → *Because of that* (the concrete operational difference) → *Ever since then* (the measurable result, from comparable evidence or the stated evaluation plan) → *The moral* (why this matters to this audience's metric now: the Why Now, replayed).

## Workflow

1. Read config, motivation record, qualified promise set, and any comparable-customer evidence in the configured catalog (achievement evidence on the cited OC-IDs).
2. Draft the spine in customer language; catalog IDs annotate the internal copy only. Comparable evidence is attributed honestly ("a customer at your scale," never an implied guarantee); projected results are framed as the evaluation plan, not as promises.
3. Render the variants for the requested moment: spoken 60-second, proposal paragraph, one-page leave-behind (their pains with numbers, mapped outcomes, the arbitrage line, one clear next step).
4. Run the swap test: substitute a competitor's product noun; if the story still works, it is anchored to nothing and gets rewritten around the differentiated mechanism.
5. Save variants to the deal workspace.

## Output contract

The requested variant first, full spine visible. Any claim that could not be evidenced is listed beneath as cut or provisional, never smuggled in.

## Security & Permissions

Local deal workspace and configured catalog; no network access.

## Trust & Verification

Every factual claim traces to the promise set, the motivation record, or named comparable evidence; the swap test result is reported. Anchors: VBS-105 (Story Spine Structure practice), Identify and Communicate Value Achieved.
