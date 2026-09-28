#!/usr/bin/env bash
# Removes the Value-Based Selling expansion pack from this repo (moved to
# claude-for-atlas). Content restores, manifest scrubs, and the renewals/rev-ops
# rebuilds were already applied to the working tree by the Cowork session on
# 2026-09-28; this script performs only the deletions that session could not
# (sandbox mounts block unlink), then stages everything for one commit.
set -euo pipefail
cd "$(dirname "$0")/.."

git rm -r --quiet vbs vfa
git rm -r --quiet managed-agent-cookbooks/loop-runner managed-agent-cookbooks/drift-sentinel managed-agent-cookbooks/deal-alignment-watcher
git rm --quiet deployment-cookbooks/solo-sales-cookbook.md deployment-cookbooks/solo-post-sales-cookbook.md
git rm --quiet dist/vbs-v0.4.3.plugin dist/vfa-v0.3.3.plugin dist/renewals-v1.0.2.plugin dist/rev-ops-v1.1.2.plugin

git add -A

echo
echo "Staged. Review with: git status && git diff --cached --stat"
echo "Then commit:"
echo "  git commit -m 'remove vbs/vfa expansion pack (moved to claude-for-atlas); restore pre-pack renewals/rev-ops skills and solo-csm cookbook'"
