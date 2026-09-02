#!/bin/bash
# AUQ resilience hook wrapper — graceful no-op when auq-resilience is not installed.
# To enable AUQ resilience, set AUQ_HOOK_PATH to an absolute path:
#   export AUQ_HOOK_PATH="$HOME/.claude/plugins/auq-resilience/hooks/auq_hook.py"
HOOK="${AUQ_HOOK_PATH:-/dev/null}"
if [ -f "$HOOK" ]; then
  python3 "$HOOK" "$@"
else
  exit 0
fi
