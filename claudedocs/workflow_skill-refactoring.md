# Workflow Plan: Skill Refactoring
**Generated:** 2026-03-29
**Branch:** `claude/implement-skill-refactoring-UIiWv`
**Source docs:** `/refactor/` + `/docs/*skill*`
**Executor:** `/sc:implement`

---

## Summary

Consolidate 79 fragmented `.claude/skills/` directories into **6 unified macro-skill architects** following the Progressive Disclosure pattern, then add **hook automation** for the most impactful workflow guardrails.

**Current state:** 79 skill dirs, 83 settings.json entries, 3 hook scripts, no hook configs for commit/push/lint
**Target state:** 6 macro-skills + ~20 standalone skills, 6 hook scripts, full commit/push/lint automation

---

## Dependency Map

```
Phase 1 (Cleanup)
  └─► Phase 2 (Macro-Skill Creation)
        ├─► Phase 3a (Hook Scripts)
        └─► Phase 3b (settings.json Update)
              └─► Phase 4 (Old Skill Removal)
                    └─► Phase 5 (Commit & Push)
```

Each phase has a **checkpoint** — validate before proceeding.

---

## Phase 1 — Structural Cleanup

**Goal:** Remove duplicate planning artifacts at root level.

### Tasks

| # | Task | Command | Verification |
|---|------|---------|--------------|
| 1.1 | Remove root `skill-audit/` | `rm -rf skill-audit/` | `ls skill-audit/ 2>&1 \| grep "No such"` |
| 1.2 | Remove root `skill-compare/` | `rm -rf skill-compare/` | `ls skill-compare/ 2>&1 \| grep "No such"` |
| 1.3 | Verify `docs/skill-audit/` still intact | `ls docs/skill-audit/` | Returns `ecosystem-analysis.md` |
| 1.4 | Verify `docs/skill-compare/` still intact | `ls docs/skill-compare/` | Returns 6 `.md` files |

**Checkpoint 1:** `ls skill-audit/ skill-compare/ 2>&1` — both must return "No such file or directory"

---

## Phase 2 — Macro-Skill Creation

**Pattern for every macro-skill:**
```
.claude/skills/<macro-skill-name>/
├── SKILL.md              # Unified dispatcher: YAML frontmatter + decision tree
└── references/
    ├── <topic-a>.md      # Content migrated from constituent skill
    └── <topic-b>.md
```

**SKILL.md frontmatter template:**
```yaml
---
name: <macro-skill-name>
description: "<union of all merged skill trigger phrases>"
risk: safe
source: self
tags: "[<tag1>, <tag2>, ...]"
date_added: "2026-03-29"
---
```

---

### Task 2.1 — Create `architecture-ddd-event-sourcing`

**Merges:** `domain-driven-design`, `ddd-strategic-design`, `ddd-tactical-patterns`, `ddd-context-mapping`, `event-sourcing-architect`, `event-store-design`, `cqrs-implementation`, `projection-patterns`, `saga-orchestration`

**Steps:**
1. Create `.claude/skills/architecture-ddd-event-sourcing/`
2. Create `.claude/skills/architecture-ddd-event-sourcing/references/`
3. Write `SKILL.md` dispatcher with:
   - **Triggers:** DDD, domain model, bounded context, ubiquitous language, subdomain, context map, aggregate, domain event, anti-corruption layer, core domain, CQRS, event sourcing, event store, saga, orchestration, projection, read model, event-driven
   - **Decision tree:** Strategic? → `references/strategic-design.md` | Tactical? → `references/tactical-patterns.md` | Event infra? → `references/event-sourcing.md` | CQRS/Saga? → `references/cqrs-sagas.md`
4. Write `references/strategic-design.md` — content from `domain-driven-design`, `ddd-strategic-design`, `ddd-context-mapping`
5. Write `references/tactical-patterns.md` — content from `ddd-tactical-patterns`
6. Write `references/event-sourcing.md` — content from `event-sourcing-architect`, `event-store-design`
7. Write `references/cqrs-sagas.md` — content from `cqrs-implementation`, `projection-patterns`, `saga-orchestration`

