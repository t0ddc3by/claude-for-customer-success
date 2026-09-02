---
name: team-vbs-diagnostic
description: >
  Team-level value-based selling diagnostic and adoption plan: audit how value
  is currently communicated across customer touchpoints (call notes,
  proposals, emails, renewal decks), score the team against the VBS good/done
  rubric dimensions, and produce a phased adoption plan plus per-person
  Start/Stop/Change playbooks with 90-day actions. For revenue and CS leaders
  rolling VBS discipline into a team, and for quarterly re-checks of whether
  the discipline is holding under pipeline pressure.
argument-hint: "[--audit <artifact-folder> | --playbook <person> | --recheck]"
version: "0.1.0"
deployment_target: plugin
---

# /vbs:team-vbs-diagnostic

VBS is a mindset and an operating discipline, not a training event. Anchors: VBS-115 practices (Diagnostic Value Communication Audit, Phased VBS Transformation, VBS Playbook).

[PROPOSED]

---

## Use when

- Rolling the vbs plugin into a team and needing the current-state read first
- Building individual Start/Stop/Change playbooks after training or onboarding
- Quarterly recheck: is the discipline holding, or is pressure eroding it? (`--recheck`)
- Leadership wants evidence of where value communication actually stands versus where it is asserted to stand

## Do NOT use for

- Individual deal work (every other vbs skill)
- Performance evaluation of individuals (the diagnostic audits artifacts and process, and its outputs are coaching inputs, not review inputs; the skill states this in its output)

## Typical activation

"Audit how the team talks about value" / "build Sam's VBS playbook" / "quarterly VBS discipline check"

---

## Workflow

1. `--audit`: sample provided artifacts (calls, proposals, emails, decks) and score against the diagnostic dimensions: outcome-language vs. feature-language ratio, promises with catalog anchors vs. without, dollar-quantified cost of inaction present vs. asserted, discovery questions vs. pitch statements, value-led vs. discount-led responses to pressure. Report per dimension with verbatim examples (anonymized), team-level.
2. Map findings to the phased transformation model: (1) diagnostic and vision alignment, (2) foundation and capability building, (3) scaled process integration, (4) cultural embedding. Name the team's current phase and the two actions that advance it.
3. `--playbook`: per person, from their own artifacts and the team findings: 3 Start, 3 Stop, 3 approach-differently, each concrete ("Start: one outcome-focused question per call. Stop: leading with product updates."), plus the 90-day plan with monthly self-review checkpoints (Regular Action Plan Revisits practice) and a peer-accountability pairing.
4. `--recheck`: re-run the audit dimensions on fresh artifacts; trend against the prior diagnostic; pressure erosion (discount-led responses creeping back, catalog anchors dropping) is the finding to lead with.
5. Save the diagnostic and playbooks to the team workspace.

## Output contract

Dimension scores with examples, current transformation phase, two advancing actions, then playbooks. Coaching frame throughout; no individual rankings.

## Security & Permissions

Reads only user-provided artifact samples and team workspace; anonymizes examples in team-level output; no network access.

## Trust & Verification

Every score cites sampled artifacts; trends compare dated diagnostics; the coaching-not-evaluation boundary is stated in every output. Anchors: VBS-115 (Diagnostic Value Communication Audit, Phased VBS Transformation, Personal VBS Playbook, Peer Sharing and Accountability, Model Behaviors to Raise Team Bar).
