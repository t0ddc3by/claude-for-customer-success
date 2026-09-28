# Managed Agent Cookbooks — Claude for Customer Success

Eleven agents for teams running Claude as a background workflow engine. Six headless scheduled
agents orchestrate a fleet of subagents for recurring CS tasks automatically. Four on-demand
managed agents run multi-stage pipelines when triggered by a CSM for account-specific work.
One event-driven agent triggers automatically when a CSQL reaches `won` status and produces
an onboarding plan before the first CSM touchpoint.

---

## Agent Directory

| Agent | Plugin | Cadence | What it produces |
|-------|--------|---------|-----------------|
| [`health-watcher`](./health-watcher/) | csm | Daily / Weekly | Health score alert digest — accounts with meaningful score movement since the prior run |
| [`churn-signal-digest`](./churn-signal-digest/) | csm | Daily / Weekly | Cross-source churn signal digest ranked P1/P2/P3 by severity |
| [`qbr-prep-agent`](./qbr-prep-agent/) | csm | On-demand (or scheduled 5 days pre-renewal) | Complete QBR prep package: snapshot, achievement assessment, narrative draft, slide outline |
| [`renewal-scanner`](./renewal-scanner/) | renewals | Daily / Weekly | Per-account renewal brief covering risk classification, expansion signals, and recommended plays |
| [`onboarding-milestone-tracker`](./onboarding-milestone-tracker/) | onboarding | Weekday mornings | Onboarding milestone report — overdue, at-risk, and due-soon accounts across the full book |
| [`portfolio-segment-digest`](./portfolio-segment-digest/) | cs-ops | Weekly (Monday) | Segment-level health distribution roll-up — band shifts, ARR at risk by segment, capacity flags, and top at-risk accounts for CS Ops/leadership |
| [`adoption-motion-agent`](./adoption-motion/) | csm | On-demand | Four-section Adoption Motion Report: feature coverage map, gap diagnosis (6-type taxonomy), prescribed TARO play, CSM next actions |
| [`expansion-builder-agent`](./expansion-builder/) | csm | On-demand | Four-section Expansion Report: whitespace inventory, business case (evidence-labeled), AE handoff package, CSM next actions |
| [`advocacy-agent`](./advocacy/) | csm | On-demand | Advocacy Package: burnout-protected advocate qualification, ask script or story structure, cs-platform task creation |
| [`churn-intelligence-agent`](./churn-intelligence/) | renewals | On-demand | Churn Intelligence Report (8 sections) written to cs-platform: signal timeline, churn drivers, exit interview guide, postmortem, learnings, win-back assessment |
| [`expansion-onboarding-agent`](./expansion-onboarding-agent/) | onboarding | Event-driven (CSQL → won) | Onboarding plan and CSM notification — triggered automatically when a CSQL reaches `won` status; plan delivered to Slack before first CSM touchpoint |

---

## Two-Layer Agent Architecture

Each managed agent exists in two complementary forms. Understanding which layer is authoritative for what prevents configuration drift and deployment confusion.

### Layer 1 — Deployable orchestrator spec (plugin `agents/` directory)

Single-file agent specs in each plugin's `agents/` directory are the **authoritative deployment artifacts**. The Claude Agent SDK reads these files to resolve agent identity, routing, and invocation. Each file has a YAML frontmatter block followed by a human-readable spec:

```
csm/agents/
├── adoption-motion-agent.md      ← SDK reads this; CSM triggers this
├── expansion-builder-agent.md
├── advocacy-agent.md
├── health-watcher.md
├── churn-signal-digest.md
└── qbr-prep-agent.md

renewals/agents/
├── renewal-scanner.md
└── churn-intelligence-agent.md
```

The `description` field in each file's YAML frontmatter contains a `Cookbook specification:` line that points to the matching cookbook directory. This is the canonical link between the two layers.

### Layer 2 — Reference architecture (this directory)

