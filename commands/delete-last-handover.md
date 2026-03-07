---
name: delete-last-handover
description: Delete the most recent handover file to remove the last session's context.
---

# Clear Last Handover

## Handover Files
```
!`ls -1t .claude/handovers/ 2>/dev/null; true`
```

---

## Instructions

Using the file listing above, determine which branch applies:

### Branch A — No Files
If the listing shows an error (e.g., "No such file or directory"), is empty, or contains **no `.md` files**:
> No handover files found — nothing to delete.
> **Tip:** `/quiver:handover` to create one.

**Stop here.**

### Branch B — Files Exist
If there are **one or more `.md` files**:
1. The **first `.md` file** is the most recent (sorted newest-first). This is the deletion target.
2. State the pre-deletion confirmation:
   > **Target:** `{filename}`
   > **Remaining after deletion:** {count - 1} handover file(s)
3. Delete it using the Bash tool:
   ```
   rm .claude/handovers/{filename}
   ```
4. **Memory cleanup:** Read the auto-memory file (`MEMORY.md` in your memory directory). If it contains entries under a `## Pending Work` section or entries that reference specific handover filenames, session-specific task status (e.g., "Phase 2 complete", "blocked on X"), or branch work that was tracked in the deleted handover, remove those entries using the Edit tool. After cleanup, inform the user:
   > Also removed {N} handover-sourced references from MEMORY.md (e.g., pending work items, session context).
   If no matching entries were found, skip this message.

---

## Output Template

After deletion, output:

> **Deleted:** `{filename}`
> **Remaining:** {count} handover file(s)
> **Tip:** `/quiver:delete-all-handovers` to wipe all, `/quiver:load-handover` to view next.

---

## Anti-Patterns

- **Don't** delete without stating the target filename first — the user needs to see what will be removed.
- **Don't** skip verification after deletion — always re-list to confirm the file is gone.
- **Don't** proceed if the directory doesn't exist — report "nothing to delete" and stop.

---

## Verification

Re-list `.claude/handovers/` after deletion to confirm the file is gone and the remaining count is correct.
