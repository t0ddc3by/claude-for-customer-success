#!/usr/bin/env bash
# commit-release-2026-09-06.sh
#
# Stages and commits the CHECK 9 / frontmatter-remediation / release wave.
# RUN IN YOUR OWN TERMINAL — the Cowork sandbox cannot unlink .git/index.lock
# and cannot delete tracked files, so `git rm` and every git write fail there.
#
#   bash bin/commit-release-2026-09-06.sh
#
# All file changes are already on disk. This only stages, commits, and pushes.
#
# SCOPE NOTES — reconciled against tasks/todo.md from the 2026-09-05 session:
#   * tasks/todo.md            stays untracked (its own rule A7)
#   * bin/commit-hooks-quoting.sh stays untracked (its rule A5)
#   * bin/commit-release-2026-09-06.sh (this file) also stays untracked, same reason
#   * agents/ and plugins/ under ~/claude-cowork are ignored by that repo's
#     `/**/` rule and are deliberately not committed anywhere
#
# Commit order is deliberate: the tool that catches the defect lands first, then
# the fix, then the release that ships it.

set -euo pipefail

MONOREPO="${MONOREPO:-$HOME/claude-cowork/projects/agent-building/claude-for-customer-success}"
SKILLS="${SKILLS:-$HOME/claude-cowork/skills}"

say() { printf "\n\033[1m==> %s\033[0m\n" "$*"; }

# ---------------------------------------------------------------------------
say "0. Clear stale git index locks"
rm -f "$MONOREPO/.git/index.lock" "$SKILLS/.git/index.lock" || true

# ---------------------------------------------------------------------------
say "1. Verify green before committing"
cd "$MONOREPO"
python3 bin/generate-manifests.py --check
python3 bin/preflight.py --all --parent .

VALIDATOR="$HOME/claude-cowork/agents/agent-skill-builder/skills/skill-builder-pro/scripts/validate-plugin-frontmatter.py"
if [ -f "$VALIDATOR" ]; then
  say "1b. Frontmatter validator across the 9 shipping archives"
  tmp="$(mktemp -d)"; fails=0
  for a in auq-resilience-v1.1.1 cs-ops-v1.0.2 csm-v1.0.8 handoff-v1.0.2 \
           onboarding-v1.0.2 renewals-v1.0.2 rev-ops-v1.1.2 vbs-v0.4.3 vfa-v0.3.3; do
    mkdir -p "$tmp/$a" && unzip -q -o "dist/$a.plugin" -d "$tmp/$a"
    if python3 "$VALIDATOR" "$tmp/$a" >/dev/null 2>&1; then
      printf "  %-28s PASS\n" "$a"
    else
      printf "  %-28s FAIL\n" "$a"; fails=$((fails+1))
    fi
  done
  rm -rf "$tmp"
  [ "$fails" -eq 0 ] || { echo "ABORT: $fails archive(s) failed frontmatter validation" >&2; exit 1; }
else
  echo "  (validator not found at $VALIDATOR — skipping; preflight already passed)"
fi

# ---------------------------------------------------------------------------
say "2. Commit — CHECK 9 (preflight gains R11 coverage)"
git add bin/preflight.py
git commit -m "feat(preflight): add CHECK 9 — non-scalar top-level frontmatter keys

