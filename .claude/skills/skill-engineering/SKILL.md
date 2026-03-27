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
  "You are a skill inventory auditor. Your goal: prevent duplicate skill creation.

   Steps:
   1. Glob .claude/skills/*/SKILL.md. For each file, read only the YAML
      frontmatter and extract: the `name` field, the first sentence of
      `description`, and the total line count.
   2. Read .claude/settings.json. List every key under 'skills' with its
      'path' value. For each path, verify the file exists on disk.
   3. Compare every skill name and description against '[TARGET_NAME]'.
      Flag any with keyword overlap >50%.

   Return three sections:
   A. Inventory: one line per skill — 'name | first sentence | lines'
   B. Registration: one line per entry — 'name | path | exists: yes/no'
   C. Overlap warnings: list any skills that may duplicate '[TARGET_NAME]'
      with the specific overlapping keywords.

   Constraint: read frontmatter only — do not read full SKILL.md bodies
   or any references/ subdirectories."

Agent(Explore, background=false):
  "You are a skill architecture analyst. Find 2-3 skills in .claude/skills/
   whose topic or purpose is most similar to '[TARGET_NAME]'.

   Steps:
   1. Skim the description field in frontmatter of all SKILL.md files.
   2. Select the 2-3 closest matches by topic/purpose similarity.
   3. For each selected skill, read the FULL SKILL.md and extract:
      - Template type it follows (technique/discipline/pattern/reference)
      - Full triggers list from frontmatter
      - Whether a references/ subdirectory exists (list filenames if yes)
      - One structural pattern worth reusing (decision table, subagent
        block, checklist, etc.)

   Return one paragraph per skill with the four data points above.
   Close with a one-sentence recommendation: 'For [TARGET_NAME], use the
   [template] template because [reason].'

   Constraint: read SKILL.md only — do not enter references/ subdirectories."

Agent(Explore, background=true):
  "Read .claude/skills/skill-engineering/references/architecture/README.md
   in full. Return verbatim: the tier criteria table and the template
   selection table. Return nothing else."
```

Wait for the two foreground agents before Phase B.

### Phase B — Select Tier + Template

Select tier per [Architecture Guide](references/architecture/README.md):
- **Tier 1** (<200 lines): `SKILL.md` only
- **Tier 2** (200–1000 lines): `SKILL.md` + `references/`
- **Tier 3** (10+ domains): `SKILL.md` + nested `references/` + subagents

Pick template from [templates/](references/templates/): `technique.md` · `discipline.md` · `pattern.md` · `reference.md`

### Phase C — Write SKILL.md

Non-negotiable rules:
1. `name` matches directory name (kebab-case); `SKILL.md` filename ALL CAPS
2. Description starts "Use when…" and lists 5+ keywords users actually type
3. File stays under 500 lines — overflow goes to `references/`
4. Discipline skills must include Anti-Rationalization — see [anti-rationalization/README.md](references/anti-rationalization/README.md)
5. Tier 2+: progressive disclosure via `references/` subdirectory

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
  "You are preparing a complete skill dossier for editing. Read every file
   in .claude/skills/[SKILL_NAME]/ without summarizing or truncating.

   Steps:
   1. Read SKILL.md. Return full text under header '=== SKILL.md ==='.
   2. Check if references/ exists. If yes, list all files in it and return
      each file's full text under '=== references/<filename> ==='.
   3. Read .claude/settings.json and extract only the JSON block for
      '[SKILL_NAME]'.

   Return the three sections concatenated. Do not summarize any file.
   This output will be used to identify exactly what needs changing."

Agent(Explore, background=true):
  "Search all SKILL.md files under .claude/skills/ — excluding
   .claude/skills/[SKILL_NAME]/ — for any mention of '[SKILL_NAME]'.
   Look for: wikilinks [[SKILL_NAME]], prerequisite mentions, 'see also'
   lines, and quoted skill name references.

   Return one line per match: 'file_path:line_number — matching text'
   If nothing found, return: 'No cross-references found.'"
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
  "You are a skill quality auditor. Read .claude/skills/[SKILL_NAME]/SKILL.md
   completely. Score each criterion 1–5 (1=absent, 3=adequate, 5=excellent).
   For any score below 4, give one specific fix as a concrete action.

   Criteria:
   1. CSO: Does description start 'Use when…'? Does it list 5+ specific
      keywords users actually type? Is it under 1024 characters?
      Evaluate against: .claude/skills/skill-engineering/references/cso/README.md
   2. Token efficiency: What is the exact SKILL.md line count? Name 3
      specific sections that could move to references/ with no loss of
      navigability.
   3. Anti-rationalization (skip if not a discipline/rule-enforcing skill,
      score N/A): Does it have an iron law, violation table, rationalization
      counters, and red flags section?
      Evaluate against: .claude/skills/skill-engineering/references/anti-rationalization/README.md
   4. Progressive disclosure: Is complex detail deferred to references/ files,
      or is everything crammed into SKILL.md?
   5. Trigger coverage: List the current triggers. Propose 3 additional
      keywords that users plausibly type when they need this skill.
   6. Template fit: Which template (technique/discipline/pattern/reference)
      best matches this skill's purpose? Does the actual structure match it?

   Return: numbered list, one line per criterion —
   '[n]/5 — [one-sentence verdict]. Fix: [specific action]'
   Omit the Fix line if score is 4 or higher."
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
  "You are auditing the current hook configuration. Read two sources:

   1. .claude/settings.json — extract the entire 'hooks' object. For each
      entry record: event type, command path, matcher (if any), statusMessage.
   2. Every file in .claude/hooks/ — for each file, describe in one sentence:
      what it detects, what it outputs (stdout/stderr/additionalContext),
      and its exit-code logic (0=allow, 2=block).

   Return three sections:
   A. Registered hooks: 'event | command | matcher | statusMessage'
   B. Hook file analysis: 'filename — [one-sentence description]'
   C. Gaps: list any event types with no registered hook
      (SessionStart / UserPromptSubmit / PreToolUse / PostToolUse / Stop)"
```

### Phase B — Design Decisions

Answer before writing code:
1. Which hook event? (`SessionStart` / `UserPromptSubmit` / `PreToolUse` / `PostToolUse` / `Stop`)
2. Block (exit 2 + stderr → Claude) or suggest (exit 0 + `additionalContext`)?
3. What JSON arrives on stdin for this event type?
4. What is the exact detection trigger condition?
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
  "You are conducting a comprehensive skill quality audit. Read ALL files
   in .claude/skills/[SKILL_NAME]/ — SKILL.md plus every file in
   references/ — and .claude/settings.json for its registration entry.

   Score each dimension 1–5 (1=absent, 3=adequate, 5=excellent).
   For any score below 4, give one specific fix with effort estimate.

   Dimensions:
   1. DISCOVERY — description has 5+ keywords users actually type?
      Starts with 'Use when…'?
   2. STRUCTURE — correct tier (1/2/3)? File structure matches tier template?
   3. TOKEN EFFICIENCY — SKILL.md line count. Name 3 sections to extract
      to references/.
   4. ANTI-RATIONALIZATION — if discipline skill: iron law, violation table,
      rationalization counters, red flags present? (Mark N/A if not applicable)
   5. HOOK COVERAGE — does the skill explain how/when a hook should trigger
      it? Should a dedicated hook exist for this skill?
   6. SUBAGENT USAGE — does the skill instruct Claude to delegate heavy
      analysis to subagents? Should it?
   7. REGISTRATION — correct entry in .claude/settings.json? Path resolves
      to an existing file on disk?
   8. STALENESS — list every reference to a file, tool, or hook that does
      not exist on disk. Include exact path and line number.

   Return format:
   - One line per dimension: '[DIMENSION] [score]/5 — [verdict]. Fix: [action] ([effort])'
   - Final block: 'TOP 3 PRIORITIES' — the three highest-ROI improvements, ranked."
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
