# Skills Hook Analysis & Automation Opportunities

## Context

This analysis identifies which Claude Code skills would benefit from hook integration to automate workflows, enforce guardrails, and improve developer experience. Hooks can trigger skill activation, validate outputs, enforce processes (like pre-commit validation), and create automated workflows.

## Skills Analysis: Hook Opportunities

### HIGH PRIORITY (Immediate Candidates for Hooks)

#### 1. **lint-and-validate**
- **Current**: Manual execution after code changes
- **Hook Opportunities**:
  - `PreToolUse` on Edit/Write: Auto-suggest lint after changes
  - `UserPromptSubmit`: Detect validation keywords, trigger linting
  - Pre-commit hook: Block commits with style violations
  - Pre-push hook: Final validation before remote push
- **Automatable Parts**: Auto-fix eligible issues (ESLint --fix, Ruff --fix)
- **Effort**: MEDIUM | **Impact**: HIGH

#### 2. **commit**
- **Current**: Manual format compliance, branch protection missing
- **Hook Opportunities**:
  - `PreToolUse` on Bash (git commit): Validate conventional format
  - Branch protection: Block commits on main/master
  - Post-commit: Auto-append Claude session footer
  - Intent detection: Suggest skill when "commit" mentioned
- **Automatable Parts**: Format validation, footer injection, issue reference extraction
- **Effort**: MEDIUM | **Impact**: HIGH

#### 3. **git-pushing**
- **Current**: Manual stage→commit→push workflow
- **Hook Opportunities**:
  - `UserPromptSubmit`: Trigger on "push", "save to github" keywords
  - `PostToolUse` on Edit: Suggest after significant changes
  - Pre-push hook: Block if tests failing locally
  - Chaining: Enforce lint-and-validate before push
- **Automatable Parts**: Lint check gate, test validation gate, upstream flag handling
- **Effort**: MEDIUM | **Impact**: HIGH

#### 4. **test-driven-development**
- **Current**: Manual discipline enforcement
- **Hook Opportunities**:
  - `PreToolUse` on Edit: Block code changes without corresponding test file
  - Post-test: Verify test failure before accepting implementation
  - Guardrail: Enforce test-first discipline with clear errors
  - Session tracking: Monitor TDD compliance rate
- **Automatable Parts**: Test existence validation, failure verification, compliance tracking
- **Effort**: MEDIUM | **Impact**: HIGH

---

### MEDIUM PRIORITY (Good Candidates with Moderate Effort)

#### 5. **test-fixing**
- **Current**: Manual test execution and error analysis
- **Hook Opportunities**:
  - `PostToolUse` on Bash (test run): Detect failures, trigger skill
  - Post-commit hook: Auto-detect broken tests
  - Pre-push hook: Block if test suite failing
  - CI integration: Trigger on remote test failures
- **Automatable Parts**: Error grouping, failure pattern detection, fix suggestion ordering
- **Effort**: HIGH | **Impact**: MEDIUM

#### 6. **changelog-automation**
- **Current**: Manual generation; playbook-driven approach
- **Hook Opportunities**:
  - Tag detection hook: Trigger on git tag creation
  - Pre-release hook: Generate changelog before version bump
  - GitHub Actions integration: Automated release workflow
  - Commit analysis: Detect when release should occur
- **Automatable Parts**: Changelog generation, semantic versioning, release notes, GitHub integration
- **Effort**: MEDIUM | **Impact**: MEDIUM

#### 7. **requesting-code-review**
- **Current**: Manual initiation, subagent dispatch
- **Hook Opportunities**:
  - `UserPromptSubmit`: Suggest after "completed", "done" phrases
  - Post-commit hook: Auto-suggest after feature commits
  - Task completion detection: Pattern matching on achievement statements
  - PR auto-creation: Generate PR from commit history
- **Automatable Parts**: Completion detection, PR description generation, SHA extraction
- **Effort**: HIGH | **Impact**: MEDIUM

#### 8. **git-advanced-workflows**
- **Current**: Reference/guidance skill, no automation
- **Hook Opportunities**:
  - `PreToolUse` on Bash (git commands): Validate command safety
  - Post-rebase hook: Verify history integrity
  - Conflict detection: Trigger with merge/rebase conflicts
  - Branch cleanup: Auto-suggest deletion of merged branches
- **Automatable Parts**: Destructive command validation, conflict detection, cleanup suggestions
- **Effort**: MEDIUM | **Impact**: MEDIUM

---

### MEDIUM-LOW PRIORITY (Moderate Value, Higher Effort)

#### 9. **verification-before-completion**
- **Current**: Manual assertion of completion
- **Hook Opportunities**:
  - `UserPromptSubmit`: Detect completion claims, verify with checklist
  - Session end: Final verification before session closes
  - Smart blocking: Require verification before allowing "done" claims
  - Evidence tracking: Collect test runs, linter passes as proof
