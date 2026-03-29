# Overall Ecosystem Audit & Refactoring Strategy

## Overview
A total of 88 local AI skills were analyzed and categorized into 6 primary domains: Python, Architecture, Frontend, Testing Quality, Data, and Git Workflow.

## The "Unified Architect" Refactoring Plan

The current ecosystem suffers from extreme fragmentation. 88 isolated skills compete for the LLM's context window, leading to missed triggers and inconsistent quality.

The strategy is to combine these into **6 Core "Architect" Skills**. Each Architect will serve as the single entry point for its domain. It will analyze the user's request, perform context gathering, and delegate execution to specialized **Submodules**.

Below is the concrete Interaction Design, Submodule breakdown, and inspiration mapping for each new Architect.

---

### 1. Python Architect (`python-architect`)
**Interaction Design:**
Triggers on any backend, data engineering, or Python-specific task. It first detects the framework (Django vs. FastAPI) by scanning the `pyproject.toml` or `requirements.txt`. It then delegates API creation to the API Submodule and data tasks to the Data Engineering Submodule. It must hook into the `Testing Quality Architect` before finalizing any code.

**Submodules & Inspirations:**
- **Web Frameworks Submodule:** (Inspiration: `fastapi-pro`, `django-pro`, `fastapi-templates`, `senior-fullstack`)
- **Async & Performance Submodule:** (Inspiration: `async-python-patterns`, `python-patterns`, `python-pro`)
- **Integration & API Submodule:** (Inspiration: `api-patterns`, `integrate`, `stripe-integration`)
- **AI/LLM Engineering Submodule:** (Inspiration: `embedding-strategies`, `book-sft-pipeline`, `digital-brain-skill`)
- **Data Engineering Submodule:** (Inspiration: `data-engineer`, `ontology`, `event-store-design`)

### 2. Architecture Architect (`architecture-architect`)
**Interaction Design:**
Triggers on system design, planning, or refactoring tasks. It operates highly interactively. Instead of immediately writing code, it asks 2-3 targeted questions to determine boundaries (e.g., "Is this a new microservice or part of the monolith?"). It produces Machine-Readable Architectural Decision Records (ADRs) that other Architects must read.

**Submodules & Inspirations:**
- **Strategic Design Submodule:** (Inspiration: `ddd-strategic-design`, `domain-driven-design`, `ddd-context-mapping`)
- **Tactical Implementation Submodule:** (Inspiration: `ddd-tactical-patterns`, `architecture-patterns`, `cqrs-implementation`)
- **Microservices & Orchestration Submodule:** (Inspiration: `microservices-patterns`, `saga-orchestration`, `event-sourcing-architect`)
- **Decision & ADR Submodule:** (Inspiration: `architecture-decision-records`, `senior-architect`, `projection-patterns`)

### 3. Frontend Architect (`frontend-architect`)
**Interaction Design:**
Triggers on UI/UX, browser automation, or client-side logic. It enforces a strict separation of concerns (State vs. UI). It coordinates with the `Testing Quality Architect` for visual regression setups and interacts directly with browser automation tools to verify UI changes in real-time.

**Submodules & Inspirations:**
- **UI/Component Design Submodule:** (Inspiration: `frontend-developer`, `senior-fullstack`)
- **Browser Automation Submodule:** (Inspiration: `browser-automation`)

### 4. Testing Quality Architect (`testing-quality-architect`)
**Interaction Design:**
Acts as the ultimate gatekeeper. It is rarely invoked directly by the user; instead, it is an event-driven skill invoked by the `python-architect` or `frontend-architect` *after* they generate code. It strictly enforces TDD (if requested) and runs systematic debugging loops if the pre-commit checks fail.

**Submodules & Inspirations:**
- **Validation & Linting Submodule:** (Inspiration: `lint-and-validate`, `python-testing-patterns`)
- **Testing Patterns & Debugging Submodule:** (Inspiration: `systematic-debugging`, `test-driven-development`, `test-fixing`, `e2e-testing-patterns`)
- **Evaluation Submodule:** (Inspiration: `evaluation`, `advanced-evaluation`)

### 5. Git Workflow Architect (`git-workflow-architect`)
**Interaction Design:**
Triggers exclusively at the end of a task or during PR creation. It reads the generated ADRs from the `Architecture Architect` to write comprehensive, context-aware PR descriptions and changelogs. It enforces semantic versioning and commit message formats.

**Submodules & Inspirations:**
- **Version Control Submodule:** (Inspiration: `git-advanced-workflows`, `git-pushing`, `commit`)
- **Code Review & PR Submodule:** (Inspiration: `create-pr`, `changelog-automation`, `requesting-code-review`, `receiving-code-review`, `code-review-checklist`)

### 6. Agent Context & Meta Architect (`agent-context-architect`)
**Interaction Design:**
The autopoietic framework. It operates continuously in the background to manage the Memory Interchange Format (MIF Level 3). It monitors the "context degradation" of the LLM and dynamically recompiles system prompts. It enforces the bitemporal tracking of all architectural decisions.

**Submodules & Inspirations:**
- **Memory & Context Optimization Submodule:** (Inspiration: `memory-systems`, `context-optimization`, `context-compression`, `context-degradation`, `filesystem-context`)
- **Skill Engineering Submodule:** (Inspiration: `skill-engineering`, `skill-developer`, `skill-creator`, `tool-design`, `context-compiler`, `prompt-architect`)
- **Cognitive Architecture Submodule:** (Inspiration: `bdi-mental-states`, `blackboard`, `multi-agent-patterns`, `interleaved-thinking`, `core`, `kohaerenz-explorer`)
- **Project Governance Submodule:** (Inspiration: `setup`, `project-development`, `kaizen`, `concise-planning`, `verification-before-completion`)

---

## Unified Interaction Flow Example

1. **User:** "Add Stripe subscription billing to the FastAPI backend."
2. **`python-architect`** triggers. It reads `pyproject.toml` and confirms FastAPI.
3. **`python-architect`** queries **`architecture-architect`** for existing payment bounded contexts. An ADR is retrieved.
4. **`python-architect`** invokes its *Integration & API Submodule* (inspired by `stripe-integration`) to generate the webhook and checkout logic.
5. **`python-architect`** hands the code to **`testing-quality-architect`**, which uses its *Testing Patterns Submodule* to write Mocked Stripe tests.
6. Once tests pass, **`git-workflow-architect`** generates the semantic commit.
