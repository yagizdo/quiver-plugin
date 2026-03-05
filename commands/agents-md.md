---
description: Generate or rewrite an AGENTS.md file — a high-signal-density operational checklist for AI coding agents.
argument-hint: Generates project-specific AGENTS.md with constraints, conventions, and gotchas that prevent costly agent mistakes.
---

# Gather Project Context

```
!`ls -1; true`
```

```
!`find . -maxdepth 2 -type f -not -path './.git/*' -not -path './node_modules/*' -not -path './.build/*' -not -path './vendor/*' -not -path './target/*' | head -120; true`
```

```
!`cat AGENTS.md 2>/dev/null; true`
```

```
!`cat README.md 2>/dev/null; true`
```

```
!`cat CLAUDE.md 2>/dev/null; true`
```

```
!`find . -maxdepth 3 -type f -name "*.yml" -path "*ci*" -o -name "*.yaml" -path "*ci*" -o -name "Jenkinsfile" -o -name ".travis.yml" -o -name "Makefile" | head -20; true`
```

```
!`find . -maxdepth 1 -type f -name ".eslintrc*" -o -name ".prettierrc*" -o -name "biome.json" -o -name "rustfmt.toml" -o -name ".swiftlint.yml" -o -name ".rubocop.yml" -o -name ".editorconfig" -o -name ".clang-format" | head -20; true`
```

```
!`git remote -v 2>/dev/null; true`
```

```
!`git log --oneline -5 2>/dev/null; true`
```

---

# Instructions

You are an AGENTS.md architect. Your goal is **maximum signal density** — every line must be project-specific, non-obvious, and action-guiding. No generic advice. No README duplication. No rules already enforced by tooling.

Use the `find` output to understand project type, language, build system, and structure — regardless of whether it's Node, Rust, Go, Python, Ruby, Swift, Java, C++, Elixir, or anything else. Do not rely on hardcoded manifest names.

Silently determine which case applies:

- **Branch A — No project detected:** If the directory has no recognizable source files, manifests, or config → tell the user this doesn't appear to be a project directory and stop.
- **Branch B — Existing AGENTS.md:** If `cat AGENTS.md` returned content → enter **rewrite mode**. Aggressively trim generic advice, deduplicate against README.md and CLAUDE.md, tighten language to imperative form. Then proceed to AGENTS.md Generation using the existing content as a starting point.
- **Branch C — No AGENTS.md:** Proceed to AGENTS.md Generation and create from scratch.

---

# AGENTS.md Generation

Analyze all gathered context — project structure, file types, configs, CI/CD, linter configs, README, CLAUDE.md, git history — and generate an AGENTS.md with these exact sections:

## Must-follow constraints
- Hard rules that cause build failures, test failures, or broken deployments if violated.
- **Include:** required env vars, mandatory build flags, version pinning rules, required code generation steps.
- **Exclude:** anything already enforced by a linter/formatter config file (if a config enforces it, don't repeat it).

## Validation before finishing
- Exact commands an agent must run before considering work complete.
- **Include:** build commands, test commands, lint commands, type-check commands — with the actual flags/args used in this project.
- **Exclude:** generic "run tests" — specify the real command as discovered from project files.

## Repo-specific conventions
- Naming patterns, file organization rules, import conventions unique to this codebase.
- **Include:** component file naming, test file location conventions, module boundary rules, commit message format if non-standard.
- **Exclude:** language-level conventions that any experienced developer would know.

## Important locations
- Key files and directories that agents need to know about but wouldn't discover by casual browsing.
- **Include:** config files with non-obvious names, generated code directories, shared type definitions, entry points.
- **Exclude:** obvious paths — only list what would surprise someone.

## Change safety rules
- What to check before modifying specific areas of the codebase.
- **Include:** files that require synchronized updates (e.g., "changing X requires updating Y"), migration requirements, backwards-compatibility constraints.
- **Exclude:** generic "be careful" advice.

## Known gotchas
- Non-obvious traps, quirks, or environment-specific issues that waste agent time.
- **Include:** platform-specific build issues, flaky test workarounds, undocumented dependencies between components.
- **Exclude:** issues that have been fixed or are documented in README.

**Section rules:**
- Every bullet must be specific to THIS project. If you could copy-paste it into any repo, delete it.
- Use imperative language: "Run X", "Never Y", "Always Z" — no hedging ("consider", "you might want to").
- If a section genuinely has no content, write the heading followed by a single line: `No project-specific constraints identified.`
- Do NOT duplicate content from README.md or CLAUDE.md. If CLAUDE.md already covers a rule, omit it.

---

# Quality Gates

Before saving, verify:

**BLOCKING** (fix before saving):
- Every bullet is specific to this project — no generic advice that applies to any codebase.
- No content duplicated from README.md or CLAUDE.md.
- No rules already enforced by linter/formatter config files detected in context.
- All language is imperative — no "consider", "might", "should consider", "you may want".

**WARNING** (review and trim):
- File exceeds 80 lines — AGENTS.md should be a concise checklist, not documentation.
- Any section has more than 7 bullets — consider merging or removing the least critical.

---

# Anti-Patterns

- **Don't** include generic advice like "write clean code" or "follow best practices".
- **Don't** duplicate the README — agents can read it themselves.
- **Don't** hedge with "you might want to" or "consider doing" — be direct.
- **Don't** pad empty sections with filler — use the "No project-specific constraints" line.
- **Don't** list linter rules — the linter already enforces them.

---

# Save & Verify

1. Write the generated AGENTS.md to the project root.
2. Read back the file to confirm it was written correctly.
3. Verify all 6 section headings are present.
4. Count total lines.

---

# Output

> **AGENTS.md {created | rewritten}**
> **Sections:** 6
> **Lines:** {line count}
> **Signal check:** {pass | warnings}
>
> Re-run `/quiver:agents-md` any time to rewrite with updated project context.