Cookbook directories in `managed-agent-cookbooks/` are the **authoritative reference architecture**. They define subagent design, configuration field specifications, deployment guidance, data gap behavior, scheduling patterns, and steering examples. Changes to subagent behavior, guardrails, or output format are specified here first.

```
managed-agent-cookbooks/
├── adoption-motion/              ← reference architecture for adoption-motion-agent
│   ├── README.md                 ← deployment guide, config reference, output spec
│   ├── agent.yaml                ← SDK-format orchestrator yaml (alternate deploy format)
│   ├── subagents/                ← subagent prompt files dispatched by orchestrator
│   └── steering-examples.json
├── expansion-builder/
├── advocacy/
├── churn-intelligence/
├── health-watcher/
│   ├── cookbook.md               ← narrative implementation guide (present in 6 cookbooks)
│   ├── README.md
│   ├── agent.yaml
│   ├── subagents/
│   └── steering-examples.json
...
```

### cookbook.md vs. README.md

Six cookbooks (health-watcher, churn-signal-digest, qbr-prep-agent, renewal-scanner, onboarding-milestone-tracker, portfolio-segment-digest) include a `cookbook.md` with a full **narrative implementation guide** — orchestrator logic reasoning, edge-case handling rationale, and embedded prompt design examples. This layer answers "why" the orchestrator is designed the way it is and is most useful during initial customization or when extending subagent behavior.

Four cookbooks (adoption-motion, expansion-builder, advocacy, churn-intelligence) have no `cookbook.md`. For these agents, the `README.md` covers deployment configuration and output spec, and the Layer 1 single-file agent (in the plugin `agents/` directory) carries the full behavioral spec including guardrails, pipeline stages, and "does NOT do" boundaries. These four cookbooks are **deployment-complete without a narrative cookbook.md** — the behavioral detail lives in the single-file agent, which is more accessible to CSMs triggering the agent than a cookbook narrative would be.

**The README.md is always present and always authoritative** for deployment configuration and output format. The `cookbook.md`, where present, provides additional narrative context useful during implementation or customization. Its absence in four cookbooks is intentional, not an omission.

### Which layer to modify

| Change type | Modify |
|-------------|--------|
| Trigger phrases, agent description, routing behavior | Layer 1 — plugin `agents/*.md` YAML frontmatter |
| Agent guardrails, behavioral rules, output sections | Layer 1 — plugin `agents/*.md` body |
| Subagent prompt, subagent logic, subagent output format | Layer 2 — `managed-agent-cookbooks/[agent]/subagents/*.md` |
| Configuration field definitions, connector requirements | Layer 2 — `managed-agent-cookbooks/[agent]/README.md` |
| Scheduling defaults, deployment guidance | Layer 2 — `managed-agent-cookbooks/[agent]/README.md` |
| Steering examples, on-demand trigger phrases | Layer 2 — `managed-agent-cookbooks/[agent]/steering-examples.json` |

When modifying subagent behavior in Layer 2, update the relevant Layer 1 guardrails and output sections if they reference the changed behavior. Both layers must remain consistent.

---

## Architecture

All ten agents follow the same structural pattern: a single orchestrator that reads config,
dispatches subagents in sequence (or parallel where appropriate), and delivers output to
Slack and/or a file path. The six scheduled agents run autonomously on a cron cadence. The
four on-demand agents run when triggered by a CSM and return their output in chat.

```
Managed Agent (orchestrator)
│
├── reads: plugin CLAUDE.md + shared company-profile.md
│
├── Subagent 1: [Data Puller]
│   Queries configured connectors; returns structured records.
│   If connector unavailable → surface error; orchestrator stops.
│
├── Subagent 2: [Analyzer / Classifier]
│   Applies thresholds, rules, or frameworks to raw records.
│   Receives pre-pulled data — calls no connectors itself.
│
├── [Subagent 3 (if needed): Secondary Analyzer or Parallel Composer]
│   Used when the analysis has two distinct dimensions that
│   benefit from separate prompts, or when drafting runs in
│   parallel with another composition task.
│
└── Subagent N: [Composer / Formatter]
    Formats the tiered output into markdown and Slack mrkdwn.
    Delivers to configured output targets.
    Calls no data connectors except Slack for delivery.
```

