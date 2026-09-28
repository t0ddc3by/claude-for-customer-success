# CfCS hooks-quoting release — PLAN (TDD+ PLAN entry, T2)

**Status:** [VALIDATED] — COMPLETED 2026-09-08 (steps 5–6 dropped by user: no reinstall wanted)
**Date:** 2026-09-05
**Repo:** `projects/agent-building/claude-for-customer-success` (branch `main`, HEAD 021207a)
**Ask (verbatim):** Rebuild and reinstall all nine CfCS plugins so the installed copies match
source, then commit the hooks fix as a release (nine hook files, nine version bumps, marketplace
manifest, nine new archives, nine superseded archives removed). Do not widen scope.
**Iteration boundary:** max 3 cycles (T2).

## Assumptions (named)
- A1 `.claude-plugin/` is gitignored (.gitignore:33-34); `plugin.json` and `marketplace.json`
  cannot be committed. The tracked version source is `bin/manifests.yaml`
  (commit 8a67e45). "Nine plugin.json + marketplace.json" in the commit scope therefore
  becomes `bin/manifests.yaml` (tracked) + regenerated plugin.json/marketplace.json (working tree).
- A2 Build recipe = the one in commit 021207a: stage a copy of each plugin minus `evals/`,
  `logs/`, `.DS_Store`, `.gitignore`, `__pycache__`, skill-level `design|output|reference`,
  then `build-plugin.sh <staged> --strict --validator <canonical validate-plugin-frontmatter.py>`.
  Verified by diffing every existing archive against its source tree (only those classes differ).
