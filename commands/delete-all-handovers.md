---
description: Delete all handover files for the current project to completely reset session history.
---

# Clear All Handovers

## Handover Files
```
!`ls -1t .claude/handovers/`
```

---

## Instructions

Using the file listing above:

1. Filter to only `.md` files. If there are **none**, report:
   > No handover files found — nothing to purge.

2. Otherwise, count the `.md` files, then delete them all using the Bash tool:
   ```
   rm -f .claude/handovers/*.md
   ```

3. Report:
   > Purged `<count>` handover file(s). Starting with a clean slate — no previous session context will be loaded on `/quiver:load-handover`.
