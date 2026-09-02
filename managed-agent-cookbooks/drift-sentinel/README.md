# Drift Sentinel: Managed Agent Cookbook

**Plugin:** vfa (Value-First Acquisition expansion pack)
**Cadence:** Monthly, first business day, 8:00 AM (configurable)
**Pipeline type:** Depth-0 aggregation (no subagents, no engine runs; pure reads over local records)
**Authoritative behavioral spec:** `vfa/agents/drift-sentinel.md` (Layer 1)

---

## What This Cookbook Does

Quarterly is the loop's cadence; sellability drift moves faster. The Drift Sentinel keeps three early-warning surfaces visible monthly: emerging segments the ICP keeps ignoring (active Shadow-ICP clustering, per the Phase 0 ruling that triggers on realized value rather than close-rate), the override reflex under pipeline pressure (cohort audit against the configured budget), and the FM-C/FM-D exposure trend from close-time reviews and churn records. It surfaces; humans decide. Nothing it produces changes a gate, a classification, or a config.

**Inputs (all from config; no per-run parameters):**
- `report_path`: where dated sentinel reports land
- `override_budget`: the quarterly cap it audits against
- Record locations: ICVP score outputs (with `shadow_icp_flag` and `override` blocks), `sale-quality-review` cohort records, `churn-analysis` FM outputs, prior sentinel reports

## Architecture

```
Scheduler (monthly)
  │
  ▼
Drift Sentinel (single agent, depth-0)
  ├── Read: scored-prospect records, review records, churn FM records, priors
  └── Write: dated report under report_path ONLY
```

Read and Write only; no Bash, no MCP, no sends. The Shadow-ICP trigger definition is the realized-value one: 2+ accounts from the same emergent segment reaching a positive Value Bridge realization fires a routing to ICP redefinition; anything below threshold is a labeled watch item.

## Deployment

1. Install the vfa plugin, complete `/vfa:cold-start-interview` (override budget and report path are collected there).
2. Volume prerequisite: the sentinel is useful once ICVP scoring runs regularly; on a fresh install its first months will correctly report "no records this period."
3. Schedule monthly, first business day; it deliberately runs between loop-runner quarters.
4. Verify the first run: a dated report; any clusters present carry counts and either a fired-trigger routing or a "small-N: watch, do not act" label.

## Output Spec

One dated report, three sections:
1. **Shadow ICP:** fired triggers first (routed to the next `icp-drift-monitor` / ICP Step 9 run), then watch items with counts.
2. **Override audit:** quarter-to-date count vs. budget; each override with owner and hypothesis; outcomes of overridden advances where recorded; budget breach flagged to the Loop 3 reviewer.
3. **FM exposure trend:** FM-C/FM-D share month over month; per-account match/divergence where both a sale-quality-review prediction and a churn FM class exist (the gate-calibration signal).

## Data-Gap Behavior

No ICVP outputs: says so, invents no clusters. Sparse records (n < 5 on any surface): counts reported, small-N label, trend claims suppressed. Missing priors: snapshot labeled no-baseline. Conflicting FM records for one account: both reported with sources, never silently resolved.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Report always empty | ICVP scorer outputs not landing where config points | Align the scorer's output workspace and the sentinel's record locations |
| Same watch item every month, never firing | Cluster real but no Value Bridge realization yet | Correct behavior; the trigger is realized-value on purpose. Nominate accounts via the ICVP quiet lane if conviction is high |
| Override budget breached repeatedly | Pipeline-pressure reflex | That is the finding; take it to the Loop 3 review, not to the agent |
| Sentinel asked to reclassify a segment | Scope misunderstanding | It cannot and will not; ICP changes route through icp-drift-monitor and Step 9 |
