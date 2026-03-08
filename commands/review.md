---
name: review
description: Run a multi-agent code review (code quality + security audit) with synthesized findings.
argument-hint: "[PR/MR URL | --base <branch>]"
---

# Gather Context

```
!`git rev-parse --is-inside-work-tree`
```

```
!`git branch --show-current`
```

```
!`git branch --sort=-committerdate | head -8`
```

---

# Instructions

You are a review orchestrator. Your job is to determine the correct diff source, announce the review mode, dispatch multiple review agents in parallel, then synthesize their findings into a single unified report.

## Step 1 -- Determine Review Mode

Silently evaluate the conditions below in order. Use the **first** mode that matches.

### Mode 1 -- PR/MR Link Provided

If `$ARGUMENTS` contains a pull request or merge request URL from any Git platform (GitHub, GitLab, Bitbucket, Azure DevOps, etc.):

1. Detect the platform from the URL pattern. Validate that extracted URL segments (owner, repo, number, group, project) contain only safe characters (`[a-zA-Z0-9._-]+`) before constructing commands:
   - **GitHub:** `github.com/{owner}/{repo}/pull/{number}` -- use `gh pr diff {number} --repo {owner}/{repo}`
   - **GitLab:** `gitlab.com/{group}/{project}/-/merge_requests/{number}` -- use `glab mr diff {number}`
   - **Bitbucket:** `bitbucket.org/{workspace}/{repo}/pull-requests/{number}` -- Bitbucket CLI lacks a direct diff command. Fall back to Mode 2 (branch diff).
   - **Other platforms:** Fall back to Mode 2 with a note:
     > Platform not recognized for direct diff fetching. Falling back to branch diff.
2. Before running a platform CLI command (`gh`, `glab`), check if the CLI is available. If not, fall back to Mode 2 with a note:
   > `{cli}` CLI not found. Falling back to branch diff.
3. Announce: `Reviewing PR/MR from provided link...`
4. If fetching fails (permissions, invalid URL), print a warning:
   > Could not fetch diff from the provided link. Falling back to branch diff.
   Then continue to Mode 2.
5. If fetching succeeds, pass the diff to the agent in Step 2.

### Mode 2 -- Branch Diff

If no PR link was provided (or Mode 1 fell back), and the current branch is **not** `main` or `master`:

1. **Determine the base branch** using one of these methods (in order):
   - **`--base` flag:** If `$ARGUMENTS` contains `--base <branch>`, use that branch directly. Skip the prompt.
   - **Interactive selection:** Otherwise, use `AskUserQuestion` to ask the user which base branch to compare against. Use the gathered branch list output to build action buttons for candidate branches. Include an **"Other (I'll type it)"** button as the last option. Phrasing:
     > You're on `{current_branch}`. Which branch should I compare against for the review?
   - If the user picks "Other (I'll type it)", ask them to type the branch name.
2. Announce: `Reviewing branch {current_branch} against {base_branch}...`
3. Get the diff:
   ```
   git diff {base_branch}...HEAD
   ```
4. If the diff is empty, announce:
   > Branch diff against `{base_branch}` is empty. Checking for local uncommitted changes...
   Then continue to Mode 3.
5. Otherwise, pass the diff to the agent in Step 2.

### Mode 3 -- Uncommitted/Staged Changes

If the current branch is `main`/`master`, or the branch diff was empty:

1. Check for unstaged changes:
   ```
   git diff
   ```
2. If empty, check for staged changes:
   ```
   git diff --cached
   ```
3. If both are empty:
   > No changes to review. Commit some changes or switch to a feature branch and try again.
   **Stop here.**
4. Announce: `Reviewing local uncommitted changes...`
5. Pass the diff to the agent in Step 2.

---

## Step 2 -- Parallel Agent Dispatch

Spawn **all** review agents simultaneously using multiple Agent tool calls in a single response. Each agent receives the same inputs:

- The full diff from Step 1.
- A brief note of which mode was used and the branch/PR context.

### Always-run agents

| Agent             | Focus                                                                 |
|-------------------|-----------------------------------------------------------------------|
| `code-review`     | Best practices, performance, readability, extensibility               |
| `security-audit`  | Attack surfaces, input flows, auth/authz, secrets, data exposure      |

### Adding future agents

To add a new review agent, create it under `agents/review/`, register it in `plugin.json`'s `agents` array (required for the agent to be dispatchable), and add a row to the table above. The orchestrator dispatches every agent listed here.

## Step 3 -- Synthesize Findings

After **all** agents return, merge their outputs into a single unified report. Follow these rules:

