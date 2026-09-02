---
name: customize
description: >
  Update the vbs plugin configuration: catalog location, buyer personas, deal
  workspace convention, commercial boundary, and evidence-plan defaults,
  without re-running the full cold-start interview. Also the review surface
  (--show). Distinct from /vbs:cold-start-interview, which is the initial
  setup flow for a blank configuration.
argument-hint: "[--section <section-name> | --show | --reset <section-name>]"
version: "0.1.0"
deployment_target: plugin
config_skill: true
---

# /vbs:customize

Update Value-Based Selling configuration section by section.

[PROPOSED]

---

## Use when

- A single config section changed (catalog moved, new persona entered the committee pattern, commercial authority shifted)
- Reviewing the current configuration (`--show`)
- Resetting one section to placeholder state after confirmation (`--reset`)

## Do NOT use for

- First-time setup on a blank config (use `/vbs:cold-start-interview`)
- Editing the Outcome Catalog itself (rev-ops catalog skills own that)

## Typical activation

"Update the vbs config"; "show me the current vbs configuration"; "deal desk now owns discount approval, update the boundary".

---

## Behavior

Read company profile, then the vbs config at `~/.claude/plugins/config/claude-for-customer-success/vbs/CLAUDE.md`. For `--section`, re-interview only that section (one AskUserQuestion at a time, AUQ resilience rules). For `--show`, render the config with placeholders highlighted. For `--reset`, restore a section to placeholder state after confirmation. A commercial-boundary change is echoed back verbatim for confirmation before writing; it changes what the negotiation skills will and will not do.

## Security & Permissions

Writes only to the plugin config path; no network access.

## Trust & Verification

`--show` is the audit surface; boundary changes are confirmed verbatim before commit.
