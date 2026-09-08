# rev-ops
## claude-for-customer-success / rev-ops plugin — v1.1.0

Revenue Operations AI for teams running Claude Code. Covers the full RevOps
mandate: forecasting, pipeline health, annual planning, CRM data quality,
Sales-to-CS revenue continuity, and deal desk governance.

Part of the `claude-for-customer-success` suite. Install alongside `csm/`,
`cs-ops/`, `renewals/`, or `onboarding/` — or standalone.

---

## Who this is for

RevOps leaders, CROs, and CS operations teams who own:
- Revenue forecasting and pipeline review
- Annual planning (territory, quota, comp)
- Sales-to-CS handoff quality and outcome tracking
- Deal desk approval workflows
- Cross-functional GTM alignment

---

## Skills

### Configuration
| Command | What it does |
|---------|-------------|
| `/rev-ops:cold-start-interview` | First-time setup. Reads existing C4CS company profile; asks only RevOps-specific fields. ~5 min if company profile exists, ~15 min from scratch. |

### SA1 — Forecast Intelligence
| Command | What it does |
|---------|-------------|
| `/rev-ops:pipeline-coverage-analysis` | Coverage ratio by segment/rep. Threshold derived from win rate, not a universal 3x. |
| `/rev-ops:forecast-variance-analysis` | Submitted vs. actual; root cause classification. Patterns only after ≥3 deals or ≥2 quarters. |
| `/rev-ops:scenario-modeling` | P10/P50/P90 range forecasts. Feeds annual planning capacity modeling. |
| `/rev-ops:deal-classification` | Independent Commit/Best Case/Pipeline scoring from CRM activity — no rep self-reporting. |

### SA2 — Pipeline Health
| Command | What it does |
|---------|-------------|
| `/rev-ops:deal-health-scoring` | Five-dimension 0–100 health score per deal. Below 50 triggers next-best-action. |
| `/rev-ops:pipeline-velocity-tracking` | Cycle time by segment/rep. Flags deals at 1.5x historical stage average. |
| `/rev-ops:stage-integrity-audit` | Detects stage-skipping, backward movement, and stale stage. Proposals for human review — no autonomous CRM edits. |
| `/rev-ops:next-best-action-recommendation` | Specific interventions for at-risk deals. Every recommendation names what, who, and why. |

### SA3 — Planning Engine
| Command | What it does |
|---------|-------------|
| `/rev-ops:annual-planning-workflow` | Seven-phase gated planning cycle. Invokes `unit-of-growth-calculator` for three-scenario capacity modeling. |

| `/rev-ops:quota-sensitivity-analysis` | Quota achievability at five attainment levels. Flags structurally challenging quotas. |
| `/rev-ops:mid-year-replan-triggering` | Monitors four drift signals. Recommends replan when threshold crossed. |

### SA4 — CRM Data Quality
| Command | What it does |
|---------|-------------|
| `/rev-ops:crm-hygiene-audit` | Overall + rep-level hygiene scorecard: completeness, accuracy, recency. |
| `/rev-ops:duplicate-detection` | Merge candidates with confidence scores. High-confidence batch for approval. No autonomous merges. |
| `/rev-ops:field-completion-monitoring` | Stage gate field tracking. Escalates missing fields 2 weeks before quarter close. |
| `/rev-ops:data-decay-tracking` | Contact/account freshness. Flags enrichment-overdue records, prioritized by account tier. |

### SA5 — Revenue Continuity
| Command | What it does |
|---------|-------------|
| `/rev-ops:deal-to-outcome-tracing` | Links closed/won deals to CS trajectory via OCV catalog. Checks catalog completeness at close; tracks L0–L3 rubric at checkpoints. |
| `/rev-ops:sales-cs-handoff-quality-scoring` | Five-dimension handoff quality score. Below 80 → Linear issue to AE manager, 48h SLA. |
| `/rev-ops:closed-won-to-cs-capacity-modeling` | Three-scenario CS capacity check. Surfaces hiring lead time flag before it's too late. |
| `/rev-ops:growth-model-vs-actuals-tracking` | Three growth vectors vs. UoG plan baseline. Variance memo when any vector diverges past threshold. |
| `/rev-ops:outcome-to-value-tracking` | L0–L3 rubric tracking per account and per OCV entry. Portfolio health view. |
| `/rev-ops:early-churn-downgrade-signal-detection` | Three-tier churn signal model starting at deal close. Tier 1 rule mode on day one; cohort mode when data is available. |
| `/rev-ops:gtm-unified-metrics-pulse` | Five-section weekly cross-functional report. Channel-split: aggregate to #revops-alignment, account-level to #cs-leadership. |

