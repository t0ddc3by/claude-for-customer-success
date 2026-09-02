---
name: jtbd-starter-set-generator
description: >
  Produce a hypothesized Jobs-to-be-Done starter set (functional, social, and
  emotional job statements, pains, gains, and trigger conditions) from the
  same public-evidence research pass that seeds a provisional Outcome Catalog,
  plus the switch-interview guide designed to validate both in one coordinated
  interview effort. The vendor-agnostic ceiling of legitimate ambition, and
  the designated counterweight to signal-visibility bias: switch interviews
  reach quiet, severe-pain accounts that loud-signal triage never surfaces.
  Everything produced is hypothesis until interviews validate it; nothing
  here is positioning input.
argument-hint: "[--from-research <notes> | --interview-guide | --quiet-segment-scan]"
version: "0.1.0"
deployment_target: plugin
---

# /vfa:jtbd-starter-set-generator

The job exists independent of the product; interview switchers, not dashboards. Anchors: jtbd-outcome-catalog-integration-framework §2, VFAS §5.5, gap 4.3.

[PROPOSED]

---

## Use when

- A coordinated research pass is starting and both the JTBD side and the provisional catalog should bootstrap from one effort
- Switch interviews are being planned and need a guide that validates jobs AND catalog hypotheses in the same sessions
- Hunting quiet segments: a severe job pattern with no loud-signal population is the gap 4.3 finding this skill exists to surface (`--quiet-segment-scan`)
- Lost-deal or churned-customer interviews are being designed (the population the catalog and registry structurally cannot reach)

## Do NOT use for

- Turning a hypothesized job into a market-facing claim (the JTBD-to-catalog proof gate: no aspiration ships without a sales-eligible catalog entry; validated-but-uncataloged jobs create provisional entries instead)
- Positioning work for a segment with no PMF evidence behind it (per the JTBD-PMF binding: a job with no PMF-validated segment is a research finding, routed to PMF Steps 1-2, not to messaging)
- Catalog entry authoring (rev-ops entry-builder skills own that; this skill hands them hypotheses)

## Typical activation

"Bootstrap the JTBD starter set from this research" / "build the switch-interview guide" / "is there a quiet segment behind this job pattern?"

---

## Workflow

1. Read config and the research inputs (public evidence, review mining, win/loss notes, provisional catalog draft if one exists).
2. Draft candidate job statements in the canonical form (when [situation], I want to [motivation], so I can [outcome]), each with: type (functional/social/emotional), hypothesized pains and gains, hypothesized trigger conditions (which double as ICVP S2 qualification inputs), and an evidence pointer. Every statement is tagged HYPOTHESIS.
3. Cross-reference the provisional catalog: jobs with a plausible catalog anchor are noted; jobs with none are flagged as potential proof-gaps (real demand the product may not serve; honest input to the Roadmap Demand Register conversation).
4. `--interview-guide`: build the switch-interview guide: recruit criteria (recent switchers in or out, lost deals, churned accounts), the timeline-reconstruction spine (first thought, passive looking, event one, event two, deciding), question sets that test the job hypotheses without leading, and the catalog-validation probes woven in so one interview program feeds both artifacts.
5. `--quiet-segment-scan`: compare validated job patterns against the loud-signal population from ICVP triage; a severe validated job with no corresponding signal-rich cohort becomes a named quiet-segment hypothesis, routed to the ICVP nomination lane and the drift-sentinel watch list.
6. Save the starter set and guide to the research workspace.

## Output contract

Job statements table (all tagged HYPOTHESIS, each with evidence pointer and catalog cross-reference), then the guide or scan output. The validation path is stated at the top: nothing here reaches positioning until interviews validate it and the proof gate maps it.

## Security & Permissions

Reads user-supplied research materials and local workspaces; no network access in this version (research collection happens outside the skill); no catalog writes.

## Trust & Verification

Hypothesis tags are non-removable by this skill; validation status changes only via recorded interview evidence. Anchors: jtbd-outcome-catalog-integration-framework §2 (shared bootstrap, proof gate), VFAS gaps 4.3 and 4.9.