- **Automatable Parts**: Completion claim detection, evidence validation, checklist generation
- **Effort**: HIGH | **Impact**: MEDIUM-LOW

#### 10. **systematic-debugging** + **test-driven-development**
- **Combined Hook**: Error-first guard
- **Hook Opportunities**:
  - `PostToolUse` on Edit: If test fails after change, suggest systematic-debugging
  - Chaining: TDD RED phase → systematic debugging workflow
  - Error categorization: Auto-classify errors for debugging approach
- **Automatable Parts**: Error classification, workflow routing, evidence collection
- **Effort**: HIGH | **Impact**: MEDIUM

#### 11. **lint-and-validate** + **test-fixing** + **commit**
- **Combined Hook**: Pre-commit validation chain
- **Hook Opportunities**:
  - Multi-step pre-commit: Lint → tests → format → commit
  - Blocking gates: Fail fast on lint/test issues
  - Auto-fix first: Try auto-fixes before blocking
  - Report summary: Show what was fixed/checked before commit
- **Automatable Parts**: Chain orchestration, gate enforcement, summary generation
- **Effort**: HIGH | **Impact**: HIGH (Cross-skill automation)

---

### LOW PRIORITY (Niche Use Cases, Higher Effort)

#### 12. **receiving-code-review**
- **Current**: Manual review processing
- **Hook Opportunities**:
  - Comment parsing: Extract feedback items automatically
  - Issue tracking: Create tasks from review feedback
  - Status updates: Acknowledge review comments
- **Automatable Parts**: Comment parsing, task creation, acknowledgments
- **Effort**: MEDIUM | **Impact**: LOW

#### 13. **architecture-decision-records**
- **Current**: Template-driven approach
- **Hook Opportunities**:
  - Major change detection: Suggest ADR creation on significant refactors
  - Template scaffolding: Auto-generate ADR structure
  - Link validation: Check ADR references in code comments
- **Automatable Parts**: ADR scaffolding, reference validation
- **Effort**: MEDIUM | **Impact**: LOW

#### 14. **changelog-automation** + **git-pushing**
- **Combined Hook**: Release automation chain
- **Hook Opportunities**:
  - Auto-release: Push main → bump version → generate changelog → create GitHub release
  - Semantic versioning: Auto-detect version bump from commits
  - Publish: Auto-create releases on version tags
- **Automatable Parts**: Version bumping, changelog generation, GitHub release creation
- **Effort**: HIGH | **Impact**: MEDIUM (for release automation)

---

### ARCHITECTURAL/INFRASTRUCTURE (System Skills)

#### 15. **skill-developer** / **skill-creator**
- **Current**: Manual skill creation and validation
- **Hook Opportunities**:
  - Skill linting: Validate SKILL.md format on save
  - Rule validation: Check skill-rules.json syntax
  - Coverage analysis: Detect untested trigger patterns
  - Performance monitoring: Track skill execution times
  - Documentation scaffolding: Auto-generate skill docs
- **Automatable Parts**: Format validation, rule syntax checking, performance monitoring
- **Effort**: MEDIUM | **Impact**: MEDIUM (Improves skill ecosystem)

#### 16. **documentation-generation** / **documentation-templates**
- **Current**: Manual documentation writing
- **Hook Opportunities**:
  - Doc scaffolding: Auto-generate doc structure from code
  - Link validation: Check documentation cross-references
  - Staleness detection: Warn when docs don't match code
  - API doc generation: Auto-extract from code/comments
- **Automatable Parts**: Scaffolding, validation, staleness detection
- **Effort**: HIGH | **Impact**: MEDIUM

---

## Hook Implementation Strategy

### Phase 1: Core Workflow Guards (HIGH Priority)
```yaml
PreToolUse on Bash(git commit):
  - Validate conventional commit format
  - Block commits on main/master
  - Suggest commit skill if message malformed

PreToolUse on Edit/Write:
  - Auto-suggest lint-and-validate on code changes
  - Check for test file before code edits (TDD guard)

PostToolUse on Bash(test):
  - Parse test output, detect failures
  - Trigger test-fixing if failures found

PreToolUse on Bash(git push):
  - Block if tests not passing
  - Block if lint issues remain
  - Require clean working directory
```

### Phase 2: Intent Detection (MEDIUM Priority)
```yaml
UserPromptSubmit patterns:
  - "completed" / "done" / "finished" → trigger requesting-code-review
  - "push" / "save to github" / "share" → trigger git-pushing
  - "commit" / "save changes" → trigger commit
  - "fix test" / "broken test" → trigger test-fixing
  - "test" / "verify" → trigger lint-and-validate

PreToolUse on Edit (batch detection):
  - After 5+ edits without commit → suggest commit skill
  - After commit without push → suggest git-pushing
```

