---
name: skill-engineering
description: Use when creating, updating, improving, refactoring, testing, or debugging any Claude Code skill or hook. Covers the full skill lifecycle: new skill creation, Kaizen improvement, CSO optimization, anti-rationalization, hook design, subagent workflows, tier selection, progressive disclosure, and settings.json registration.
triggers:
  - create skill
  - new skill
  - add skill
  - update skill
  - improve skill
  - refactor skill
  - skill not firing
  - skill hook
  - hook design
  - SKILL.md
  - 500-line rule
  - progressive disclosure
  - CSO
  - skill audit
  - kaizen
  - skill engineering
---

# Skill Engineering

Central orchestrator for the full skill lifecycle. Load this skill before touching any `.claude/skills/` file.

---

## Step 0 — Classify Intent

| The user wants to… | Intent | Workflow |
|---|---|---|
| Build a new skill from scratch | **CREATE** | §1 |
| Fix bugs or stale content in a skill | **UPDATE** | §2 |
| Improve quality, triggers, or structure | **ENHANCE** | §3 |
| Add or modify a hook in settings.json | **HOOK** | §4 |
| Score and review skill quality | **AUDIT** | §5 |
| Diagnose why a skill isn't activating | **DEBUG** | §6 |

---

## §1 CREATE Workflow

### Phase A — Research (run in parallel, mandatory)

```
Agent(Explore, background=false):
  "Scan every SKILL.md under .claude/skills/. For each extract:
   name (from frontmatter), first sentence of description, line count.
   Flag any whose name or description overlaps with '[TARGET_NAME]'.
   Also read .claude/settings.json — list all registered skills, verify
   each path exists, and return the exact JSON schema of one entry."

Agent(Explore, background=false):
  "Find 2-3 skills in .claude/skills/ most structurally similar to
   '[TARGET_NAME]'. Read their full SKILL.md. Return: template type
   (technique/discipline/pattern/reference), triggers list, whether they
   have a references/ subdirectory, and one structural pattern to reuse."

Agent(Explore, background=true):
  "Read .claude/skills/skill-engineering/references/architecture/README.md
   in full. Return the tier criteria table and template selection guide."
```

Wait for the two foreground agents before Phase B.

### Phase B — Select Tier + Template

Select tier per [Architecture Guide](references/architecture/README.md):
- **Tier 1** (<200 lines): `SKILL.md` only
- **Tier 2** (200–1000 lines): `SKILL.md` + `references/`
- **Tier 3** (10+ domains): `SKILL.md` + nested `references/` + subagents

Pick template from [templates/](references/templates/): `technique.md` · `discipline.md` · `pattern.md` · `reference.md`

### Phase C — Write SKILL.md

Non-negotiable rules (state once — do not repeat these downstream):
1. `name` matches directory name (kebab-case); `SKILL.md` filename ALL CAPS
2. Description starts "Use when…" and lists 5+ keywords users actually type
3. File stays under 500 lines — overflow goes to `references/`
4. Discipline skills must include Anti-Rationalization — see [references/anti-rationalization/README.md](references/anti-rationalization/README.md)
5. Tier 2+: use progressive disclosure via `references/` subdirectory

Full standards: [Standards](references/standards/README.md) · [CSO](references/cso/README.md) · [Gotchas](references/standards/gotchas.md)

### Phase D — Register in settings.json

```json
"skill-name": {
  "description": "[copy from SKILL.md description field]",
  "path": "skills/skill-name/SKILL.md",
  "user_invocable": true
}
```

### Phase E — Validate

Run the **Pre-Deploy Checklist** at the bottom of this file.

---

## §2 UPDATE Workflow

### Phase A — Deep Read (mandatory)

```
Agent(Explore, background=false):
  "Read the complete content of .claude/skills/[SKILL_NAME]/SKILL.md
   and every file in its references/ subdirectory. Return full text with
   filename headers — do not summarize. Also extract its settings.json entry."

Agent(Explore, background=true):
  "Search all other SKILL.md files under .claude/skills/ for any mention
   of '[SKILL_NAME]' (links, prerequisites, see-also). Return file + line."
```

### Phase B — State the Delta

Before editing, declare:
1. What is wrong (specific lines/sections)
2. What the correct content should be and why
3. Which files change (SKILL.md? references/? settings.json?)

### Phase C — Edit Precisely

Edit only what's broken. Do not reformat unrelated sections. After edit: recheck line count (must stay under 500).

---

## §3 ENHANCE Workflow

### Phase A — Quality Audit (mandatory)

