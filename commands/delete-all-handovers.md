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

Using the file listing above, determine which branch applies:

### Branch A — No Files
If there are **no `.md` files** in the listing:
> No handover files found — nothing to purge.
> **Tip:** `/quiver:handover` to create one.

**Stop here.**

### Branch B — Files Exist
If there are **one or more `.md` files**:
1. List the pre-deletion inventory:
   > **Files to delete ({count}):**
   > {bulleted list of all .md filenames}
2. Delete them all using the Bash tool:
   ```
   rm -f .claude/handovers/*.md
   ```

---

## Output Template

After deletion, output:

> **Purged:** {count} handover file(s)
> **Files deleted:** {comma-separated filenames}
> **Status:** Clean slate.
> **Tip:** `/quiver:handover` to start fresh tracking.

---

## Verification

Re-list `.claude/handovers/` after deletion to confirm the directory is empty (no `.md` files remain).