### Subagent count by agent

| Agent | Subagents | Parallel dispatch |
|-------|-----------|------------------|
| health-watcher | 3 (Health Reader → Trend Analyzer → Alert Composer) | No |
| churn-signal-digest | 3 (Signal Collector → Signal Analyzer → Digest Composer) | No |
| qbr-prep-agent | 4 (Account Data Assembler → Achievement Analyzer → Narrative Drafter ‖ Slide Outline Generator) | Yes — Step 5 |
| renewal-scanner | 3 (Pipeline Puller → Risk & Expansion Classifier → Renewal Brief Composer) | No |
| onboarding-milestone-tracker | 3 (Milestone Puller → Risk Assessor → Report Composer) | No |
| portfolio-segment-digest | 4 (Segment Data Puller → Distribution Analyzer → Portfolio Summarizer → Report Composer) | No |
| adoption-motion-agent | 3 (Product Surface Analyzer → Adoption Gap Identifier → Motion Planner) | No |
| expansion-builder-agent | 3 subagents + orchestrator health gate (Whitespace Analyzer → [gate] → Business Case Builder → Expansion Handoff Coordinator) | No |
| advocacy-agent | 3 (Advocate Qualifier → reference-matcher or story-builder [conditional route] → cs-platform task creation) | No |
| churn-intelligence-agent | 4 (exit-interviewer ‖ postmortem-facilitator → learning-extractor → winback-profiler [conditional]) | Yes — Step 2 |
| expansion-onboarding-agent | 3 (CSQL Won Scanner → Onboarding Plan Creator → Notification Composer) | No |

**Enrichment exception (renewal-scanner):** The renewal-scanner orchestrator performs
connector calls directly in Step 3 — pulling health score, usage, and support data — before
dispatching the Risk & Expansion Classifier. The classifier receives a pre-enriched account
list and calls no connectors itself. This keeps the classification prompt narrow and
prevents each classifier invocation from accumulating connector-call overhead.

---

## Subagent Grounding Protocol

All managed agents dispatch subagents that receive orchestrator-assembled data — config
values read in Step 1, connector records from previous steps, and baseline data loaded at
run start. An LLM subagent given a prompt referencing data it cannot independently read
may produce outputs that pattern-match the expected format without being grounded in the
actual data passed. The grounding protocol prevents this.

### Protocol (applied at every subagent dispatch step)

1. **Generate a dispatch marker.** At each dispatch, generate a unique marker:
   `MARKER-[8-char random hex]` — new per dispatch, never reused within or across runs.

2. **Embed in the dispatch brief.** Include at the top of every subagent dispatch prompt:
   > "Your response must begin with `[marker]` on its own line before any other content."

3. **Verify on return.** Before treating subagent output as grounded:
   - If marker appears on line 1: proceed.
   - If marker is absent: surface "[Subagent name] returned unverified output — marker not
     found. Halting run." and stop.

### Per-agent spec reference

Each agent spec includes a grounding note at every dispatch step: "Apply grounding protocol
(see managed-agent-cookbooks/README.md → Subagent Grounding Protocol): generate unique
dispatch marker; embed in brief; verify marker on line 1 before treating output as grounded."

---

## Security Model

### What managed agents CAN do

- Read from all configured data connectors (CRM, health platform, usage, support, PM tool)
- Read from the filesystem: plugin CLAUDE.md templates and shared company-profile.md
- Write to the filesystem: output digests and the health-watcher baseline file
- Post to Slack via the configured Slack connector (delivery only)
- Dispatch subagents via the Task tool

### What managed agents CANNOT do

- **Modify CRM records** — no creates, updates, or deletes to CRM data
- **Modify PM tool records** — no status updates, no task creation
- **Send direct messages to individual CSMs** — output goes to a configured channel or file
- **Draft or send customer-facing outreach** — agents report to the internal CS team; customer
  communication is always CSM-initiated
