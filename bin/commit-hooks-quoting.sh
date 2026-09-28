#!/usr/bin/env bash
# commit-hooks-quoting.sh
#
# Commits the hooks.json command-string quoting fix across all nine plugins.
# RUN IN YOUR OWN TERMINAL — the Cowork sandbox cannot unlink .git/index.lock.
#
#   bash bin/commit-hooks-quoting.sh
#
# The file changes are already on disk. This only stages, commits, and pushes.

set -euo pipefail

MONOREPO="${MONOREPO:-$HOME/claude-cowork/projects/agent-building/claude-for-customer-success}"
cd "$MONOREPO"

printf "\n\033[1m==> Clear stale index.lock\033[0m\n"
rm -f .git/index.lock || true

printf "\n\033[1m==> Verify green before committing\033[0m\n"
python3 bin/generate-manifests.py --check
python3 bin/preflight.py --all --parent .

printf "\n\033[1m==> Stage and commit\033[0m\n"
git add -- '*/hooks/hooks.json'
git commit -m "fix(hooks): quote \${CLAUDE_PLUGIN_ROOT} in hook command strings

Wraps the interpolated plugin-root path in double quotes across all nine
plugins that ship hooks, so a plugin root containing a space does not split
into multiple shell words:

  - bash \${CLAUDE_PLUGIN_ROOT}/hooks/run_auq_hook.sh
  + bash \"\${CLAUDE_PLUGIN_ROOT}/hooks/run_auq_hook.sh\"

auq-resilience uses the python3 form of the same command; the other eight
use the bash shim. 27 command strings across 9 files, 3 per file
(ask_user_input_v0 pre/post plus the .* matcher).

Also reflows the inline one-line command objects to expanded JSON. No
structural change: the nested hooks schema is unchanged (CHECK 8a), no '..'
appears in any command string (CHECK 8b/8c), and every path stays
\${CLAUDE_PLUGIN_ROOT}-relative.

Verified: preflight 10/10 PASS, manifest drift-check clean.

Caveat worth recording — no build has been submitted to the Cowork backend
with the escaped-quote form. Preflight passing means it clears the eight
known constraints; escaped quotes inside a command string were never part
of what the 2026-05-25 bisection covered. If a plugin install starts
failing after this, revert this commit first."

printf "\n\033[1m==> Push\033[0m\n"
git push origin main

printf "\n\033[1mDone.\033[0m\n"