**settings.json entry:**
```json
"architecture-ddd-event-sourcing": {
  "description": "Unified DDD + Event Sourcing architect: domain modeling, bounded contexts, CQRS, event stores, sagas, projections.",
  "path": "skills/architecture-ddd-event-sourcing/SKILL.md",
  "user_invocable": true
}
```

---

### Task 2.2 — Create `python-backend-engineering`

**Merges:** `python-pro`, `python-patterns`, `async-python-patterns`, `fastapi-pro`, `fastapi-templates`, `django-pro`

**Steps:**
1. Create `.claude/skills/python-backend-engineering/references/`
2. Write `SKILL.md` dispatcher with:
   - **Triggers:** Python, Python 3.12, FastAPI, Django, async, asyncio, pydantic, ruff, uv, endpoint, ORM, Celery, SQLAlchemy, Alembic, WSGI, ASGI, Uvicorn, Gunicorn
   - **Decision tree:** FastAPI project? → `references/fastapi.md` | Django project? → `references/django.md` | Core language? → `references/core-python.md` | Async patterns? → `references/async-patterns.md`
3. Write `references/core-python.md` — content from `python-pro`, `python-patterns`
4. Write `references/async-patterns.md` — content from `async-python-patterns`
5. Write `references/fastapi.md` — content from `fastapi-pro`, `fastapi-templates`
6. Write `references/django.md` — content from `django-pro`

**settings.json entry:**
```json
"python-backend-engineering": {
  "description": "Python 3.12+ backend mastery: core language, async patterns, FastAPI, Django, production tooling.",
  "path": "skills/python-backend-engineering/SKILL.md",
  "user_invocable": true
}
```

---

### Task 2.3 — Create `quality-assurance-testing`

**Merges:** `systematic-debugging`, `test-fixing`, `test-driven-development`, `e2e-testing-patterns`, `python-testing-patterns`, `browser-automation`, `lint-and-validate`, `verification-before-completion`

**Steps:**
1. Create `.claude/skills/quality-assurance-testing/references/`
2. Write `SKILL.md` dispatcher with:
   - **Triggers:** test, TDD, test-driven, bug, debug, debugging, root cause, lint, validate, ruff, eslint, E2E, end-to-end, browser automation, Playwright, Puppeteer, pytest, assertion, verification, done, complete, finished
   - **Decision tree:** Writing tests first? → `references/tdd.md` | Debugging unknown bug? → `references/debugging.md` | Fixing broken tests? → `references/test-fixing.md` | E2E/browser? → `references/e2e-browser.md` | Code quality check? → `references/lint-validate.md`
3. Write `references/tdd.md` — content from `test-driven-development`, `python-testing-patterns`
4. Write `references/debugging.md` — content from `systematic-debugging`
5. Write `references/test-fixing.md` — content from `test-fixing`
6. Write `references/e2e-browser.md` — content from `e2e-testing-patterns`, `browser-automation`
7. Write `references/lint-validate.md` — content from `lint-and-validate`, `verification-before-completion`

**settings.json entry:**
```json
"quality-assurance-testing": {
  "description": "Quality guardian: TDD, systematic debugging, test fixing, E2E automation, lint/validate, verification.",
  "path": "skills/quality-assurance-testing/SKILL.md",
  "user_invocable": true
}
```

---

### Task 2.4 — Create `version-control-and-review`

**Merges:** `git-advanced-workflows`, `git-pushing`, `commit`, `changelog-automation`, `create-pr`, `requesting-code-review`, `receiving-code-review`, `code-review-checklist`

**Steps:**
1. Create `.claude/skills/version-control-and-review/references/`
2. Write `SKILL.md` dispatcher with:
   - **Triggers:** commit, git commit, push, git push, save to github, pull request, PR, code review, review, changelog, release, branch, merge, rebase, conventional commit, semantic versioning
   - **Decision tree:** Committing? → `references/commit-workflow.md` | Creating PR? → `references/pr-creation.md` | Reviewing code? → `references/code-review.md` | Generating changelog? → `references/changelog.md`
3. Write `references/commit-workflow.md` — content from `commit`, `git-pushing`, `git-advanced-workflows`
4. Write `references/pr-creation.md` — content from `create-pr`, `requesting-code-review`
5. Write `references/code-review.md` — content from `receiving-code-review`, `code-review-checklist`
6. Write `references/changelog.md` — content from `changelog-automation`

