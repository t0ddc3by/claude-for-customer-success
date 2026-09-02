---
name: cold-start-interview
description: >
  Run the vbs plugin configuration interview: collects the Outcome Catalog
  location, buyer personas and their metrics, the deal workspace convention,
  and the commercial boundary (who owns pricing and discount authority), then
  writes the vbs practice config file. Runs automatically on first use of any
  vbs skill when config is missing. Distinct from other plugins'
  cold-start-interview skills: this one configures the seller-facing deal
  craft (discovery, qualification, gate, narrative, negotiation), not CS
  execution or acquisition-system gating.
argument-hint: "[--full | --section <section-name>]"
version: "0.1.0"
deployment_target: plugin
config_skill: true
---

# /vbs:cold-start-interview

Configure Value-Based Selling so every skill sells your outcomes, from your catalog, inside your commercial rules.

[PROPOSED]

---

## Use when

- Installing the vbs plugin for the first time (no config file exists)
- Any vbs skill stops and routes here because config is missing or carries pervasive `[PLACEHOLDER]` markers
- A catalog restructure, persona shift, or commercial-authority change invalidates the existing config

## Do NOT use for

- Targeted single-section updates when config exists and is mostly complete (use `/vbs:customize --section <name>`)
- Reviewing current configuration (use `/vbs:customize --show`)

## Typical activation

Automatic routing from any vbs skill on missing config; "set up the vbs plugin"; "configure value-based selling".

---

## Interview flow

Read `~/.claude/plugins/config/claude-for-customer-success/company-profile.md` first; do not re-ask what it already answers. Then collect, one AskUserQuestion at a time (prose fallback per AUQ resilience; honor `/auq force-prose`):

1. **Outcome Catalog**: location; confirm the canonical 7-tier deliverability field (deviations route to the taxonomy crosswalk). Without a catalog, state plainly that outcome qualification degrades to seller judgment, which is the drift this plugin exists to prevent; offer the rev-ops catalog skills as the prerequisite path.
2. **Personas**: the 3-5 buyer roles typically in a committee, each with the metric they answer for and their common fear.
3. **Selling motion**: sales-led, PLG-assist, or expansion-led; typical committee size; where the vfa ICVP score can be found on an account, if the vfa plugin is installed.
4. **Deal workspace**: where per-deal artifacts live (motivation records, promise sets, gate results, prep sheets).
5. **Commercial boundary**: who owns pricing, discount floors, and terms approval; the vbs negotiation skills stop at that line.
6. **Evidence plan defaults**: how delivered value is typically measured and who acknowledges it (seeds the gate's dimension 5 and the Phase 3 commitment builder).

Write the completed config to `~/.claude/plugins/config/claude-for-customer-success/vbs/CLAUDE.md` (create parents as needed), replacing every placeholder or explicitly marking a section deferred. Close by naming the first recommended run: `/vbs:good-sale-gate` on the deal closest to close.

## Security & Permissions

Writes only to the plugin's own config path under the user's home; no network access; no data collection beyond the user's answers.

## Trust & Verification

Config completeness is verifiable with `/vbs:customize --show`; any remaining `[PLACEHOLDER]` blocks substantive skill runs.
