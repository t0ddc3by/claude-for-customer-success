# Quickstart — Claude for Customer Success

Get a plugin running in under 60 seconds. Pick your install path below, run the cold-start interview once, and every skill in that plugin knows your firm context, CRM schema, and thresholds from the first use.

---

## Install in Claude Cowork

1. Open Cowork and click the **Plugins** icon in the sidebar
2. Click **Install from file** and select the plugin file from [`dist/`](./dist/)
3. The plugin appears in your plugin list — click it to open the panel
4. Run the cold-start interview to write your company profile:

```
/[plugin]:cold-start-interview
```

> **Video walkthrough** — *coming soon*

---

## Install in Claude Code

1. Clone or download this repository
2. From the repo root, install the plugin:

```bash
/install dist/[plugin]-[version].plugin
```

Use the exact filename from `dist/` (versions are listed below). For example: `/install dist/csm-v1.0.8.plugin`.

3. Run the cold-start interview:

```bash
/[plugin]:cold-start-interview
```

**Available plugin files in `dist/`:**

| File | Plugin |
|------|--------|
| `csm-v1.0.8.plugin` | Core CSM workflows |
| `renewals-v1.0.2.plugin` | Renewal pipeline |
| `cs-ops-v1.0.2.plugin` | CS operations |
| `onboarding-v1.0.2.plugin` | Customer onboarding |
| `rev-ops-v1.1.2.plugin` | Revenue operations |
| `auq-resilience-v1.1.1.plugin` | AUQ fallback hooks (Claude Code) + `/auq` command (Cowork) |

---

## User-scoped vs. project-scoped install

Install at **user scope** (the default) when your CSM workflow touches files outside a single project folder — for example, when you're working across multiple account folders or reading from `~/.claude/plugins/config/`. User-scoped plugins are available in every Claude Code session regardless of the working directory.

Install at **project scope** only when the plugin is purpose-built for a specific repo and you want it isolated to that folder:

```bash
/install dist/[plugin]-[version].plugin --scope project
```

If skills fail to read the company profile or connector config, the most likely cause is a project-scoped install trying to read a user-level path. Reinstall at user scope.

---

## Which plugin is for me?

| Role | Start here | First command |
|------|-----------|---------------|
| Customer Success Manager | `csm` | `/csm:cold-start-interview` |
| Renewals Manager | `renewals` | `/renewals:cold-start-interview` |
| CS Operations | `cs-ops` | `/cs-ops:cold-start-interview` |
| Onboarding / Implementation | `onboarding` | `/onboarding:cold-start-interview` |
| Revenue Operations | `rev-ops` | `/rev-ops:cold-start-interview` |
| IT Admin (M365 provisioning) | `claude-for-msft-365-install` | `/claude-for-msft-365-install:setup` |
| Any plugin user | `auq-resilience` | Install alongside any other plugin |

Install `auq-resilience` alongside any other plugin to prevent dead-end AUQ widget failures. It requires no configuration.

---

## What you're installing

Each plugin is a self-contained Claude Code / Cowork bundle containing skills, commands, and connector configuration. Skills are triggered automatically when their conditions match; commands are invoked explicitly with `/[plugin]:[command]`.

The `cold-start-interview` in each plugin writes a **company profile** — a Markdown file at `~/.claude/plugins/config/claude-for-customer-success/[plugin]/CLAUDE.md`. Every subsequent skill reads that file for firm context: your CRM field names, health score thresholds, escalation matrix, renewal risk criteria, and template preferences. Update it at any time with `/[plugin]:customize`.

Connector dependencies are soft. Skills degrade gracefully when a connector is absent — they tell you what data they couldn't retrieve rather than failing silently. Edit `.mcp.json` in the plugin directory to point connectors at your specific CRM instance, CS platform, or Slack workspace.

---

## What's in the box

| Plugin | Skills | Managed agent cookbooks |
|--------|--------|------------------------|
| csm | 19 | 4 (health-watcher, churn-signal-digest, qbr-prep-agent, adoption-motion, expansion-builder, advocacy) |
| renewals | 12 | 2 (renewal-scanner, churn-intelligence) |
| cs-ops | 9 | 1 (portfolio-segment-digest) |
| onboarding | 10 | 1 (onboarding-milestone-tracker) |
| rev-ops | 36 | 5 (gtm-pulse-runner, capacity-monitor, churn-signal-scanner, deal-desk-watcher, planning-cycle-orchestrator) |
| auq-resilience | 0 skills — hooks + `/auq` command | — |
| **Total** | **86 skills** | **16 cookbook agents** |

Full skill and command descriptions are in the [Skill & Command Reference](./README.md#skill--command-reference) section of the README.

---

## Stuck?

**Plugin doesn't appear after install**
Close and reopen Cowork or restart Claude Code. If the plugin still doesn't appear, check that the `.plugin` file is not corrupted by verifying its file size is greater than zero.

**Cold-start interview widget doesn't render**
Install `auq-resilience` alongside the plugin. It catches empty widget responses and injects a prose fallback so the interview can complete. Alternatively, type `/auq-resilience:auq force-prose` to switch the session to prose-only questions for the rest of the session.

**Skills say "company profile not found"**
Run `/[plugin]:cold-start-interview` to create the profile. If you've already done that, check whether the plugin is installed at project scope but the profile is at the user path — reinstall at user scope with no `--scope` flag.

**Connector returns auth failure or timeout**
Open the plugin's `.mcp.json` and verify the endpoint URL, credentials, and scopes. Skills that depend on the connector will surface a partial output with an explicit data gap notice rather than failing silently.

**Managed agent returns "agent_id not found"**
Run `scripts/deploy-managed-agent.sh <slug>` to deploy the cookbook and write the agent ID to `.env.deploy`. Confirm the ID is loaded before calling `orchestrate.py`.

**Still stuck?**
Open an issue at [github.com/t0ddc3by/claude-for-customer-success/issues](https://github.com/t0ddc3by/claude-for-customer-success/issues) with the plugin name, the command you ran, and the error or unexpected output you received.
