---
description: Delete the most recent handover file to remove the last session's context.
---

# Clear Last Handover

!`latest=$(ls -1t .claude/handovers/*.md 2>/dev/null | head -1); if [ -n "$latest" ]; then rm "$latest" && echo "Deleted: $(basename $latest)"; remaining=$(ls -1 .claude/handovers/*.md 2>/dev/null | wc -l | tr -d ' '); echo "Remaining: $remaining"; else echo "No handover files found — nothing to delete."; fi`

---

The most recent handover file has been deleted. If there are older handovers, the next `/quiver:load-handover` will load from those. Use `/quiver:delete-all-handovers` to wipe everything.
