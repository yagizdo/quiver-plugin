---
description: Delete the most recent handover file to remove the last session's context.
---

# Clear Last Handover

## Handover Files
```
!`ls -1t .claude/handovers/`
```

---

## Instructions

Using the file listing above:

1. Filter to only `.md` files. If there are **none**, report:
   > No handover files found — nothing to delete.

2. Otherwise, the **first `.md` file** is the most recent. Delete it using the Bash tool:
   ```
   rm .claude/handovers/<filename>
   ```

3. Count how many `.md` files remain and report:
   > Deleted: `<filename>`
   > Remaining: `<count>` handover file(s)

4. Mention: use `/quiver:delete-all-handovers` to wipe everything.