Ports R11 from validate-plugin-frontmatter.py. BLOCKs any top-level SKILL.md
frontmatter key holding a list or dict. \`metadata\` is exempt by design: the
agentskills.io specification puts structured custom fields (tags, author,
category, keywords) inside that mapping, and four vfa skills in this repo
already ship it that way.

Found by cross-validator comparison, not by a backend failure. Running the
frontmatter validator against the packaged artifacts surfaced four skills
carrying a top-level \`tags: [list]\` — two in csm, two in renewals — that
preflight had passed at 10/10 in the same state. CHECKs 1-8 inspect the
security block, description length, name format and the two capability
flags; none of them look at value types. The four had been shipping that
shape since csm v1.0.7 and renewals v1.0.1.

Remediation text points at \`metadata:\` rather than at deletion, so the next
author meets the spec-correct fix first.

Verified both directions: CHECK 9 fires against the pre-remediation file
taken from \`git show HEAD:csm/skills/success-plan-canvas/SKILL.md\`, and the
remediated tree stays 10/10.

Confidence: the rule is inferred, not bisected. No build has been submitted
with a top-level non-scalar isolated from other violations; the rationale is
inherited from the copilotkit nested-object bisection (2026-06-10), and a
flat list is a different shape. Cheap insurance, not characterized backend
behavior.

Toolkit bumped to v1.3.3."

# ---------------------------------------------------------------------------
say "3. Commit — frontmatter remediation for the four flagged skills"
git add csm/skills/success-plan-canvas/SKILL.md \
        csm/skills/success-plan-progress-review/SKILL.md \
        renewals/skills/churn-rca/SKILL.md \
        renewals/skills/downgrade-analysis/SKILL.md
git commit -m "fix(skills): move tags/author into metadata: per agentskills.io spec

Clears the CHECK 9 BLOCK on success-plan-canvas, success-plan-progress-review,
churn-rca and downgrade-analysis.

  - tags: [csm, success-plan, canvas]
  - author: todd@successhacker.co
  + metadata:
  +   author: \"todd@successhacker.co\"
  +   tags: \"csm success-plan canvas\"

Relocated rather than deleted. Under the agentskills.io open specification
\`tags\` is a supported field carried inside the optional \`metadata:\` mapping
as a delimited string, which is what keeps it portable across Claude Code,
Cursor and Codex. Deleting would have discarded valid metadata to satisfy a
rule never aimed at it.

\`version\` stays top-level — it is in the validator's canonical allowlist and
105 of 115 skills already put it there; moving it for four files would trade
one inconsistency for another.

Shape follows existing repo precedent: the four vfa skills (icp-drift-monitor,
icp-scorecard-builder, pmf-retention-curve-classifier,
pmf-sean-ellis-survey-analyzer) already carry \`license: MIT\` plus a
\`metadata:\` block and pass validation."

# ---------------------------------------------------------------------------
say "4. Commit — release wave: version bumps, docs, 9 archives in / 9 out"
git add bin/manifests.yaml \
        CHANGELOG.md QUICKSTART.md README.md \
        auq-resilience/CHANGELOG.md rev-ops/README.md
git add dist/auq-resilience-v1.1.1.plugin dist/cs-ops-v1.0.2.plugin \
        dist/csm-v1.0.8.plugin dist/handoff-v1.0.2.plugin \
        dist/onboarding-v1.0.2.plugin dist/renewals-v1.0.2.plugin \
        dist/rev-ops-v1.1.2.plugin dist/vbs-v0.4.3.plugin dist/vfa-v0.3.3.plugin
git rm --quiet --ignore-unmatch \
        dist/auq-resilience-v1.1.0.plugin dist/cs-ops-v1.0.1.plugin \
        dist/csm-v1.0.7.plugin dist/handoff-v1.0.1.plugin \
        dist/onboarding-v1.0.1.plugin dist/renewals-v1.0.1.plugin \
        dist/rev-ops-v1.1.1.plugin dist/vbs-v0.4.2.plugin dist/vfa-v0.3.2.plugin
git commit -m "release: patch bump 9 plugins for the hooks-quoting fix

Ships commit 12237a5 (quoted \${CLAUDE_PLUGIN_ROOT} in hook command strings) as
built artifacts. Every plugin that carries hooks/ is bumped one patch:

  auq-resilience 1.1.0 -> 1.1.1      onboarding 1.0.1 -> 1.0.2
  cs-ops         1.0.1 -> 1.0.2      renewals   1.0.1 -> 1.0.2
  csm            1.0.7 -> 1.0.8      rev-ops    1.1.1 -> 1.1.2
  handoff        1.0.1 -> 1.0.2      vbs        0.4.2 -> 0.4.3
                                     vfa        0.3.2 -> 0.3.3

claude-for-msft-365-install stays at 0.1.2 — it ships no hooks and is
unaffected.

Versions come from bin/manifests.yaml (the tracked source added in 8a67e45);
plugin.json is regenerated from it and remains gitignored.

All nine archives built through build-plugin.sh, which validates the source,
zips, tests archive integrity, extracts and re-validates the extracted tree.
Each was then checked against both validators: preflight CHECKs 1-9 and
validate-plugin-frontmatter R1-R11. 9/9 PASS on both.

Nine superseded archives removed so dist/ holds exactly one per plugin.
QUICKSTART.md and README.md updated in the same commit — both named archive
filenames that this release supersedes, matching repo precedent (b7c22f6).

Not included, deliberately: tasks/todo.md and the two bin/commit-*.sh helper
scripts stay untracked as working state."

# ---------------------------------------------------------------------------
say "5. Push monorepo"
git push origin main

# ---------------------------------------------------------------------------
say "6. Skills library — toolkit v1.3.3"
cd "$SKILLS"
echo "NOTE: this repo has no remote; commit is local only."
git add plugin-preflight-validator plugin-validation-debugger
git commit -m "feat(plugin-validation-toolkit): CHECK 9, v1.3.3

Documents CHECK 9 (non-scalar top-level frontmatter key, \`metadata\` exempt)
in both known-constraints.md copies, which stay byte-identical, and bumps both
SKILL.md version rows to 1.3.3. preflight.py synced from the monorepo copy.

The constraint entry records how it was found — cross-validator comparison
rather than a backend rejection — states plainly that it is inferred rather
than bisected, and shows the spec-correct \`metadata:\` remediation instead of
deletion."

say "Done. Monorepo pushed; skills committed locally."
echo
echo "Still untracked by design: tasks/todo.md, bin/commit-hooks-quoting.sh,"
echo "bin/commit-release-2026-09-06.sh."
echo "Not committed anywhere: the validator, fixtures, report and toolkit .plugin"
echo "under ~/claude-cowork/agents and ~/claude-cowork/plugins — that repo's"
echo "/**/ ignore rule covers them."
