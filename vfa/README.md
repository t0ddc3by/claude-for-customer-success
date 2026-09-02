# vfa: Value-First Acquisition

[PROPOSED] v0.3.0 (Phases 1 + 3 + 4)

The system stratum of the **Claude for Value-Based Selling** add-on to Claude for Customer Success. Where the `vbs` plugin (Phase 2) gives sellers the craft to work a deal well, `vfa` gives revenue leaders the gates and feedback loops that decide which deals should exist at all: the Value-First Acquisition System's answer to "who should want to buy?" rather than "who can we sell to?"

Governing plan: `projects/claude-for-customer-success-portal/docs/plans/claude-for-vbs-addon-proposal.md`. Methodology corpus: `projects/value-based-acquisition/` (VFAS capstone, PMF Methodology, ICP Methodology) plus the ICVP corpus in `projects/outcome-catalog/`.

## Skills

| Skill | VFAS layer | What it does |
|---|---|---|
| `pmf-sean-ellis-survey-analyzer` | L1 | Sean Ellis survey scoring with HXC segmentation; PMF verdict per segment |
| `pmf-retention-curve-classifier` | L1 | Cohort retention curve classification against stage/category PMF thresholds |
| `icp-scorecard-builder` | L2 | Weighted fit+intent ICP scorecard with tiered routing and explainability |
| `icp-drift-monitor` | L2 / loop R3 | ICP drift and misfit detection from segmented NRR and churn root-cause data |
| `icvp-composite-scorer` | L3 | The value-fit gate: ICVP Composite Score (100-pt, 8-component), readiness classification, value arbitrage, audit trail. Spec: `icvp-composite-score-spec-v1.0.md` |
| `value-bridge-realization-tracker` | L6 / loop R1-R4 | The Value Registry's single writer: entry lifecycle, Bridge discipline enforcement, FM classification, quarterly write-back payload. Engine: `scripts/registry.py` |
| `deliverability-taxonomy-reconciler` | L5/L7 | Executable Phase 0 crosswalk: vocabulary detection, canonical mapping, sales-eligibility rulings. Engine: `scripts/taxonomy_reconcile.py` |
| `cold-start-interview` | config | First-run configuration interview producing the vfa practice config |
| `customize` | config | Targeted config updates and `--show` review |

## Managed agents (Phase 4)

| Agent | Cadence | Role |
|---|---|---|
| `loop-runner` | Quarterly | Runs the R1-R4 write-back; every gate change emitted as a human-approval PROPOSAL |
| `drift-sentinel` | Monthly | Active Shadow-ICP clustering, override-cohort audit, FM-C/D trend; watch-and-report only |

Both agents are read-and-report with scoped Write to their own report files; neither touches the Registry, catalog, weights, or any config. Optional skills `jtbd-starter-set-generator` (JTBD ceiling + quiet-segment counterweight) and `motion-fit-icvp-reconciler` (the three Step 5/6/9 bindings + red-team C1/M4 corrections) shipped in v0.3.0.

## Skill provenance

The four L1/L2 skills are synced from workspace canonical (`claude-cowork/skills/<name>/`); canonical wins on drift. `icvp-composite-scorer` is authored here against the version-locked spec at `projects/value-based-acquisition/docs/specs/icvp-composite-score-spec-v1.0.md`.

## Governance defaults (non-negotiable, per VFAS §4.8)

Readiness triage always runs (Type 1/2 archive, only Type 3 advances); every advanced prospect carries a written dollar cost-of-inaction with a confidence tier; overrides are budgeted, tagged, and reviewed as a cohort; low signal density defers research, never disqualifies; escalation is arbitrage-gated, decoupled from company size. Scoring weights are configuration (`icvp-composite-scorer/config/weights.json`); the R2 feedback loop proposes new weight versions and a human approves every re-fit.

Install independently; composes with `rev-ops` (catalog write path), `handoff` (Gate 0), and, when it ships, `vbs`.
