# Changelog — auq-resilience

All notable changes to the `auq-resilience` plugin are recorded here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versions follow [Semantic Versioning](https://semver.org/).

---

## [1.1.1] — 2026-09-06

### Fixed
- `hooks/hooks.json`: hook commands now quote `"${CLAUDE_PLUGIN_ROOT}"` so a plugin
  root containing a space (desktop app install path) no longer word-splits and
  breaks every hook invocation.

---

## [1.1.0] — 2026-05-29

### Added
- `commands/auq.md` — the `/auq` slash command, invoked as `/auq-resilience:auq`.
  Provides the Cowork-native control surface for the AUQ protocol:
  `force-prose` (prose-only for the session), `status` (report current mode),
  and `reset` (return to widget-first). This is the only part of the plugin that
  functions in Cowork, where Claude Code hooks do not run.

### Changed
- `plugin.json` description updated to cover both the Claude Code hook path and
  the Cowork command + `CLAUDE.md` behavioral path.
- `README.md` Cowork section rewritten to document the real `/auq` command
  rather than treating `/auq force-prose` as a behavioral instruction only.

### Notes
- No change to hook behavior. `auq_hook.py` and `auq_parser.py` are unchanged.
- In Cowork, the T1/T2/T3 protocol is enforced by the **AskUserQuestion (AUQ)
  Resilience** section already present in each CS plugin's `CLAUDE.md`; the
  bundled `/auq` command auto-registers on install (no wiring required).

---

## [1.0.1] — 2026-05-26

### Added
- `hooks/hooks.json` — self-contained hook registration using
  `${CLAUDE_PLUGIN_ROOT}` so the plugin wires its own Pre/PostToolUse and
  UserPromptSubmit handlers without per-plugin path edits.

---

## [1.0.0] — 2026-04-01

### Added
- Initial release. `PreToolUse` / `PostToolUse` hooks enforcing the
  single-question protocol and injecting the T1/T2/T3 prose fallback.
- `auq_parser.py` response parser (letter / keyword / semantic / default).
- `design/AUQ_PROTOCOL_SPEC.md` behavioral spec.
