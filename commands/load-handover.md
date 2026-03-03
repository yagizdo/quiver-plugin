---
description: Load the most recent handover note from the previous session into context.
---

# Previous Session Handover

## Handover Files
```
!`ls -1t .claude/handovers/`
```

---

## Instructions

Using the file listing above:

1. Filter to only `.md` files. If there are **none**, report:
   > No handover files found for this project.
   > This is a fresh session — no previous context to load.
   > Run /quiver:handover at the end of this session to start tracking.

2. Otherwise, the **first `.md` file** in the listing is the most recent (sorted newest-first). Read it using the Read tool at path `.claude/handovers/<filename>`.

3. Present its contents, then:
   - Confirm you understand the current state of the project
   - State what the top priority Next Step is
   - Proceed directly with the highest-priority Next Step unless the user has already provided instructions
