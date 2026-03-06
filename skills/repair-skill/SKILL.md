---
name: repair-skill
description: "Diagnostic patterns and repair strategies for fixing broken Claude Code skills. Use when analyzing skill structure, identifying stale API references, or applying targeted repairs."
disable-model-invocation: true
---

# Skill Repair Reference

This skill contains diagnostic patterns, failure taxonomies, and repair strategies for fixing broken Claude Code skills. It is used by the `/quiver:repair-skill` command.

---

## Skill Anatomy

A valid skill is a directory under `skills/` containing at minimum a `SKILL.md` file.

### Required Structure

```
skills/{name}/
  SKILL.md          # Main skill file (required)
  references/       # Supporting docs (optional)
  scripts/          # Helper scripts (optional)
```

### SKILL.md Required Fields

| Field | Required | Validation |
|-------|----------|------------|
| `name` | Yes | Must match directory name. Kebab-case. |
| `description` | Yes | Quoted string. Should describe when/why to use the skill. |
| `disable-model-invocation` | Recommended | `true` for knowledge-base skills that should not be invoked as agents. |

### Frontmatter Validation Rules

- YAML must be valid (no tabs, proper quoting, correct nesting).
- `name` value must exactly match the parent directory name.
- `description` must be a non-empty string. Wrap in quotes if it contains colons or special YAML characters.
- No unknown fields that could confuse the runtime.

---

## Common Failure Patterns

| # | Pattern | Severity | Symptoms | Detection Method |
|---|---------|----------|----------|------------------|
| F1 | Missing/malformed frontmatter | CRITICAL | Skill not recognized, load errors | YAML parse check |
| F2 | `name` mismatch | CRITICAL | Skill not found when referenced | Compare `name` field to directory name |
| F3 | Stale API references | WARNING | Instructions produce errors when followed | Context7 lookup against current docs |
| F4 | Deprecated function calls | WARNING | Code examples fail at runtime | Context7 lookup, changelog review |
| F5 | Vague/generic instructions | WARNING | Agent produces shallow or off-target output | Manual review: look for "as needed", "if applicable", "consider" |
| F6 | Broken file references | CRITICAL | Skill references files that don't exist | Check `references/` and `scripts/` paths |
| F7 | Overly long skill (>300 lines) | INFO | Token waste, diluted focus | Line count check |
| F8 | Missing examples | INFO | Hard to understand when to use the skill | Check for absence of example blocks |
| F9 | Wrong model recommendation | WARNING | Skill suggests `haiku` for complex reasoning tasks, or `opus` for simple lookups | Review model guidance against task complexity |
| F10 | Script syntax errors | CRITICAL | Hook/helper scripts fail | `bash -n` check |

---

## Diagnostic Checklist

Run these checks in order. Stop at any CRITICAL finding -- fix it before continuing.

### 1. Structural Validation

- [ ] `SKILL.md` exists in the skill directory
- [ ] YAML frontmatter parses without errors
- [ ] `name` field matches directory name
- [ ] `description` field is present and non-empty
- [ ] All files referenced in the skill body actually exist

### 2. Content Quality

- [ ] Instructions are specific and actionable (not generic advice)
- [ ] Examples are realistic and domain-specific
- [ ] Methodology steps are ordered by impact
- [ ] No placeholder text ("TODO", "TBD", "add later")
- [ ] No contradictory instructions

### 3. API/Library Verification (context7)

- [ ] Identify all external library/API references in the skill
- [ ] For each library: resolve library ID via `resolve-library-id`
- [ ] Query current docs for specific APIs/patterns mentioned
- [ ] Flag any deprecated APIs, changed parameters, or updated practices
- [ ] Verify code examples match current library versions

### 4. Integration Check

- [ ] Skill directory is under a path registered in `plugin.json` `skills` array
- [ ] If skill has scripts, they pass `bash -n` syntax check
- [ ] Cross-references to other skills/commands use correct paths

---

## Repair Strategies

### F1: Missing/Malformed Frontmatter

**Fix:** Add or correct the YAML frontmatter block. Ensure `---` delimiters are on their own lines, no tabs are used, and strings with special characters are quoted.

### F2: Name Mismatch

**Fix:** Update the `name` field to match the directory name exactly. Do not rename the directory -- change the field.

### F3/F4: Stale API References

**Fix:** Use context7 to look up current documentation. Replace outdated API calls, parameters, and patterns with current equivalents. Preserve the skill's intent while updating the implementation details.

### F5: Vague Instructions

**Fix:** Replace generic phrases with specific, actionable directives. "Consider security implications" becomes "Check for SQL injection in user-input parameters, XSS in rendered output, and CSRF token presence on state-changing endpoints."

### F6: Broken File References

**Fix:** Either create the missing file or update the reference. If the referenced content was important, reconstruct it from context. If it was optional, remove the reference.

### F7: Overly Long Skill

**Fix:** Identify the highest-impact sections and trim the rest. Move detailed reference material to `references/` files. Keep SKILL.md under 200 lines for focused skills, 300 for comprehensive ones.

### F8: Missing Examples

**Fix:** Add 2-3 realistic trigger examples in XML format showing when the skill should be used.

### F9: Wrong Model Recommendation

**Fix:** Match model to task complexity: `haiku` for lightweight checks, `sonnet` for balanced work, `opus` for deep reasoning, `inherit` when unsure.

### F10: Script Syntax Errors

**Fix:** Run `bash -n` on the script, fix reported syntax errors. Common issues: unclosed quotes, missing `fi`/`done`, incorrect variable expansion.

---

## Context7 Lookup Guide

### Extracting Library References

Scan the skill body for:
- Import/require statements in code examples
- Package names mentioned in prose (e.g., "uses the Stripe API")
- CLI tool references (e.g., "run `eslint`")
- Framework patterns (e.g., "Rails ActiveRecord", "React hooks")

### Formulating Queries

For each identified library:

1. **Resolve:** Call `resolve-library-id` with the library name (e.g., "stripe", "react", "rails")
2. **Query:** Call `query-docs` with the resolved ID and a targeted query about the specific API pattern used in the skill
3. **Compare:** Check the returned docs against what the skill instructs

### Query Examples

| Skill References | resolve-library-id | query-docs Query |
|-----------------|-------------------|------------------|
| `Stripe.charges.create` | "stripe node" | "create a charge" |
| `useEffect cleanup` | "react" | "useEffect cleanup function" |
| `ActiveRecord.find_by` | "rails" | "find_by query method" |

### Comparison Checklist

- Are the function/method signatures still correct?
- Have required parameters changed?
- Are there new required options or deprecated ones?
- Has the recommended pattern changed (e.g., callbacks to promises)?
- Are version-specific notes still accurate?

**Limit:** Maximum 3 context7 calls per library to avoid excessive token usage.