**settings.json entry:**
```json
"version-control-and-review": {
  "description": "Full VCS lifecycle: conventional commits, git workflows, PR creation, code review, changelog automation.",
  "path": "skills/version-control-and-review/SKILL.md",
  "user_invocable": true
}
```

---

### Task 2.5 — Create `data-engineering-ai`

**Merges:** `data-engineer`, `dbt-transformation-patterns`, `airflow-dag-patterns`, `vector-database-engineer`, `embedding-strategies`

**Steps:**
1. Create `.claude/skills/data-engineering-ai/references/`
2. Write `SKILL.md` dispatcher with:
   - **Triggers:** data pipeline, ETL, ELT, dbt, Airflow, DAG, data warehouse, lakehouse, vector database, embeddings, Pinecone, Weaviate, Qdrant, Milvus, pgvector, Spark, Kafka, streaming, RAG
   - **Decision tree:** Traditional ETL/pipelines? → `references/etl-pipelines.md` | dbt/Airflow? → `references/dbt-airflow.md` | Vector DB/AI? → `references/vector-embeddings.md`
3. Write `references/etl-pipelines.md` — content from `data-engineer`
4. Write `references/dbt-airflow.md` — content from `dbt-transformation-patterns`, `airflow-dag-patterns`
5. Write `references/vector-embeddings.md` — content from `vector-database-engineer`, `embedding-strategies`

**settings.json entry:**
```json
"data-engineering-ai": {
  "description": "Data & AI engineering: ETL pipelines, dbt, Airflow, vector databases, embeddings, streaming.",
  "path": "skills/data-engineering-ai/SKILL.md",
  "user_invocable": true
}
```

---

### Task 2.6 — Create `engineering-standards-docs`

**Merges:** `documentation-generation-doc-generate`, `documentation-templates`, `architecture-decision-records`, `architecture-patterns`, `microservices-patterns`, `backend-dev-guidelines`, `senior-architect`, `senior-fullstack`, `api-patterns`

**Steps:**
1. Create `.claude/skills/engineering-standards-docs/references/`
2. Write `SKILL.md` dispatcher with:
   - **Triggers:** documentation, docs, README, ADR, architecture decision, API design, REST, GraphQL, tRPC, microservices, service mesh, event-driven architecture, backend guidelines, senior architect, senior fullstack, system design, scalability, Clean Architecture, Hexagonal
   - **Decision tree:** Writing docs? → `references/doc-generation.md` | Architecture decision? → `references/adr-patterns.md` | API/microservices design? → `references/api-microservices.md` | General best practices? → `references/senior-guidelines.md`
3. Write `references/doc-generation.md` — content from `documentation-generation-doc-generate`, `documentation-templates`
4. Write `references/adr-patterns.md` — content from `architecture-decision-records`
5. Write `references/api-microservices.md` — content from `api-patterns`, `microservices-patterns`, `architecture-patterns`
6. Write `references/senior-guidelines.md` — content from `backend-dev-guidelines`, `senior-architect`, `senior-fullstack`

**settings.json entry:**
```json
"engineering-standards-docs": {
  "description": "Engineering excellence: documentation generation, ADRs, API design, microservices, senior engineering standards.",
  "path": "skills/engineering-standards-docs/SKILL.md",
  "user_invocable": true
}
```

---

**Checkpoint 2:** For each macro-skill, verify:
```bash
test -f .claude/skills/<name>/SKILL.md && echo "SKILL.md ✓"
ls .claude/skills/<name>/references/ | wc -l  # must be >= 3
```

---

## Phase 3 — Hook Automation

### Task 3.1 — Create Hook Scripts

**Location:** `.claude/hooks/scripts/`
All scripts must be executable (`chmod +x`) and complete in < 2 seconds.

#### `lint-suggest.sh` — PreToolUse on Edit/Write
```bash
#!/usr/bin/env bash
# Non-blocking: outputs suggestion to stderr, always approves
# Triggers after any Edit or Write tool call
echo '{"decision":"approve","reason":"Run quality-assurance-testing after this change if modifying logic"}' >&2
exit 0
```

