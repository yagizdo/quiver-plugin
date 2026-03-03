---
description: Summarize the current work state and prepare a handover note for the next session.
---

# Automatically Gathered Context

## Git Status
```
!`git status --short 2>&1`
```

## Git Diff Summary
```
!`git diff --stat 2>&1`
```

# Handover Instructions

**Your role:** You are a session handover specialist. Your goal is to produce a zero-re-discovery handover — the next session should never re-investigate what this session already learned. Be specific: include file paths, function names, line numbers, and exact error messages.

If the git commands above produced errors (e.g. "not a git repository", "command not found"), that's fine — skip the git-related context and note "Git not available" in the Summary. Build the handover from the conversation context alone.

**Workflow:**
```
┌─────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│ 1. GATHER       │ ──► │ 2. BUILD         │ ──► │ 3. SAVE & VERIFY │
│ Read git status  │     │ Write 8 sections │     │ Write file       │
│ Review convo     │     │ Check quality    │     │ Prune old files  │
│ Identify files   │     │ gates            │     │ Update MEMORY.md │
└─────────────────┘     └──────────────────┘     └──────────────────┘
```

<!-- SYNC: The 8 section headings below must match hooks/scripts/pre-compact-handover.sh:25 PROMPT_PREFIX. -->
Using the context above and our conversation, prepare a structured handover note with these exact sections:

## Summary
{One-paragraph TL;DR. Include: what feature/bug was worked on, current status (done / in-progress / blocked), and branch name if applicable. Example:}
> Implemented JWT refresh token rotation on `feature/auth-refresh`. All tests passing; PR ready for review.

## What Was Done
{Bulleted list. Each item: file path + what changed. Example:}
- `src/auth.ts` — Added JWT refresh token rotation
- `tests/auth.test.ts` — Added 3 test cases for token expiry

## What We Tried / Dead Ends
{Approaches that didn't work and why. Include enough detail to prevent re-investigation. Example:}
- Tried using `jsonwebtoken` v8 but it lacks `rotateRefresh()` — downgraded to v7 API

## Bugs & Fixes
{Issues found and how they were resolved. Include file paths and line numbers. Example:}
- `src/auth.ts:42` — Off-by-one in token expiry calculation; changed `>=` to `>`

## Key Decisions (and Why)
{Architectural choices made this session. State the alternatives considered. Example:}
- Chose Redis over in-memory cache for token blacklist — survives server restarts

## Gotchas / Things to Watch Out For
{Non-obvious constraints, traps, or environment quirks. Example:}
- `AUTH_SECRET` env var must be ≥32 chars or the signing silently falls back to HS256

## Next Steps
{Ordered list — first item is the highest priority action for the next session. Example:}
1. Open PR for `feature/auth-refresh` and request review
2. Add rate limiting to `/token/refresh` endpoint

## Important Files Map
{Key files and their roles in the current work. Example:}
- `src/auth.ts` — Main authentication module (token issue + refresh)
- `config/redis.yml` — Token blacklist store configuration

**If a section has no content, write `N/A — {reason}` instead of omitting the heading.**

---

## Quality Gates

Before saving, verify the handover passes these checks:

**BLOCKING** (fix before saving):
- Summary is not empty
- Next Steps has at least one item
- What Was Done references at least one file path

**WARNING** (review if session was longer than ~15 minutes):
- What We Tried / Dead Ends is empty — long sessions usually have dead ends worth noting

---

## Anti-Patterns

- **Don't** write vague summaries like "worked on auth stuff" — include the specific feature and current status.
- **Don't** paste full file contents into the handover — summarize changes with file paths and line references.
- **Don't** skip updating MEMORY.md — it's the cross-session index.
- **Don't** leave Next Steps empty — every session has a logical continuation.

---

## Save to Disk (Required)

After writing the handover above, do all of the following:

### 1. Write handover file
Get a timestamp: run `date '+%Y-%m-%d_%H-%M-%S'` via Bash.
Create directory: `.claude/handovers/` in the project root (if it doesn't exist).
Write the full 8-section handover to: `.claude/handovers/{timestamp}.md`
**Verify:** Read back the file to confirm it was written correctly.

### 2. Prune old handover files
List all `.md` files in `.claude/handovers/`, sorted by name (newest first).
Delete all files beyond the 3 most recent.
**Verify:** Re-list the directory and confirm only ≤3 files remain.

### 3. Update MEMORY.md
In the project memory file, update (or add) a `## Last Handover` section:
```
## Last Handover
- file: .claude/handovers/{timestamp}.md
- summary: {one sentence from the Summary section}
```
**Verify:** Read MEMORY.md to confirm the update.

### 4. Save any active plan
If there is an unsaved implementation plan in context, save it to `PLAN.md`. Skip if already current.

### Completion Confirmation

After all saves, output this confirmation:

> **Handover saved:** `.claude/handovers/{timestamp}.md`
> **Files retained:** {comma-separated list of kept handover files}
> **MEMORY.md updated:** yes/no
> **Ready to close the session.**
