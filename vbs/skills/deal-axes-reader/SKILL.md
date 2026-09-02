---
name: deal-axes-reader
description: >
  Operate the Expanded Triaxial Model's two pre-sale instruments for a deal:
  the value-validation parallel state (Problem Evidenced through Business
  Case Accepted) and the buying-readiness inferred ladder (Pain Evidenced
  through Commitment Evidenced, computed from buyer-verifiable evidence with
  the first missing rung governing). Records evidence events and rep
  assertions, reads the complete triaxial picture of a deal including the
  declared-stage-vs-validation divergence (the slipping-deal signal caught
  structurally), and freezes both final readings at every close outcome for
  the handoff payload and honest win-loss analysis. The engine computes;
  nobody declares an instrument position, ever.
argument-hint: "[evidence|assert|declare-stage|read|close <deal-log>]"
version: "0.1.0"
deployment_target: plugin
---

# /vbs:deal-axes-reader

A pipeline stage is an address; it says nothing about whether the deal is real. These two instruments say whether it is real.

[PROPOSED]

---

## Use when

- Any buyer-verifiable evidence lands (recorded pain call, signed success criteria, buyer-confirmed value model, economic-buyer meeting, MAP tasks completing): record it
- A rep claims a champion exists or legal is reviewing: record the assertion with their name (it moves nothing until corroborated; uncorroborated past 21 days it becomes a warning)
- Reading the complete state of a deal before a review, forecast call, or the good-sale-gate
- A champion departs or evidence dies: invalidate the affected artifacts and let the state fall back honestly
- Any close, won or not: freeze both readings (`close`), producing the AX-1.5.1 payload inputs and the win-loss record

## Do NOT use for

- The keepability synthesis (that is `/vbs:good-sale-gate`, which consumes these readings per the ETM crosswalk)
- Post-sale value tracking (the Value Registry and Value Map own the post-seam instruments; these axes end at close and travel in the payload)
- Moving an instrument on seller output ("delivering the value deck moves nothing; the buyer confirming the numbers in it does": the engine enforces this)

## Typical activation

"Record the pain call for Summit" / "where does this deal really stand?" / "the champion left, invalidate her sign-offs" / "close Alturo as no-decision"

---

## The instruments (ETM §4.2-4.3, implemented verbatim)

**Value validation (parallel state):** five states, each defined over what the buyer verifiably did. The recorded state is the highest with live buyer-verifiable evidence; invalidation drops it back. Divergence against the declared pipeline stage is a first-class read: stage ahead of validation is the slipping deal; validation ahead of stage is a positive signal, reported as one.

**Buying readiness (inferred ladder):** seven rungs, computed by walking up from Pain Evidenced; the first missing rung governs regardless of evidence above it. Framework-neutral: MEDDPICC, SPICED, and BANT constructs seed evidence for the rungs they cover; the rungs they miss must be evidenced directly. Distinct from the ICVP account readiness classification (whether the account is ready to be sold to at all); this ladder asks how real this specific deal is.

## Workflow

1. All operations run through `scripts/deal_axes.py` against the deal's axes log (deal workspace); never re-derive a reading in-context, never hand-edit the log.
2. On `read`, present: validation state with gaps below it, readiness rungs established with the governing gap named, evidence noted above the gap (never credited), divergence verdict, stale-assertion warnings, and the non-verifiable artifacts recorded-but-ignored.
3. On `close won`, hand the frozen readings to `/vbs:value-commitment-builder` for the seam payload; a `validation_shortfall_flag` (won below Business Case Accepted) is stated plainly, never suppressed: onboarding starts with eyes open.
4. On `close lost|no_decision`, the frozen readings are the win-loss record: they separate deals that were never real from deals genuinely lost.

## Output contract

Engine JSON first, one-paragraph interpretation second, leading with the governing gap or the divergence, whichever is worse.

## Security & Permissions

Writes only the deal's own axes log (append-only, this engine is its sole writer; the shared post-sale surfaces are untouched); no network access; evidence refs are pointers to artifacts, not ingested content.

## Trust & Verification

`scripts/deal_axes.py --self-test`: 14 checks covering first-missing-rung governance, seller-sent inertness, invalidation fallback, both divergence directions, staleness warnings, close freezing, and the shortfall flag. Anchors: EXPANDED-TRIAXIAL-MODEL-GUIDE §4.2, §4.3, §5, §6 (HC-3 / AX-1.5.1); etm-conformance-audit-and-crosswalk.md.
