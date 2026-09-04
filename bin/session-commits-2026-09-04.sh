#!/usr/bin/env bash
# session-commits-2026-09-04.sh
#
# Git operations for the 2026-09-04 polish session. RUN THIS IN YOUR OWN
# TERMINAL, not in the Cowork sandbox — the sandbox cannot unlink files under
# .git/ (stale index.lock) and cannot delete tracked files, so every git write
# below fails there.
#
#   bash bin/session-commits-2026-09-04.sh
#
# Everything is idempotent-ish: re-running after a partial failure is safe,
# though already-made commits will simply report "nothing to commit".
#
# All file content changes are ALREADY ON DISK. This script only stages,
# commits, and pushes them.

set -euo pipefail

MONOREPO="${MONOREPO:-$HOME/claude-cowork/projects/agent-building/claude-for-customer-success}"
SKILLS="${SKILLS:-$HOME/claude-cowork/skills}"

say() { printf "\n\033[1m==> %s\033[0m\n" "$*"; }

# ---------------------------------------------------------------------------
say "0. Clear stale git index locks (sandbox leftovers)"
rm -f "$MONOREPO/.git/index.lock" "$SKILLS/.git/index.lock" || true

# ---------------------------------------------------------------------------
say "1. Monorepo — verify green before committing"
cd "$MONOREPO"
python3 bin/generate-manifests.py --check
python3 bin/preflight.py --all --parent .

# ---------------------------------------------------------------------------
say "2. Commit — CHECK 8c (preflight hardening)"
git add bin/preflight.py
git commit -m "feat(preflight): add CHECK 8c — '..' traversal in inline hooks.json commands

CHECK 8b scans only .sh/.bash/.py files under hooks/. A plugin that inlines
its command directly in hooks.json ('command': 'python ../shared/foo.py')
has no script file for 8b to read, so the traversal was invisible to the
validator. CHECK 8c walks the parsed hooks.json shape-agnostically and
flags '../' in any command string, under the nested schema, the deprecated
flat schema, or any future nesting.

8c is defensive hardening, not a bisected backend constraint: no build was
submitted with an inline '..' command isolated from other violations, so
backend rejection is reasoned by analogy with 8b rather than observed.

Verified with a fixture that fires 8c, a clean fixture that does not, and a
full monorepo run that stays at 10/10 PASS.

Toolkit bumped to v1.3.2." || echo "(nothing to commit)"

# ---------------------------------------------------------------------------
say "3. Commit — manifests as tracked source of truth"
git add bin/manifests.yaml bin/generate-manifests.py \
        .github/workflows/preflight.yml README.md \
        bin/session-commits-2026-09-04.sh
git commit -m "feat(build): make bin/manifests.yaml the tracked source for plugin.json

.claude-plugin/ is gitignored, so every <plugin>/.claude-plugin/plugin.json
lived only in a working tree. Version bumps made during a build session did
not survive a fresh clone — csm 1.0.7, cs-ops 1.0.1, onboarding 1.0.1,
renewals 1.0.1, rev-ops 1.1.1, auq-resilience 1.1.0, handoff 1.0.1,
vbs 0.4.2 and vfa 0.3.2 were all at risk.

bin/manifests.yaml now carries name, version, description and author for all
ten plugins; bin/generate-manifests.py writes the manifests from it.
  generate-manifests.py           write all manifests
  generate-manifests.py --check   verify on-disk == source (drift detection)
  generate-manifests.py --list    version table

The generator refuses to emit a description over 388 chars (CHECK 6), so an
over-length description cannot reach a build.

CI now generates manifests before running preflight. Previously CHECK 6
skipped silently in CI because plugin.json never existed in a checkout;
it is now enforced on every push and PR.

Verified: seeded from the current on-disk manifests, regenerated, and all
ten compare semantically identical to the pre-change files (only JSON key
order and trailing newline moved). A fresh clone plus the generator recovers
every version, and all eight versioned dist/ artifacts match." || echo "(nothing to commit)"

# ---------------------------------------------------------------------------
say "4. Commit — dist/ artifacts"
git add dist/vfa-v0.3.2.plugin
git rm --quiet --ignore-unmatch \
  dist/renewals.plugin dist/rev-ops.plugin dist/vbs.plugin dist/vfa.plugin
git commit -m "chore(dist): add vfa-v0.3.2, drop unversioned artifacts

vfa had no versioned artifact. dist/vfa.plugin was a non-conforming build
that shipped evals/ and logs/. Rebuilt at v0.3.2 with the standard recipe
(source minus evals/, logs/, skill-level design|output|reference, .DS_Store,
__pycache__, .gitignore) via build-plugin.sh, which validates the source and
re-validates the extracted archive.

Removed unversioned artifacts, each superseded:
  renewals.plugin  v1.0.1 -> renewals-v1.0.1.plugin
  rev-ops.plugin   v1.1.1 -> rev-ops-v1.1.1.plugin
  vbs.plugin       v0.4.1 -> vbs-v0.4.2.plugin
  vfa.plugin       v0.3.2 -> vfa-v0.3.2.plugin (and it carried evals/, logs/)" \
  || echo "(nothing to commit)"

# ---------------------------------------------------------------------------
say "5. Push monorepo"
git push origin main

# ---------------------------------------------------------------------------
say "6. Skills library — commit the validation toolkit skills"
cd "$SKILLS"
echo "NOTE: this repo has no remote and ~2000 pre-existing dirty paths."
echo "      Staging ONLY the two toolkit skill directories."
git add plugin-preflight-validator plugin-validation-debugger
git commit -m "feat(plugin-validation-toolkit): document CHECK 8c, sync preflight.py to v1.3.2

Both skills were entirely untracked. This commits them at v1.3.2 with:
  - preflight.py carrying the discovery fix, the CHECK 3 name-format
    recalibration, and the new CHECK 8c
  - CHECK 8c documented in both SKILL.md files and both known-constraints.md
    copies (which remain byte-identical to each other), labeled [Inferred]
    rather than empirically bisected
  - open question 5 updated to note which part of the gap 8c closes and
    which part (non-Python/shell hook script extensions) stays open" \
  || echo "(nothing to commit)"

say "Done. Monorepo pushed; skills committed locally (no remote configured)."