- **Run plays autonomously** — TARO play recommendations in output are for the CSM to
  evaluate and act on; the agent does not trigger plays
- **Estimate missing data** — missing ARR, renewal dates, contract start dates, or health
  scores are flagged in the output; never derived or estimated

### Tool grants by agent

| Agent | Read | Write | Task | Slack post | Search/Query |
|-------|------|-------|------|-----------|-------------|
| health-watcher | ✓ | ✓ (baseline + digest) | ✓ | ✓ | ✓ |
| churn-signal-digest | ✓ | ✓ (baseline + digest) | ✓ | ✓ | ✓ |
| qbr-prep-agent | ✓ | ✓ (prep package) | ✓ | — | ✓ |
| renewal-scanner | ✓ | ✓ (brief) | ✓ | ✓ | ✓ |
| onboarding-milestone-tracker | ✓ | ✓ (report) | ✓ | ✓ | ✓ |
| portfolio-segment-digest | ✓ | ✓ (baseline + digest) | ✓ | ✓ | ✓ |
| adoption-motion-agent | ✓ | — | ✓ | — | ✓ |
| expansion-builder-agent | ✓ | — (task created by subagent) | ✓ | — | ✓ |
| advocacy-agent | ✓ | — (task created by subagent) | ✓ | — | ✓ |
| churn-intelligence-agent | ✓ | ✓ (Churn Intelligence Report + optional Stage 0 handoff to cs-platform) | ✓ | — | ✓ |
| expansion-onboarding-agent | ✓ | ✓ (onboarding plan) | ✓ | ✓ | ✓ |

The qbr-prep-agent does not post to Slack by default — QBR prep packages are saved to
a file path and reviewed by the CSM before any sharing.

The four on-demand agents (adoption-motion, expansion-builder, advocacy, churn-intelligence)
do not post to Slack. Output is delivered in chat to the CSM who triggered the run.
adoption-motion does not write files. expansion-builder and advocacy write cs-platform tasks
via their final subagent (not direct orchestrator writes). churn-intelligence writes the
Churn Intelligence Report directly to cs-platform before returning to the CSM.

**Tool grant security caveat:** The `mcp__*__query_*` and `mcp__*__search_*` wildcard
grants assume connector authors follow the convention that `query_` and `search_` tools
are read-only operations. Before deploying any new connector against a managed agent,
verify that no `query_*` or `search_*` tool in that connector performs write, create,
update, or delete operations. Connectors from unverified sources should be audited against
the CS Skill Security Baseline before being granted these wildcards.

---

## Connector Requirements

### Required connectors (by agent)

| Agent | Required | Optional |
|-------|----------|---------|
| health-watcher | Health score source | Slack, CRM (CSM lookup) |
| churn-signal-digest | CRM | Support, usage, NPS/CSAT, Slack |
| qbr-prep-agent | CRM | Usage, support, NPS/CSAT |
| renewal-scanner | CRM | Health score source, usage, support, Slack |
| onboarding-milestone-tracker | Project management (PM) tool | Slack |
| portfolio-segment-digest | CS Platform, CRM | Slack, BI tool |
| adoption-motion-agent | cs-platform | product-analytics (coverage map; flagged unavailable if absent) |
| expansion-builder-agent | cs-platform, CRM | product-analytics (health gate prompts manual confirm if absent) |
| advocacy-agent | cs-platform, CRM | — |
| churn-intelligence-agent | cs-platform, CRM | product-analytics (90-day usage trend) |
| expansion-onboarding-agent | CSQL source (CRM), cs-platform | Slack (notification delivery) |

All agents degrade gracefully when optional connectors are unavailable — they note the
gap in the output rather than halting. Required connector unavailability halts the run
immediately to prevent output based on stale or fabricated data.

### Connector names by platform

Configure the connector name in the plugin CLAUDE.md to match your installed MCP connector:

