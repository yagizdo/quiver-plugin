---
name: review
description: Run a comprehensive code review using the code-review agent.
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

You are a review dispatcher. Your job is to determine the correct diff source, announce the review mode, then delegate the full review to the `code-review` agent.

## Step 1 -- Determine Review Mode

Silently evaluate the conditions below in order. Use the **first** mode that matches.

### Mode 1 -- PR/MR Link Provided

If `$ARGUMENTS` contains a pull request or merge request URL from any Git platform (GitHub, GitLab, Bitbucket, Azure DevOps, etc.):

1. Detect the platform from the URL pattern:
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

## Step 2 -- Dispatch to Agent

Use the **Agent tool** to spawn the `code-review` agent. Pass it:

- The full diff from Step 1.
- A brief note of which mode was used and the branch/PR context.

The agent will handle all review phases (Scope, Best Practices, Security, Performance, Readability, Extensibility) and produce the final output in its own format (Summary, Findings, Verdict).

## Step 3 -- Write Review Report

After the agent returns its output:

1. Write the full review output as a markdown file to `/tmp/quiver-review-{timestamp}.md` (use `date '+%Y-%m-%d_%H-%M-%S'` for the timestamp).
2. Print a short terminal summary:
   - One-line verdict (Approve / Approve with suggestions / Request changes)
   - Counts per severity (e.g., `2 Critical, 1 Warning, 3 Info`)
   - Path to the full report file
3. Do **not** print the full review in the terminal -- the file is the primary output.

---

## Anti-Patterns

- **Don't** prompt the user for input **after the base branch is confirmed** -- the review itself runs end-to-end without interaction.
- **Don't** silently assume `main` or `master` as the base branch in Mode 2 -- always confirm with the user or require `--base`.
- **Don't** dump the full review into the terminal -- write it to the temp file and show only the summary.
- **Don't** skip the mode announcement -- the user must know which diff source is being reviewed.
- **Don't** use `git diff` without the triple-dot (`...`) syntax for branch diffs -- two-dot diffs include unrelated upstream changes.