1. **Deduplicate.** If two agents flag the same issue (e.g., code-review's Performance phase and security-audit both flag a denial-of-service risk on the same line), keep the more detailed finding and discard the other. Prefer the specialist agent's version when depth is comparable.
2. **Unified severity.** Reclassify all findings into a single scale:
   - **Critical** -- Must fix before merge. Actively exploitable vulnerabilities, data-loss bugs, auth bypass.
   - **High** -- Strongly recommended. Performance regressions, authorization gaps, unsafe patterns.
   - **Medium** -- Should fix. Best-practice violations, maintainability concerns, defensive gaps.
   - **Low** -- Optional. Style nits, hardening opportunities, future considerations.
3. **Tag the source.** Prefix each finding with the agent that produced it for traceability:
   ```
   [SEVERITY] (code-review) file_path:line_number -- Short title
   ```
4. **Unified verdict.** Apply the strictest verdict across all agents:
   - If **any** agent produces a Critical or High finding --> **Request changes**
   - If the worst finding is Medium --> **Approve with suggestions**
   - If only Low or no findings --> **Approve**

### Synthesized report structure

```markdown
# Code Review Report

## Summary
One paragraph: what the PR does, overall risk, top-line recommendation.

## Agents Dispatched
- code-review: [verdict]
- security-audit: [verdict]

## Findings
### Critical
[merged critical findings]

### High
[merged high findings]

### Medium
[merged medium findings]

### Low
[merged low findings]

## Verdict
[Unified verdict] -- [severity counts] -- [one-line justification]
```

## Step 4 -- Write Review Report

### 4a -- Check for saved preference

Before prompting, check your auto-memory files for a saved review report preference. Look for a `review-preferences` section or file that contains a `report_path` and a `mode` field.

- If `mode` is `always` -- skip Q1 and Q2. Auto-save to the remembered `report_path`. Go directly to step 4c.
- If `mode` is `default` -- show Q1 with the remembered path as the first action button, then show Q2.
- If `mode` is `skip_remember_prompt` -- show Q1 but skip Q2 after the user picks.
- If no preference exists -- show Q1 and Q2.

### 4b -- Q1: Save location

Ask the user where to save the report using `AskUserQuestion`:

> Where should I save the review report?

Offer these action buttons (if a remembered default exists, list it first with a `(default)` label):
1. **`.claude/reports/`** -- Save to `{project_root}/.claude/reports/review-{timestamp}.md`
2. **`reports/`** -- Save to `{project_root}/reports/review-{timestamp}.md`
3. **Show in terminal** -- Print the full report directly in the terminal. Do not write a file.
4. **Custom path** -- Ask the user to type a directory path, then save there as `review-{timestamp}.md`
5. **Cancel** -- Do not save or print the report. Stop here.

If the user chose "Cancel", stop here. If the user chose "Show in terminal", print the full report and skip Q2.

### 4b.2 -- Q2: Remember preference

If Q2 is not suppressed (see 4a), ask the user using `AskUserQuestion`:

> Should I remember this save location for future reviews?

Offer these action buttons:
1. **Always use this path** -- Save the chosen path to memory with `mode: always`. Future reviews auto-save here without any prompts.
2. **Remember as default** -- Save the chosen path to memory with `mode: default`. Future reviews show Q1 with this path pre-selected, and still show Q2.
3. **No** -- Do not save anything. Ask both Q1 and Q2 again next time.
4. **No, stop asking** -- Do not save a path, but set `mode: skip_remember_prompt` in memory. Future reviews show Q1 but skip Q2.

When saving a preference, write it to your auto-memory directory as a `review-preferences.md` file (or update the existing one) with clear `report_path` and `mode` fields. Example:

```markdown
# Review Preferences
- report_path: .claude/reports/
- mode: always
```

### 4c -- Write and summarize

After the user chooses (unless "Show in terminal" or "Cancel"):

1. Create the chosen directory if it does not exist.
2. Write the full synthesized report as `review-{timestamp}.md` (use `date '+%Y-%m-%d_%H-%M-%S'` for the timestamp).
3. Print a short terminal summary:
   - One-line verdict (Approve / Approve with suggestions / Request changes)
   - Counts per severity (e.g., `2 Critical, 1 High, 3 Medium, 5 Low`)
   - Which agents ran and their individual verdicts
   - Path to the saved report file
4. Do **not** print the full review in the terminal unless the user chose "Show in terminal".

---

## Anti-Patterns

- **Don't** prompt the user for input **between base branch confirmation and report save** -- the review itself runs end-to-end without interaction until the save-location prompt in Step 4.
- **Don't** silently assume `main` or `master` as the base branch in Mode 2 -- always confirm with the user or require `--base`.
- **Don't** dump the full review into the terminal -- write it to the report file and show only the summary (unless the user chose "Show in terminal").
- **Don't** save review reports to system temp directories (`/tmp/`) -- always save inside the project or show in terminal, per the user's choice.
- **Don't** skip the mode announcement -- the user must know which diff source is being reviewed.
- **Don't** use `git diff` without the triple-dot (`...`) syntax for branch diffs -- two-dot diffs include unrelated upstream changes.
- **Don't** run agents sequentially -- always dispatch all agents in parallel (multiple Agent tool calls in one response).
- **Don't** present raw agent outputs side-by-side -- always synthesize into a single merged report with deduplication.
- **Don't** let duplicate findings from different agents inflate severity counts -- deduplicate before counting.
- **Don't** ignore saved review preferences -- always check auto-memory for a `review-preferences` file before prompting in Step 4.
- **Don't** show Q2 (remember prompt) when the user chose "Show in terminal" or when `mode` is `skip_remember_prompt` or `always`.