```
Agent(Explore, background=false):
  "Audit .claude/skills/[SKILL_NAME]/SKILL.md. Score each criterion 1–5.
   Give one concrete fix per score below 4.

   1. CSO: description starts 'Use when…'? 5+ specific trigger keywords?
      Under 1024 chars? (criteria in references/cso/README.md)
   2. Token efficiency: SKILL.md line count. What 3 sections could move
      to references/ with no information loss?
   3. Anti-rationalization (discipline skills only): iron law, violation
      table, rationalization counters, red flags present?
      (criteria in references/anti-rationalization/README.md)
   4. Progressive disclosure: is detail deferred to references/, or all
      in the main file?
   5. Trigger coverage: list current triggers. Suggest 3 additional keywords
      users plausibly type when they need this skill.
   6. Template fit: which template (technique/discipline/pattern/reference)
      best matches? Does structure match it?

   Return: numbered list, one line per criterion — score + one-sentence verdict."
```

### Phase B — Apply by Priority

1. CSO fixes first (broken description = skill never loads)
2. Anti-rationalization (for discipline skills)
3. Progressive disclosure (token efficiency)
4. Template alignment

---

## §4 HOOK Workflow

Hook event types and exit code rules: [HOOK_MECHANISMS.md](references/triggers_and_hooks/HOOK_MECHANISMS.md)

### Phase A — Research (mandatory)

```
Agent(Explore, background=false):
  "Read .claude/settings.json in full. Extract all hooks by event type
   with their commands and matchers. Then read every file in .claude/hooks/
   and describe what each does, its detection logic, and its output."
```

### Phase B — Design Decisions

Answer before writing code:
1. Which hook event? (`SessionStart` / `UserPromptSubmit` / `PreToolUse` / `PostToolUse` / `Stop`)
2. Block (exit 2 + stderr) or suggest (exit 0 + additionalContext)?
3. What JSON arrives on stdin?
4. What is the detection trigger condition?
5. Implementation: Python (preferred) or Bash/jq for trivial one-liners?

### Phase C — Implement

Use the Python starters in [hook-templates.md](references/triggers_and_hooks/hook-templates.md) — one template per hook type, copy and fill in detection logic.

### Phase D — Register in settings.json

```json
"UserPromptSubmit": [{
  "type": "command",
  "command": "python3 /absolute/path/.claude/hooks/your-hook.py",
  "statusMessage": "Analyzing..."
}]
```

For PreToolUse with a matcher, see [hook-templates.md](references/triggers_and_hooks/hook-templates.md).

---

## §5 AUDIT Workflow

```
Agent(Plan, background=false):
  "Comprehensive quality audit of .claude/skills/[SKILL_NAME]/. Read ALL
   files (SKILL.md + every file in references/). Score each dimension 1–5.
   Give one specific fix per score below 4.

   1. DISCOVERY — description has 5+ keywords users actually type?
   2. STRUCTURE — correct tier? Structure matches tier template?
   3. TOKEN EFFICIENCY — SKILL.md line count. What to extract to references/?
   4. ANTI-RATIONALIZATION — if discipline skill: iron law, violation table,
      rationalization counters, red flags?
   5. HOOK COVERAGE — does skill describe when/how hooks activate it?
   6. SUBAGENT USAGE — does skill delegate heavy analysis to subagents?
   7. REGISTRATION — correct entry in settings.json? Path resolves?
   8. STALENESS — references to files/tools/hooks that don't exist?

   Return: numbered list, one verdict per dimension. Then: top 3 priority
   improvements with effort estimate (low/med/high)."
```

---

## §6 DEBUG Workflow

Work through [TROUBLESHOOTING.md](references/kaizen/TROUBLESHOOTING.md) in order — it covers registration, description keywords, frontmatter, file existence, line count, and priority conflicts step by step.

---

## Pre-Deploy Checklist

Before deploying or updating any skill:

- [ ] `name` field in YAML matches the directory name exactly (kebab-case)
- [ ] `SKILL.md` filename is ALL CAPS
- [ ] Description starts "Use when…" and lists 5+ trigger keywords
- [ ] `triggers` is a YAML list (not a comma string)
- [ ] SKILL.md is under 500 lines
- [ ] Path registered in settings.json resolves to a real file
- [ ] Send a prompt containing trigger keywords — confirm the skill loads

---

## Reference Index

- [Architecture: Tier 1/2/3 guide + template selection](references/architecture/README.md)
- [Templates: technique / discipline / pattern / reference](references/templates/)
- [CSO: making skills discoverable](references/cso/README.md)
- [Anti-rationalization: discipline skill enforcement](references/anti-rationalization/README.md)
- [Hook exit codes + I/O contracts](references/triggers_and_hooks/HOOK_MECHANISMS.md)
- [Hook Python templates](references/triggers_and_hooks/hook-templates.md)
- [Trigger types: keyword / intent / file / content](references/triggers_and_hooks/TRIGGER_TYPES.md)
- [Anthropic best practices](references/standards/anthropic-best-practices.md)
- [Common mistakes](references/standards/gotchas.md)
- [Testing skills with subagents](references/testing/testing-skills-with-subagents.md)
- [Kaizen principles](references/kaizen/kaizen_principles.md)
- [Troubleshooting](references/kaizen/TROUBLESHOOTING.md)
- [Pattern library (regex / glob)](references/workflows/PATTERNS_LIBRARY.md)