#### `commit-format-validate.sh` — PreToolUse on Bash matching `git commit`
```bash
#!/usr/bin/env bash
# Reads the git commit command from stdin JSON, validates conventional format
# Blocks commits on main/master without feature branch
INPUT=$(cat)
BRANCH=$(git branch --show-current 2>/dev/null)
if [[ "$BRANCH" == "main" || "$BRANCH" == "master" ]]; then
  echo '{"decision":"block","reason":"Cannot commit directly to main/master. Create a feature branch first using the version-control-and-review skill."}'
  exit 0
fi
# Extract commit message from command
CMD=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('input',{}).get('command',''))" 2>/dev/null)
if echo "$CMD" | grep -qE 'git commit'; then
  MSG=$(echo "$CMD" | grep -oP '(?<=-m )["\x27].*?["\x27]' | tr -d '"'"'" || true)
  if [[ -n "$MSG" ]] && ! echo "$MSG" | grep -qE '^(feat|fix|docs|refactor|test|chore|style|perf|ci|build|revert)(\(.+\))?: .+'; then
    echo '{"decision":"block","reason":"Commit message must follow conventional commits format: type(scope): description. Use the version-control-and-review skill."}'
    exit 0
  fi
fi
echo '{"decision":"approve"}'
exit 0
```

#### `pre-push-validate.sh` — PreToolUse on Bash matching `git push`
```bash
#!/usr/bin/env bash
# Non-blocking check: warns if there are uncommitted changes or lint is skipped
UNSTAGED=$(git diff --name-only 2>/dev/null | wc -l)
if [[ "$UNSTAGED" -gt 0 ]]; then
  echo '{"decision":"block","reason":"Unstaged changes detected. Stage all files before pushing."}'
  exit 0
fi
echo '{"decision":"approve"}'
exit 0
```

#### `tdd-guard.sh` — PreToolUse on Edit (code files)
```bash
#!/usr/bin/env bash
# Advisory only: suggests TDD when editing implementation files without test counterpart
INPUT=$(cat)
FILE=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('input',{}).get('file_path',''))" 2>/dev/null)
# Only check non-test Python files
if [[ "$FILE" == *.py ]] && [[ "$FILE" != *test* ]] && [[ "$FILE" != *_test* ]]; then
  BASENAME=$(basename "$FILE" .py)
  DIR=$(dirname "$FILE")
  if ! ls "$DIR/test_${BASENAME}.py" "$DIR/${BASENAME}_test.py" 2>/dev/null | grep -q .; then
    echo "Advisory: No test file found for ${BASENAME}.py — consider TDD approach (quality-assurance-testing)" >&2
  fi
fi
echo '{"decision":"approve"}'
exit 0
```

---

### Task 3.2 — Update `.claude/settings.json` Hooks Section

Add to the existing `"hooks"` object in settings.json:

```json
"PreToolUse": [
  {
    "matcher": "Write|Edit",
    "hooks": [
      {
        "type": "command",
        "command": ".claude/hooks/scripts/lint-suggest.sh",
        "statusMessage": "Suggesting lint check..."
      }
    ]
  },
  {
    "matcher": "Bash",
    "hooks": [
      {
        "type": "command",
        "command": ".claude/hooks/scripts/commit-format-validate.sh",
        "statusMessage": "Validating commit format..."
      },
      {
        "type": "command",
        "command": ".claude/hooks/scripts/pre-push-validate.sh",
        "statusMessage": "Checking push prerequisites..."
      },
      {
        "type": "command",
        "command": ".claude/hooks/scripts/tdd-guard.sh",
        "statusMessage": "TDD check..."
      }
    ]
  }
]
```

> **Note:** Merge with existing `PreToolUse` entries — do not replace the venv-activation hooks already present.

**Checkpoint 3:**
```bash
ls -la .claude/hooks/scripts/  # Must show 4 scripts
bash -n .claude/hooks/scripts/commit-format-validate.sh && echo "syntax ✓"
python3 -c "import json; json.load(open('.claude/settings.json'))" && echo "JSON valid ✓"
```

---

## Phase 4 — Settings.json Skill Updates

### Task 4.1 — Add New Macro-Skill Entries

Add the 6 new macro-skill entries (from Task 2.x blocks above) to the `"skills"` object.

### Task 4.2 — Remove Deprecated Skill Entries

