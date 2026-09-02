# vbs: Value-Based Selling

[PROPOSED] v0.4.0 (Phases 2-4 + ETM alignment)

The deal stratum of the **Claude for Value-Based Selling** add-on to Claude for Customer Success. Where `vfa` gives revenue leaders the gates that decide which deals should exist, `vbs` gives the seller the craft to work a qualified deal so the outcomes promised equal the outcomes deliverable, and the revenue survives its first renewal.

Grounded in the SuccessCOACHING VBS curriculum (VBS-100 through VBS-115) and its frameworks: Three Whys, GROWTH, Consultative Approach, Stakeholder Engagement Ladder, SIMAC, Story Spine, BATNA-based negotiation. Corpus map: `projects/value-based-acquisition/docs/phase0/distribution-matrix.md`.

## Skills

**Cluster 1: discovery and qualification**

| Skill | Anchor | What it does |
|---|---|---|
| `three-whys-discovery` | VBS-103 | Why Change / Why Now / Why Us discovery producing a structured alignment record |
| `outcome-qualification` | VBS-101/102 | Maps stated buyer outcomes to the Outcome Catalog; flags un-cataloged promises |
| `good-sale-gate` | VBS-100/115 | The signature skill: pre-close keepability verdict, not a win probability |
| `consultative-call-prep` | VBS-104 | Buyer-outcome-oriented call prep per the Consultative Approach |
| `stakeholder-influence-plan` | VBS-110 | Champion/blocker/skeptic mapping with SIMAC-based per-stakeholder strategy |

**Cluster 2: narrative and commercial craft**

| Skill | Anchor | What it does |
|---|---|---|
| `value-narrative` | VBS-105 | Story Spine value story from evidence |
| `negotiation-prep` | VBS-112 | BATNA, value exchange, calibrated questions; value-led, not concession-led |
| `objection-reframe` | VBS-115 | Value-focused objection handling with prepared reframes |

**ETM alignment (2026-09-02):** every craft skill is bound to Expanded Triaxial Model pipeline coordinates and instrument feeds per `etm-conformance-audit-and-crosswalk.md` (value-based-acquisition/docs/specs/). New skill:

| Skill | Anchor | What it does |
|---|---|---|
| `deal-axes-reader` | ETM §4.2-4.3, §5 | The two pre-sale instruments: value-validation state and buying-readiness ladder (first-missing-rung, buyer-verifiable evidence only, divergence reads, close freezing with validation_shortfall_flag). Engine: `scripts/deal_axes.py` |

**Cluster 3: the boundary**

| Skill | Anchor | What it does |
|---|---|---|
| `value-commitment-builder` | VBS-107/108, Value Registry | Drafts Registry commitment entries at close with verbatim EVB discipline; hands to the vfa tracker (single writer) |
| `sale-quality-review` | gate rubric, FM taxonomy | Post-close was-the-sale-good verdict with FM-C/FM-D exposure prediction; feeds Gate 0 beside handoff completeness scoring |

**Cluster 4: post-sale commercial depth**

| Skill | Anchor | What it does |
|---|---|---|
| `value-reinforcement` | VBS-106 | Between-review value touchpoints from registry evidence |
| `renewal-influence-plan` | VBS-111/113 | 90-day value-based renewal influence campaign; hands the case to the renewals plugin's motion |
| `expansion-value-case` | VBS-114, GROWTH | Expansion framed as next-outcome delivery with a trust gate; feeds csm expansion-business-case |
| `team-vbs-diagnostic` | VBS-115 | Team value-communication audit, phased adoption plan, Start/Stop/Change playbooks |

Plus `cold-start-interview` and `customize` (config pair, suite convention).

## Managed agent (Phase 4)

`deal-alignment-watcher` (weekly): re-checks late-stage deals for keepability drift (catalog tier changes, champion departures, stale motivation records, unscheduled EVBs) and digests fixes per deal. Read-and-report; scoped Write to its own digest only; never fabricates a verdict for a deal with missing inputs.

## Boundaries

Account-level value-fit gating belongs to `vfa` (`icvp-composite-scorer`); this plugin works deals that cleared it (or scores them deal-level via `good-sale-gate`). Renewal pricing, discount authority, and commercial terms belong to the `renewals` plugin; `vbs` supplies negotiation and influence methodology up to that boundary. Catalog writes route through `rev-ops`; `vbs` drafts, never commits.

Install independently; composes with `vfa`, `handoff`, `csm`, `renewals`, and `rev-ops`.
