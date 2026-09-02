---
name: motion-fit-icvp-reconciler
description: >
  Reconcile a Motion-Fit positioning exercise against the ICVP evidence:
  verify Step 6's "who cares a lot" segment is actually the value-arbitrage
  concentration the composite scores show (not a firmographic or reachability
  segment wearing value language), enforce the governed-exception protocol on
  the "broader reach" escape hatch, confirm every Step 5/9 claim cites a
  sales-eligible catalog OC-ID, and apply the red-team corrections: the
  declared motion is a provisional hypothesis until the confirm checkpoint,
  and the segment definition must name a concrete non-fit example. The front
  door's value-fit brain.
argument-hint: "[--step6 <segment-def> | --claims <positioning-doc> | --exception <justification>]"
version: "0.1.0"
deployment_target: plugin
---

# /vfa:motion-fit-icvp-reconciler

Motion-Fit stays the front door; ICVP is its brain, the catalog its conscience. Anchors: motion-fit-positioning-methodology Steps 5/6/9/12, VFAS gap 4.10, red-team findings C1 and M4.

[PROPOSED]

---

## Use when

- A Motion-Fit Step 6 segment definition is drafted and needs the value-concentration check before sign-off
- Positioning copy (Step 5 attribute-to-value work or Step 9 claims) is ready for the claim gate (`--claims`)
- Someone invokes the "broader reach" escape hatch and the governed-exception record must be produced (`--exception`)
- Step 12's quarterly re-validation runs and positioning should be checked against the latest registry write-back

## Do NOT use for

- Running the Motion-Fit playbook itself (the methodology doc owns the twelve steps; this skill audits three seams in it)
- Scoring prospects (that is `icvp-composite-scorer`; this skill consumes its outputs)
- Brand-voice distinctiveness review (out of scope per the red-team's M8 boundary; reference a brand-voice discipline for that)

## Typical activation

"Check the Step 6 segment against the ICVP scores" / "gate these positioning claims" / "we need broader reach this quarter, record the exception"

---

## The three bindings (from the Phase 0 architecture, made operational)

1. **Step 6 is produced by, or reconciled against, ICVP evidence.** The drafted segment is compared with the actual distribution of Prime/Strong composite scores and arbitrage concentration. A segment whose definition predicts the high-arbitrage population is confirmed; a segment defined on firmographics or reachability that diverges from the value concentration is flagged with the divergence shown. Per the red-team's craft bar, a confirmed segment must also name at least one concrete non-fit example; a definition that excludes nobody defines nothing.
2. **The escape hatch is a governed exception, never a default.** "Unless revenue targets explicitly require broader reach" requires: the named revenue target, the explicit acceptance of lower expected realized value (in writing), an expiry or review date, and registration in the Loop 3 review. This skill produces that record; without all four elements it declines to bless the broadening.
3. **Steps 5/9 inherit the claim gate.** Every market-facing claim cites a catalog OC-ID at a sales-eligible tier (reconciler pre-flight runs `deliverability-taxonomy-reconciler` when vocabulary is unconfirmed) or carries the explicit "provisional: pending catalog validation" flag. Unanchored claims are listed for rewrite, not silently passed.

Plus the red-team corrections this skill enforces wherever it touches the playbook's outputs: the declared motion (Step 1) is treated as a provisional hypothesis until the Motion Hypothesis Checkpoint confirms it against surfaced buying-committee evidence (C1), and any motion-fit assertion must state the evidence that would falsify it, not just the reasoning that supports it (M4).

## Workflow

1. Read config, the ICVP score records for the candidate population, the current catalog, and the latest registry write-back if present.
2. Run the requested binding check; show the evidence both ways (what the draft claims, what the scores show).
3. Emit the verdict record to the positioning workspace: confirmed / flagged with divergence / exception-recorded, each with the evidence table. Step 12 runs append to the same record so positioning drift is trended against registry evidence, not re-argued from scratch.

## Output contract

Verdict first, evidence table second, required rewrites or missing exception elements listed explicitly. This skill blesses, flags, or records; it never rewrites positioning itself.

## Security & Permissions

Local records and configured catalog only; no network access; no writes outside the positioning workspace record.

## Trust & Verification

Every verdict cites score records and OC-IDs; exception records are complete or refused; C1/M4 corrections are applied verbatim from the red-team roadmap. Anchors: motion-fit-positioning-methodology, red-team-report-motion-fit-positioning-playbook (C1, M4, craft bars), VFAS gap 4.10, deliverability-taxonomy-crosswalk.