Remove entries for all skills that were merged into macro-skills:

**Remove from settings.json (Cluster 1 — architecture-ddd-event-sourcing):**
- `domain-driven-design`, `ddd-strategic-design`, `ddd-tactical-patterns`, `ddd-context-mapping`
- `event-sourcing-architect`, `event-store-design`, `cqrs-implementation`, `projection-patterns`, `saga-orchestration`

**Remove from settings.json (Cluster 2 — python-backend-engineering):**
- `python-pro`, `python-patterns`, `async-python-patterns`, `fastapi-pro`, `fastapi-templates`, `django-pro`

**Remove from settings.json (Cluster 3 — quality-assurance-testing):**
- `systematic-debugging`, `test-fixing`, `test-driven-development`, `e2e-testing-patterns`
- `python-testing-patterns`, `browser-automation`, `lint-and-validate`, `verification-before-completion`

**Remove from settings.json (Cluster 4 — version-control-and-review):**
- `git-advanced-workflows`, `git-pushing`, `commit`, `changelog-automation`
- `create-pr`, `requesting-code-review`, `receiving-code-review`, `code-review-checklist`

**Remove from settings.json (Cluster 5 — data-engineering-ai):**
- `data-engineer`, `dbt-transformation-patterns`, `airflow-dag-patterns`, `vector-database-engineer`, `embedding-strategies`

**Remove from settings.json (Cluster 6 — engineering-standards-docs):**
- `documentation-generation-doc-generate`, `documentation-templates`, `architecture-decision-records`
- `architecture-patterns`, `microservices-patterns`, `backend-dev-guidelines`, `senior-architect`, `senior-fullstack`, `api-patterns`

### Standalone Skills — DO NOT TOUCH

These remain as-is in settings.json and `.claude/skills/`:
- `frontend-developer`, `stripe-integration`, `concise-planning`, `ab-test-setup`
- `kohaerenz-explorer`, `agent-rules`, `skill-engineering`, `skill-developer`, `skill-creator`
- `kaizen`, `database-design`, `evaluation`, `advanced-evaluation`
- All mnemonic/context/memory skills: `core`, `format`, `setup`, `blackboard`, `memory-systems`, `memory-integrator`, `context-compiler`, `context-compression`, `context-degradation`, `context-engineering-collection`, `context-fundamentals`, `context-optimization`, `bdi-mental-states`, `ontology`, `custodian`, `filesystem-context`, `prompt-architect`
- Agent/tool skills: `multi-agent-patterns`, `tool-design`, `hosted-agents`, `integrate`, `qmd-setup`, `qmd-reindex`, `search`
- `writing-skills` (standalone creative writing)

**Checkpoint 4:**
```bash
python3 -c "import json; j=json.load(open('.claude/settings.json')); print(len(j.get('skills',{})), 'skills')"
# Should show ~30 (was 83, removed ~45 merged entries, added 6 macro-skills)
python3 -c "import json; json.load(open('.claude/settings.json'))" && echo "JSON valid ✓"
```

---

## Phase 5 — Old Skill Directory Removal

After Phase 4 checkpoint passes:

### Task 5.1 — Remove Merged Skill Dirs

