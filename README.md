<p align="center">
  <img src="./public/claude-for-cs-hero.png" alt="Claude for Customer Success" width="100%"/>
</p>

[![License](https://img.shields.io/badge/license-Apache%202.0-34A7D2)](./LICENSE)
[![Latest Release](https://img.shields.io/github/v/release/t0ddc3by/claude-for-customer-success)](https://github.com/t0ddc3by/claude-for-customer-success/releases)
[![Last Commit](https://img.shields.io/github/last-commit/t0ddc3by/claude-for-customer-success)](https://github.com/t0ddc3by/claude-for-customer-success/commits)
[![Plugins](https://img.shields.io/badge/plugins-6-34A7D2)](./dist/)
[![Skills](https://img.shields.io/badge/skills-81-2B89AC)](./csm/)
[![Built for Claude](https://img.shields.io/badge/built%20for-Claude%20Code%20%7C%20Cowork-24718E)](https://claude.com/product/cowork)
[![Changelog](https://img.shields.io/badge/changelog-Keep%20a%20Changelog-90C83D)](./CHANGELOG.md)

A reference implementation showing what AI-native Customer Success looks like when built on deep domain knowledge — not a deployment-ready product, but a working demonstration of what's possible and what a minimum viable architecture requires.

Six Claude Code/Claude Cowork plugins covering every function in a modern CS organization: CSMs, CS Ops, renewals specialists, onboarding teams, RevOps (for Customer Success), and the infrastructure that connects them. Methodology-opinionated (SuccessCOACHING Customer Success methodologies and frameworks), tool-agnostic.

> New here? Start with **[QUICKSTART.md](./QUICKSTART.md)** — install in 60 seconds. This README is the full reference.

Everything here is available two ways from one source: install it as a **[Claude Cowork](https://claude.com/product/cowork)** or **[Claude Code](https://claude.com/product/claude-code)** plugin, or deploy it through the **[Claude Managed Agents API](https://platform.claude.com/docs/en/managed-agents/overview)** behind your own workflow engine. Same system prompt, same skills — you choose where it runs.

---

## Who This Document Is For

This README serves three audiences. Jump to the section most relevant to you.

**CS leaders and practitioners** using this as a reference for what AI-enabled CS looks like in practice: read [Plugins](#plugins), [Methodology](#methodology), and [Managed Agents](#managed-agents). The plugin and agent breakdown shows what capability coverage across the full lifecycle actually requires — scope, skill count, and architectural decisions most point solutions never reach.

**Operators and developers** building on or adapting the suite: read [Architecture Extensions](#architecture-extensions), [Skill Design](#skill-design), [File Locations](#file-locations), and [Documentation](#documentation). The machine-readable capability model and cross-skill registry are your primary reference artifacts.

**Architects** evaluating the design as a pattern for building multi-plugin suites: the [Methodology](#methodology) section explains why domain knowledge is the real work, and the [Architecture Extensions](#architecture-extensions) section documents the six structural decisions that make an 81-skill coordinated suite maintainable.

---

## Plugins

| Plugin | Who it's for | Core skills |
|--------|-------------|-------------|
| [`csm/`](./csm/) | Customer Success Managers on daily account work | Account research, QBR prep, success plans, health review, risk flags, TARO plays, value statements |
| [`cs-ops/`](./cs-ops/) | CS Operations handling portfolio analytics and systems | Health model review, segmentation, capacity planning, playbook audits, data quality |
| [`renewals/`](./renewals/) | Renewals managers and AMs owning GRR/NRR | Renewal forecasting, expansion signals, churn analysis, negotiation prep, contract review |
| [`onboarding/`](./onboarding/) | Onboarding teams and implementation managers | Kickoff prep, onboarding plans, milestone tracking, TtV review, handoff documentation |
| [`rev-ops/`](./rev-ops/) | CS revenue operations — the infrastructure CS needs to report and forecast like a revenue center | CRM data quality, expansion and renewal pipeline, forecasting, quota and incentive planning, deal desk governance, outcome-to-value tracking, revenue leakage scanning |
| [`auq-resilience/`](./auq-resilience/) | Infrastructure for all teams using interactive workflows | Fallback protocol when `AskUserQuestion` fails to render; T1/T2/T3 recovery hooks (Claude Code) plus the `/auq` command for Cowork |

Each plugin installs independently. Install only what your team needs.

The rev-ops plugin carries the largest footprint (34 of the 81 total skills) and acts as the portfolio intelligence and revenue operations layer for the suite. The auq-resilience plugin is optional infrastructure: it ships no skills (one command, `/auq`) but makes interactive AUQ prompts resilient to render failures across all five CS plugins — via hooks in Claude Code, and via the `/auq` command plus per-plugin `CLAUDE.md` rules in Cowork.

All six plugins are distributed as pre-built `.plugin` files in [`dist/`](./dist/).

### A note on rev-ops for CS

These plugins are organized by function, not by role. Several of them — rev-ops in particular — exist because the capability is missing from most CS organizations, not because there's a dedicated person to own it.

The core problem: CS teams that want to be treated as a revenue center need to operate like one. That means owning expansion and renewal pipeline visibility, providing forecasting guidance on both, and reporting on revenue outcomes the way sales does. Most CS organizations don't have this infrastructure. Rev-ops for CS is the part of CS Ops that fills that gap.

Within the rev-ops plugin, four skill clusters are not optional enhancements — they are blockers. A CS organization missing them is running blind on its most important commercial responsibilities:

**CRM Data Quality** (3 skills) — Garbage in, garbage out. Clean CRM data is a prerequisite for every other revenue operation. Health signals, pipeline forecasts, and expansion models all degrade without it.

**Forecasting and Pipeline** (4 skills) — CS needs to visualize and forecast expansion and renewal pipeline the same way sales forecasts new business. Without this, CS leadership cannot make credible revenue commitments or defend budget.

**Planning and Incentive** (5 skills) — Critical for quota-carrying CSM organizations. Compensation design, quota setting, and attainment tracking require the same rigor in CS as in sales.

**Deal Desk and Commercial Terms** (3 skills) — Deal desk serves two functions in CS: bridging the handoff from sales (ensuring commercial terms land correctly with the CS team) and governing expansion sales that originate inside the CS motion. Both are frequently unmanaged.

If your CS organization is not quota-carrying and has no expansion pipeline accountability, some of these clusters may not apply. If it is, they are the foundation everything else runs on.

---

## Methodology

The agents and skills in this suite are tools. What makes the solution work is the domain knowledge underneath them.

Customer Success and SaaS revenue operations are complex systems. Without deep, structured domain knowledge encoding how these systems actually behave — how customers move through a lifecycle, how value is realized, how churn signals accumulate, how renewal motions work — agentic solutions stay point solutions. They make individual tasks faster. They don't change what's possible. They can't deliver the capability addition that is the actual promise of agentic AI: doing things that weren't previously achievable, not just doing existing things more efficiently.

The reason this domain resists point solutions is structural. The customer lifecycle isn't a sequence of independent tasks. It's a complex adaptive system. Value doesn't arrive at a single stage; it threads through the entire relationship, evolving from theoretical (the outcome promised at sale) to demonstrated (evidence accumulated through adoption) to networked (the expanded value a customer builds on top of your product over time). A tool that optimizes one stage in isolation — faster QBR prep, better renewal forecasting — doesn't touch this progression. It accelerates a piece of work without changing what that work produces.

Effective lifecycle management creates reinforcing feedback loops across CLV, CAC recovery, revenue predictability, and competitive differentiation. Capturing those requires understanding how the stages interlock, not just executing them faster.

### What this suite is not

Most vertical AI plugins are task accelerants. A pitch-deck agent compresses the analyst work inside one stage of a deal process. A contract renewal-watcher screens a document portfolio faster than a paralegal can. Both are genuinely useful. Neither changes what the practitioner does on either side of that moment: the mandate conversation still happens, the negotiation still happens, the close still happens. A human holds the arc. The agent handles one artifact cluster within it.

That model works for domains where the practitioner workflow is a sequence of largely independent tasks. Legal contract review is a bounded artifact problem. Pitch deck preparation is a bounded research-to-document problem. Automating either changes the speed at which an individual deliverable gets produced.

Customer Success doesn't decompose that way. The relationship doesn't have discrete deliverables at each stage — it has a progression, and the quality of that progression determines whether the relationship compounds or deteriorates. An agent that makes QBR prep faster doesn't change the arc. An agent that monitors health signals, diagnoses adoption gaps, prescribes the right motion, builds the expansion case, protects advocates, and reconstructs the churn story — across 15 agents spanning every stage from onboarding through non-renewal — changes what's possible for the team running it.

This suite is built on **SuccessCOACHING** Customer Success Management methodologies because those methodologies are what makes the domain knowledge operational. The **TARO Playbook framework** (Trigger, Action, Resource, Outcome) encodes how CS practitioners should respond to account signals. The **Customer Lifecycle** (Onboarding → Adoption → Value Realization → Renewal/Expansion) encodes how customer relationships actually progress. The **Customer Value Chain** (Product Capabilities → Deliverable Outcomes → Desired Outcomes → Business Goals → Expected Value → Realized Value → Impact) maps how product capabilities transform into business impact — the value transformation mechanism operating within and across those lifecycle stages. The **Two-Layer Outcome/Value Model** separates what the product can deliver at the market level from what it has delivered for a specific account.

These aren't decorative. They are the guiding intelligence of every skill in the suite. A skill without this structure is a more efficient way to produce a document. A skill built on it can reason about whether the right action is being taken at the right lifecycle stage for the right reason.

The skills carry that reasoning. You don't need prior experience with the SuccessCOACHING frameworks. They're encoded into the design of the plugins. Cold-start interviews introduce relevant methodology concepts contextually, tied to your actual accounts and tools.

### Why SuccessCOACHING

The choice isn't arbitrary. Over the past two-plus years, SuccessCOACHING has been building the structural foundations that make deep-domain agentic systems possible for Customer Success.

The **CSMBOK Knowledge Graph** maps the body of knowledge for Customer Success as a discipline — concepts, competencies, relationships, and the connections between them — in a form that machines can traverse and reason over, not just search. What's encoded in it is the full SuccessCOACHING corpus: 12+ years of CS education and advisory work, every curriculum, research paper, framework, playbook, coaching engagement, and published article the firm has produced. Behind that institutional record sits the founding team's 30+ years each in the field — practitioner experience that predates the Customer Success job title itself. The **CS Skill Graph** maps what CS professionals need to be able to do at each career stage and role type, grounded in observable behaviors rather than job description language. Together they give the agents a shared semantic foundation for the domain that no prompt engineering exercise can replicate.

The **Agentic Capability Graph** takes that foundation and maps it to the Customer Lifecycle and Value Chain specifically — what capabilities are needed at each stage, how they connect across stages, and where agent intervention changes outcomes rather than just accelerating tasks. This is what made it possible to design 15 agents that cover the full arc rather than 15 agents that each do one thing faster.

The **Training/Fine-tuning Datasets** and **Developer Toolkits** built alongside these graphs provide the technical scaffolding for AI-enabled CS solutions: structured content representations, entity models, intent taxonomies, and query-to-capability mappings that let skills reason about CS work the way a senior practitioner would.

This suite is one application of that research — a **working reference implementation** and **customizable harness** for building and testing AI-enabled CS solutions and CS-tuned models. The domain knowledge itself is packaged for consumption in multiple forms: MCPs, APIs, Playbooks, and Developer Kits. The suite shows one way to use it. The methodologies aren't a selection from available options — they're the output of a deliberate program to build the domain knowledge layer that makes agent-enabled Customer Success actually work.

### Dual-Track Architecture

The suite organizes work across two parallel tracks because the customer relationship has two distinct progress dimensions that advance simultaneously. Conflating them produces the most common failure mode in CS practice: measuring activity at the account level while missing value delivery at the outcome level.

**Track 1 — Customer Lifecycle** maps the relational journey. **Track 2 — Value Realization** maps the delivery journey. They are tightly coupled at Stage 3, where demonstrating value is what sustains the relationship. Keeping them as separate tracks means skills can be precise about which dimension they're operating on, and where they interlock.

**Track 1 — Customer Lifecycle** maps the eight stages of the customer relationship from sales handoff through potential churn:

| Stage | Name | Primary Plugin(s) |
|-------|------|-------------------|
| Stage 0 | Pre-Onboarding & Handoff | csm, rev-ops |
| Stage 1 | Onboarding & Initial Setup | onboarding, csm |
| Stage 2 | Adoption | csm |
| Stage 3 | Value Realization | csm, cs-ops |
| Stage 4 | Value Expansion & Growth | renewals, rev-ops, csm |
| Stage 5 | Renewal | renewals, csm, rev-ops |
| Stage 6 | Advocacy | csm |
| Stage 7 | Churn / Non-Renewal | renewals |

**Track 2 — Value Realization** maps the five stages of the value delivery journey: Discovery → Planning → Delivery → Measurement → Expansion. Both tracks advance in parallel; Stage 3 (Value Realization) is where they most tightly interlock.

### Two-Layer Outcome/Value Model

The suite uses a two-layer model to separate market-level value definitions from account-level value evidence. The distinction matters operationally: market outcomes define what the product *can* deliver; account value statements document what it *has* delivered for a specific customer. Conflating them produces outcome language in account materials that lacks evidence, or account evidence that doesn't connect back to the product's documented value chain.

```
Layer 1 — Market Outcomes (canonical, portfolio-scoped)
  └── Produced by: rev-ops:outcome-statement-builder
      Output: Outcome & Value Catalog (OCV)
      Consumed by: rev-ops:outcome-to-value-tracking (portfolio scoring)

Layer 2 — Account Value (instantiated, per-account)
  └── Produced by: csm:value-statement
      Source: OCV + account business goals + lifecycle stage
      Lifecycle: evolves through Stages 1–5
```

**Layer 1 — Market Outcomes (canonical):** `rev-ops:outcome-statement-builder` produces the **Outcome & Value Catalog (OCV)**, a structured set of outcome statements tied to the customer value chain. This is a one-time (or periodic) artifact that codifies the outcomes the company's product can deliver. The OCV is consumed by `rev-ops:outcome-to-value-tracking` to score value evidence at the portfolio level.

**Layer 2 — Account Value (instantiated):** `csm:value-statement` instantiates an account-specific value statement from the canonical OCV, tied to that customer's business goals, success criteria, and lifecycle stage. This is a living artifact that evolves through Stages 1–5.

The OCV is produced once and referenced by many skills. Account value statements are produced per account and evolve through the customer journey.

---

## Setup

> **Production-grade, not production-ready.** This suite is a reference implementation — built to production standards so the architecture, patterns, and domain knowledge are real, but not designed to drop into your team's workflow without adaptation. Customer Success is practiced differently across organizations. Lifecycle stage definitions, segmentation models, health scoring logic, toolstacks, and team structures vary enough that any honest implementation requires deliberate tailoring. What this suite answers is the harder question: what does a complete, domain-grounded, AI-native CS capability look like, and what does building one actually require? Use it as a working reference and starting point, not a finished product.

### Install from the marketplace

This repository ships a Claude Code plugin marketplace. Add it once, then install any plugin by name. Users get version pinning and `/plugin marketplace update` for refreshes.

```bash
# 1. Add the marketplace (one-time)
/plugin marketplace add t0ddc3by/claude-for-customer-success

# 2. Install the plugins you need
/plugin install csm@claude-for-customer-success
/plugin install cs-ops@claude-for-customer-success
/plugin install renewals@claude-for-customer-success
/plugin install onboarding@claude-for-customer-success
/plugin install rev-ops@claude-for-customer-success
/plugin install auq-resilience@claude-for-customer-success

# 3. Later, refresh to pick up new versions
/plugin marketplace update claude-for-customer-success
```

Each plugin installs independently — install only what your team needs. The marketplace catalog lives at [`.claude-plugin/marketplace.json`](./.claude-plugin/marketplace.json).

**Alternative — install from `dist/` archives.** Pre-built `.plugin` files are also published in [`dist/`](./dist/) for users who prefer file-based installation or are working offline. Drop the archive into your Claude plugin directory or use the Cowork plugin install flow.

### First install (any plugin)

Run the cold-start interview in whichever plugin you install first. It will:
1. Build a **shared company profile** at `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`
2. Configure that plugin's company profile

Subsequent plugin installs reuse the shared company profile and skip company-level questions (~2 min vs. ~15 min for the full first setup).

```bash
# CSM plugin (most common first install)
/csm:cold-start-interview

# Or any other plugin
/cs-ops:cold-start-interview
/renewals:cold-start-interview
/onboarding:cold-start-interview
/rev-ops:cold-start-interview
```

### Integrations

Each plugin works with whatever you have connected. Cold-start will detect what's available and report which integrations are live. Skills have fallbacks for every integration: no connector is required to get value, but connected tools give significantly richer outputs.

**CSM** — CRM (Salesforce, HubSpot), CS Platform (Gainsight, Totango, ChurnZero, Vitally, Planhat), Call recording (Gong, Chorus, Clari, Krisp)

**CS Ops** — Data warehouse (Snowflake, BigQuery, Redshift), CS Platform, BI (Looker, Tableau, Metabase)

**Renewals** — CRM, CPQ (Salesforce CPQ, DealHub, Conga), Contract storage (DocuSign CLM, Ironclad, Drive/SharePoint)

**Onboarding** — Project management (Asana, Linear, Jira, Monday), CRM

**Rev-Ops** — CRM (Salesforce, HubSpot), Slack, Google Drive, CS Platform, Zapier

**AUQ Resilience** — No MCP connectors required. Operates through Claude Code hooks; in Cowork (no hooks) it operates through the `/auq` command plus each plugin's `CLAUDE.md` rules.

#### MCP Dependency Matrix

The table below shows which connectors are required vs. optional per plugin. Skills degrade gracefully without optional connectors, falling back to user-provided context. Required connectors are needed for the plugin's primary skills to function; cold-start will flag missing required connectors.

| Plugin | Required | Optional |
|--------|----------|----------|
| csm | None (user-provided context is sufficient for core skills) | CRM, CS Platform, Call recording |
| cs-ops | CS Platform or Data warehouse (for portfolio analytics) | BI, CRM |
| renewals | CRM (for renewal date and ARR data) | CPQ, Contract storage |
| onboarding | None (user-provided context is sufficient) | Project management, CRM |
| rev-ops | CRM (for pipeline and forecast skills) | CS Platform, Slack, Google Drive, Zapier |
| auq-resilience | None | None |

---

## Managed Agent Cookbooks

The [`managed-agent-cookbooks/`](./managed-agent-cookbooks/) directory contains fifteen agents for teams running Claude as a background workflow engine, plus five rev-ops agents in [`rev-ops/managed-agent-cookbooks/`](./rev-ops/managed-agent-cookbooks/). Six CS suite agents are scheduled headless agents that run autonomously on a cron cadence; four are on-demand agents; and five form the coordinated value-map-system fleet. All five rev-ops agents support both scheduled and on-demand modes.

Each cookbook agent is a thin orchestration layer over the existing plugin skills. It does not define new capabilities. The scheduled agents call the same skills available interactively; what changes is invocation authority (the agent runs unattended) and output routing (Slack digest, Linear issue, or file write instead of chat response).

### Scheduled agents

| Agent | What it does | Primary plugin |
|-------|-------------|----------------|
| [`health-watcher`](./managed-agent-cookbooks/health-watcher/) | Scans portfolio health daily; routes movement alerts | csm |
| [`churn-signal-digest`](./managed-agent-cookbooks/churn-signal-digest/) | Aggregates cross-source churn signals; P1/P2/P3 digest | csm |
| [`qbr-prep-agent`](./managed-agent-cookbooks/qbr-prep-agent/) | Researches and drafts QBR packages on a schedule or on-demand | csm |
| [`renewal-scanner`](./managed-agent-cookbooks/renewal-scanner/) | Reviews upcoming renewals; risk classification 90/60/30 days out | renewals |
| [`onboarding-milestone-tracker`](./managed-agent-cookbooks/onboarding-milestone-tracker/) | Tracks M1–M5 milestone completion; flags at-risk accounts | onboarding |
| [`portfolio-segment-digest`](./managed-agent-cookbooks/portfolio-segment-digest/) | Segment-level health roll-up; ARR at risk by band; CS Ops / leadership | cs-ops |

### On-demand agents

| Agent | What it does | Primary plugin |
|-------|-------------|----------------|
| [`adoption-motion-agent`](./managed-agent-cookbooks/adoption-motion/) | Feature coverage map, gap diagnosis (6-type taxonomy), TARO play prescription | csm |
| [`expansion-builder-agent`](./managed-agent-cookbooks/expansion-builder/) | Whitespace inventory, business case, AE handoff package | csm |
| [`advocacy-agent`](./managed-agent-cookbooks/advocacy/) | Burnout-protected advocate qualification, ask script or story structure | csm |
| [`churn-intelligence-agent`](./managed-agent-cookbooks/churn-intelligence/) | Signal timeline, churn drivers, exit interview guide, postmortem, win-back assessment | renewals |

### Rev-ops agents (scheduled and on-demand)

| Agent | What it does |
|-------|-------------|
| [`gtm-pulse-runner`](./rev-ops/managed-agent-cookbooks/gtm-pulse-runner/) | Weekly GTM metrics pulse: pipeline, run-rate, velocity, churn signals; five Slack sections with HITL gate |
| [`capacity-monitor`](./rev-ops/managed-agent-cookbooks/capacity-monitor/) | CS capacity headroom vs. closed-won actuals; NRR-adjusted projections; silent-green Slack pattern |
| [`churn-signal-scanner`](./rev-ops/managed-agent-cookbooks/churn-signal-scanner/) | Tier 1/2/3 churn signal scan; Tier-3 triggers Linear escalation with human confirmation |
| [`deal-desk-watcher`](./rev-ops/managed-agent-cookbooks/deal-desk-watcher/) | SLA breach monitor across stage age, approval aging, close date drift, and single-threaded risk |
| [`planning-cycle-orchestrator`](./rev-ops/managed-agent-cookbooks/planning-cycle-orchestrator/) | Five-phase GTM planning cycle with phase-gate governance and Slack digest after every run |

### Value map system (multi-cookbook fleet)

The [`value-map-system`](./managed-agent-cookbooks/value-map-system/) is a coordinated fleet of five cookbooks operating on a shared filesystem control plane — the Customer Value Map. Unlike the single-purpose agents above, this system maintains persistent per-account state across the full customer lifecycle. Agents are classified by write authority: **Blue agents** write to the Value Map; **Green agents** read from it. P1/P2 leakage constrains Green agent output: VCS flags the leakage pattern; QBR still produces the full brief but suppresses the expansion angles section; ERD produces no score or brief at all until leakage is resolved.

| Agent | Color | Trigger | What it does |
|-------|-------|---------|--------------|
| [`hie`](./managed-agent-cookbooks/value-map-system/) — Handoff Integrity Enforcer | 🔵 Blue | CRM `opportunity.won` | Builds the initial Value Map from the sales handoff; enforces seven-stage value chain alignment before kickoff |
| [`vmb`](./managed-agent-cookbooks/value-map-system/) — Value Map Builder | 🔵 Blue | CS platform `kickoff_completed` | Populates all four quadrants from kickoff interviews, early usage data, and the success plan |
| [`vcs`](./managed-agent-cookbooks/value-map-system/) — Value Chain Position Scanner | 🟢 Green | Weekly, Mon 06:00 | Scores position health (stage alignment, evidence density, active leakage); flags P1/P2 leakage patterns |
| [`qbr`](./managed-agent-cookbooks/value-map-system/) — QBR Intelligence Agent | 🟢 Green | Quarterly schedule (`qbr_due` event); CSM manual invocation | Generates QBR brief from full Value Map history; expansion angles section blocked when `signals.hard_block_active` is true or `signals.intervention_priority` is P1/P2 — full brief still produced |
| [`erd`](./managed-agent-cookbooks/value-map-system/) — Expansion Readiness Detector | 🟢 Green | Weekly, Mon 06:00 + Growth stage entry | Evaluates expansion signal against leakage state; produces no score or brief when active leakage exists |

See [`managed-agent-cookbooks/value-map-system/README.md`](./managed-agent-cookbooks/value-map-system/README.md) for the full Value Map schema, position health scoring model, and leakage pattern taxonomy.

Agent registration files for the CS plugin agents live in `csm/agents/` and `renewals/agents/`; rev-ops agent cookbooks live in `rev-ops/managed-agent-cookbooks/`. See each cookbook's `README.md` for deployment instructions and `steering-examples.json` for prompting patterns. Full architecture documentation is in [`managed-agent-cookbooks/README.md`](./managed-agent-cookbooks/README.md).

### Failure Modes

Running cookbook agents unattended introduces failure scenarios that interactive skill use does not. The most common:

**Connector unavailability** — A scheduled agent calls a CRM connector that returns a timeout or auth failure. Agents log the failure and produce a partial output with an explicit data gap notice rather than silently omitting affected accounts. Check `agent.yaml` MCP server configuration if connectors are consistently unavailable.

**Stale configuration** — An agent reads a company profile (`~/.claude/plugins/config/claude-for-customer-success/[plugin]/CLAUDE.md`) that was written at cold-start but not updated when the team's segmentation thresholds, escalation matrix, or renewal fields changed. Agents surface a configuration staleness warning when they detect a mismatch between profile values and live CRM data. Run `/[plugin]:customize` to refresh the relevant configuration section.

**HITL gate timeout** — Agents with human-in-the-loop gates (e.g., `gtm-pulse-runner`) wait for an approval before posting final output. If no approval arrives within the configured timeout window, the agent aborts the run and logs the timeout. Set the `hitl_timeout_minutes` field in `agent.yaml` to match your team's response SLA.

**Subagent failure** — Cookbook agents that use subagents (e.g., `health-watcher` spawns `health-reader`, `trend-analyzer`, and `alert-composer`) will produce degraded output if a subagent fails. The parent agent logs which subagent failed and what output is missing. Each subagent's `agent.yaml` includes a `fallback` field specifying behavior when it cannot complete its task.

---

## Claude Managed Agents

Deploy a cookbook agent using the included script:

```bash
scripts/deploy-managed-agent.sh <slug>
```

The script reads `managed-agent-cookbooks/<slug>/agent.yaml`, posts to `/v1/agents`, and writes the returned `agent_id` to `.env.deploy`. Pass `agent_id` as the `model` parameter in every API call targeting that agent:

```python
client.messages.create(
    model="<agent_id>",
    max_tokens=4096,
    messages=[{"role": "user", "content": "Run portfolio health scan"}],
)
```

`scripts/orchestrate.py` is a reference event loop that routes `handoff_request` events between agents. Update `AGENT_ROUTING_TABLE` with your deployed agent IDs before running it.

Subagent delegation (`callable_agents`) is a preview capability — it requires a preview-tier API key. Each cookbook `README.md` flags which agents use it and documents the preview constraints.

Scheduled agents include a `suggested_cron` field in `agent.yaml`. On-demand agents omit it. Both types deploy through the same script.

---

## Shared Guardrails

All six plugins enforce these constraints. They are not optional and cannot be overridden by plugin configuration:

1. **Health scores are heuristics, not verdicts.** Never present a health score as a definitive churn prediction. Surface the signal; the CSM owns the judgment.
2. **Expansion requires qualification.** Flag early-stage expansion signals as leads. Do not present expansion opportunity as confirmed pipeline without sales qualification.
3. **Renewal forecasts have revenue accounting implications.** Language that could be construed as a revenue commitment requires the reviewer to validate before sharing with finance.
4. **No triage recommendation without an escalation path and owner.** A risk flag is not complete unless it names who handles it and how.
5. **Account content is confidential customer data.** Before producing or sending any output containing customer information, check the destination audience.
6. **TARO plays are leads, not mandates.** The CSM reads the play, validates the trigger, and owns the decision to run it. The agent does not run plays autonomously.
7. **No silent data freshness.** Every output that draws on CRM or CSP data surfaces the data-as-of timestamp. Stale data that drives a wrong action is worse than no data.

---

## Architecture Extensions

The 81 skills across these six plugins are built on the standard [Agent Skills](https://agentskills.io/) SKILL.md pattern: frontmatter metadata, trigger blocks, instruction body, and guardrails with some extensions that our research have shown help skills greatly. That baseline is sufficient for a standalone skill. It isn't sufficient for a coordinated suite where 81 skills across 6 plugins need to produce consistent outputs, apply the same domain formulas, enforce the same behavioral constraints, and remain maintainable over time.

A single-skill codebase gets away with embedding domain logic in the skill itself. An 81-skill suite that does that drifts: health score bands defined differently in the CSM health review skill vs. the CS Ops health model review skill, GRR formulas that don't match across renewals and ops, guardrails that exist in some skills but not others. The extensions below solve that problem.

### Shared Domain Model

**File:** [`shared/cs-domain-model.md`](./shared/cs-domain-model.md)

The single authoritative source for every domain constant the suite uses. Skills reference this document rather than defining their own versions of shared concepts.

What it contains:
- Health model score bands (0–100) and the 6-component model (product engagement, business outcomes, relationship strength, support health, adoption breadth, contract health), with the 14-day staleness threshold and the interpretation rule that forbids presenting a health score as a churn prediction
- Customer segmentation labels (Enterprise / Mid-Market / SMB) aligned to ARR thresholds
- GRR and NRR formulas, exact arithmetic, not approximations
- Renewal forecast pipeline stage weights and the 3-scenario modeling approach (conservative / base / upside)
- Time-to-Value definitions, the pace multiplier formula, and the projected TtV calculation
- Source attribution taxonomy: 8 labels (`[CRM ✓ live]`, `[CS Platform ✓ live]`, `[PM ✓ live]`, `[user provided]`, `[config]`, `[inferred]`, `[stale — N days]`, `[unknown]`) that every skill uses when attributing data in its outputs
- The 7 shared guardrails (G1–G7) in their canonical form

**Why this matters:** When a CSM asks for a health summary and separately asks for a portfolio health review, the two outputs use identical scoring definitions. When a renewals skill calculates NRR and a CS Ops skill audits NRR, they use the same formula. Domain consistency doesn't happen automatically. It requires a single source and explicit references to it.

### RevOps Domain Model

**File:** [`shared/revops-domain-model.md`](./shared/revops-domain-model.md)

The authoritative source for rev-ops-specific operational definitions that fall outside the suite-wide constants in `cs-domain-model.md`. Where `cs-domain-model.md` covers domain concepts shared across all 81 skills, this document covers definitions, formulas, thresholds, and governance rules that the rev-ops plugin's 34 skills use. Skills reference it by section anchor — `[revops-domain-model.md §N]` — rather than embedding definitions in individual SKILL.md files.

What it contains:
- Confidence bands calibrated for rev-ops data (High / Moderate / Low), including the 14-day staleness rule for pipeline and capacity figures
- Data authority hierarchy: HubSpot as the primary source of record, with Finance Sheets, CS Platform, and Slack/Linear as successively lower-authority fallbacks — skills use this to attribute data and resolve source conflicts
- Variance classification taxonomy: 5 categories (volume, mix, price, timing, structural) with formulas and a pattern confidence gate that determines when a variance finding is surfaced vs. suppressed
- CS capacity formulas using the UoG (units-of-growth) model, with a 3-scenario check (conservative / base / upside) and defined thresholds for headroom signals and hiring lead time recommendations
- OCV (Outcome-Confirmed Value) catalog conventions: entry lifecycle states (Draft / Ratified / Deprecated), the G8 rule governing when OCV entries can be cited in outputs, and the L0–L3 rubric for evidence quality
- Pipeline coverage signal thresholds: five bands from `<2× CRITICAL` through `>5× INSPECT`, with the interpretation rules skills apply when flagging coverage risk
- Churn signal tiers: Tier 1 (at close), Tier 2 (30–90 days pre-renewal), Tier 3 (90–120 days pre-renewal) — the canonical timing windows for proactive churn intervention
- Governance tiers and write protocol: discount approval tiers, deal desk stage definitions, and the Read/Write protocol controlling which outputs require human approval before action
- Handoff quality scoring rubric: 5 dimensions at 20 points each, 100-point total, with 80 as the pass threshold — used by skills that generate or evaluate handoff packages
- Output destination labels: DRAFT labels and the G1–G9 governance tags that skills attach to their outputs to signal confidence and required handling
- Shared rev-ops guardrails G1–G9: non-overridable governance rules parallel to but distinct from the suite-wide G1–G7 in `cs-domain-model.md`

**Why this matters:** The rev-ops plugin has 34 skills that all need to apply the same confidence bands, churn tier timing, pipeline coverage thresholds, and governance tiers. Without a single source, those definitions drift the same way suite-wide domain constants drift without `cs-domain-model.md` — a pipeline coverage skill and a forecasting skill end up using different thresholds for what counts as adequate coverage. One file, explicit `§N` references from every skill that needs it, no drift.

### Cross-Skill Registry

**File:** [`shared/cross-skill-registry.md`](./shared/cross-skill-registry.md)

A canonical routing table listing all 81 skills with their command format, available modes, and typical trigger conditions. Skills that reference other skills (e.g., a renewal prep skill that hands off to a negotiation skill) point here instead of hardcoding command strings.

**Why this matters:** Hardcoded command strings in SKILL.md files break when skill names change or plugins are reorganized. The registry is the single place to update routing; every skill that references it picks up the change automatically. It also gives contributors and operators a complete map of the suite at a glance.

### Cross-Stage Composition Patterns

The suite defines 11 named multi-skill invocation sequences that span stage boundaries. Examples:

- **QBR Preparation Chain** — `csm.account-research` → `csm.health-score-review` → `csm.value-statement` → `csm.qbr-builder`
- **Renewal Execution Chain** — `renewals.renewal-forecast` → `renewals.risk-assessment` → `renewals.negotiation-prep` → `renewals.executive-summary`
- **At-Risk Escalation Chain** — `csm.risk-flag` → `csm.escalation-memo` → `csm.taro-play-runner`
- **Expansion Intelligence Chain** — `renewals.expansion-signal` → `rev-ops.outcome-to-value-tracking` → `rev-ops.next-best-action-recommendation`

Full composition pattern definitions live in [`docs/claude-for-cs-agent-capability-model.md`](./docs/claude-for-cs-agent-capability-model.md).

### Per-Plugin Config Schemas

**Files:** `[plugin]/reference/config-schema.md` (one per plugin)

Structured schemas defining every configuration field each plugin reads from its company profile: field names, types, valid values, defaults, and required vs. optional status. Skills reference these schemas when reading configuration rather than making assumptions about what fields exist.

**Why this matters:** Cold-start interviews write company profiles that skills then read. Without a schema, skills guess at field names, handle missing fields inconsistently, and break silently when configuration is incomplete. The schema creates a contract between the interview that writes configuration and the skills that consume it.

### Per-Plugin Token Economics

**Files:** `[plugin]/reference/token-economics.md` (one per plugin)

Per-skill token cost estimates covering prompt construction, tool call overhead, connector data volume, and output generation. Estimates are provided for typical (well-configured), minimal (no connectors), and heavy (large account, full connector stack) usage patterns.

**Why this matters:** Token cost is architecture. A skill that pulls 15 CRM records, 30 days of usage data, and a contract PDF in a single pass can consume 40,000+ tokens. Without visibility into that, operators can't decide which skills to run autonomously vs. interactively, or how to scope connector data fetches. Token economics belong in the repository alongside the skills themselves.

### Version Fields

Every SKILL.md frontmatter carries a `version:` field. Version bumps follow semantic versioning conventions: patch for copy fixes, minor for behavior changes, major for breaking changes to inputs or outputs.

**Why this matters:** Plugin update deployments are opaque without versioning. When a skill produces unexpected output, `version:` tells the operator whether they're running the file they think they are. Version history in commit logs correlates with behavior changes across the fleet.

### Reasoning Protocol Sections

Every skill body includes a `## Reasoning Protocol` section: a structured 6-step pre-output checklist the skill runs before generating its response:

1. Confirm activation matches trigger conditions
2. Check connector availability and set fallback path
3. Confirm an escalation path and owner exist before flagging risk
4. Apply the guardrails relevant to this skill's output type
5. Assess output destination (internal CSM use, customer-facing, finance)
6. Confirm mode selection (e.g., research vs. draft vs. update)

Config skills (cold-start interviews and customize commands) run a simplified protocol with no guardrail checks, since they don't produce account-level outputs.

**Why this matters:** Guardrail application is the most common failure mode in production CS AI deployments. A skill that "knows" the guardrails in its documentation but doesn't have a structured point in its reasoning to apply them will miss them under pressure: when the question is complex, the data is stale, or the output is destined for finance. The Reasoning Protocol makes guardrail application explicit and auditable. When a skill produces an output that violates G3 (revenue commitment language), the question "did the Reasoning Protocol run step 4?" has a checkable answer.

### How the Extensions Interact

The extensions form a stack. The domain model provides constants and guardrail definitions. The Reasoning Protocol enforces guardrails at output time. The cross-skill registry enables composition without coupling. Config schemas make cold-start configuration machine-readable. Token economics make cost visible before deployment decisions are made. Versioning makes change traceable.

A skill that uses all six extensions reads domain constants from `shared/cs-domain-model.md` rather than defining its own, applies guardrails through its Reasoning Protocol rather than hoping they're remembered, routes to peer skills through the registry rather than hardcoded commands, reads configuration against a known schema, runs within a documented token budget, and carries a version that can be pinned and audited.

---

## Skill Design

Every skill in this suite is a SKILL.md file: a self-contained specification that Claude reads at invocation time. Understanding the anatomy of a SKILL.md and how skills reference one another explains both how individual skills work and how the suite functions as a coordinated system.

### SKILL.md Anatomy

Each SKILL.md opens with a YAML frontmatter block, followed by a structured Markdown body.

#### Frontmatter

```yaml
---
name: risk-flag
description: >
  Structured risk memo for an at-risk account — signals present, severity
  assessment, escalation routing from your configured matrix, and recommended
  intervention.
argument-hint: "[account name] [--brief | --escalation-memo]"
version: "1.0.0"
deployment_target: plugin
---
```

**Field explanations:**

| Field | Purpose |
|-------|---------|
| `name` | The skill's identifier. Matches the slash command segment after the colon (e.g., `name: risk-flag` → `/csm:risk-flag`). Must be unique within the plugin. |
| `description` | What Claude reads to decide whether to invoke this skill. It must activate on the right inputs (true positives) and stay silent on everything else (true negatives). This is the primary trigger surface — precision here determines whether the right skill fires. |
| `argument-hint` | Documents the optional arguments the skill accepts, shown in command palettes and documentation. Defines the mode flags available to the user (e.g., `--brief` for a condensed output, `--escalation-memo` to route directly to a memo format). |
| `version` | Semantic version string. Patch for copy fixes, minor for behavior changes, major for breaking input/output changes. Lets operators verify which version of a skill is deployed and correlate behavior changes with code history. |
| `deployment_target` | Controls which frontmatter rules apply. `plugin` means this skill ships in a Claude Code `.plugin` file; the plugin loader rejects a `security:` block in frontmatter at this target. `catalog` means MCP-delivery deployment; the catalog parser requires a `security:` block with all v5.3 sub-fields. All skills in this suite use `deployment_target: plugin`. |

The `description` field is the most consequential. It's what Claude's skill routing reads when deciding whether to invoke a skill. A description that's too broad causes false positives (the wrong skill fires). A description that's too narrow causes false negatives (the right skill doesn't fire when it should).

#### Body Sections

The body follows a consistent section structure across all skills:

| Section | Purpose |
|---------|---------|
| `## Use When` | Positive trigger conditions: the situations where this skill should fire. Written as a list of concrete scenarios, not vague capabilities. |
| `## Do NOT Use For` | Negative trigger conditions and routing table. Situations that look similar but should route elsewhere. Often contains explicit pointers to the correct skill (see [Inter-Skill Referencing](#inter-skill-referencing)). |
| `## Typical Activation` | Example invocations showing how a user would naturally phrase requests that should trigger this skill. Used during evaluation to test trigger precision. |
| `## Pre-flight` | Checks Claude runs before generating output: connector availability detection, config validation, fallback path selection. |
| `## Reasoning Protocol` | A structured checklist Claude applies before generating the final output. Enforces guardrail application, escalation path verification, output destination check, and mode selection. See the [Reasoning Protocol Sections](#reasoning-protocol-sections) note in Architecture Extensions. |
| `## Mode` | Behavior variations based on the active mode flag. Each mode flag (e.g., `--brief`, `--deep`) produces a different output structure or depth. |
| `## Data Gathering` | Which connectors to call, in what order, with what fallbacks. Defines what happens when a connector is unavailable vs. what happens when it's live. |
| `## Output` | The output structure template: headers, required fields, conditional sections, formatting rules. Consuming skills and managed agents expect this structure. |
| `## Guardrails` | Skill-specific behavioral constraints that layer on top of the shared G1–G7 guardrails. |
| `## After the Skill` | Post-output guidance: what the user should do next, which skills to run next, and under what conditions. This is where chaining prompts live (see [Next-Step Chaining](#next-step-chaining)). |
| `## Security & Permissions` | Trust boundary declarations: what external systems this skill can read from, write to, or call. Required for `deployment_target: plugin` skills; placed in the body (not frontmatter) since the plugin loader does not parse security blocks in frontmatter. |
| `## Trust & Verification` | Config integrity checks: what configuration the skill requires to be present before it proceeds. Defines the halt condition when required config is missing. |

Config skills (cold-start interviews and `customize` commands) use a simplified section structure. They have no Guardrails, After the Skill, or Trust & Verification sections, since they produce config rather than account-level outputs.

---

### Inter-Skill Referencing

Skills in this suite reference each other through four distinct mechanisms. All of them use command strings drawn from the cross-skill registry (`shared/cross-skill-registry.md`) rather than hardcoded alternatives.

#### 1. Routing in "Do NOT Use For" Blocks

When a user invocation is close but wrong (right intent, wrong skill), the `## Do NOT Use For` block names the correct skill explicitly. This is the primary mechanism for routing misfires at invocation time.

From `csm/skills/risk-flag/SKILL.md`:

```markdown
## Do NOT Use For
- Escalation memos for leadership — use `/csm:escalation-memo`
- Routine health reviews without active risk signals — use `/csm:health-score-review`
```

This pattern keeps the routing logic distributed across skills rather than centralized in a single dispatcher. Each skill owns its own exclusion boundaries and points outward to peers.

#### 2. Next-Step Chaining

After generating output, skills suggest the next skill in the workflow, with the exact invocation string and relevant flags. This guides the user through a multi-skill sequence without requiring them to know the full workflow upfront.

From `csm/skills/risk-flag/SKILL.md`:

```markdown
## After the Skill
If renewal is within 90 days, run `/csm:renewal-readiness [account]` to assess renewal exposure alongside the risk posture.

If executive sponsor access is in question, run `/csm:stakeholder-map [account] --sponsor-risk` to map the relationship landscape.
```

The chaining is conditional. It fires based on what the current output revealed, not as a rote sequence. Claude can tailor which next step it suggests based on the actual risk profile surfaced.

#### 3. Config Scope Redirect

Some skills depend on configuration that lives in a different plugin's company profile. Rather than duplicating configuration logic, those skills redirect to the owning plugin's `customize` command.

From `onboarding/skills/handoff-doc/SKILL.md`:

```markdown
## Do NOT Use For
- Changing handoff template structure or required fields — use `/cs-ops:customize`
  to configure the handoff template. Then re-run this skill.
```

This enforces a single point of configuration ownership. CS Ops owns the handoff template schema; the Onboarding plugin consumes it. When a user tries to configure template structure through the Onboarding skill, the skill redirects to the owning plugin rather than attempting to write config it doesn't own.

For section-level config changes:

```markdown
- Updating graduation criteria only — use `/onboarding:cold-start-interview --section handoff`
```

#### 4. Downstream Blocking Notation

Some skills explicitly document which downstream skills are unavailable until required configuration exists. This surfaces dependency failures at the earliest possible point rather than when the downstream skill fires.

From `onboarding/skills/handoff-doc/SKILL.md`:

```markdown
## Trust & Verification
Missing graduation milestone configuration blocks `/onboarding:handoff-doc`. Run
`/cs-ops:customize` to define graduation criteria before using this skill.
```

The user learns about the missing config when they try to use the skill that requires it, not when the config-dependent output turns out wrong. The Trust & Verification section is the canonical place to declare blocking conditions.

---

### How the Cross-Skill Registry Enables This

All four referencing mechanisms use command strings drawn from `shared/cross-skill-registry.md`. The registry is a flat table of every skill across all six plugins: command format, available mode flags, and the lifecycle stage each skill belongs to.

```
/csm:risk-flag [account] [--brief | --escalation-memo]
/csm:renewal-readiness [account] [--brief | --deep | --exec-summary]
/csm:stakeholder-map [account] [--full | --sponsor-risk | --decision-maker]
```

When a skill author adds a next-step chaining prompt, they copy the command string from the registry. When a skill is renamed or a flag is added, the registry is updated first, and all skills that reference it pick up the change naturally at the next edit pass. No skill hardcodes an alternative command string.

The registry also documents six cross-plugin workflow sequences: named multi-skill chains that cross plugin boundaries. Example:

| Pattern | Sequence |
|---------|---------|
| At-Risk Triage | `csm:risk-flag` → `csm:escalation-memo` → `csm:taro-play-runner` |
| Renewal Prep | `renewals:renewal-forecast` → `csm:renewal-readiness` → `renewals:negotiation-prep` |
| Onboarding Handoff | `onboarding:milestone-tracker` → `onboarding:handoff-doc` → `csm:account-research` |

These cross-plugin sequences are documented in the registry so operators understand the full multi-plugin workflow, not just individual skill capabilities.

**The maintenance rule is strict:** `shared/cross-skill-registry.md` is the source of truth for all command strings. Individual SKILL.md files must not hardcode alternative command strings. This rule keeps the registry authoritative and prevents routing drift when skills evolve.

#### Machine-Readable Capability Model

For tooling, integrations, and operators who need structured per-skill metadata, [`docs/claude-for-cs-agent-capability-model.yaml`](./docs/claude-for-cs-agent-capability-model.yaml) is the authoritative machine-readable representation of all 81 skills. Each entry carries:

| Field | What it captures |
|-------|-----------------|
| `id` | Canonical skill identifier, matches the `name:` frontmatter field |
| `version` | Current deployed version, mirrors SKILL.md frontmatter |
| `summary` | One-sentence capability description |
| `intended_tasks` | Structured list of tasks this skill is built to handle |
| `out_of_scope` | Explicit exclusions: the machine-readable equivalent of `## Do NOT Use For` |
| `invocation_cues` | Natural-language patterns that should trigger this skill |
| `anti_cues` | Patterns that look relevant but should not trigger this skill |
| `constraints` | Behavioral constraints active during this skill's execution |
| `tools_used` | Connectors and MCP tools the skill may call |
| `related_skills` | Skills that compose with this one: the machine-readable form of next-step chaining |
| `success_criteria` | Observable conditions that constitute a correct output |

The YAML model and the SKILL.md files are parallel representations of the same skills: SKILL.md is what Claude reads at runtime; the YAML is what tooling reads at build time or integration time. When a SKILL.md is updated, the YAML model should be updated to match.

---

## Coverage Notes

The suite's 81 skills break down as 47 lifecycle skills (Stages 0–6) and 34 cross-cutting ops skills. Coverage is not uniform across lifecycle stages (but will be expanded in subsequent releases and can be augmented by solutions like our skill-enabled TARO playbooks that feature 850+ additional skills see the **taro-play-runner** skill):

- **Stages 0–5** have full or near-full skill coverage with documented workflows and stage gate criteria.
- **Stage 6 (Advocacy)** has minimal dedicated coverage: two skills, `csm.advocate-identification` and `csm.advocacy-ask`. Broader advocacy program design, community management, and reference program coordination are deliberately out of scope for v1.1.0. These activities require human relationship judgment that doesn't compress well into a skill interaction; the agent cookbook `advocacy-agent` handles the research and qualification work that does.
- **Stage 7 (Churn / Non-Renewal)** has partial coverage. `renewals.churn-analysis` and the `churn-intelligence-agent` cookbook address post-decision analysis; proactive churn prevention is handled through Stage 5 skills and `rev-ops.early-churn-downgrade-signal-detection`. Win-back motion skills and automated exit interview synthesis are on the backlog for v1.2.0.

The coverage gaps in Stages 6 and 7 are architectural decisions, not oversights. Our skill development backlog prioritizes win-back motions and expanded advocacy program support for the next minor version.

---

## File Locations

```
~/.claude/plugins/config/claude-for-customer-success/
├── company-profile.md          # Shared — all six plugins read this
├── csm/CLAUDE.md               # CSM company profile (written at cold-start)
├── cs-ops/CLAUDE.md            # CS Ops company profile
├── renewals/CLAUDE.md          # Renewals company profile
├── onboarding/CLAUDE.md        # Onboarding company profile
└── rev-ops/CLAUDE.md           # Rev-Ops company profile
```

Plugin templates (this directory) ship with the plugin and are replaced on update. User data lives only in `~/.claude/plugins/config/`.

Practitioner deployment guides live in the repository under `deployment-cookbooks/`:

```
deployment-cookbooks/
├── README.md                   # Reference build explanation and tailoring guidance
└── solo-post-sales-cookbook.md        # Solo CSM deployment guide — full lifecycle, personal use
```

### Developer Tooling

The repository includes build and evaluation tooling for contributors and operators maintaining the suite:

```
scripts/
├── build-plugins.sh            # Packages all six plugins into dist/*.plugin files
├── validate-skills.sh          # Runs frontmatter validation across all SKILL.md files
└── update-registry.sh          # Syncs cross-skill-registry.md from SKILL.md frontmatter

[plugin]/skills/[skill-name]/
└── evals/                      # Per-skill evaluation sets (gitignored — not shipped in plugin)
    ├── true-positives.md       # Invocation cues that should trigger the skill
    ├── true-negatives.md       # Inputs that should not trigger it
    └── output-rubric.md        # Criteria for evaluating output quality
```

The `evals/` directories are present during development but excluded from built plugins via `.gitignore`. To run evaluations against a deployed plugin, pull the skill source from the repository rather than the installed plugin file.

---

## Documentation

The [`docs/`](./docs/) directory contains extended reference documentation:

| Document | Contents |
|----------|----------|
| [`claude-for-cs-agent-capability-model.md`](./docs/claude-for-cs-agent-capability-model.md) | Complete 81-skill capability catalog organized by lifecycle stage; 11 composition patterns; tier distribution; coverage gap analysis |
| [`claude-for-cs-agent-capability-model-lifecycle.md`](./docs/claude-for-cs-agent-capability-model-lifecycle.md) | Skills organized by lifecycle stage with Two-Layer Outcome/Value Model integration; coverage summary table |
| [`claude-for-cs-integrated-journey-value-realization-guide.md`](./docs/claude-for-cs-integrated-journey-value-realization-guide.md) | Stage-by-stage workflow guide with Mermaid diagrams, value chain focus tables, gap risk tables, and stage gate criteria for all lifecycle stages |
| [`claude-for-cs-agent-capability-model.yaml`](./docs/claude-for-cs-agent-capability-model.yaml) | Machine-readable capability registry for all 81 skills: structured YAML with per-skill `id`, `version`, `summary`, `intended_tasks`, `out_of_scope`, `invocation_cues`, `anti_cues`, `constraints`, `tools_used`, `related_skills`, and `success_criteria`; authoritative source for tooling and integrations |

---

## Deployment Cookbooks

The [`deployment-cookbooks/`](./deployment-cookbooks/) directory contains operational guides for practitioners deploying the suite. These are role-specific deployment companions — not the same as the automated managed-agent cookbooks in `managed-agent-cookbooks/`.

> **These are reference builds, not plug-and-play deployments.** The plugins and workflows described in the cookbooks are designed around generalizable patterns. Every deployment requires tailoring to the specific tools, data schema, and CS motion of the organization using them. See [`deployment-cookbooks/README.md`](./deployment-cookbooks/README.md) for the full explanation of what "reference build" means and what tailoring is required before going live.

| Cookbook | Audience | Status |
|----------|----------|--------|
| [`solo-post-sales-cookbook.md`](./deployment-cookbooks/solo-post-sales-cookbook.md) | Individual CSMs deploying the full suite for solo use across the customer lifecycle | [PROPOSED] |

To add a cookbook for a different role, motion, or deployment variant, follow the instructions in [`deployment-cookbooks/README.md`](./deployment-cookbooks/README.md).

---

## AUQ Resilience

**Package:** [`auq-resilience/`](./auq-resilience/) · **Distributed:** [`dist/auq-resilience-v1.1.0.plugin`](./dist/)

The CS plugins use `AskUserQuestion` (AUQ) extensively for cold-start interviews, skill mode selection, and interactive clarification. When AUQ works, the user gets an interactive multiple-choice widget. When it fails (unsupported client, missed render, tool error), Claude receives an empty response with no recoverable path. Without a fallback, the entire skill interaction stops.

The `auq-resilience` plugin installs two Claude Code hooks:

- **`PreToolUse` hook** — intercepts AUQ calls and injects prose fallback instructions alongside the widget render request
- **`PostToolUse` hook** — detects empty or unparseable AUQ responses and injects a structured prose multiple-choice block so Claude can proceed

The hooks implement a T1/T2/T3 protocol: T1 retries the widget once, T2 injects the prose fallback, T3 logs the failure and continues with a declared default. An AUQ render failure never produces a dead end. Claude always has a recoverable path.

Installing the plugin is a one-step install. Wiring it into a plugin requires adding two entries to that plugin's `hooks/hooks.json`. All five CS plugins ship with empty hook slots ready to receive the wiring. The auq-resilience plugin does not change how AUQ works when it succeeds. It only catches failures.

### Enabling in Cowork

Claude Code hooks do not run in Cowork — `PreToolUse`/`PostToolUse`/`UserPromptSubmit` never fire there, so the mechanical fallback above is unavailable. In Cowork the same protocol is delivered two ways, both already in place:

- **Behavioral rules** — every CS plugin's `CLAUDE.md` carries an **AskUserQuestion (AUQ) Resilience** section (single-question, T2 prose fallback, T3 embedded default). These apply automatically whenever that plugin is active. No setup beyond installing the plugin.
- **The `/auq` command** (v1.1.0+) — `auq-resilience` ships `commands/auq.md`, invoked as `/auq-resilience:auq` with `force-prose`, `status`, or `reset`. Commands are the one plugin surface that runs in Cowork, so the command auto-registers on install — no wiring required.

To enable: install `auq-resilience` in Cowork (desktop plugin install), then restart Cowork so the command registers. Nothing else is needed — the behavioral rules ship inside each CS plugin.

See [`auq-resilience/README.md`](./auq-resilience/README.md) for install steps, the `/auq` command reference, and the full T1/T2/T3 protocol.

---

## Making It Yours

Every plugin ships with defaults that work out of the box. Four layers of configuration let you tune behavior without modifying plugin source files:

- **Swap connectors** — edit the plugin's `.mcp.json` to point at your CRM, CS platform, Slack workspace, or data warehouse. Skills that use a connector degrade gracefully when the connector is absent; skills that don't need one ignore the file entirely.
- **Add firm context** — the `cold-start-interview` command in each plugin writes a company profile to `~/.claude/plugins/config/claude-for-customer-success/[plugin]/CLAUDE.md`. Edit that file directly to update segmentation thresholds, renewal risk criteria, escalation matrices, and named contacts. Agents and skills read the profile on every run.
- **Bring your own templates** — paste your team's QBR template, success plan format, or executive summary structure into the relevant section of the company profile. Skills use your template instead of the built-in one.
- **Adjust agent scope** — fork a cookbook's `agent.yaml` to change which skills it calls, what output it routes, and which HITL gates it enforces. No changes to the plugin itself are required.
- **Add your own** — write a `SKILL.md` using the CS plugin skill pattern and bundle it into a new plugin file alongside the stock skills. The [Skill Design](#skill-design) section documents the pattern and required frontmatter.

---

## Claude for Microsoft 365 — Install Tooling

`claude-for-msft-365-install/` is a Claude Code plugin — not a Cowork plugin — for IT administrators provisioning the Claude for Microsoft 365 add-in. It is separate from the six CS suite plugins and does not need to be installed by individual CS team members.

Install in Claude Code (admin terminal):

```
/install claude-for-msft-365-install
```

Then run the setup command:

```
/claude-for-msft-365-install:setup
```

The setup command provisions the M365 add-in via Microsoft Graph API. It supports Vertex AI, Amazon Bedrock, and internal LLM gateways as the backing model endpoint and writes a deployment summary to `~/.claude/plugins/config/msft-365-install/deployment.md` on completion.

---

## Skill & Command Reference

Run `/[plugin]:cold-start-interview` first in any plugin — it writes the company profile that every other skill reads for firm context, thresholds, and templates.

### csm (19 skills)

| Command | What it does |
|---------|-------------|
| `/csm:cold-start-interview` | Writes firm context, segmentation thresholds, and templates to company profile |
| `/csm:customize` | Updates any section of the CSM company profile interactively |
| `/csm:account-research` | Multi-source account intelligence snapshot before a call or review |
| `/csm:call-prep` | Call agenda, talking points, and risk context from CRM and CS platform data |
| `/csm:communication-planner` | Builds a structured comms sequence for a lifecycle moment |
| `/csm:customer-comms` | Drafts customer-facing messages: check-ins, updates, and announcements |
| `/csm:escalation-memo` | Writes a structured escalation package for internal stakeholders |
| `/csm:expansion-business-case` | Builds the business case and AE handoff package for an expansion |
| `/csm:expansion-onboarding` | Plans onboarding for a newly expanded or cross-sold product |
| `/csm:health-score-review` | Interprets health score signals and recommends a response motion |
| `/csm:qbr-builder` | Researches and assembles a QBR package from CRM, CS platform, and usage data |
| `/csm:renewal-readiness` | 90/60/30-day renewal readiness check with risk classification |
| `/csm:risk-flag` | Generates a structured risk flag with evidence, severity, and escalation path |
| `/csm:stakeholder-map` | Maps account stakeholders: sponsors, champions, detractors, and coverage gaps |
| `/csm:success-plan-builder` | Creates a structured success plan from onboarding data and business goals |
| `/csm:success-plan-canvas` | Interactive canvas for co-building a success plan with the customer |
| `/csm:success-plan-progress-review` | Reviews milestone progress and surfaces course corrections |
| `/csm:taro-play-runner` | Selects and executes a TARO play for a detected account trigger |
| `/csm:value-statement` | Builds a value statement using two-layer outcome and value chain models |

### renewals (12 skills)

| Command | What it does |
|---------|-------------|
| `/renewals:cold-start-interview` | Writes renewal thresholds, risk criteria, and team context to company profile |
| `/renewals:customize` | Updates any section of the renewals company profile |
| `/renewals:churn-analysis` | Synthesizes churn signals into a risk score and recommended play |
| `/renewals:churn-rca` | Root cause analysis on a churned or churning account |
| `/renewals:contract-review` | Reviews contract terms for renewal, uplift, and risk clauses |
| `/renewals:downgrade-analysis` | Diagnoses downgrade drivers and quantifies ARR impact |
| `/renewals:executive-summary` | Produces an executive-ready renewal situation summary |
| `/renewals:expansion-signal` | Identifies expansion readiness signals in a renewal account |
| `/renewals:negotiation-prep` | Prepares negotiation posture, fallback positions, and authority matrix |
| `/renewals:price-increase-prep` | Builds a price-increase rationale package for the renewal conversation |
| `/renewals:renewal-forecast` | Generates a confidence-weighted renewal forecast |
| `/renewals:risk-assessment` | Structured risk assessment with severity, evidence, and recommended action |

### cs-ops (9 skills)

| Command | What it does |
|---------|-------------|
| `/cs-ops:cold-start-interview` | Writes ops scope, tech stack, and metrics context to company profile |
| `/cs-ops:customize` | Updates any section of the CS-Ops company profile |
| `/cs-ops:capacity-planner` | Models current vs. projected CSM capacity against book-of-business growth |
| `/cs-ops:data-quality-check` | Audits CRM field completion and data consistency across the CS portfolio |
| `/cs-ops:health-model-review` | Reviews the health scoring model for signal coverage and weighting logic |
| `/cs-ops:metric-dashboard` | Builds a metric dashboard spec or reviews current CS KPI coverage |
| `/cs-ops:playbook-auditor` | Reviews playbooks for trigger coverage, action completeness, and gaps |
| `/cs-ops:process-doc` | Documents a CS workflow or process for team reference |
| `/cs-ops:segment-analyzer` | Profiles portfolio segments by ARR band, industry, and health distribution |

### onboarding (10 skills)

| Command | What it does |
|---------|-------------|
| `/onboarding:cold-start-interview` | Writes onboarding scope, milestone definitions, and team context to company profile |
| `/onboarding:customize` | Updates any section of the onboarding company profile |
| `/onboarding:blocker-review` | Identifies and prioritizes implementation blockers with recommended actions |
| `/onboarding:handoff-doc` | Generates a structured sales-to-CS handoff document |
| `/onboarding:kickoff-prep` | Prepares kickoff agenda, stakeholder brief, and success criteria for Day 1 |
| `/onboarding:milestone-tracker` | Reviews milestone completion and flags at-risk accounts |
| `/onboarding:onboarding-plan` | Builds a time-to-value onboarding plan tailored to customer goals |
| `/onboarding:references` | Identifies reference candidates from the onboarding cohort |
| `/onboarding:success-criteria` | Defines measurable success criteria aligned to customer business goals |
| `/onboarding:ttv-analysis` | Analyzes time-to-value performance and identifies acceleration opportunities |

### rev-ops (36 skills)

| Command | What it does |
|---------|-------------|
| `/rev-ops:cold-start-interview` | Writes GTM scope, CRM schema, and metrics baseline to company profile |
| `/rev-ops:annual-planning-workflow` | Orchestrates the annual GTM planning cycle with phase-gate governance |
| `/rev-ops:change-communication-packaging` | Packages process or policy changes for field communication |
| `/rev-ops:closed-won-to-cs-capacity-modeling` | Models CS capacity requirements from closed-won actuals |
| `/rev-ops:comp-simulation` | Simulates comp plan scenarios and models quota/OTE sensitivity |
| `/rev-ops:crm-hygiene-audit` | Audits CRM data quality across field completion, consistency, and accuracy |
| `/rev-ops:cross-system-reconciliation` | Reconciles data across CRM, CS platform, billing, and product systems |
| `/rev-ops:csql-tracking` | Tracks CS-qualified lead volume, conversion, and pipeline contribution |
| `/rev-ops:csql-tracking-workspace` | Multi-account CSQL pipeline workspace with filtering and export |
| `/rev-ops:data-decay-tracking` | Monitors data decay rates and surfaces stale records requiring refresh |
| `/rev-ops:deal-classification` | Classifies deals by type, complexity, and CS handoff requirements |
| `/rev-ops:deal-desk-workflow-management` | Manages deal desk SLA compliance and approval pipeline hygiene |
| `/rev-ops:deal-health-scoring` | Scores deal health across stage, velocity, stakeholder coverage, and risk |
| `/rev-ops:deal-to-outcome-tracing` | Traces deals from closed-won through onboarding to value delivery |
| `/rev-ops:discount-threshold-monitoring` | Flags deals exceeding discount thresholds for deal desk review |
| `/rev-ops:duplicate-detection` | Detects duplicate accounts, contacts, and opportunities in CRM |
| `/rev-ops:early-churn-downgrade-signal-detection` | Scans for early churn and downgrade signals across the portfolio |
| `/rev-ops:field-completion-monitoring` | Monitors CRM field completion rates by object, team, and region |
| `/rev-ops:forecast-variance-analysis` | Decomposes forecast variance into deal, rep, and category drivers |
| `/rev-ops:growth-model-vs-actuals-tracking` | Compares growth model assumptions to actuals for planning revalidation |
| `/rev-ops:gtm-unified-metrics-pulse` | Produces the weekly unified GTM metrics digest across pipeline, NRR, and CS |
| `/rev-ops:mid-year-replan-triggering` | Evaluates mid-year variance and triggers a replan when thresholds are breached |
| `/rev-ops:next-best-action-recommendation` | Recommends the highest-value next action per account from signal data |
| `/rev-ops:non-standard-terms-detection` | Flags non-standard contract terms requiring deal desk or legal review |
| `/rev-ops:outcome-statement-builder` | Builds structured outcome statements for the CS outcome catalog |
| `/rev-ops:outcome-to-value-tracking` | Traces customer outcomes to value chain delivery milestones |
| `/rev-ops:pipeline-coverage-analysis` | Analyzes pipeline coverage by segment, stage, and close-date cohort |
| `/rev-ops:pipeline-velocity-tracking` | Tracks pipeline velocity changes and surfaces acceleration and friction signals |
| `/rev-ops:portfolio-health-report` | Generates a portfolio health report segmented by ARR, tier, and region |
| `/rev-ops:quota-sensitivity-analysis` | Models quota attainment sensitivity to ramp, churn, and expansion inputs |
| `/rev-ops:revenue-brief-generation` | Produces an executive revenue brief for leadership and board review |
| `/rev-ops:revenue-leakage-scanning` | Scans for revenue leakage: missed expansions, discount overuse, delayed renewals |
| `/rev-ops:sales-cs-handoff-quality-scoring` | Scores the quality of sales-to-CS handoffs against defined criteria |
| `/rev-ops:scenario-modeling` | Models GTM scenarios for planning, reforecast, and board preparation |
| `/rev-ops:stage-integrity-audit` | Audits stage-gate criteria compliance across the pipeline |
| `/rev-ops:unit-of-growth-calculator` | Calculates unit of growth economics: CAC, LTV, payback, and NRR contribution |

### auq-resilience

Infrastructure plugin. Ships no skills. Installs `PreToolUse`/`PostToolUse` hooks (Claude Code) and one command, `/auq` (`/auq-resilience:auq` — `force-prose` / `status` / `reset`), which is the Cowork-native control surface. See [AUQ Resilience](#auq-resilience) for the T1/T2/T3 fallback protocol and Cowork enablement.

---

## Contributing

Contributions are welcome. The workflow below keeps skill sources consistent across all plugin bundles.

**Before you start:**
- Read the [Code of Conduct](./CODE_OF_CONDUCT.md). This repo is a professional tool for Customer Success teams handling confidential customer data and revenue-sensitive account intelligence. All contributors — whether submitting a new skill, fixing a bug, or improving documentation — are expected to follow that standard.

**Skill edits:**
- **Always edit skills in `vertical-plugins/`**, not in `agent-plugins/<slug>/skills/`. The agent-plugin skill directories are generated copies. Edits made there directly will be overwritten.
- After editing, run `python3 scripts/sync-agent-skills.py` to propagate changes into all agent bundles that depend on that skill.
- Run `python3 scripts/check.py` before committing. The check script lints every manifest, verifies all `system.file` / `skills.path` / `callable_agents.manifest` references resolve, and fails if any agent-plugin skill copy has drifted from its vertical-plugin source.

**Plugin versions and manifests:**
- `.claude-plugin/` is gitignored, so `<plugin>/.claude-plugin/plugin.json` is a **build artifact**, not source. The tracked source of truth is [`bin/manifests.yaml`](./bin/manifests.yaml).
- To bump a version or edit a plugin description, edit `bin/manifests.yaml`, then run `python3 bin/generate-manifests.py` to write the manifests.
- On a fresh clone, run `python3 bin/generate-manifests.py` **before** building or packaging anything — without it there are no manifests on disk.
- `python3 bin/generate-manifests.py --check` reports drift between the on-disk manifests and the canonical source. `--list` prints the version table.
- The generator refuses to emit a `description` over 388 characters (CHECK 6, the empirical Cowork backend ceiling), so an over-length description cannot reach a build.

**Validation:**
- `python3 bin/preflight.py --all --parent .` runs all 8 backend-constraint checks across every plugin. CI ([`.github/workflows/preflight.yml`](./.github/workflows/preflight.yml)) generates the manifests, then runs the same command on every push and PR that touches plugin source.
- Constraint reference and discovery evidence: `skills/plugin-preflight-validator/references/known-constraints.md` in the workspace skills library.

**Pull requests:**
1. Fork the repository and create a feature branch from `main`.
2. Make your changes following the skill-edit workflow above.
3. Ensure `check.py` passes with no errors.
4. Open a pull request with a clear description of what changed, which plugin(s) are affected, and any testing you performed.
5. For new skills, include the trigger conditions, example invocations, and the connector dependencies the skill requires.

**Scope guidance:**
- Bug fixes and documentation improvements: open a PR directly.
- New skills or significant architecture changes: open a GitHub Issue first to discuss scope and fit before investing in implementation.
- Changes to managed agent cookbooks or MCP configurations: flag in the PR description — these require additional review given their behavioral and security surface area.

---

## Bugs and Issues

Report bugs and unexpected behavior via [GitHub Issues](https://github.com/t0ddc3by/claude-for-customer-success/issues).

When filing a bug, include:

| Field | What to provide |
|-------|-----------------|
| **Plugin** | Which plugin (csm, renewals, cs-ops, rev-ops, onboarding, auq-resilience) |
| **Skill slug** | The skill name as it appears in the plugin (e.g., `renewal-risk-briefing`) |
| **Command** | The slash command used, if applicable (e.g., `/csm:qbr-prep`) |
| **Claude model** | Model version (e.g., `claude-sonnet-4-6`) |
| **Connectors** | Which MCP connectors were active (Salesforce, HubSpot, Gainsight, etc.) |
| **Expected behavior** | What you expected the skill to do |
| **Actual behavior** | What it actually did — include the full Claude response if relevant |
| **Reproduction steps** | Minimal steps to reproduce |

**What counts as a bug:** skill behavior that diverges from the documented trigger conditions or output specification; `check.py` failures on unmodified files; manifest resolution errors; hook intercept failures in the auq-resilience plugin.

**What is not a bug:** Claude producing different outputs on repeated invocations with the same prompt (model inference is non-deterministic); skill outputs that are reasonable but not what you hoped for; connector failures caused by third-party API changes or rate limits.

---

## Support

**For bugs and unexpected skill behavior:** [GitHub Issues](https://github.com/t0ddc3by/claude-for-customer-success/issues) — use the bug report template above.

**For questions about how to use the plugins, install connectors, or wire up the auq-resilience hooks:** [GitHub Discussions](https://github.com/t0ddc3by/claude-for-customer-success/discussions).

**For questions about SuccessCOACHING methodologies** (TARO, Customer Lifecycle, Value Chain, Two-Layer Outcome/Value Model) and how the skills operationalize them: reach the SuccessCOACHING team at [successhacker.co](https://successhacker.co).

**For enterprise deployment, custom skill development, or managed agent configuration assistance:** contact SuccessCOACHING directly via [successhacker.co](https://successhacker.co).

Response time for GitHub Issues and Discussions is best-effort. This is an open-source reference implementation, not a supported commercial product.

---

## Security

**Do not open a public GitHub Issue to report a security vulnerability.**

If you discover a vulnerability in this repository — including prompt injection risks in skill content, insecure MCP configuration patterns, hook intercept bypasses, or credential exposure in managed agent cookbooks — report it privately:

**Email:** security@successhacker.co  
**Subject line:** `[Security] claude-for-customer-success — <brief description>`

Include:
- A description of the vulnerability and its potential impact
- The file(s) and line(s) involved
- Steps to reproduce or a proof-of-concept if applicable

We will acknowledge receipt within 5 business days and work with you on a coordinated disclosure timeline.

**Scope note.** Most security-relevant behavior in this suite is governed by Claude's model-level safety systems, Anthropic's usage policies, and the access permissions you configure on your MCP connectors. The skills and plugins in this repo do not execute code or make API calls directly — they are prompts and configuration files. The primary security surface is data access: what connectors you authorize, what data those connectors can reach, and who has access to the Claude session that invokes the skills. Review the [Disclaimer](#disclaimer) for data handling guidance.

---

## Changelog

See [CHANGELOG.md](./CHANGELOG.md) for a version-by-version record of changes.

Per-plugin release notes are in each plugin's `CHANGELOG.md`:

- [`csm/CHANGELOG.md`](./csm/CHANGELOG.md)
- [`renewals/CHANGELOG.md`](./renewals/CHANGELOG.md)
- [`cs-ops/CHANGELOG.md`](./cs-ops/CHANGELOG.md)
- [`rev-ops/CHANGELOG.md`](./rev-ops/CHANGELOG.md)
- [`onboarding/CHANGELOG.md`](./onboarding/CHANGELOG.md)
- [`auq-resilience/CHANGELOG.md`](./auq-resilience/CHANGELOG.md)

---

## Version

`claude-for-customer-success` v1.1.0 · Built for Anthropic Claude Code and Claude Cowork.

Compatible with Claude claude-sonnet-4-6 and claude-opus-4-6.

---

## License

Copyright 2026 SuccessCOACHING. Licensed under the [Apache License, Version 2.0](./LICENSE).

---

## Disclaimer

**Independent project — not affiliated with Anthropic PBC.** This is an independent open-source project. It is not affiliated with, endorsed by, sponsored by, or approved by Anthropic PBC. "Claude" is a trademark of Anthropic PBC; its use here is solely to identify the underlying AI model platform on which these plugins and agents are designed to operate. The name "Claude for Customer Success" does not imply any association with, endorsement by, or approval from Anthropic PBC. The views, methodologies, frameworks, and content expressed in this repository are those of SuccessCOACHING and its contributors and do not represent the views of Anthropic PBC.

This repository — including all skills, plugins, managed agent cookbooks, commands, Claude Code hooks, MCP configurations, and accompanying documentation — is provided for **demonstration and educational purposes only**. It is a reference implementation, not a production-ready deployment.

**Skills and plugins.** The 81 skills and six plugins in this suite illustrate patterns and possibilities for AI-enabled Customer Success. While the capabilities they describe may be available in Claude, the specific behaviors you observe will vary based on the Claude model version, the connectors you have installed, the quality and completeness of your CRM and tooling data, and how your organization's context differs from the assumptions encoded in each skill. Skill outputs should be reviewed by a qualified practitioner before any consequential action is taken.

**Managed agents and cookbooks.** The managed agent cookbooks in `managed-agent-cookbooks/` describe multi-agent orchestration patterns using the Claude Managed Agents platform. Agent behavior — including subagent routing, tool selection, and output synthesis — depends on model inference and is not deterministic. The cookbooks define intent and architecture; they do not guarantee specific outputs. Test each agent cookbook in a sandbox environment with representative data before deploying to a live account or revenue workflow.

**Commands.** Slash commands (e.g., `/csm:qbr-prep`) are invocation shortcuts that pass context to skill prompts. They depend on the plugin being correctly installed, the connected MCP tools being available and authenticated, and the Claude session having sufficient context. A command that works in one session may produce different results in another if connector state, model version, or available context differs.

**Claude Code hooks.** The `auq-resilience` hooks modify Claude's tool use behavior at the `PreToolUse` and `PostToolUse` intercept points. Hook behavior depends on the Claude Code version, the host environment, and the specific tool being intercepted. Test hooks against your target plugin configuration before treating them as reliable infrastructure in production workflows.

**MCP configurations.** The `.mcp.json` files in this repository define MCP server connections for third-party tools (CRM, analytics, communication platforms). MCP server availability, authentication behavior, tool schema, and rate limits are controlled by the respective third-party providers and may change without notice. MCP-dependent skills will degrade or fail if the underlying connector is unavailable, misconfigured, or returns unexpected data shapes.

**Connector and data dependencies.** Many skills in this suite require live data from external systems — Salesforce, HubSpot, Gainsight, Slack, and others. The quality of skill outputs is directly dependent on the quality, completeness, and currency of the data those connectors surface. Skills that produce health scores, renewal forecasts, churn risk assessments, or expansion recommendations are only as reliable as the underlying data. No skill in this suite constitutes a substitute for human judgment on commercial decisions.

**Confidential and sensitive data.** Skills in the csm, renewals, rev-ops, and cs-ops plugins are designed to operate on confidential customer data, contract terms, ARR figures, churn risk assessments, and renewal pipeline information. Before connecting live production data to any plugin, ensure your organization's data handling, privacy, and security requirements are met. Review connector permissions carefully — grant only the access each plugin requires to function.

**Methodology frameworks.** References to SuccessCOACHING methodologies (TARO, Customer Lifecycle, Value Chain, Two-Layer Outcome/Value Model) describe frameworks that inform skill design. These frameworks are encoded as structural guidance, not executable rules. Claude interprets and applies them through language model inference; outputs may diverge from strict framework intent. Practitioners familiar with SuccessCOACHING methodologies should treat agent outputs as informed starting points, not authoritative framework applications.

**No warranty.** This suite is provided "as is" under the Apache License 2.0. SuccessCOACHING makes no representations or warranties about the accuracy, completeness, or fitness for a particular purpose of any skill, plugin, agent, hook, or configuration in this repository. See the [License](./LICENSE) for the full terms.
