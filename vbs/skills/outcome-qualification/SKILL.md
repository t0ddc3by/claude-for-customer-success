---
name: outcome-qualification
description: >
  Map a buyer's stated outcomes and discovered pains to Outcome Catalog
  entries and their canonical 7-tier deliverability, producing the qualified
  promise set for the deal: what may be committed as-is, what only with stated
  conditions or subset boundaries, and what may not be promised at all. Flags
  un-cataloged promises as provisional and routes real-but-undeliverable
  demand to the Roadmap Demand Register instead of silently dropping or
  silently selling it. The step between discovery and any customer-facing
  claim.
argument-hint: "[--from-motivation-record | --check <claim>]"
version: "0.1.0"
deployment_target: plugin
---

# /vbs:outcome-qualification

Every promise gets a catalog anchor before it gets an audience. Anchors: VBS-101/102, the Outcome Catalog and the deliverability taxonomy crosswalk.

[PROPOSED]

ETM coordinates: pipeline 2 Qualified - 5 Proposal. Grounds validation state 2 (Success Criteria Agreed); catalog anchoring per the OC/VR pair.

---

## Use when

- Turning a completed motivation record (three-whys-discovery output) into the deal's qualified promise set
- Checking a single proposed claim, email line, or proposal bullet before it ships (`--check`)
- A buyer asks for something and the seller is unsure whether it is deliverable
- Re-qualifying after a catalog update changes deliverability tiers

## Do NOT use for

- Authoring new catalog entries (that is `rev-ops` catalog skills; this skill reads the catalog, never writes it)
- The overall keepability verdict on the deal (use `/vbs:good-sale-gate`, which consumes this output)

## Typical activation

"Can we promise them automated territory scoring?" / "qualify the promises for the Summit deal" / "check this proposal paragraph against the catalog"

---

## The rule (from the taxonomy crosswalk, restated for sellers)

An outcome may be committed only if its evidence tier is **Fully, Partially, or Conditionally Deliverable** AND it is not roadmap-dependent. Partially Deliverable: state the subset boundary in the commitment. Conditionally Deliverable: state the verifiable conditions. Aspirational and Requires Investigation: not committable; route to the Roadmap Demand Register with the quantified demand attached. Provisional / Not Supported: not committable, full stop.

## Workflow

1. Read config; load the Outcome Catalog from the configured location. If the catalog uses a non-canonical tier vocabulary, stop and flag it against the taxonomy crosswalk rather than guessing mappings.
2. For each buyer outcome or pain: find candidate catalog entries; record OC-ID, deliverability tier, roadmap flag, and mapping confidence (strong / plausible / stretch). A stretch mapping is a finding, not a match.
3. Classify each into: **Commit as-is** / **Commit with stated conditions or subset** / **Roadmap Demand Register** / **Do not promise**. For conditions and subsets, draft the exact sentence the seller will use.
4. Anything with no catalog entry at all: mark "provisional: pending catalog validation" and notify the user that selling it before validation is an FM-C (sales over-commitment) waiting to happen.
5. Output the qualified promise set to the deal workspace; catalog IDs stay in the record, customer language goes in the customer-facing draft.

## Output contract

A table: buyer outcome | OC-ID | tier | classification | commitment language (or routing). Lead with anything in the Do-not-promise and Register buckets; those are the conversations to have before the next call, not after the close.

## Security & Permissions

Reads the configured catalog and local deal workspace; no network access; no catalog writes.

## Trust & Verification

Every classification cites an OC-ID and tier readable in the catalog; provisional flags are never dropped in later drafts. Anchors: VBS-101/102; `vbs-sales-outcome-catalog.md`; deliverability-taxonomy-crosswalk.md.
