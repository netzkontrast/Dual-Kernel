# Refactor Folder

This folder contains planning and analysis documents for the Dual-Kernel project reorganization and skills hook automation initiative.

## Documents

### 1. **SKILL_HOOKS_ANALYSIS.md**
Comprehensive analysis of all 50+ Claude Code skills identifying which ones would benefit from hook integration. Includes:
- 16 skills analyzed by priority (HIGH/MEDIUM/MEDIUM-LOW/LOW)
- Hook opportunity identification for each skill
- Implementation strategy with 3-phase roadmap
- Cross-skill automation chains
- Hook implementation examples

**Key Finding**: 11 skills have repetitive manual workflows that could be automated with hooks, saving 5-15 minutes per session.

### 2. **EXECUTION_PLAN.md**
Step-by-step guide for reorganizing the project directory structure:
- Move `.agents/skills/agent-rules/` → `.claude/skills/agent-rules/`
- Move `skills/skill-dev/skill-engineering/` → `.claude/skills/skill-engineering/`
- Delete obsolete files (`Plan.md`, `/docs/`)
- Update `.claude/settings.json` paths
- Git commit and push strategy
- Rollback plan if issues occur

### 3. **skill-refactor-todo.md**
(Moved from root) High-level skill clustering and refactoring strategy proposing 7 major skill clusters to merge:
1. DDD & Event Sourcing Architecture
2. Python Backend Mastery
3. Testing & Debugging Ecosystem
4. Git, PRs & Code Review
5. Data & Vector Engineering
6. Documentation & Architecture Guidelines
7. Specialized / Standalone Tasks

## Usage

1. **First Time**: Read `SKILL_HOOKS_ANALYSIS.md` to understand hook opportunities
2. **Implementation**: Follow `EXECUTION_PLAN.md` for directory reorganization
3. **Future Work**: Use `skill-refactor-todo.md` to plan skill clustering/merging

## Current Status

- [x] Skill hook analysis completed
- [x] Planning documents created
- [x] skill-refactor-todo.md moved to refactor/
- [ ] Directory reorganization (ready for execution)
- [ ] Hook implementation (Phase 3, after reorganization)

## Branch

All work is on branch: `claude/analyze-skills-hooks-fPV32`

Ready to execute when confirmed by user.
