# Refactoring Execution Plan

## Overview
Reorganize the Claude Code project structure to:
1. Consolidate skills into `.claude/skills/` (remove duplication with `.agents/`)
2. Remove obsolete files (`Plan.md`, `/docs/`)
3. Implement hooks for skill automation (as detailed in `SKILL_HOOKS_ANALYSIS.md`)

---

## Phase 1: Directory Structure Reorganization

### Step 1.1: Consolidate `.agents/skills/agent-rules/` → `.claude/skills/agent-rules/`

**Current State:**
```
.agents/
└── skills/
    └── agent-rules/          ← SOURCE
        ├── SKILL.md
        └── ...

.claude/skills/
└── agent-rules/             ← SYMLINK (points to ../../.agents/skills/agent-rules)
```

**Action:**
```bash
# 1. Copy the actual directory
cp -r .agents/skills/agent-rules/ .claude/skills/agent-rules-new/

# 2. Remove the symlink
rm .claude/skills/agent-rules

# 3. Move the copy into place
mv .claude/skills/agent-rules-new/ .claude/skills/agent-rules

# 4. Remove .agents/skills/ (now redundant)
rm -rf .agents/

# 5. Update settings.json path (if needed)
# Change: "path": "skills/agent-rules"
# To:     "path": ".claude/skills/agent-rules" (if relative path needed)
# Or keep: "path": "skills/agent-rules" if it's relative to .claude/ directory
```

**Verification:**
```bash
ls -la .claude/skills/agent-rules/
# Should show SKILL.md and other files
```

---

### Step 1.2: Move `skills/skill-dev/skill-engineering/` → `.claude/skills/skill-engineering/`

**Current State:**
```
skills/skill-dev/skill-engineering/   ← SOURCE (outside .claude)
├── SKILL.md
└── references/
    ├── templates/
    ├── standards/
    └── ...
```

**Action:**
```bash
# 1. Copy the directory
cp -r skills/skill-dev/skill-engineering/ .claude/skills/skill-engineering

# 2. Remove the old location
rm -rf skills/

# 3. Verify new location
ls -la .claude/skills/skill-engineering/
```

**Verification:**
```bash
# Check that all files are present
ls .claude/skills/skill-engineering/
# Should show: SKILL.md, references/, etc.
```

---

### Step 1.3: Remove Obsolete Files

**Action:**
```bash
# Delete Plan.md from root (archived in refactor/)
rm Plan.md

# Delete /docs/ (PDF backups - per CLAUDE.md, source-of-truth is Markdown-docs/)
rm -rf docs/
```

**Verification:**
```bash
# Root directory should not contain these files
ls -la | grep -E "Plan.md|docs"
# Should return empty
```

---

## Phase 2: Settings Configuration Updates

### Step 2.1: Update `.claude/settings.json`

**Changes Needed:**

1. **If using relative paths within `.claude/` directory:**
   - Current: `"path": "skills/agent-rules"` works as-is
   - No change needed if paths are relative to `.claude/` root

2. **If using full paths (not recommended):**
   - Change: `.agents/skills/agent-rules` → `.claude/skills/agent-rules`
   - Add entries for new skills if not present

3. **Ensure skill-developer entry is correct:**
   - Check: `"path": "skills/skill-developer/SKILL.md"`
   - Verify this still points to correct location in `.claude/skills/`

**Current settings.json skills section (relevant entries):**
```json
{
  "skills": {
    "agent-rules": {
      "description": "Maintain and generate AGENTS.md files...",
      "path": "skills/agent-rules",
      "user_invocable": true
    },
    "skill-developer": {
      "description": "Implement triggers, hooks, and skill lifecycle...",
      "path": "skills/skill-developer/SKILL.md",
      "user_invocable": true
    }
  }
}
```

**Verification:**
```bash
# Check that paths are valid
test -f .claude/skills/agent-rules/SKILL.md && echo "✓ agent-rules found"
test -f .claude/skills/skill-engineering/SKILL.md && echo "✓ skill-engineering found"
test -f .claude/skills/skill-developer/SKILL.md && echo "✓ skill-developer found"
```