```bash
# Cluster 1
rm -rf .claude/skills/domain-driven-design
rm -rf .claude/skills/ddd-strategic-design
rm -rf .claude/skills/ddd-tactical-patterns
rm -rf .claude/skills/ddd-context-mapping
rm -rf .claude/skills/event-sourcing-architect
rm -rf .claude/skills/event-store-design
rm -rf .claude/skills/cqrs-implementation
rm -rf .claude/skills/projection-patterns
rm -rf .claude/skills/saga-orchestration

# Cluster 2
rm -rf .claude/skills/python-pro
rm -rf .claude/skills/python-patterns
rm -rf .claude/skills/async-python-patterns
rm -rf .claude/skills/fastapi-pro
rm -rf .claude/skills/fastapi-templates
rm -rf .claude/skills/django-pro

# Cluster 3
rm -rf .claude/skills/systematic-debugging
rm -rf .claude/skills/test-fixing
rm -rf .claude/skills/test-driven-development
rm -rf .claude/skills/e2e-testing-patterns
rm -rf .claude/skills/python-testing-patterns
rm -rf .claude/skills/browser-automation
rm -rf .claude/skills/lint-and-validate
rm -rf .claude/skills/verification-before-completion

# Cluster 4
rm -rf .claude/skills/git-advanced-workflows
rm -rf .claude/skills/git-pushing
rm -rf .claude/skills/commit
rm -rf .claude/skills/changelog-automation
rm -rf .claude/skills/create-pr
rm -rf .claude/skills/requesting-code-review
rm -rf .claude/skills/receiving-code-review
rm -rf .claude/skills/code-review-checklist

# Cluster 5
rm -rf .claude/skills/data-engineer
rm -rf .claude/skills/dbt-transformation-patterns
rm -rf .claude/skills/airflow-dag-patterns
rm -rf .claude/skills/vector-database-engineer
rm -rf .claude/skills/embedding-strategies

# Cluster 6
rm -rf .claude/skills/documentation-generation-doc-generate
rm -rf .claude/skills/documentation-templates
rm -rf .claude/skills/architecture-decision-records
rm -rf .claude/skills/architecture-patterns
rm -rf .claude/skills/microservices-patterns
rm -rf .claude/skills/backend-dev-guidelines
rm -rf .claude/skills/senior-architect
rm -rf .claude/skills/senior-fullstack
rm -rf .claude/skills/api-patterns
```

**Checkpoint 5:**
```bash
ls .claude/skills/ | wc -l   # Should be ~30 (6 macro + ~24 standalone)
# Verify all 6 macro-skills exist
for s in architecture-ddd-event-sourcing python-backend-engineering quality-assurance-testing version-control-and-review data-engineering-ai engineering-standards-docs; do
  test -d ".claude/skills/$s" && echo "✓ $s" || echo "✗ $s MISSING"
done
```

---

## Phase 6 — Commit & Push

```bash
git add .claude/skills/ .claude/settings.json .claude/hooks/scripts/ claudedocs/
git add -u  # Stage deletions of removed dirs

git commit -m "refactor: consolidate 79 skills into 6 macro-skill architects + hook automation

- Create 6 macro-skills with Progressive Disclosure pattern (SKILL.md + references/)
  - architecture-ddd-event-sourcing (merges 9 DDD/ES skills)
  - python-backend-engineering (merges 6 Python skills)
  - quality-assurance-testing (merges 8 testing/QA skills)
  - version-control-and-review (merges 8 git/PR/review skills)
  - data-engineering-ai (merges 5 data/vector skills)
  - engineering-standards-docs (merges 9 docs/arch skills)
- Add 4 hook scripts: lint-suggest, commit-format-validate, pre-push-validate, tdd-guard
- Update settings.json: 83 entries → ~30, add hook configs
- Remove root-level skill-audit/ and skill-compare/ (duplicates in docs/)
- Remove 45 merged skill directories"

git push -u origin claude/implement-skill-refactoring-UIiWv
```

---

## Final Acceptance Checklist

- [ ] `.claude/skills/` has exactly 6 macro-skill dirs + standalone dirs
- [ ] Each macro-skill: `SKILL.md` + `references/` with 3–4 files
- [ ] All 45 merged skill dirs removed
- [ ] `skill-audit/` and `skill-compare/` removed from root
- [ ] `.claude/hooks/scripts/` contains 4 scripts, all executable
- [ ] `settings.json` valid JSON, ~30 skill entries, hooks section updated
- [ ] `git log --oneline -1` shows conventional commit message
- [ ] Branch pushed: `claude/implement-skill-refactoring-UIiWv`

---

## Risk Register

| Risk | Mitigation |
|------|-----------|
| Skill content loss during migration | Read each source SKILL.md in full before writing references/ |
| settings.json JSON syntax error | Validate with `python3 -c "import json; json.load(...)"` after every edit |
| Hook script breaks existing venv hooks | Merge, don't replace, existing `PreToolUse` entries |
| commit-format-validate blocks valid commits | Test with `echo '{"input":{"command":"git commit -m \"feat: test\""}}' \| bash .claude/hooks/scripts/commit-format-validate.sh` |
| Phase 5 deletes wrong dirs | Run `ls .claude/skills/` diff before/after to verify counts |

---

*Next step: `/sc:implement` — execute this plan phase by phase*
