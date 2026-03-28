# Skill Refactoring TODO

This document outlines a plan to simplify and merge existing skills in `.claude/skills/` to eliminate overlap and create cohesive, modular agent tools.

## 🧠 Insights from the Example Refactoring (Skill Engineering)
During the refactoring of `skill-creator`, `writing-skills`, `skill-developer`, and `kaizen` into the unified `skill-engineering` skill, several key lessons emerged:
1. **The "Progressive Disclosure" Pattern is Essential:** Monolithic `SKILL.md` files over 500 lines confuse the agent. Instead, a central dispatcher `SKILL.md` should route to specific `references/` directories (e.g., templates, hooks, testing).
2. **Eliminate Concept Overlap:** `writing-skills` and `skill-developer` both contained templates and standards. By grouping them into `references/templates` and `references/standards` respectively, the AI has a single source of truth.
3. **Trigger Specificity:** Rely on clear `use when` statements and `triggers:` lists in the YAML frontmatter instead of generic descriptions.
4. **Action-Oriented Dispatching:** A skill shouldn't just be an encyclopedia. It should be an actionable decision tree (e.g., "If you are doing X, apply Y rules").

---

## 🏗️ Proposed Skill Clusters for Refactoring

### Cluster 1: Domain-Driven Design (DDD) & Event Sourcing Architecture
**Skills to Merge:**
- `domain-driven-design` (Audited)
- `ddd-strategic-design` (Audited)
- `ddd-tactical-patterns` (Audited)
- `ddd-context-mapping` (Audited)
- `event-sourcing-architect` (Audited)
- `event-store-design` (Audited)
- `cqrs-implementation` (Audited)
- `projection-patterns` (Audited)
- `saga-orchestration` (Audited)

**Refactoring Strategy:**
Create a unified **`architecture-ddd-event-sourcing`** skill. The root `SKILL.md` acts as an Architectural Decision Record (ADR) dispatcher. Break tactical implementations (CQRS, Sagas) and strategic modeling (Context Maps) into separate files under `references/architecture` and `references/patterns`.

### Cluster 2: Python Backend Mastery
**Skills to Merge:**
- `python-pro`
- `python-patterns`
- `async-python-patterns`
- `fastapi-pro`
- `fastapi-templates`
- `django-pro`

**Refactoring Strategy:**
Create a unified **`python-backend-engineering`** skill. Group by framework (`fastapi`, `django`) and core language features (`async`, `patterns`) under `references/`. This prevents conflict between standard Python rules and FastAPI specific async rules.

### Cluster 3: Testing & Debugging Ecosystem
**Skills to Merge:**
- `systematic-debugging`
- `test-fixing`
- `test-driven-development`
- `e2e-testing-patterns`
- `python-testing-patterns`
- `browser-automation`
- `lint-and-validate`
- `verification-before-completion`

**Refactoring Strategy:**
Create a unified **`quality-assurance-testing`** skill. The dispatcher routes based on the current phase: Are we writing tests (TDD)? Fixing broken tests? Debugging an unknown issue? Running E2E browser automation? Consolidating these ensures testing principles (like systematic isolation) are universally applied.

### Cluster 4: Git, PRs & Code Review
**Skills to Merge:**
- `git-advanced-workflows`
- `git-pushing`
- `commit`
- `changelog-automation`
- `create-pr`
- `requesting-code-review`
- `receiving-code-review`
- `code-review-checklist`

**Refactoring Strategy:**
Create a unified **`version-control-and-review`** skill. This tracks the entire lifecycle from local commit -> push -> PR creation -> code review -> changelog. Having this as a single progressive skill ensures the agent follows the complete pipeline without missing steps like conventional commits or PR templates.

### Cluster 5: Data & Vector Engineering
**Skills to Merge:**
- `data-engineer`
- `dbt-transformation-patterns`
- `airflow-dag-patterns`
- `vector-database-engineer`
- `embedding-strategies`

**Refactoring Strategy:**
Create a unified **`data-engineering-ai`** skill. Split the knowledge base into traditional ETL (dbt, Airflow) and Modern AI Data (Vector DBs, Embeddings) within the `references/` directory.

### Cluster 6: Documentation & Architecture Guidelines
**Skills to Merge:**
- `documentation-generation-doc-generate`
- `documentation-templates`
- `architecture-decision-records`
- `architecture-patterns` (Audited)
- `microservices-patterns`
- `backend-dev-guidelines`
- `senior-architect`
- `senior-fullstack`
- `api-patterns`

**Refactoring Strategy:**
Create a unified **`engineering-standards-docs`** skill. Since "senior-architect" and "senior-fullstack" are broad personas, they should be mapped to concrete API patterns, microservice strategies, and documentation generation workflows.

### Cluster 7: Specialized / Standalone Tasks
**Skills to KEEP or handle individually:**
- `frontend-developer` (Could be its own skill, or merged if backend/frontend become fullstack)
- `stripe-integration` (Too specific, keep as standalone reference)
- `concise-planning` (Keep as a meta-planning tool)
- `ab-test-setup` (Keep standalone)

---

## 🚀 Execution Steps
1. For each cluster, create a new directory (e.g., `skills/architecture-ddd-event-sourcing`).
2. Move all constituent `SKILL.md` files into the new directory's `references/` folder.
3. Write a new master `SKILL.md` that categorizes the tasks and provides a decision tree (referencing the moved files).
4. Update `metadata.triggers` to include keywords from all merged skills.
5. Remove the old, overlapping skill directories from `.claude/skills/`.