- A3 Validator: repo declares none for build-plugin.sh; use the script's canonical default
  `agents/agent-skill-builder/skills/skill-builder-pro/scripts/validate-plugin-frontmatter.py`,
  plus run `bin/preflight.py` on each extracted archive (repo's own check).
- A4 Changelog homes: root `CHANGELOG.md` (Keep-a-Changelog, new `[1.2.1]` entry),
  `auq-resilience/CHANGELOG.md` (new `[1.1.1]`), `rev-ops/README.md` changelog table (new row).
  Other plugins keep no changelog.
- A5 Untracked `bin/commit-hooks-quoting.sh` (previous-session helper that commits AND pushes)
  is left untracked and NOT committed.
- A6 Stale `.git/index.lock` (0 bytes, no git process running) removed before git writes.
- A7 `tasks/todo.md` lives here (repo root, untracked, not committed) per the ask.

## Tasks
- [x] 1. Verify starting state (status = 9 hooks.json + 1 untracked helper; diffs quote-only; JSON parses; zero unquoted)
- [x] 2. Preflight (`bin/preflight.py --all .`, `bin/generate-manifests.py --check`)
- [x] 3a. Bump 9 patch versions in `bin/manifests.yaml`; regenerate plugin.json; sync marketplace.json versions; changelog lines
- [x] 3b. Build 9 archives (staged copy → build-plugin.sh --strict --validator) → `dist/<p>-v<new>.plugin`, exit 0 each
- [x] 3c. `git rm` 9 superseded archives → dist holds exactly 9
- [x] 4. Extract hooks/hooks.json from each archive; 27/27 commands quoted; preflight PASS on each extracted tree
- [~] 5. DROPPED (user 2026-09-08): plugins are not being installed; build + repo update only
- [~] 6. DROPPED (follows from 5)
- [x] 7. `gitnexus_detect_changes()`; confirm scope; commit on main (no push) — 3 commits per user decision

## DOD Rubric (dimensional)
### D1 Correctness of fix
- [x] REQUIRED: 0 unquoted `${CLAUDE_PLUGIN_ROOT}` in any of 9 archives' hooks.json — evidence: extraction check output
- [x] REQUIRED: every archive's hooks.json byte-identical to source — evidence: cmp
### D2 Build integrity
- [x] REQUIRED: 9 × build-plugin.sh exit 0 under --strict — evidence: captured PASS lines
- [x] REQUIRED: archive file list = source minus recipe exclusions (A2) — evidence: diff script
- [x] REQUIRED: preflight PASS on each extracted archive — evidence: output
### D3 Release bookkeeping
- [x] REQUIRED: manifests.yaml, plugin.json, marketplace.json versions agree (generate-manifests --check clean) — evidence: output
- [x] REQUIRED: dist/ holds exactly 9 version-named archives, one per plugin — evidence: ls
- [x] REQUIRED: changelog line present in each changelog home (A4) — evidence: git diff
### D4 Scope discipline
- [x] REQUIRED: commits touch only the agreed scope (hooks already in 12237a5; release = manifests.yaml, 3 changelog files, QUICKSTART, README, 9 in/9 out; plus the two 2026-09-06 scope additions in their own commits) — evidence: git show --stat below
- [x] REQUIRED: nothing written outside scope files, design/, scratchpad, tasks/todo.md — evidence: git status after commit
- [x] REQUIRED: gitnexus_detect_changes output recorded — evidence: Review section
### D5 Runtime verification
- [~] REQUIRED (or explicitly pending): post-reinstall Write — N/A, reinstall dropped by user
- [~] OPTIONAL: rpm/ copies show quoted command — N/A, reinstall dropped by user

## Findings surfaced during PLAN (not acted on — outside scope)
- F1 Untracked `bin/commit-hooks-quoting.sh` in repo root (see A5).
- F2 `QUICKSTART.md:43-48` and `README.md:702` name the archive files being superseded
  (`csm-v1.0.7.plugin`, …, `auq-resilience-v1.1.0.plugin`); they will dangle after this
  release. Repo precedent (b7c22f6) fixed QUICKSTART in the same dist commit.
- F3 `csm/hooks/hooks.json` diff also reflows three one-line objects to multi-line JSON
  (semantically identical; matches the other eight files' formatting).
- F4 `marketplace.json` lists 6 of the 9 CfCS plugins (vbs, vfa, handoff absent) and lags every
  version; gitignored, so any fix is working-tree only.
- F5 `rev-ops/README.md:182` footer says v1.1.0 (already stale vs 1.1.1).
- F6 gitnexus index is 11 commits behind HEAD; `.gitnexus/` is excluded via .git/info/exclude
  so re-indexing would not widen the diff, but detect_changes will run against a stale index.
- F7 Source files newer than the current archives (will ship for the first time in this rebuild): see Review.

## Review (in progress — 2026-09-08)
- Hooks fix committed as 12237a5 (via bin/commit-hooks-quoting.sh, run outside this session) and already on origin/main.
- Scope grew on 2026-09-06 in a parallel session: bin/preflight.py CHECK 9 (non-scalar top-level frontmatter) + four SKILL.md `tags:` lists moved under `metadata:`. Both verified here: CHECK 9 fires on `git show HEAD:csm/skills/success-plan-canvas/SKILL.md`, stays silent on the fixed tree.
- Nine archives verified: hooks.json byte-identical to source (9/9), 27/27 commands quoted, 0 unquoted, preflight CHECKs 1–9 PASS (9/9), canonical validate-plugin-frontmatter PASS (9/9). File lists equal source-minus-recipe and equal the superseded archives (no added/removed files).
- dist/ holds exactly 9 version-named archives; superseded 9 staged for deletion (git rm).
- generate-manifests --check clean; preflight --all 10/10.
- gitnexus_detect_changes (scope=all, index 12 commits stale): 6 doc-section symbols touched, 0 affected processes, risk low.
- Sandbox can write the git index and delete files (probe OK); the helper scripts' claim that it cannot did not hold in this session.
- PENDING: step 5 reinstall (manual), step 6 runtime check, step 7 commit — commit shape undecided (1 combined commit per original ask vs 3 commits per bin/commit-release-2026-09-06.sh). No push.

## Review — FINAL (2026-09-08)

### Commits on main (pushed 2026-09-08; origin/main = 08bbd3b)
| Hash | Subject | Files |
|---|---|---|
| 12237a5 | fix(hooks): quote ${CLAUDE_PLUGIN_ROOT} in hook command strings | 9 hooks.json (already on origin) |
| a8f36a1 | feat(preflight): add CHECK 9 — non-scalar top-level frontmatter keys | bin/preflight.py |
| 2c86681 | fix(skills): move tags/author into metadata: per agentskills.io spec | 4 SKILL.md |
| 08bbd3b | release: patch bump 9 plugins for the hooks-quoting fix | manifests.yaml, CHANGELOG.md, QUICKSTART.md, README.md, auq-resilience/CHANGELOG.md, rev-ops/README.md, 9 dist in / 9 dist out |

### Scorecard
- D1 Correctness: PASS — 9/9 archives hooks.json byte-identical to source; 27/27 quoted; 0 unquoted.
- D2 Build integrity: PASS — 9 archives built via build-plugin.sh (2026-09-06 session); preflight 1–9 PASS 9/9 on extracted trees; canonical validator PASS 9/9; file lists = source − recipe = superseded archives.
- D3 Release bookkeeping: PASS — generate-manifests --check clean; dist/ = exactly 9; changelog lines in all 3 homes; marketplace.json synced (working tree, gitignored).
- D4 Scope discipline: PASS — untracked leftovers: bin/commit-hooks-quoting.sh, bin/commit-release-2026-09-06.sh, tasks/ (all by design). gitnexus_detect_changes (scope=all, twice): 6 doc-section symbols, 0 affected processes, risk low.
- D5 Runtime: N/A — reinstall dropped by user.

### JUDGEMENT: PASS (all REQUIRED criteria met or explicitly N/A by user decision)
### ADVERSARIAL_REVIEW (T2, self-run, 2 passes): CONDITIONAL PASS
- Attack 1 — "archives match source": held (file-list diff + hooks cmp + both validators).
- Attack 2 — "commit scope": FOUND a defect. First run of the helper produced acb5422 carrying the 9 dist deletions because step 3c had pre-staged them. Corrected by local soft-reset redo (old tip df86567 in reflog); final tree byte-identical. Condition: user reviews `git log origin/main..HEAD` before pushing.
- Attack 3 — "R11 backend risk": inferred, not bisected (per helper's own message); mitigated by moving tags under metadata:, matching 4 existing vfa skills.

### Lessons captured
- ai_self_mistake: never hand a scripted `git commit` sequence an index that already holds staged changes; run `git status --porcelain` and `git diff --cached --stat` immediately before, and reset the index if anything is pre-staged. Rule recorded in memory note plugin-hooks-quote-plugin-root (L5) — promote to behavioral-defaults if it recurs.
- tooling_finding: build-plugin.sh --strict + canonical validator cannot validate skill-less plugins (handoff, auq-resilience); the repo's bin/preflight.py can. Not fixed here (out of scope).
- Not done per DoD write restriction: projects/agent-building/_context.md session entry (workspace convention) — user to decide.
