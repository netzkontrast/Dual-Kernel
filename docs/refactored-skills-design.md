# Comprehensive Design Concept: The Refactored Skill Suite

## 1. Executive Summary

Following a deep ecosystem analysis of 88 local AI skills, it was determined that the current skill repository suffers from severe fragmentation, overlapping triggers, and inconsistent quality (many skills lacking error handling, dynamic scope, or security depth).

This design document outlines a **Unified Architect Model**. Rather than maintaining 88 discrete, microscopic skills, the ecosystem will be refactored into **Six Core Macro-Skills** (Architects) that internally delegate tasks to specialized sub-routines (ADRs or embedded logic).

## 2. The "Unified Architect" Architecture

### 2.1 Core Philosophy
- **Consolidation over Fragmentation:** Centralize capabilities by domain (e.g., Python, Frontend, Architecture).
- **Intelligent Delegation:** A single macro-skill acts as the "front door" for the user. It evaluates the context, decides the optimal approach (Decision Intelligence), and executes the specific sub-tasks seamlessly.
- **Unified Triggers:** Reduce the likelihood of AI agents missing a trigger by having one broad, robust trigger per domain, rather than 30+ highly specific ones that fight for attention in the context window.

### 2.2 Interaction Flow
1. **User Request:** User asks to "Build a new FastAPI endpoint."
2. **Domain Routing:** The `python-architect` skill triggers.
3. **Context Gathering:** `python-architect` reads the codebase and consults `architecture-architect` (if needed for CQRS/DDD patterns) and `testing-quality-skills` (to ensure test coverage).
4. **Execution & Sub-routines:** `python-architect` generates the code (utilizing internal logic from what used to be `fastapi-pro`, `async-python-patterns`, and `api-patterns`).
5. **Validation:** It automatically triggers `testing-quality-skills` to validate the output before presenting it to the user.

---

## 3. The Refactored Macro-Skills

### 3.1 `python-architect` (Consolidated from 37 skills)
**Scope:** The ultimate master skill for all Python development (Django, FastAPI, Data Engineering).
**Replaces:** `fastapi-pro`, `django-pro`, `async-python-patterns`, `python-patterns`, `python-pro`, `api-patterns`, `data-engineer`, etc.
**Key Features:**
- **Dynamic Framework Detection:** Detects if the project is Django or FastAPI and applies the correct routing and ORM patterns automatically.
- **Embedded Data Engineering:** Contains specialized sub-routines for ETLs, embeddings (`embedding-strategies`), and vector DBs.
- **Strict Quality Enforcement:** Interleaves type-checking and async pattern validation natively.

### 3.2 `architecture-architect` (Consolidated from 33 skills)
**Scope:** High-level system design, Domain-Driven Design (DDD), Event Sourcing, and CQRS.
**Replaces:** `ddd-strategic-design`, `ddd-tactical-patterns`, `cqrs-implementation`, `event-store-design`, `microservices-patterns`, `saga-orchestration`, `architecture-patterns`, etc.
**Key Features:**
- **Decision Trees:** Actively asks the user questions to decide whether a monolithic, microservices, or serverless approach is best.
- **ADR Generation:** Automatically documents architectural decisions in a standardized Machine-Readable ADR format.
- **Pattern Enforcement:** Ensures boundaries between bounded contexts are respected during code generation.

### 3.3 `frontend-architect` (Consolidated from 10 skills)
**Scope:** All UI/UX, browser automation, React/Vue patterns, and frontend state management.
**Replaces:** `frontend-developer`, `browser-automation`, and various other UI-focused skills.
**Key Features:**
- **Component Consistency:** Enforces strict component hierarchy and design token usage.
- **Automated Verification:** Integrates with Playwright/Puppeteer logic for visual regression testing during development.

### 3.4 `testing-quality-architect` (Consolidated from 5 skills)
**Scope:** The guardian of the codebase. Handles linting, validation, test-driven development (TDD), and systematic debugging.
**Replaces:** `lint-and-validate`, `systematic-debugging`, `test-driven-development`, `test-fixing`, `evaluation`.
**Key Features:**
- **Event-Driven Hooks:** Automatically triggers *after* the `python-architect` or `frontend-architect` completes a code change.
- **Failing First (TDD):** Can be invoked explicitly to write failing test cases based on ADR requirements before implementation begins.

### 3.5 `git-workflow-architect` (Consolidated from 2 skills)
**Scope:** Version control, PR generation, changelogs, and code review management.
**Replaces:** `git-advanced-workflows`, `changelog-automation`, `create-pr`, etc.
**Key Features:**
- **Semantic Commits:** Enforces semantic versioning and commit messages.
- **Automated Summaries:** Hooks into the LLM context to automatically generate robust PR descriptions based on the diff and ADRs.

### 3.6 `agent-context-architect` (Consolidated Context/Prompt/Memory Skills)
**Scope:** Manages the AI's internal state, memory systems (bitemporal tracking, procedural/episodic memory), and system prompts.
**Replaces:** `memory-systems`, `context-optimization`, `context-compiler`, `prompt-architect`, `bdi-mental-states`, `ontology`, etc.
**Key Features:**
- **The "Meta-Skill":** This skill governs how the agent thinks and learns. It strictly enforces the MIF Level 3 standard for all memory storage.
- **Continuous Learning:** Periodically compiles context engineering skills into denser system prompts to prevent context degradation.

---

## 4. Implementation Strategy

**Phase 1: Foundation (Weeks 1-2)**
- Build the `agent-context-architect` and `testing-quality-architect` first to ensure the base memory system and validation loops are robust.

**Phase 2: Core Engineering (Weeks 3-4)**
- Consolidate the massive Python and Architecture directories into `python-architect` and `architecture-architect`.
- Ensure cross-architect communication (e.g., Python skill querying the Architecture skill for DDD boundaries).

**Phase 3: Peripherals (Week 5)**
- Implement the `frontend-architect` and `git-workflow-architect`.

**Phase 4: Deprecation (Week 6)**
- Gradually remove the old 88 `.claude/skills` files as the new 6 Unified Architects prove stable.
