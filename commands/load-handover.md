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

Using the file listing above, determine which branch applies:

### Branch A — No Files
If there are **no `.md` files** in the listing:
> No handover files found for this project.
> This is a fresh session — no previous context to load.
> Run `/quiver:handover` at the end of this session to start tracking.

**Stop here.** Do not proceed to Branch B or C.

### Branch B — One File
If there is **exactly one `.md` file**:
1. Read it using the Read tool at path `.claude/handovers/{filename}`.
2. Present it using the template below.

### Branch C — Multiple Files
If there are **two or more `.md` files**:
1. The **first `.md` file** in the listing is the most recent (sorted newest-first). Read it using the Read tool at path `.claude/handovers/{filename}`.
2. Present it using the template below.
3. Mention: "{count} older handover(s) also available."

---

## Presentation Template

After reading the handover file, present this summary:

> **Session loaded:** `{filename}`
> **Date:** {date extracted from timestamp in filename}
> **Top Priority:** {first item from Next Steps section}

Then:
1. Confirm you understand the current state of the project.
2. List all Next Steps with their priority order and a short explanation of each.
3. Ask the user which one they'd like to work on.

---

## Anti-Patterns

- **Don't** dump the raw handover contents without a summary header — always lead with the presentation template.
- **Don't** auto-start the first Next Step without asking — always present the list and let the user choose.
- **Don't** read older handover files unless the user explicitly requests it.

---

## Verification

- Confirm the file read succeeded (non-empty content returned).
- If the file content looks malformed (no section headings, empty body), warn: "This handover may be incomplete — proceeding with available context."
