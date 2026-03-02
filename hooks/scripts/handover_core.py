#!/usr/bin/env python3
"""Shared handover logic — used by the PreCompact hook."""

import os
import subprocess
from datetime import datetime
from pathlib import Path

HANDOVER_SUBDIR = ".claude/handovers"
KEEP_LAST = 3

HANDOVER_PROMPT_TEMPLATE = """
Read the following Claude Code session transcript and produce a HANDOVER note.
Goal: The next Claude session (or a teammate) should be able to continue from where we left off.

Use these exact headings (H2 markdown):
## Summary
## What Was Done
## What We Tried / Dead Ends
## Bugs & Fixes
## Key Decisions (and Why)
## Gotchas / Things to Watch Out For
## Next Steps
## Important Files Map

Transcript:
{transcript}
""".strip()


def get_handover_dir(project_dir: Path) -> Path:
    """Returns .claude/handovers/ path, creating it if needed."""
    d = project_dir / HANDOVER_SUBDIR
    d.mkdir(parents=True, exist_ok=True)
    return d


def make_timestamp() -> str:
    """Returns YYYY-MM-DD_HH-mm-ss timestamp."""
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def prune_old_files(handover_dir: Path, keep: int = KEEP_LAST) -> int:
    """Deletes all but the `keep` most recent .md files. Returns count deleted."""
    files = sorted(handover_dir.glob("*.md"), key=lambda f: f.name, reverse=True)
    to_delete = files[keep:]
    for f in to_delete:
        f.unlink()
    return len(to_delete)


def save_handover(project_dir: Path, content: str) -> Path:
    """Writes content to .claude/handovers/{timestamp}.md, then prunes old files."""
    handover_dir = get_handover_dir(project_dir)
    ts = make_timestamp()
    out_path = handover_dir / f"{ts}.md"
    out_path.write_text(content.strip() + "\n", encoding="utf-8")
    prune_old_files(handover_dir)
    return out_path


def generate_from_transcript(transcript: str) -> str:
    """Runs claude -p to generate a handover from a session transcript."""
    prompt = HANDOVER_PROMPT_TEMPLATE.format(transcript=transcript)
    result = subprocess.run(
        ["claude", "-p", prompt],
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() if result.stdout else ""