---

## Phase 3: Hook Implementation (After Reorganization)

Once directory structure is clean, implement hooks for automation. See `SKILL_HOOKS_ANALYSIS.md` for detailed strategy.

### Hooks to Add to `.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "type": "command",
        "command": "./.claude/hooks/session-start.sh"
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "./.claude/hooks/lint-suggest.sh",
            "statusMessage": "Checking for lint issues..."
          }
        ]
      },
      {
        "matcher": "Bash",
        "pattern": "git commit",
        "hooks": [
          {
            "type": "command",
            "command": "./.claude/hooks/commit-format-validate.sh",
            "statusMessage": "Validating commit format..."
          }
        ]
      },
      {
        "matcher": "Bash",
        "pattern": "git push",
        "hooks": [
          {
            "type": "command",
            "command": "./.claude/hooks/pre-push-validate.sh",
            "statusMessage": "Running pre-push validation..."
          }
        ]
      }
    ]
  }
}
```

---

## Phase 4: Git Commit & Push

### Step 4.1: Stage Changes

```bash
git add -A
```

### Step 4.2: Create Commit

```bash
git commit -m "refactor: reorganize .claude/skills and remove obsolete files

- Consolidate .agents/skills/agent-rules → .claude/skills/agent-rules
- Move skills/skill-dev/skill-engineering → .claude/skills/skill-engineering
- Remove obsolete Plan.md from root (archived in /refactor/)
- Remove /docs/ folder (PDFs backup per CLAUDE.md)
- Clean up directory structure for hook implementation
- Simplify skill path configuration in settings.json

This prepares the project for hook-based skill automation."
```

### Step 4.3: Push to Branch

```bash
git push -u origin claude/analyze-skills-hooks-fPV32
```

---

## Verification Checklist

- [ ] `.agents/` directory no longer exists
- [ ] `skills/` directory no longer exists (top-level)
- [ ] All skills consolidated under `.claude/skills/`
- [ ] `Plan.md` removed from root
- [ ] `/docs/` folder removed from root
- [ ] `.claude/settings.json` has correct paths
- [ ] `agent-rules` SKILL.md accessible at `.claude/skills/agent-rules/`
- [ ] `skill-engineering` SKILL.md accessible at `.claude/skills/skill-engineering/`
- [ ] All hooks in `.claude/settings.json` reference valid scripts
- [ ] Git history clean and commit messages conventional
- [ ] Branch pushed successfully to remote

---

## Rollback Plan (if needed)

If issues occur:

```bash
# 1. Revert the commit
git revert HEAD

# 2. Or reset to previous state
git reset --hard HEAD~1

# 3. Or restore from git history
git checkout HEAD~1 -- .agents/
git checkout HEAD~1 -- skills/
git checkout HEAD~1 -- Plan.md
git checkout HEAD~1 -- docs/
```

---

## Files Modified/Created in This Plan

- **Created:** `/refactor/SKILL_HOOKS_ANALYSIS.md` (Detailed hook opportunities)
- **Created:** `/refactor/EXECUTION_PLAN.md` (This file)
- **Moved:** `skill-refactor-todo.md` → `/refactor/skill-refactor-todo.md`
- **Modified:** `.claude/settings.json` (Update paths if needed)
- **Deleted:** `Plan.md` (root)
- **Deleted:** `/docs/` (folder)
- **Moved:** `.agents/skills/agent-rules/` → `.claude/skills/agent-rules/`
- **Moved:** `skills/skill-dev/skill-engineering/` → `.claude/skills/skill-engineering/`

---

## Next Steps After Execution

1. **Test hook activation:** Run Claude Code and verify hooks trigger correctly
2. **Verify skill discovery:** Check that all skills load via `/kohaerenz-explorer` or skill list
3. **Implement Phase 1 hooks:** Start with `lint-and-validate`, `commit`, `git-pushing`
4. **Document changes:** Update CLAUDE.md if needed to reflect new structure
5. **Monitor performance:** Track hook execution times, ensure no slowdowns

