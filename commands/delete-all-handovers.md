---
description: Delete all handover files for the current project to completely reset session history.
---

# Clear All Handovers

!`count=$(ls -1 .claude/handovers/*.md 2>/dev/null | wc -l | tr -d ' '); rm -f .claude/handovers/*.md; echo "Purged $count handover file(s)."`

---

All handover files have been purged. The AI is starting with a clean slate — no previous session context will be loaded on `/quiver:load-handover`.
