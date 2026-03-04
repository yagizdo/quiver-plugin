---
description: Generate a Conventional Commits-compliant git commit message from staged changes.
---

# Gather Git Context

```
!`git rev-parse --is-inside-work-tree 2>&1; true`
```

```
!`git status --short 2>/dev/null; true`
```

```
!`git diff --cached 2>/dev/null; true`
```

```
!`git diff 2>/dev/null; true`
```

```
!`git log --oneline -10 2>/dev/null; true`
```

---

# Instructions

**Your role:** You are a commit message specialist. Your goal is to produce a single, precise Conventional Commits message that accurately describes the staged changes — no more, no less.

Using the gathered context above, determine which branch applies:

### Branch A — Not a Git Repo or No Changes

If `git rev-parse` output contains "not a git repository", or `git status` is empty (no staged, unstaged, or untracked files):

> **Cannot commit** — This is not a git repository, or there are no changes to commit.
> **Tip:** `/quiver:handover` to save session context before closing.

**Stop here.**

### Branch B — Unstaged Changes Only

If `git diff --cached` is empty (nothing staged) but `git status` shows modified or untracked files:

> **Nothing staged for commit.** Stage the files you want to commit first:
> - `git add <file>` — stage a specific file
> - `git add -p` — interactively stage hunks
> - `git add .` — stage everything (use with caution)
>
> Then run `/quiver:commit` again.

**Stop here.**

### Branch C — Staged Changes Exist

If `git diff --cached` has content, proceed to the Commit Message Generation section below.

---

# Commit Message Generation

Analyze the staged diff (`git diff --cached`) and the recent commit log, then follow these six steps:

## Step 1 — Determine Type

Select **one** type from this table based on the primary intent of the change:

| Type | When to Use |
|------|-------------|
| `feat` | New feature or capability visible to users |
| `fix` | Bug fix |
| `docs` | Documentation only (README, comments, JSDoc) |
| `style` | Formatting, whitespace, semicolons — no logic change |
| `refactor` | Code restructuring with no behavior change |
| `perf` | Performance improvement |
| `test` | Adding or fixing tests |
| `build` | Build system or external dependencies (npm, Makefile) |
| `ci` | CI/CD configuration (GitHub Actions, CircleCI) |
| `chore` | Maintenance tasks (version bumps, tooling config) |
| `revert` | Reverting a previous commit |

If the change spans multiple types, choose the one that best describes the **primary intent**.

## Step 2 — Determine Scope

Infer the scope from the file paths in the staged diff:
- Single module/directory → use its name (e.g., `auth`, `hooks`, `commands`)
- Single file with a clear domain → use the domain name
- Cross-cutting changes touching many areas → omit scope entirely

## Step 3 — Detect Breaking Changes

Check for any of these in the staged diff:
- Removed or renamed public API functions/methods
- Changed function signatures (added required params, changed return types)
- Removed or renamed CLI flags, commands, or environment variables
- Changed data formats, schemas, or wire protocols
- Removed files that other code may depend on

If found, the commit requires a `!` after the type/scope and a `BREAKING CHANGE:` footer.

## Step 4 — Write Subject Line

Rules:
- Imperative mood ("add", "fix", "remove" — not "added", "fixes", "removing")
- Lowercase first letter after the colon
- No period at the end
- Maximum 50 characters total (including `type(scope): `)
- Describe **what** changed, not **how**

## Step 5 — Write Body (Optional)

Include a body **only** when the "why" is not obvious from the subject:
- Separate from subject with a blank line
- Wrap at 72 characters
- Explain motivation and contrast with previous behavior
- Omit if the change is self-explanatory

## Step 6 — Write Footers (Optional)

Add footers when applicable:
- `BREAKING CHANGE: {description}` — required if Step 3 found breaking changes
- `Refs: #{issue}` — if the change relates to a known issue
- `Co-authored-by: {name} <{email}>` — if pair-programmed

---

# Output Template

Present the generated commit message inside a fenced code block, preceded by a metadata summary:

> **Type:** `{type}`
> **Scope:** `{scope or "none"}`
> **Breaking:** {yes/no}
> **Files:** {count} file(s) changed

```
{type}({scope}): {subject}

{body — if applicable}

{footers — if applicable}
```

Then ask:

> **Proceed?**
> - **yes** — commit with this message
> - **edit** — revise the message (tell me what to change)
> - **cancel** — abort without committing

---

# Commit Execution

When the user confirms **yes**:

1. Run the commit using a HEREDOC to preserve formatting:
   ```
   git commit -m "$(cat <<'EOF'
   {full commit message}
   EOF
   )"
   ```
2. **Verify:** Run `git log --oneline -1` to confirm the commit was created.
3. **Verify:** Run `git status --short` to confirm the staging area is clean.

Output the completion confirmation:

> **Committed:** `{short hash}` {subject}
> **Branch:** `{branch name}`
> **Tip:** `/quiver:handover` to save session context before closing.

When the user says **edit**:

1. Ask what should change.
2. Revise the message and re-present using the Output Template above.
3. Ask for confirmation again.

When the user says **cancel**:

> **Commit cancelled.** Your staged changes are still intact.
> **Tip:** `/quiver:handover` to save session context before closing.

**Stop here.**

---

## Quality Gates

Before presenting the commit message, verify:

**BLOCKING** (fix before presenting):
- Subject line is in imperative mood
- Subject line (full `type(scope): description`) is ≤ 50 characters
- Type is one of the 11 allowed values
- Breaking changes detected in Step 3 have a `BREAKING CHANGE:` footer

**WARNING** (review but don't block):
- Body is present for a multi-file change — large changes often benefit from a "why"
- Scope is omitted for a single-directory change — consider adding it

---

## Anti-Patterns

- **Don't** include file lists in the commit body — `git log --stat` already shows this.
- **Don't** use past tense ("added", "fixed") — Conventional Commits uses imperative mood.
- **Don't** exceed 50 chars in the subject — tools truncate longer subjects.
- **Don't** commit without user confirmation — always present the message and wait for yes/edit/cancel.
- **Don't** stage additional files — only commit what the user has already staged.

---

## Verification

After committing, run `git log -1 --format="%h %s"` to confirm the commit exists and the subject matches. If verification fails, inform the user immediately.

---

## Cross-Command References

> **Tip:** `/quiver:handover` to save session context after committing.
