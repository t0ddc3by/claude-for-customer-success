---
name: deliverability-taxonomy-reconciler
description: >
  Pre-flight governance check for deliverability vocabulary: scan any catalog,
  skill file, proposal, or webapp artifact to detect which tier system it uses
  (canonical 7-tier, Product Spec governance 4-tier, entry-builder subset, or
  historical v1.0), map every legacy value to the canonical two-axis model
  (evidence tier + roadmap-dependent flag) via the Phase 0 crosswalk, and
  validate individual tiers against the single sales-eligibility rule before
  any claim gate or deliverability-multiplier computation runs. Flags
  pre-canonical artifacts for the re-tag backlog rather than silently
  translating them.
argument-hint: "[<artifact> | --check-tier \"<tier>\" [--roadmap-dependent]]"
version: "0.1.0"
deployment_target: plugin
---

# /vfa:deliverability-taxonomy-reconciler

When qualification vocabulary is ambiguous, the softest bar wins under pressure. This skill removes the ambiguity.

[PROPOSED]

---

## Use when

- Before any ICVP scoring run or vbs outcome-qualification pass against a catalog not yet confirmed canonical
- A single tier value needs a committable/not-committable ruling (`--check-tier`)
- Auditing an artifact (catalog file, skill, proposal, webapp config) for pre-canonical vocabulary
- Working the re-tag backlog from the Phase 0 crosswalk (entry-builder skills, webapp gapStatus, legacy examples)

## Do NOT use for

- Assigning a deliverability tier to a new outcome (evidence assessment belongs to the catalog authoring skills against the quality rubric)
- Editing artifacts it flags (it reports; humans or the owning skills re-tag)

## Typical activation

"Is this catalog on the canonical taxonomy?" / "can we commit a Roadmap Dependent outcome?" / "scan the proposal for legacy tier language"

---

## The rule it enforces

An outcome is sales-committable only if its canonical evidence tier is Fully, Partially, or Conditionally Deliverable AND roadmap-dependent is false. Partially requires the subset boundary stated; Conditionally requires the verifiable conditions stated; Aspirational and Requires Investigation route to the Roadmap Demand Register; roadmap-dependent anything is blocked until its graduation trigger (GA release plus joint CS/Product review).

## Workflow

1. Run `scripts/taxonomy_reconcile.py` on the artifact or tier; never eyeball-map vocabulary in-context.
2. Canonical result (exit 0): proceed; say so in one line.
3. Pre-canonical result (exit 2): present the detected system, the occurrence counts, and the crosswalk mappings; add the artifact to the re-tag backlog with its priority from the Phase 0 crosswalk §3; downstream computation may proceed using the mapped canonical values, with the mapping stated in the output it feeds.
4. `--check-tier` rulings are quoted verbatim into whatever claim gate asked.

## Output contract

Detection verdict first, then mappings and rulings. A flagged artifact always names its re-tag priority; nothing is silently translated without the translation being visible.

## Security & Permissions

Reads user-named local artifacts only via the bundled stdlib script; no network access; no writes.

## Trust & Verification

`scripts/taxonomy_reconcile.py --self-test` (10 checks covering every crosswalk row and eligibility ruling). Crosswalk source: `deliverability-taxonomy-crosswalk.md` (Phase 0), which adopts the outcome-catalog reconciliation memo's evidenced ruling (188/188 production entries on the 7-tier system).