| Platform | Typical connector name | Agents that use it |
|----------|----------------------|-------------------|
| Salesforce | `salesforce-mcp` | churn-signal-digest, qbr-prep-agent, renewal-scanner, portfolio-segment-digest |
| HubSpot | `hubspot-mcp` | churn-signal-digest, qbr-prep-agent, renewal-scanner, portfolio-segment-digest |
| Gainsight | `gainsight-mcp` | health-watcher, renewal-scanner, portfolio-segment-digest |
| Totango | `totango-mcp` | health-watcher, renewal-scanner, portfolio-segment-digest |
| Asana | `asana-mcp` | onboarding-milestone-tracker |
| Linear | `linear-mcp` | onboarding-milestone-tracker |
| Jira | `jira-mcp` | onboarding-milestone-tracker |
| Slack | `slack-mcp` | health-watcher, churn-signal-digest, renewal-scanner, onboarding-milestone-tracker, portfolio-segment-digest |

---

## Configuration

### Shared configuration files

All agents read from a two-file config stack:

```
~/.claude/plugins/config/claude-for-customer-success/
├── company-profile.md          # Shared — all agents read this (product, segments, methodology)
├── csm/CLAUDE.md               # Read by: health-watcher, churn-signal-digest, qbr-prep-agent, renewal-scanner
├── cs-ops/CLAUDE.md            # Read by: portfolio-segment-digest (segment definitions, capacity model, cadence)
└── onboarding/CLAUDE.md        # Read by: onboarding-milestone-tracker, expansion-onboarding-agent (NOT csm/CLAUDE.md)
```

The renewal-scanner reads `../csm/CLAUDE.md` (not a dedicated `../renewals/CLAUDE.md`) because
the renewal pipeline configuration is part of the CSM company profile. The portfolio-segment-digest
reads `../cs-ops/CLAUDE.md` (not csm/CLAUDE.md) because segment definitions, capacity targets, and
reporting cadences are configured there. The onboarding milestone tracker and the expansion-onboarding-agent both read from
`../onboarding/CLAUDE.md` — they are the only CSM-adjacent agents that do not read csm/CLAUDE.md.
The churn-intelligence-agent reads `../renewals/CLAUDE.md` — this file must exist and be populated
before deploying the churn-intelligence-agent. It is the only agent in the renewals plugin that has
its own dedicated config file separate from csm/CLAUDE.md. Run `/renewals:cold-start-interview` to
build it before first run.

### Setting up configuration

Run the cold-start interview in the relevant plugin before deploying a managed agent.
The interview builds the required config file interactively:

```bash
/csm:cold-start-interview       # For health-watcher, churn-signal-digest, qbr-prep-agent, renewal-scanner
/cs-ops:cold-start-interview    # For portfolio-segment-digest
/onboarding:cold-start-interview # For onboarding-milestone-tracker
```

If the config file contains `[PLACEHOLDER]` values, the agent will surface which fields
need configuration before completing its first run.

---

## Scheduling

All scheduled agents are deployed using Claude Code's scheduled task mechanism. Invoke
the relevant agent on a cron schedule.

### Recommended schedule reference

| Agent | Recommended cron | Prompt |
|-------|-----------------|--------|
| health-watcher (daily) | `0 8 * * *` | `"Run the health watcher."` |
| health-watcher (weekly) | `30 8 * * 1` | `"Run the weekly health watcher."` |
| churn-signal-digest (daily) | `0 7 * * *` | `"Run the churn signal digest."` |
| churn-signal-digest (weekly) | `30 7 * * 1` | `"Run the weekly churn signal digest."` |
| renewal-scanner (daily) | `0 7 * * 1-5` | `"Run the renewal scanner."` |
| renewal-scanner (weekly) | `30 7 * * 1` | `"Run the weekly renewal pipeline summary."` |
| onboarding-milestone-tracker | `0 7 * * 1-5` | `"Run the onboarding milestone tracker."` |
| portfolio-segment-digest | `0 7 * * 1` | `"Run the portfolio segment digest."` |
| qbr-prep-agent | On-demand or 5 days pre-renewal | `"Run QBR prep for [Account Name]."` |

