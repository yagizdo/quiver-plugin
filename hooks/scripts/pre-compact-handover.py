#!/usr/bin/env python3
"""PreCompact hook — auto-generates a handover from the session transcript before compaction."""

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import handover_core


def main() -> int:
    event = json.loads(sys.stdin.read() or "{}")
    transcript_path = event.get("transcript_path")
    project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd()))

    if not transcript_path:
        return 0

    transcript = Path(transcript_path).read_text(encoding="utf-8", errors="ignore")
    content = handover_core.generate_from_transcript(transcript)

    if not content:
        return 0

    handover_core.save_handover(project_dir, content)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
