---
name: customize
description: >
  Update the vfa plugin configuration: PMF segment status, ICP and catalog
  locations, vendor cost model, signal half-lives, override budget, and
  cold-start posture, without re-running the full cold-start interview. Also
  the review surface (--show) and the entry point for proposing a new scoring
  weights version after an R2 loop re-fit. Distinct from
  /vfa:cold-start-interview, which is the initial setup flow for a blank
  configuration.
argument-hint: "[--section <section-name> | --show | --reset <section-name> | --propose-weights <path>]"
version: "0.1.0"
deployment_target: plugin
config_skill: true
---

# /vfa:customize

Update Value-First Acquisition configuration section by section.

[PROPOSED]

---

## Use when

- A single config section changed (new catalog location, revised override budget, updated vendor pricing)
- Reviewing the current configuration (`--show`)
- The Registry crossed the ten-entry threshold for a segment and the cold-start posture should be retired for it
- An R2 re-fit produced a proposed `weights.json` update (`--propose-weights <path>`): present the diff against the current version, require explicit human approval, and record the decision; NEVER apply silently

## Do NOT use for

- First-time setup on a blank config (use `/vfa:cold-start-interview`)
- Editing scoring weights conversationally without a proposed config version (prohibited by the plugin's governance rules)

## Typical activation

"Update the vfa config"; "show me the current vfa configuration"; "our override budget changed"; "apply the proposed weight re-fit".

---

## Behavior

Read company profile, then the vfa config at `~/.claude/plugins/config/claude-for-customer-success/vfa/CLAUDE.md`. For `--section`, re-interview only that section (one AskUserQuestion at a time, AUQ resilience rules). For `--show`, render the config with placeholders highlighted. For `--reset`, restore a section to placeholder state after confirmation. For `--propose-weights`, show a field-by-field diff of the proposed vs. current `weights.json`, confirm spec_version compatibility, obtain explicit approval, then write the new version alongside a dated decision note; a declined proposal is recorded as declined.

## Security & Permissions

Writes only to the plugin config path and, for approved weight proposals, the skill's config directory; no network access.

## Trust & Verification

Every weight change leaves a dated decision note naming the approver and the versions involved; `--show` is the audit surface.