### On-demand invocation

All agents can also be triggered manually. Each agent's README includes a
`steering-examples.json` with the complete prompting pattern library for that agent.

The expansion-onboarding-agent is event-driven and has no cron schedule. It fires when the
orchestrator detects a CSQL record transitioning to `won` status. Trigger it by polling or
via a CRM webhook — see the [cookbook](./expansion-onboarding-agent/cookbook.md) for the
recommended polling interval and event detection pattern.

The four on-demand agents (adoption-motion, expansion-builder, advocacy, churn-intelligence)
are CSM-triggered only and have no recommended cron schedule. Trigger them directly in chat:

| Agent | Example trigger |
|-------|----------------|
| adoption-motion-agent | `"Run adoption motion for Acme Corp."` |
| expansion-builder-agent | `"Run expansion builder for Acme Corp."` |
| advocacy-agent | `"Build advocacy package for Acme Corp."` |
| churn-intelligence-agent | `"Run churn intelligence for Acme Corp."` |

Common on-demand triggers for scheduled agents:

```
"Run the health watcher."
"Check for churn signals this week."
"Run QBR prep for Acme Corp."
"What's renewing in the next 90 days?"
"Which onboarding accounts need attention?"
```

---

## Shared Output Conventions

All ten agents follow these conventions regardless of individual formatting differences:

**Data provenance:** Every output section names its data source connector and includes a
data-as-of timestamp. Stale or missing data is never silently omitted — it is surfaced
in the output as a named gap.

**Severity language:** Agents use observational language only. "Signaling renewal risk"
not "at risk of churning." "Score dropped from 72 to 57" not "account is deteriorating."
The CSM owns the interpretation; the agent presents observations.

**Internal metrics:** TtV projections and any field labeled `[review — internal planning
target]` in the config file never appear in any agent output — digest, report, Slack post,
or saved file.

**No-signal all-clears:** When an agent's run finds nothing to flag (zero overdue
milestones, zero P1 signals, zero high-risk renewals), it posts a brief all-clear
message rather than omitting the output entirely. Silence is not an all-clear signal.

**Missing data handling:** Missing ARR, renewal dates, health scores, or contract start
dates are flagged in the output (e.g., `[unverified dates]`). The agent does not estimate,
impute, or derive these values from other fields.

---

## Agent-Specific Documentation

For deployment instructions, full configuration field reference, output format
specification, and per-agent prompting patterns, see each agent's README:

- [Health Watcher](./health-watcher/README.md) — health score monitoring and movement alerts
- [Churn Signal Digest](./churn-signal-digest/README.md) — cross-source signal aggregation and severity ranking
- [QBR Prep Agent](./qbr-prep-agent/README.md) — account research and QBR material drafting
- [Renewal Scanner](./renewal-scanner/README.md) — renewal pipeline risk classification and expansion signals
- [Onboarding Milestone Tracker](./onboarding-milestone-tracker/README.md) — M1–M5 milestone monitoring and at-risk detection
- [Portfolio Segment Digest](./portfolio-segment-digest/README.md) — segment-level health distribution shifts, ARR at risk by segment, and capacity flags for CS Ops and leadership
- [Adoption Motion Agent](./adoption-motion/README.md) — adoption gap diagnosis using six-type taxonomy and TARO play prescription
- [Expansion Builder Agent](./expansion-builder/README.md) — whitespace analysis, adoption health gate, business case construction, and AE handoff
- [Advocacy Agent](./advocacy/README.md) — advocate qualification with burnout protection gates and advocacy package generation
- [Churn Intelligence Agent](./churn-intelligence/README.md) — exit interview guide, blameless postmortem, playbook learnings, and win-back assessment
- [Expansion Onboarding Agent](./expansion-onboarding-agent/cookbook.md) — event-driven onboarding plan generation triggered on CSQL `won`; two-layer idempotency, dry-run mode, and Slack notification via Notification Composer