### Phase 3: Cross-Skill Chains (HIGH Impact)
```yaml
edit_validate_commit_push_chain:
  Edit → lint-and-validate → test-tdd → commit → git-pushing → changelog

Pre-commit validation:
  - Lint check (auto-fix first)
  - Test suite validation
  - Format validation
  - Conventional commit format

Release automation:
  Tag creation → changelog-automation → git-pushing → GitHub release
```

---

## Skills Sorted by Hook Benefit

### By Impact/Effort Ratio (Best ROI)

1. **lint-and-validate** — HIGH impact, MEDIUM effort ✅
2. **commit** — HIGH impact, MEDIUM effort ✅
3. **git-pushing** — HIGH impact, MEDIUM effort ✅
4. **test-driven-development** — HIGH impact, MEDIUM effort ✅
5. **changelog-automation** — MEDIUM impact, MEDIUM effort ✅
6. **git-advanced-workflows** — MEDIUM impact, MEDIUM effort ✅
7. **test-fixing** — MEDIUM impact, HIGH effort (block on pre-push)
8. **requesting-code-review** — MEDIUM impact, HIGH effort (completion detection)
9. **skill-developer** — MEDIUM impact, MEDIUM effort (ecosystem health)
10. **receiving-code-review** — LOW impact, MEDIUM effort

### By Implementation Complexity

**Easiest** (Pure validation, no AI logic):
- commit (format validation)
- lint-and-validate (call existing scripts)
- test-driven-development (test file existence check)

**Moderate** (Pattern detection):
- git-pushing (compile error detection)
- test-fixing (error parsing)
- changelog-automation (commit analysis)

**Complex** (NLP/Intent understanding):
- requesting-code-review (task completion detection)
- verification-before-completion (completion claim parsing)
- git-advanced-workflows (conflict detection, workflow routing)

---

## Recommended Implementation Order

### Iteration 1 (Foundation)
- [ ] `lint-and-validate`: PreToolUse on Edit, PreToolUse on push
- [ ] `commit`: Branch protection, format validation
- [ ] `test-driven-development`: Test file existence guard

### Iteration 2 (Workflow Automation)
- [ ] `git-pushing`: Lint/test gates, auto-suggest on push intent
- [ ] `test-fixing`: Error detection on test runs
- [ ] Chaining: Edit → lint → test → commit → push

### Iteration 3 (Release & Review)
- [ ] `changelog-automation`: Tag detection, auto-generation
- [ ] `requesting-code-review`: Completion detection, PR auto-creation
- [ ] `git-advanced-workflows`: Destructive command validation

### Iteration 4 (Polish & Observability)
- [ ] `skill-developer`: Skill linting, performance monitoring
- [ ] `verification-before-completion`: Evidence tracking
- [ ] Session analytics: Hook execution tracking, success rates

---

## Critical Files to Modify

1. `.claude/hooks/` — Add new hooks for each phase
2. `.claude/settings.json` — Register hook configurations
3. Individual skill SKILL.md files — Document hook integration
4. Scripts in `.claude/hooks/scripts/` — Create hook helper scripts

---

## Current Project Structure Cleanup

### Tasks
- [x] Move `/refactor/SKILL_HOOKS_ANALYSIS.md` (this file)
- [x] Move `skill-refactor-todo.md` to `/refactor/`
- [ ] Delete `Plan.md` from root
- [ ] Delete `/docs/` folder (PDF backups, per CLAUDE.md)
- [ ] Move `.agents/skills/agent-rules/` to `.claude/skills/agent-rules/`
- [ ] Move `skills/skill-dev/skill-engineering/` to `.claude/skills/skill-engineering/`
- [ ] Update `.claude/settings.json` paths

### Current State
- `.agents/skills/agent-rules/` exists (needs moving to `.claude/skills/`)
- `.claude/skills/agent-rules/` is a symlink to `../../.agents/skills/agent-rules`
- `skills/skill-dev/skill-engineering/` exists (needs moving to `.claude/skills/`)
- `.claude/settings.json` has `"path": "skills/agent-rules"` (needs updating)
- `.claude/settings.json` has `"path": "skills/skill-developer/SKILL.md"` (needs checking)

---

## Verification Plan

After implementing hooks:

1. **Functional Testing**: Each hook triggers on expected events
2. **Integration Testing**: Chained workflows complete successfully
3. **Guardrail Testing**: Blockers prevent unwanted actions
4. **UX Testing**: Suggestions appear at right time, not intrusive
5. **Performance**: Hook execution doesn't cause slowdowns
6. **Fallback**: Manual skill invocation still works if hooks disabled

---

## Dependencies & Conflicts

- `commit` hook depends on `git-pushing` workflow (can't break convention)
- `test-tdd` and `lint-and-validate` should run together in chain
- `changelog-automation` depends on conventional commits (enforced by `commit`)
- `requesting-code-review` could conflict with manual PR creation

