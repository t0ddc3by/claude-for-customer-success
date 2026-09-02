# Loop Runner: Managed Agent Cookbook

**Plugin:** vfa (Value-First Acquisition expansion pack)
**Cadence:** Quarterly, first Monday, 7:00 AM (configurable)
**Pipeline type:** Depth-0 engine orchestration (no subagents; two scoped engine invocations)
**Authoritative behavioral spec:** `vfa/agents/loop-runner.md` (Layer 1)

---

## What This Cookbook Does

The Loop Runner is the quarterly heartbeat of the Value-First Acquisition feedback loop. It executes the Value Registry report with the four-edge write-back payload (R1 catalog, R2 ICVP weights, R3 ICP, R4 PMF decay), routes each edge to its designated consumer, and produces the quarterly loop readout with FM-C/FM-D share as the headline drift metric. Its defining constraint: it is read-and-report, and every gate change it produces is a PROPOSAL requiring explicit human approval. The loop trains the gates on realized-value evidence; this agent is how that training is delivered without ever applying itself.

**Inputs (all from config; no per-run parameters):**
- `registry_path`: the Value Registry JSONL (written only by `/vfa:value-bridge-realization-tracker`)
- `report_path`: where readouts and R2 proposal files land
- `override_budget`: quarterly override cap for the Loop 3 governance section
- Prior-quarter readout (auto-discovered at `report_path`) for trend comparison

## Architecture

```
Scheduler (quarterly)
  │
  ▼
Loop Runner (single agent, depth-0)
  ├── Bash: registry.py report --writeback     ← the only computation; never re-derived in-context
  ├── Bash: icvp_score.py --self-test          ← sanity gate before any weights proposal
  ├── Read: config, prior readout
  └── Write: dated readout + (conditionally) weights-vX.Y.json PROPOSAL
```

No subagents, no MCP servers, no network. The two engine scripts are the only executables it may invoke; their output is quoted, never recomputed. Consumers are named in the readout for humans to execute: R1 to the catalog's writer (`rev-ops.outcome-statement-builder`), R2 via `/vfa:customize --propose-weights`, R3 to `icp-drift-monitor`, R4 as a PMF re-run recommendation.

## Deployment

1. Install the vfa plugin and complete `/vfa:cold-start-interview` (the agent halts on `[PLACEHOLDER]` config).
2. Confirm `registry_path` points at the tracker's registry file and at least one entry exists; otherwise the first run emits the cold-start readout and stops, by design.
3. Schedule quarterly (Claude Code scheduler, Cowork scheduled task, or cron invoking the agent). First Monday 7:00 AM is the shipped default so the readout precedes quarterly business reviews.
4. Verify the first run: a dated readout at `report_path`; if a weights proposal was emitted, confirm it was NOT applied (the `weights.json` in the plugin config must be unchanged).

## Output Spec

One dated markdown readout:
1. **Headline:** achievement rate (value + trend) and FM-C/FM-D share, framed as the drift dashboard.
2. **R1:** per-outcome achievement table addressed to the catalog writer.
3. **R2:** either "no change supported by data" or a proposal file reference with field-by-field diff and the approval route, always labeled PROPOSAL ONLY.
4. **R3/R4:** segment distributions for the ICP rebuild; achievement-rate trend against the PMF decay tripwire (2+ declining readouts recommends a segment PMF re-run).
5. **Loop 3 governance:** override count vs. budget, outcomes of past overridden advances, cold-start-provisional advances due for review.

## Data-Gap Behavior

Empty registry or all-pre-calibration segments: cold-start readout naming counts and the "[Pre-calibration]" posture, zero recommendations. Missing prior readout: values without trends, labeled first-readout. Engine error: surfaced verbatim, no partial aggregates. The agent never fabricates portfolio signal; a thin quarter produces a thin, honest readout.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| "no readout: registry unavailable" | `registry_path` wrong or tracker never ran | Point config at the tracker's file; run one `ingest` |
| Readout says pre-calibration for a busy segment | Under 10 closed entries in that segment | Expected until volume accrues (VFAS gap 4.2); do not force |
| Weights proposal every quarter | Achievement-by-band data genuinely shifting, or noise on small N | Check the n per band in the readout; decline proposals on small-N evidence |
| Proposal was applied without review | Someone edited weights.json directly | Governance breach: restore prior version; all changes route via `/vfa:customize --propose-weights` |