### SA6 — Deal Desk
| Command | What it does |
|---------|-------------|
| `/rev-ops:discount-threshold-monitoring` | Threshold-based approval routing. Tiered by discount depth. Never approves autonomously. |
| `/rev-ops:non-standard-terms-detection` | Off-playbook payment terms, multi-year structures, custom provisions. Routes to Legal or Finance. |
| `/rev-ops:revenue-leakage-scanning` | Deal structure leakage before close. Primary window: Negotiation stage. |
| `/rev-ops:deal-desk-workflow-management` | Full approval chain management: submit → brief → route → decide → log. SLA tracking. |

### ARIA Orchestrator
| Command | What it does |
|---------|-------------|
| `/rev-ops:revenue-brief-generation` | Weekly or monthly executive narrative synthesizing all five agents. |
| `/rev-ops:cross-system-reconciliation` | Traces conflicting numbers to root cause. Never silently resolves conflicts. |
| `/rev-ops:change-communication-packaging` | Rep-facing rationale memo + FAQ + rollout sequence for planning changes. |

---

## Managed Agent Cookbooks

Five headless agents in `managed-agent-cookbooks/` for automated workflows:

| Agent | What it does | Schedule |
|-------|-------------|---------|
| `gtm-pulse-runner` | Runs the weekly GTM unified metrics pulse | Weekly |
| `capacity-monitor` | Monitors CS capacity headroom; fires hiring lead time alerts | Weekly |
| `churn-signal-scanner` | Portfolio churn signal scan; routes Tier 3 to #cs-leadership | Weekly |
| `deal-desk-watcher` | Monitors deals for threshold crossings; tracks SLA compliance | Daily |
| `planning-cycle-orchestrator` | Orchestrates annual/mid-year planning with phase gates | Quarterly |

See each cookbook's `README.md` for deployment instructions and steering examples.

---

## Guardrails

Eight guardrails enforced by every skill's Reasoning Protocol. Not optional.

| # | Guardrail |
|---|----------|
| G1 | Forecast language is not a revenue commitment |
| G2 | Capacity models are structural inputs, not hiring mandates |
| G3 | Compensation outputs require HR + Finance dual review |
| G4 | Territory proposals are drafts until dual-confirmed |
| G5 | Data drives analysis; the rep owns the judgment |
| G6 | No silent data freshness — every output timestamps its data |
| G7 | Risk flags require escalation path and named owner |
| G8 | OCV catalog entries are ratified references, not live commitments |

---

## Architecture Extensions

This plugin follows the `claude-for-customer-success` architecture:

| Extension | File | What it does |
|-----------|------|-------------|
| Domain model | `reference/revops-domain-model.md` | Single source for all formulas, guardrails, bands |
| Config schema | `reference/config-schema.md` | Contract between cold-start and all skills |
| Token economics | `reference/token-economics.md` | Per-skill cost estimates for deployment decisions |
| Cross-skill registry | `reference/cross-skill-registry.md` | Routing table; no hardcoded command strings |
| Version fields | Every SKILL.md frontmatter | Semver versioning on every skill |
| Reasoning Protocol | Every skill body | 6-step pre-output checklist for guardrail enforcement |

---

## External Skills Required

Two SuccessCOACHING skills integrate with this plugin. Install separately.

| Skill | Used by | Purpose |
|-------|---------|---------|
| `outcome-statement-builder` v1.1.0 | SA5 skills | Builds and maintains the OCV Outcome Catalog |
| `unit-of-growth-calculator` v1.1.0 | SA3 annual-planning-workflow | GTM headcount and capacity modeling with benchmarks |

SA5 skills degrade to `[Confidence: Low]` if the OCV catalog is not configured.
SA3 planning workflow requires the UoG calculator for Phase 2 capacity modeling.

---

## Setup

```bash
/rev-ops:cold-start-interview
```

If another C4CS plugin is already installed, cold-start reads your existing
`company-profile.md` and skips company-level questions (~5 min). Otherwise
~15 min for full setup.

---

## File Locations

```
~/.claude/plugins/config/claude-for-customer-success/
├── company-profile.md              # Shared — written by first C4CS plugin cold-start
└── rev-ops/CLAUDE.md               # Rev-ops company profile — written by cold-start
```

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| v1.1.2 | 2026-09-06 | Quoted `"${CLAUDE_PLUGIN_ROOT}"` in `hooks/hooks.json` commands so hooks run from install paths containing a space (desktop app). |
| v1.1.0 | 2026-05-15 | Added `planning-cycle-orchestrator` managed agent cookbook — 5-phase GTM planning cycle with phase-gate governance, HubSpot pipeline criteria, and Slack digest delivery. Completes the 5-cookbook managed agent suite. |
| v1.0.0 | 2026-03 | Initial release — 31 skills across 8 skill areas, 4 managed agent cookbooks (gtm-pulse-runner, capacity-monitor, churn-signal-scanner, deal-desk-watcher). |

---

`claude-for-customer-success / rev-ops` v1.1.0 · Built for Anthropic Claude Code.
Compatible with claude-sonnet-4-6 and claude-opus-4-6.
