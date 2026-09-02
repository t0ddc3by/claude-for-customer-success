---
name: cold-start-interview
description: >
  Run the vfa plugin configuration interview: collects PMF status by segment,
  the ratified ICP location, the Outcome Catalog location, the vendor annual
  cost model, signal half-life defaults, the override budget, and the
  cold-start posture, then writes the vfa practice config file. Runs
  automatically on first use of any vfa skill when config is missing. Distinct
  from other plugins' cold-start-interview skills: this one configures the
  acquisition system stratum (value-fit gating and loop feedback), not
  account-level or portfolio CS execution.
argument-hint: "[--full | --section <section-name>]"
version: "0.1.0"
deployment_target: plugin
config_skill: true
---

# /vfa:cold-start-interview

Configure the Value-First Acquisition plugin so the value-fit gate scores against your actual catalog, economics, and segments, not generic defaults.

[PROPOSED]

---

## Use when

- Installing the vfa plugin for the first time (no config file exists)
- Any vfa skill stops and routes here because config is missing or carries pervasive `[PLACEHOLDER]` markers
- A major change (new ICP ratification, catalog restructure, pricing model change) invalidates the existing config

## Do NOT use for

- Targeted single-section updates when config exists and is mostly complete (use `/vfa:customize --section <name>`)
- Reviewing current configuration (use `/vfa:customize --show`)

## Typical activation

Automatic routing from any vfa skill on missing config; "set up the vfa plugin"; "configure the value-fit gate".

---

## Interview flow

Read `~/.claude/plugins/config/claude-for-customer-success/company-profile.md` first; do not re-ask what it already answers. Then collect, one AskUserQuestion at a time (prose fallback per AUQ resilience; honor `/auq force-prose`):

1. **PMF status**: which segments have confirmed PMF (survey + retention + GRR evidence), and as of when. If none: state plainly that acquisition spend ahead of validated fit is the premature-scaling anti-pattern, and offer the two L1 skills as the starting point.
2. **ICP**: where the ratified ICP and negative ICP live; hard-fail criteria for the S1 gate.
3. **Outcome Catalog**: location; confirm it uses the canonical 7-tier deliverability field (route deviations to the taxonomy crosswalk).
4. **Vendor economics**: how annual engagement cost is estimated per prospect (tiers, per-learner, flat); cost-to-serve level definitions.
5. **Signals**: the signal taxonomy in use and half-life defaults, or accept the shipped defaults.
6. **Governance**: override budget (% of quarterly advanced pipeline); who reviews the Loop 3 cohort; cold-start posture start date.

Write the completed config to `~/.claude/plugins/config/claude-for-customer-success/vfa/CLAUDE.md` (create parents as needed), replacing every placeholder or explicitly marking a section deferred. Close by naming the first recommended run: an `icvp-composite-scorer --batch` over the current ICP-qualified list.

## Security & Permissions

Writes only to the plugin's own config path under the user's home; no network access; no external data collection beyond the user's answers.

## Trust & Verification

Config completeness is verifiable with `/vfa:customize --show`; any remaining `[PLACEHOLDER]` blocks substantive skill runs.
