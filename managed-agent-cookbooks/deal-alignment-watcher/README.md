# Deal Alignment Watcher: Managed Agent Cookbook

**Plugin:** vbs (Value-Based Selling expansion pack)
**Cadence:** Weekly, Friday 7:00 AM, ahead of pipeline review (configurable)
**Pipeline type:** Depth-0 scan (no subagents; rubric re-application plus deal-axes reads over local records)
**Authoritative behavioral spec:** `vbs/agents/deal-alignment-watcher.md` (Layer 1)

---

## What This Cookbook Does

A Keep-Ready gate verdict from three weeks ago can quietly become Fragile: catalogs update, champions leave, motivation records go stale, and EVB conversations never get scheduled. The Deal Alignment Watcher re-reads the evidence on every late-stage deal weekly (ETM pipeline addresses 5 Proposal and 6 Negotiation/Commit), flags dimension regressions against the last dated gate result, folds in the deal-axes divergence read (a SLIPPING declared-stage-vs-validation divergence is a regression in its own right), and digests one highest-priority fix per deal with the owning skill named. Its most valuable single output is the EVB-unscheduled-at-contract list: the most common silent failure crossing the seam.

**Inputs (all from config; no per-run parameters):**
- `deal_workspace_root`: where per-deal artifacts live (motivation records, promise sets, gate results, commitment drafts, stakeholder maps, deal-axes logs)
- `report_path`: where the weekly digest lands
- `late_stage_definition`: defaults to ETM addresses 5-6
- The configured Outcome Catalog (for tier-freshness checks)

## Architecture

```
Scheduler (weekly)
  │
  ▼
Deal Alignment Watcher (single agent, depth-0)
  ├── Read: config, deal workspaces, catalog, prior digests, deal-axes logs (read output only)
  └── Write: dated digest under report_path ONLY
```

Read and Write only. It re-applies the good-sale-gate rubric as reasoning over records; it runs no engines itself and reads `deal_axes.py read` output where a log exists rather than recomputing instruments. It never writes a deal workspace, never fabricates a verdict for a deal with missing inputs (those are reported unscannable with the prerequisite named), and repeat flags carry a consecutive-weeks count instead of re-alarming.

## Deployment

1. Install the vbs plugin, complete `/vbs:cold-start-interview` (deal workspace convention and report path are collected there).
2. Useful from the first gated deal; ungated late-stage deals are listed as "never gated" with the `/vbs:good-sale-gate` recommendation rather than scored.
3. Schedule weekly, Friday morning, so the digest is on the table for pipeline review.
4. Verify the first run: a dated digest with the roll-up first; every flag citing a record and date.

## Output Spec

One dated digest:
1. **Roll-up:** counts by verdict band; the week's regressions; the EVB-unscheduled-at-contract list; any catalog update that touched multiple deals.
2. **Per-deal entries** (ordered by regression severity): current-vs-prior dimension deltas, the deal-axes divergence verdict and stale-assertion warnings where a log exists, the single highest-priority fix, and the owning skill (`/vbs:outcome-qualification`, `/vbs:three-whys-discovery --revalidate`, `/vbs:stakeholder-influence-plan --movement-check`, `/vbs:value-commitment-builder --capture-evb`, `/vbs:deal-axes-reader`).

## Data-Gap Behavior

Workspace root missing: one-line "no scan" with the path, nothing else. Partial deal records: that deal unscannable with the missing artifact named; the scan continues. Catalog unreachable: dimension-1 checks skipped and labeled; other dimensions still scanned. No deal-axes log: divergence checks skipped for that deal, noted once, not weekly-alarmed.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Everything reports "never gated" | Sellers not running the gate | Adoption issue, not agent issue: start with the deal closest to close |
| Same EVB flag for weeks | The capture conversation genuinely is not scheduled | That is the point; the flag names `--capture-evb` as the fix and counts the weeks |
| Digest silent on a slipping deal | No deal-axes log for it | Start recording evidence via `/vbs:deal-axes-reader`; divergence needs the instrument |
| Agent asked to update a deal record | Scope misunderstanding | It never writes deal workspaces; fixes are executed by sellers through the named skills |
