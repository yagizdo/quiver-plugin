# Quiver Plugin

Session handover plugin for Claude Code. Automatically saves and restores conversation context across sessions so nothing is lost.

## Architecture

```
quiver-plugin/
  .claude-plugin/plugin.json   — Plugin manifest (name: "quiver", v1.0.0)
  commands/                    — Slash commands (Markdown files with shell expansions)
    handover.md                — /quiver:handover — generates 8-section handover, saves to disk, prunes old files
    load-handover.md           — /quiver:load-handover — loads most recent handover into context
    delete-all-handovers.md    — /quiver:delete-all-handovers — purges all handover files
    delete-last-handover.md    — /quiver:delete-last-handover — removes most recent handover
  hooks/
    hooks.json                 — Registers PreCompact hook
    scripts/
      handover_core.py         — Shared logic: save, prune (keep 3), generate via `claude -p`
      pre-compact-handover.py  — PreCompact hook entry point, reads transcript from stdin JSON
```

## How It Works

- **Commands** are Markdown files. Shell commands inside `` !`...` `` blocks run inline and inject output into the prompt.
- **Hooks** run Python scripts. The PreCompact hook reads `transcript_path` from the stdin JSON event, calls `claude -p` to summarize, then saves to `.claude/handovers/`.
- Handover files live at `<project>/.claude/handovers/YYYY-MM-DD_HH-mm-ss.md`. Only the 3 most recent are kept.

## Key Conventions

- Commands must not rely on `CLAUDE_PLUGIN_ROOT` — it is only available in `hooks.json` and hook scripts.
- Hook scripts use `CLAUDE_PROJECT_DIR` (falls back to `os.getcwd()`).
- `handover_core.py` is the single source of truth for handover logic (prompt template, save, prune). The command in `handover.md` duplicates the save/prune steps as Claude instructions because commands can't call Python directly.
- Plugin requires Python 3 and `claude` CLI in PATH.

## Development

Install locally for testing:
```bash
claude --plugin-dir /path/to/quiver-plugin
```

Permanent install:
```bash
claude plugin install /path/to/quiver-plugin
```

No build step. No dependencies beyond Python 3 stdlib and the `claude` CLI.

## Testing Changes

- **Commands**: Run the slash command (e.g. `/quiver:handover`) in a Claude Code session and verify output.
- **Hook**: Trigger a compaction (or test `pre-compact-handover.py` directly by piping JSON with a `transcript_path` to stdin).
- **Core logic**: `handover_core.py` functions can be tested with a Python REPL. Key functions: `save_handover(project_dir, content)`, `prune_old_files(handover_dir)`, `generate_from_transcript(transcript)`.
