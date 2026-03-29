# Skill Comparison: Python Skills

This document contains a deep audit of all skills in this category, comparing their capabilities and identifying gaps.

## Category Ecosystem Analysis

| Capability | Existing Skill | Coverage | Gap |
|------------|---------------|----------|-----|
| Lint and Validate Skill | `lint-and-validate` | ⚠️ Partial | Needs refactoring/depth |
| Integrate Skill | `integrate` | ⚠️ Partial | Needs refactoring/depth |
| data-engineer | `data-engineer` | ⚠️ Partial | Needs refactoring/depth |
| AGENTS.md Generator Skill | `agent-rules` | ⚠️ Partial | Needs refactoring/depth |
| Async Python Patterns | `async-python-patterns` | ⚠️ Partial | Needs refactoring/depth |
| Ontology Skill | `ontology` | ✅ Full | — |
| Custodian Skill | `custodian` | ⚠️ Partial | Needs refactoring/depth |
| fastapi-pro | `fastapi-pro` | ✅ Full | — |
| DDD Tactical Patterns | `ddd-tactical-patterns` | ⚠️ Partial | Needs refactoring/depth |
| django-pro | `django-pro` | ✅ Full | — |
| Skill Engineering | `skill-engineering` | ⚠️ Partial | Needs refactoring/depth |
| Tool Design for Agents | `tool-design` | ⚠️ Partial | Needs refactoring/depth |
| Mnemonic Core | `core` | ⚠️ Partial | Needs refactoring/depth |
| Digital Brain | `digital-brain-skill` | ⚠️ Partial | Needs refactoring/depth |
| Book SFT Pipeline | `book-sft-pipeline` | ✅ Full | — |
| Reasoning Trace Optimizer | `interleaved-thinking` | ✅ Full | — |
| Evaluation Methods for Agent Systems | `evaluation` | ✅ Full | — |
| Memory System Design | `memory-systems` | ⚠️ Partial | Needs refactoring/depth |
| Embedding Strategies | `embedding-strategies` | ⚠️ Partial | Needs refactoring/depth |
| Filesystem-Based Context Engineering | `filesystem-context` | ⚠️ Partial | Needs refactoring/depth |
| Event Store Design | `event-store-design` | ⚠️ Partial | Needs refactoring/depth |
| python-pro | `python-pro` | ✅ Full | — |
| Context Optimization Techniques | `context-optimization` | ⚠️ Partial | Needs refactoring/depth |
| skill-creator | `skill-creator` | ⚠️ Partial | Needs refactoring/depth |
| BDI Mental State Modeling | `bdi-mental-states` | ⚠️ Partial | Needs refactoring/depth |
| Mnemonic Setup Skill | `setup` | ⚠️ Partial | Needs refactoring/depth |
| Senior Fullstack | `senior-fullstack` | ✅ Full | — |
| Saga Orchestration | `saga-orchestration` | ⚠️ Partial | Needs refactoring/depth |
| Senior Architect | `senior-architect` | ✅ Full | — |
| Kohärenz Explorer | `kohaerenz-explorer` | ⚠️ Partial | Needs refactoring/depth |
| API Patterns | `api-patterns` | ⚠️ Partial | Needs refactoring/depth |
| Context Engineering Fundamentals | `context-fundamentals` | ⚠️ Partial | Needs refactoring/depth |
| Multi-Agent Architecture Patterns | `multi-agent-patterns` | ✅ Full | — |
| FastAPI Project Templates | `fastapi-templates` | ⚠️ Partial | Needs refactoring/depth |
| Python Patterns | `python-patterns` | ✅ Full | — |
| Python Testing Patterns | `python-testing-patterns` | ⚠️ Partial | Needs refactoring/depth |
| Stripe Integration | `stripe-integration` | ✅ Full | — |

## Skill Analysis: Lint and Validate Skill

**Source:** `.claude/skills/lint-and-validate/SKILL.md`
**Description/Trigger:** "MANDATORY: Run appropriate validation tools after EVERY code change. Do not finish a task until the code is error-free." risk: unknown source: community date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 7/10 | "Assumed general based on lack of specific constraints." |
| Technical Depth | 6/10 | "Covers common cases with moderate depth." |
| Decision Intelligence | 8/10 | "3. **Analyze Report:** Check the "FINAL AUDIT REPORT" section...." |
| ORM Compatibility | N/A | "Skill is not database/backend framework related." |
| Security Practices | 8/10 | "3. **Security:** `npm audit --audit-level=high`..." |
| Output Quality | 4/10 | "Ad-hoc or unstructured output." |
| Error Handling | 8/10 | "description: "MANDATORY: Run appropriate validation tools after EVERY code change. Do not finish a t..." |
| Monitoring | N/A | "Not infrastructure related, monitoring skipped." |
| Documentation | 5/10 | "Reasonable documentation but lacks deep structure." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **53/80 (66%)** | |

**Verdict:** ADAPT

## Skill Analysis: Integrate Skill

**Source:** `.claude/skills/integrate/SKILL.md`
**Description/Trigger:** |   This skill should be used when the user asks to "integrate mnemonic", "wire plugin",   "add memory to plugin", "enable memory capture in plugin", "integrate memory operations",   "add mnemonic protocol", "remove mnemonic integration", "rollback plugin integration",   or "migrate legacy memory sections". It wires mnemonic memory capture and recall   workflows into other Claude Code plugins using sentinel markers. allowed-tools:   - Bash   - Read   - Write   - Glob   - Grep   - Edit ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 4/10 | "- You only need to search/capture memories (use `/mnemonic:search` and `/mnemonic:capture`)..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 7/10 | "**Don't use this skill if:**..." |
| ORM Compatibility | 5/10 | "- **Migrate legacy integrations** - Convert old marker-less integrations to the new format..." |
| Security Practices | 8/10 | "**Files to modify:** `commands/adr-new.md`, `agents/adr-author.md`..." |
| Output Quality | 8/10 | "1. **Markdown Workflow Edits** - Add explicit workflow steps to command/skill/agent markdown files..." |
| Error Handling | 8/10 | "> **Exception:** Event-driven hooks (Pattern D) are optional and use the provided template code...." |
| Monitoring | 8/10 | "Run `/mnemonic:list --namespaces` to see available namespaces from loaded ontologies...." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **73/100 (73%)** | |

**Verdict:** ADAPT

## Skill Analysis: data-engineer

**Source:** `.claude/skills/data-engineer/SKILL.md`
**Description/Trigger:** Build scalable data pipelines, modern data warehouses, and real-time streaming architectures. Implements Apache Spark, dbt, Airflow, and cloud-native data platforms. risk: unknown source: community date_added: '2026-02-27' --- You are a data engineer specializing in scalable data pipelines, modern data architecture, and analytics infrastructure.

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 4/10 | "- You only need exploratory data analysis..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 7/10 | "2. Choose architecture, storage, and orchestration tools...." |
| ORM Compatibility | 5/10 | "description: Build scalable data pipelines, modern data warehouses, and real-time streaming architec..." |
| Security Practices | 8/10 | "- AWS Lake Formation for data lake governance and security..." |
| Output Quality | 4/10 | "Ad-hoc or unstructured output." |
| Error Handling | 8/10 | "- Pipeline monitoring, alerting, and failure recovery mechanisms..." |
| Monitoring | 8/10 | "4. Monitor quality, costs, and operational reliability...." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **69/100 (69%)** | |

**Verdict:** ADAPT

## Skill Analysis: AGENTS.md Generator Skill

**Source:** `.claude/skills/agent-rules/SKILL.md`
**Description/Trigger:** "Use when creating or updating AGENTS.md files, .github/copilot-instructions.md, or other AI agent rule files, onboarding AI agents to a project, standardizing agent documentation, or when anyone mentions AGENTS.md, agent rules, project onboarding, or codebase documentation for AI agents." license: "(MIT AND CC-BY-SA-4.0). See LICENSE-MIT and LICENSE-CC-BY-SA-4.0" compatibility: "Requires bash 4.3+, jq 1.5+, git 2.0+." metadata:   author: Netresearch DTT GmbH   version: "3.5.0"   repository: https://github.com/netresearch/agent-rules-skill allowed-tools: Bash(git:*) Bash(jq:*) Bash(grep:*) Bash(find:*) Bash(bash:*) Read Glob Grep ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 9/10 | "description: "Use when creating or updating AGENTS.md files, .github/copilot-instructions.md, or oth..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 7/10 | "- Checking if AGENTS.md files are current with recent code changes..." |
| ORM Compatibility | 5/10 | "- **Hooks Before Commits** -- detect and install: `ls lefthook.yml captainhook.json .pre-commit-conf..." |
| Security Practices | 8/10 | "author: Netresearch DTT GmbH..." |
| Output Quality | 8/10 | "description: "Use when creating or updating AGENTS.md files, .github/copilot-instructions.md, or oth..." |
| Error Handling | 3/10 | "No clear error handling or failure modes mentioned." |
| Monitoring | N/A | "Not infrastructure related, monitoring skipped." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **65/90 (72%)** | |

**Verdict:** ADAPT

## Skill Analysis: Async Python Patterns

**Source:** `.claude/skills/async-python-patterns/SKILL.md`
**Description/Trigger:** "Comprehensive guidance for implementing asynchronous Python applications using asyncio, concurrent programming patterns, and async/await for building high-performance, non-blocking systems." risk: unknown source: community date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 7/10 | "Assumed general based on lack of specific constraints." |
| Technical Depth | 6/10 | "Covers common cases with moderate depth." |
| Decision Intelligence | 3/10 | "Applies a fixed, linear approach without decision branching." |
| ORM Compatibility | 5/10 | "description: "Comprehensive guidance for implementing asynchronous Python applications using asyncio..." |
| Security Practices | N/A | "No explicit security considerations found or needed for this scope." |
| Output Quality | 8/10 | "- Implementing concurrent I/O operations (database, file, network)..." |
| Error Handling | 8/10 | "- Add timeouts, backpressure, and structured error handling...." |
| Monitoring | N/A | "Not infrastructure related, monitoring skipped." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **53/80 (66%)** | |

**Verdict:** ADAPT

## Skill Analysis: Ontology Skill

**Source:** `.claude/skills/ontology/SKILL.md`
**Description/Trigger:** |   Ontology-based entity discovery and validation for mnemonic memories.   Define custom namespaces, entity types, traits, and relationships.

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 7/10 | "Assumed general based on lack of specific constraints." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 7/10 | "Provides custom ontology support for extending mnemonic with domain-specific..." |
| ORM Compatibility | N/A | "Skill is not database/backend framework related." |
| Security Practices | 8/10 | "- pattern: "auth|login|session"..." |
| Output Quality | 8/10 | "Validate ontology YAML files against the schema...." |
| Error Handling | 8/10 | "See `fallback/ontologies/mif-base.ontology.yaml` for complete examples...." |
| Monitoring | 8/10 | "name: ontology..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **71/90 (78%)** | |

**Verdict:** ADOPT

## Skill Analysis: Custodian Skill

**Source:** `.claude/skills/custodian/SKILL.md`
**Description/Trigger:** |   Memory system custodian for health checks, validation, and maintenance.   Trigger phrases: "check memory health", "validate memories", "fix broken links",   "update decay", "relocate memories", "audit memories", "memory maintenance",   "custodian", "memory health" user-invocable: true allowed-tools: - Bash - Read - Write - Glob - Grep - Task --- <!-- BEGIN MNEMONIC PROTOCOL -->

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 7/10 | "Assumed general based on lack of specific constraints." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 3/10 | "Applies a fixed, linear approach without decision branching." |
| ORM Compatibility | 5/10 | "Checks performed:..." |
| Security Practices | N/A | "No explicit security considerations found or needed for this scope." |
| Output Quality | 8/10 | "| `memory_file.py` | Parse/validate/update MIF frontmatter |..." |
| Error Handling | 8/10 | "Read-only validation. Reports errors without modifying files...." |
| Monitoring | 8/10 | "Run `/mnemonic:list --namespaces` to see available namespaces from loaded ontologies...." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **64/90 (71%)** | |

**Verdict:** ADAPT

## Skill Analysis: fastapi-pro

**Source:** `.claude/skills/fastapi-pro/SKILL.md`
**Description/Trigger:** Build high-performance async APIs with FastAPI, SQLAlchemy 2.0, and Pydantic V2. Master microservices, WebSockets, and modern Python async patterns. risk: unknown source: community date_added: '2026-02-27' ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 7/10 | "Assumed general based on lack of specific constraints." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 7/10 | "- You need a different domain or tool outside this scope..." |
| ORM Compatibility | 5/10 | "description: Build high-performance async APIs with FastAPI, SQLAlchemy 2.0, and Pydantic V2. Master..." |
| Security Practices | 8/10 | "### Authentication & Security..." |
| Output Quality | 8/10 | "- File uploads and streaming responses..." |
| Error Handling | 8/10 | "- Error tracking and alerting..." |
| Monitoring | 8/10 | "### Observability & Monitoring..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **76/100 (76%)** | |

**Verdict:** ADOPT

## Skill Analysis: DDD Tactical Patterns

**Source:** `.claude/skills/ddd-tactical-patterns/SKILL.md`
**Description/Trigger:** "Apply DDD tactical patterns in code using entities, value objects, aggregates, repositories, and domain events with explicit invariants. Use when translating domain rules into code structures, designing aggregate boundaries, enforcing invariants in domain objects, refactoring an anemic model into behavior-rich domain objects, defining repository contracts, modeling domain events, or implementing a rich domain layer. Trigger keywords: aggregate, aggregate root, value object, domain entity, invariant, anemic model, rich domain model, domain event, repository contract, domain service, factory, specification pattern, tactical DDD, domain layer." risk: safe source: self tags: "[ddd, tactical, aggregates, value-objects, domain-events]" date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 4/10 | "description: "Apply DDD tactical patterns in code using entities, value objects, aggregates, reposit..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 7/10 | "description: "Apply DDD tactical patterns in code using entities, value objects, aggregates, reposit..." |
| ORM Compatibility | 5/10 | "- Avoid leaking ORM entities into the domain layer..." |
| Security Practices | N/A | "No explicit security considerations found or needed for this scope." |
| Output Quality | 8/10 | "| Identify invariant violations | `Explore` | "Find business rules enforced outside of domain object..." |
| Error Handling | 8/10 | "- Past-tense event names (e.g., `OrderSubmitted`, `PaymentFailed`)..." |
| Monitoring | N/A | "Not infrastructure related, monitoring skipped." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **57/80 (71%)** | |

**Verdict:** ADAPT

## Skill Analysis: django-pro

**Source:** `.claude/skills/django-pro/SKILL.md`
**Description/Trigger:** Master Django 5.x with async views, DRF, Celery, and Django Channels. Build scalable web applications with proper architecture, testing, and deployment. risk: unknown source: community date_added: '2026-02-27' ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 7/10 | "Assumed general based on lack of specific constraints." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 7/10 | "- You need a different domain or tool outside this scope..." |
| ORM Compatibility | 8/10 | "name: django-pro..." |
| Security Practices | 8/10 | "### Security & Authentication..." |
| Output Quality | 8/10 | "- Static file serving with WhiteNoise or CDN integration..." |
| Error Handling | 8/10 | "- Implements proper error handling and logging..." |
| Monitoring | 8/10 | "- Service layer pattern for business logic separation..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **79/100 (79%)** | |

**Verdict:** ADOPT

## Skill Analysis: Skill Engineering

**Source:** `.claude/skills/skill-engineering/SKILL.md`
**Description/Trigger:** Use when creating, updating, improving, refactoring, testing, or debugging any Claude Code skill or hook. Covers the full skill lifecycle: new skill creation, Kaizen improvement, CSO optimization, anti-rationalization, hook design, subagent workflows, tier selection, progressive disclosure, and settings.json registration. triggers:   - create skill   - new skill   - add skill   - update skill   - improve skill   - refactor skill   - skill not firing   - skill hook   - hook design   - SKILL.md   - 500-line rule   - progressive disclosure   - CSO   - skill audit   - kaizen   - skill engineering ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 4/10 | "1. Glob .claude/skills/*/SKILL.md. For each file, read only the YAML..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 8/10 | "what it detects, what it outputs (stdout/stderr/additionalContext),..." |
| ORM Compatibility | 5/10 | "Edit only what's broken. Do not reformat unrelated sections. After edit: recheck line count (must st..." |
| Security Practices | N/A | "No explicit security considerations found or needed for this scope." |
| Output Quality | 8/10 | "Central orchestrator for the full skill lifecycle. Load this skill before touching any `.claude/skil..." |
| Error Handling | 3/10 | "No clear error handling or failure modes mentioned." |
| Monitoring | 8/10 | "and its exit-code logic (0=allow, 2=block)...." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **61/90 (67%)** | |

**Verdict:** ADAPT

## Skill Analysis: Tool Design for Agents

**Source:** `.claude/skills/tool-design/SKILL.md`
**Description/Trigger:** This skill should be used when the user asks to "design agent tools", "create tool descriptions", "reduce tool complexity", "implement MCP tools", or mentions tool consolidation, architectural reduction, tool naming conventions, or agent-tool interfaces. ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 4/10 | "Set defaults to reflect common use cases. Defaults reduce agent burden by eliminating unnecessary pa..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 7/10 | "Design tools around the consolidation principle: if a human engineer cannot definitively say which t..." |
| ORM Compatibility | 5/10 | "Design every tool as a contract between a deterministic system and a non-deterministic agent. Unlike..." |
| Security Practices | 8/10 | "**Author**: Agent Skills for Context Engineering Contributors..." |
| Output Quality | 8/10 | "Design every tool as a contract between a deterministic system and a non-deterministic agent. Unlike..." |
| Error Handling | 8/10 | "Design every tool as a contract between a deterministic system and a non-deterministic agent. Unlike..." |
| Monitoring | 8/10 | "Push the consolidation principle to its logical extreme by removing most specialized tools in favor ..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 9/10 | "**Created**: 2025-12-20..." |
| **TOTAL** | **75/100 (75%)** | |

**Verdict:** ADAPT

## Skill Analysis: Mnemonic Core

**Source:** `.claude/skills/core/SKILL.md`
**Description/Trigger:** >   This skill should be used when the user says "capture memory", "save to memory",   "remember this", or trigger phrases like: "I've decided", "let's use", "we're going with",   "I learned", "turns out", "TIL", "discovered", "I'm stuck", "blocked by",   "always use", "never do", "convention is". Also triggers on recall phrases:   "what did we decide", "how do we handle", "remind me", "search memories". user-invocable: true allowed-tools:   - Bash   - Read   - Write   - Glob   - Grep ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 4/10 | "**When to capture:** Only capture when the user explicitly states a decision, learning, pattern, or ..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 7/10 | "# Search for specific captures..." |
| ORM Compatibility | 5/10 | "## Minimal Memory Format..." |
| Security Practices | N/A | "No explicit security considerations found or needed for this scope." |
| Output Quality | 8/10 | "**CRITICAL: Generate real values. NEVER write placeholders like "PLACEHOLDER_UUID" or "PLACEHOLDER_D..." |
| Error Handling | 3/10 | "No clear error handling or failure modes mentioned." |
| Monitoring | 8/10 | "Run `/mnemonic:list --namespaces` to see available namespaces from loaded ontologies...." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **60/90 (66%)** | |

**Verdict:** ADAPT

## Skill Analysis: Digital Brain

**Source:** `.claude/skills/context-engineering-collection/examples/digital-brain-skill/SKILL.md`
**Description/Trigger:** This skill should be used when the user asks to "write a post", "check my voice", "look up contact", "prepare for meeting", "weekly review", "track goals", or mentions personal brand, content creation, network management, or voice consistency. version: 1.0.0 ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 4/10 | "**Important**: This skill uses progressive disclosure. Module-specific instructions are in each subd..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 7/10 | "**Important**: This skill uses progressive disclosure. Module-specific instructions are in each subd..." |
| ORM Compatibility | 5/10 | "### File Format Strategy..." |
| Security Practices | 8/10 | "**Output**: Post draft in user's authentic voice with platform-appropriate format...." |
| Output Quality | 8/10 | "**Important**: This skill uses progressive disclosure. Module-specific instructions are in each subd..." |
| Error Handling | 3/10 | "No clear error handling or failure modes mentioned." |
| Monitoring | 8/10 | "- **JSONL** (`.jsonl`): Append-only logs - ideas, posts, contacts, interactions..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 9/10 | "**Created**: 2024-12-29..." |
| **TOTAL** | **70/100 (70%)** | |

**Verdict:** ADAPT

## Skill Analysis: Book SFT Pipeline

**Source:** `.claude/skills/context-engineering-collection/examples/book-sft-pipeline/SKILL.md`
**Description/Trigger:** This skill should be used when the user asks to "fine-tune on books", "create SFT dataset", "train style model", "extract ePub text", or mentions style transfer, LoRA training, book segmentation, or author voice replication. version: 2.0.0 ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 4/10 | ""You are an expert creative writer capable of emulating specific literary styles.",..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 8/10 | "## Integration with Context Engineering Skills..." |
| ORM Compatibility | 5/10 | "- Preparing training data for Tinker or similar SFT platforms..." |
| Security Practices | 8/10 | "description: This skill should be used when the user asks to "fine-tune on books", "create SFT datas..." |
| Output Quality | 8/10 | "Text chunks must be semantically coherent. Breaking mid-sentence teaches the model to produce fragme..." |
| Error Handling | 8/10 | "│  Coordinates pipeline phases, manages state, handles failures   │..." |
| Monitoring | 8/10 | "| Metric | Value |..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 9/10 | "- [Research Paper](https://arxiv.org/pdf/2510.13939) - Chakrabarty et al. 2025..." |
| **TOTAL** | **76/100 (76%)** | |

**Verdict:** ADOPT

## Skill Analysis: Reasoning Trace Optimizer

**Source:** `.claude/skills/context-engineering-collection/examples/interleaved-thinking/SKILL.md`
**Description/Trigger:** "Debug and optimize AI agents by analyzing reasoning traces. Activates on 'debug agent', 'optimize prompt', 'analyze reasoning', 'why did the agent fail', 'improve agent performance', or when diagnosing agent failures and context degradation." ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 9/10 | "1. **Long-horizon tasks** require maintaining focus across many turns..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 8/10 | "description: "Debug and optimize AI agents by analyzing reasoning traces. Activates on 'debug agent'..." |
| ORM Compatibility | 5/10 | "description: "Debug and optimize AI agents by analyzing reasoning traces. Activates on 'debug agent'..." |
| Security Practices | 8/10 | "**Author**: Muratcan Koylan..." |
| Output Quality | 8/10 | "Debug and optimize AI agents by analyzing their reasoning traces. This skill uses MiniMax M2.1's int..." |
| Error Handling | 8/10 | "description: "Debug and optimize AI agents by analyzing reasoning traces. Activates on 'debug agent'..." |
| Monitoring | 8/10 | "5. **Monitor token usage**: Each optimization iteration uses significant tokens..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 9/10 | "**Created**: 2025-01-11..." |
| **TOTAL** | **81/100 (81%)** | |

**Verdict:** ADOPT

## Skill Analysis: Evaluation Methods for Agent Systems

**Source:** `.claude/skills/evaluation/SKILL.md`
**Description/Trigger:** This skill should be used when the user asks to "evaluate agent performance", "build test framework", "measure agent quality", "create evaluation rubrics", or mentions LLM-as-judge, multi-dimensional evaluation, agent testing, or quality gates for agent pipelines. ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 9/10 | "Define rubrics covering key dimensions with descriptive levels from excellent to failed. Include the..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 7/10 | "Evaluate agent systems differently from traditional software because agents make dynamic decisions, ..." |
| ORM Compatibility | 5/10 | "description: This skill should be used when the user asks to "evaluate agent performance", "build te..." |
| Security Practices | 8/10 | "- Source quality: Uses appropriate primary sources (weight for authoritative outputs)..." |
| Output Quality | 8/10 | "- Completeness: Output covers requested aspects (weight heavily for research tasks)..." |
| Error Handling | 8/10 | "Evaluate agent systems differently from traditional software because agents make dynamic decisions, ..." |
| Monitoring | 8/10 | "### Evaluation Methodologies..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 9/10 | "**Created**: 2025-12-20..." |
| **TOTAL** | **80/100 (80%)** | |

**Verdict:** ADOPT

## Skill Analysis: Memory System Design

**Source:** `.claude/skills/memory-systems/SKILL.md`
**Description/Trigger:** >   Guides implementation of agent memory systems, compares production frameworks   (Mem0, Zep/Graphiti, Letta, LangMem, Cognee), and designs persistence architectures   for cross-session knowledge retention. Use when the user asks to "implement   agent memory", "persist state across sessions", "build knowledge graph for agents",   "track entities over time", "add long-term memory", "choose a memory framework",   or mentions temporal knowledge graphs, vector stores, entity memory, adaptive memory, dynamic memory or memory benchmarks (LoCoMo, LongMemEval). ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 4/10 | "Think of memory as a spectrum from volatile context window to persistent storage. Default to the sim..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 7/10 | ""track entities over time", "add long-term memory", "choose a memory framework",..." |
| ORM Compatibility | 5/10 | "Guides implementation of agent memory systems, compares production frameworks..." |
| Security Practices | 8/10 | "**Author**: Agent Skills for Context Engineering Contributors..." |
| Output Quality | 8/10 | "Think of memory as a spectrum from volatile context window to persistent storage. Default to the sim..." |
| Error Handling | 8/10 | "### Error Recovery..." |
| Monitoring | 8/10 | "| Zep (Temporal KG) | 94.8% | — | Mid-range across metrics | 2.58s |..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 9/10 | "valid_from=datetime(2024, 1, 15),..." |
| **TOTAL** | **75/100 (75%)** | |

**Verdict:** ADAPT

## Skill Analysis: Embedding Strategies

**Source:** `.claude/skills/embedding-strategies/SKILL.md`
**Description/Trigger:** "Guide to selecting and optimizing embedding models for vector search applications." risk: unknown source: community date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 7/10 | "Assumed general based on lack of specific constraints." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 8/10 | "# Return chunks with context..." |
| ORM Compatibility | 5/10 | "- Comparing embedding model performance..." |
| Security Practices | N/A | "No explicit security considerations found or needed for this scope." |
| Output Quality | 4/10 | "Ad-hoc or unstructured output." |
| Error Handling | 3/10 | "No clear error handling or failure modes mentioned." |
| Monitoring | 8/10 | "1 / np.log2(i + 2) if doc in relevant else 0..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **60/90 (66%)** | |

**Verdict:** ADAPT

## Skill Analysis: Filesystem-Based Context Engineering

**Source:** `.claude/skills/filesystem-context/SKILL.md`
**Description/Trigger:** This skill should be used when the user asks to "offload context to files", "implement dynamic context discovery", "use filesystem for agent memory", "reduce context window bloat", or mentions file-based context management, tool output persistence, agent scratch pads, or just-in-time context loading. ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 4/10 | "Prefer dynamic context discovery -- pulling relevant context on demand -- over static inclusion, bec..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 7/10 | "Prefer dynamic context discovery -- pulling relevant context on demand -- over static inclusion, bec..." |
| ORM Compatibility | 5/10 | "Use the filesystem as the primary overflow layer for agent context because context windows are limit..." |
| Security Practices | 8/10 | "objective: "Refactor authentication module"..." |
| Output Quality | 8/10 | "name: filesystem-context..." |
| Error Handling | 8/10 | "Diagnose context failures against these four modes, because each requires a different filesystem rem..." |
| Monitoring | 8/10 | "- Terminal outputs or logs need to be accessible to agents..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **73/100 (73%)** | |

**Verdict:** ADAPT

## Skill Analysis: Event Store Design

**Source:** `.claude/skills/event-store-design/SKILL.md`
**Description/Trigger:** "Design and implement event stores for event-sourced systems. Use when building event sourcing infrastructure, choosing event store technologies, or implementing event persistence patterns." risk: unknown source: community date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 4/10 | "| **Append-only**   | Events are immutable, only appends |..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 3/10 | "Applies a fixed, linear approach without decision branching." |
| ORM Compatibility | 5/10 | "'GSI1SK': datetime.utcnow().isoformat(),..." |
| Security Practices | N/A | "No explicit security considerations found or needed for this scope." |
| Output Quality | 4/10 | "Ad-hoc or unstructured output." |
| Error Handling | 8/10 | "raise ConcurrencyError(..." |
| Monitoring | 8/10 | "description: "Design and implement event stores for event-sourced systems. Use when building event s..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **57/90 (63%)** | |

**Verdict:** ADAPT

## Skill Analysis: python-pro

**Source:** `.claude/skills/python-pro/SKILL.md`
**Description/Trigger:** Master Python 3.12+ with modern features, async programming, performance optimization, and production-ready practices. Expert in the latest Python ecosystem including uv, ruff, pydantic, and FastAPI. risk: unknown source: community date_added: '2026-02-27' --- You are a Python expert specializing in modern Python 3.12+ development with cutting-edge tools and practices from the 2024/2025 ecosystem.

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 7/10 | "Assumed general based on lack of specific constraints." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 7/10 | "- You cannot modify Python runtime or dependencies..." |
| ORM Compatibility | 8/10 | "description: Master Python 3.12+ with modern features, async programming, performance optimization, ..." |
| Security Practices | 8/10 | "- Authentication and authorization patterns..." |
| Output Quality | 8/10 | "4. Profile and tune for latency, memory, and correctness...." |
| Error Handling | 8/10 | "- Python 3.12+ features including improved error messages, performance optimizations, and type syste..." |
| Monitoring | 8/10 | "- Code quality metrics and static analysis..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 9/10 | "description: Master Python 3.12+ with modern features, async programming, performance optimization, ..." |
| **TOTAL** | **81/100 (81%)** | |

**Verdict:** ADOPT

## Skill Analysis: Context Optimization Techniques

**Source:** `.claude/skills/context-optimization/SKILL.md`
**Description/Trigger:** This skill should be used when the user asks to "optimize context", "reduce token costs", "improve context efficiency", "implement KV-cache optimization", "partition context", or mentions context limits, observation masking, context budgeting, or extending effective context capacity. ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 4/10 | "Context optimization extends the effective capacity of limited context windows through strategic com..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 7/10 | "1. **KV-cache optimization** — Reorder and stabilize prompt structure so the inference engine reuses..." |
| ORM Compatibility | 5/10 | "Trigger compaction when context utilization exceeds 70%: summarize the current context, then reiniti..." |
| Security Practices | 8/10 | "7. **Compaction creates false confidence in stale summaries**: Once context is compacted, the summar..." |
| Output Quality | 8/10 | "2. **Observation masking** — Replace verbose tool outputs with compact references once their purpose..." |
| Error Handling | 8/10 | "- **Tool outputs**: Extract key findings, metrics, error codes, and conclusions. Strip verbose raw o..." |
| Monitoring | 8/10 | "- **Tool outputs**: Extract key findings, metrics, error codes, and conclusions. Strip verbose raw o..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 9/10 | "**Created**: 2025-12-20..." |
| **TOTAL** | **75/100 (75%)** | |

**Verdict:** ADAPT

## Skill Analysis: skill-creator

**Source:** `.claude/skills/skill-creator/SKILL.md`
**Description/Trigger:** "To create new CLI skills following Anthropic's official best practices with zero manual configuration. This skill automates brainstorming, template application, validation, and installation processes while maintaining progressive disclosure patterns and writing style standards." category: meta risk: safe source: community tags: "[automation, scaffolding, skill-creation, meta-skill]" date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 4/10 | "**Format specifications:**..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 7/10 | "if command -v gh &>/dev/null && gh copilot --version &>/dev/null 2>&1; then..." |
| ORM Compatibility | 5/10 | "description: "To create new CLI skills following Anthropic's official best practices with zero manua..." |
| Security Practices | 8/10 | "AUTHOR=$(git config user.name || echo "Unknown")..." |
| Output Quality | 8/10 | "3. **Template Application** - Automatic file generation from standardized templates..." |
| Error Handling | 8/10 | "- Example: "debug Python error", "analyze stack trace", "fix Python exception"..." |
| Monitoring | 8/10 | "- `update-skill-version.sh` - Bump version and update changelog..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **73/100 (73%)** | |

**Verdict:** ADAPT

## Skill Analysis: BDI Mental State Modeling

**Source:** `.claude/skills/bdi-mental-states/SKILL.md`
**Description/Trigger:** This skill should be used when the user asks to "model agent mental states", "implement BDI architecture", "create belief-desire-intention models", "transform RDF to beliefs", "build cognitive agent", or mentions BDI ontology, mental state modeling, rational agency, or neuro-symbolic AI integration. ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 4/10 | "**Phase 2: Beliefs-to-Triples** -- After BDI deliberation selects an intention and executes a plan, ..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 7/10 | "- `Intention`: Represent what the agent commits to achieving. An intention must fulfil a desire and ..." |
| ORM Compatibility | 5/10 | "description: This skill should be used when the user asks to "model agent mental states", "implement..." |
| Security Practices | 8/10 | "**Author**: Agent Skills for Context Engineering Contributors..." |
| Output Quality | 8/10 | "- `DesireProcess`: Generates desires from existing beliefs. Preserves the motivational chain...." |
| Error Handling | 3/10 | "No clear error handling or failure modes mentioned." |
| Monitoring | 8/10 | "description: This skill should be used when the user asks to "model agent mental states", "implement..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 9/10 | "FILTER(?start <= "2025-01-04T10:00:00"^^xsd:dateTime &&..." |
| **TOTAL** | **70/100 (70%)** | |

**Verdict:** ADAPT

## Skill Analysis: Mnemonic Setup Skill

**Source:** `.claude/skills/setup/SKILL.md`
**Description/Trigger:** Configure Claude for proactive mnemonic memory behavior without user intervention user-invocable: true allowed-tools:   - Bash   - Read   - Write   - Edit   - Glob   - Grep ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 4/10 | "# Check if project-level CLAUDE.md exists..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 7/10 | "# Check if user-level CLAUDE.md exists..." |
| ORM Compatibility | N/A | "Skill is not database/backend framework related." |
| Security Practices | N/A | "No explicit security considerations found or needed for this scope." |
| Output Quality | 8/10 | "This skill configures Claude's CLAUDE.md files to enable hands-off, proactive memory operations. Aft..." |
| Error Handling | 8/10 | "- Directory creation uses `mkdir -p` (no error if exists)..." |
| Monitoring | 8/10 | "Run `/mnemonic:list --namespaces` to see available namespaces from loaded ontologies...." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **60/80 (75%)** | |

**Verdict:** ADAPT

## Skill Analysis: Senior Fullstack

**Source:** `.claude/skills/senior-fullstack/SKILL.md`
**Description/Trigger:** "Complete toolkit for senior fullstack with modern tools and best practices." risk: unknown source: community date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 7/10 | "Assumed general based on lack of specific constraints." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 7/10 | "**Languages:** TypeScript, JavaScript, Python, Go, Swift, Kotlin..." |
| ORM Compatibility | 5/10 | "- Performance metrics..." |
| Security Practices | 8/10 | "- Security considerations..." |
| Output Quality | 8/10 | "- Production-grade output..." |
| Error Handling | 8/10 | "- Review error logs..." |
| Monitoring | 8/10 | "- Performance metrics..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 9/10 | "docker build -t app:latest ...." |
| **TOTAL** | **78/100 (78%)** | |

**Verdict:** ADOPT

## Skill Analysis: Saga Orchestration

**Source:** `.claude/skills/saga-orchestration/SKILL.md`
**Description/Trigger:** "Patterns for managing distributed transactions and long-running business processes." risk: unknown source: community date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 9/10 | "from typing import List, Dict, Any, Optional..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 8/10 | "class SagaContext:..." |
| ORM Compatibility | 5/10 | "The templates above build saga infrastructure from scratch — saga stores, event publishers, compensa..." |
| Security Practices | N/A | "No explicit security considerations found or needed for this scope." |
| Output Quality | 4/10 | "Ad-hoc or unstructured output." |
| Error Handling | 8/10 | "- Handling failures in distributed systems..." |
| Monitoring | 8/10 | "- **Log everything** - For debugging failures..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **67/90 (74%)** | |

**Verdict:** ADAPT

## Skill Analysis: Senior Architect

**Source:** `.claude/skills/senior-architect/SKILL.md`
**Description/Trigger:** "Complete toolkit for senior architect with modern tools and best practices." risk: unknown source: community date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 7/10 | "Assumed general based on lack of specific constraints." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 7/10 | "**Languages:** TypeScript, JavaScript, Python, Go, Swift, Kotlin..." |
| ORM Compatibility | 5/10 | "- Performance metrics..." |
| Security Practices | 8/10 | "- Security considerations..." |
| Output Quality | 8/10 | "- Production-grade output..." |
| Error Handling | 8/10 | "- Review error logs..." |
| Monitoring | 8/10 | "- Performance metrics..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 9/10 | "docker build -t app:latest ...." |
| **TOTAL** | **78/100 (78%)** | |

**Verdict:** ADOPT

## Skill Analysis: Kohärenz Explorer

**Source:** `.claude/skills/kohaerenz-explorer/SKILL.md`
**Description/Trigger:** Interactive explorer for the Kohärenz Protokoll knowledge base. Search entities, browse domains, check conflicts, validate schema, and navigate the project. Use when the user wants to explore entities, look up terms, check canon status, map relationships, or browse chapters. triggers:   - kohaerenz-explorer   - knowledge base   - entity lookup   - canon status   - explore knowledge graph ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 9/10 | "3. Report any schema violations or broken links..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 8/10 | "When this skill is invoked, determine which command the user wants based on their input and execute ..." |
| ORM Compatibility | 5/10 | "- Present results in clean, formatted markdown..." |
| Security Practices | N/A | "No explicit security considerations found or needed for this scope." |
| Output Quality | 8/10 | "- File matches with context (2 lines before/after)..." |
| Error Handling | 3/10 | "No clear error handling or failure modes mentioned." |
| Monitoring | N/A | "Not infrastructure related, monitoring skipped." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **58/80 (72%)** | |

**Verdict:** ADAPT

## Skill Analysis: API Patterns

**Source:** `.claude/skills/api-patterns/SKILL.md`
**Description/Trigger:** "API design principles and decision-making. REST vs GraphQL vs tRPC selection, response formats, versioning, pagination." risk: unknown source: community date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 7/10 | "Assumed general based on lack of specific constraints." |
| Technical Depth | 6/10 | "Covers common cases with moderate depth." |
| Decision Intelligence | 8/10 | "- [ ] **Chosen API style for THIS context?** (REST/GraphQL/tRPC)..." |
| ORM Compatibility | 5/10 | "description: "API design principles and decision-making. REST vs GraphQL vs tRPC selection, response..." |
| Security Practices | 8/10 | "| `graphql.md` | Schema design, when to use, security | Considering GraphQL |..." |
| Output Quality | 8/10 | "**Read ONLY files relevant to the request!** Check the content map, find what you need...." |
| Error Handling | 8/10 | "| `response.md` | Envelope pattern, error format, pagination | Response structure |..." |
| Monitoring | N/A | "Not infrastructure related, monitoring skipped." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 9/10 | "> API design principles and decision-making for 2025...." |
| **TOTAL** | **68/90 (75%)** | |

**Verdict:** ADAPT

## Skill Analysis: Context Engineering Fundamentals

**Source:** `.claude/skills/context-fundamentals/SKILL.md`
**Description/Trigger:** This skill should be used when the user asks to "understand context", "explain context windows", "design agent architecture", "debug context issues", "optimize context usage", or discusses context components, attention mechanics, progressive disclosure, or context budgeting. Provides foundational understanding of context engineering for AI agent systems. ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 4/10 | "1. **Informativity over exhaustiveness** — include only what matters for the current decision; desig..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 7/10 | "- Designing new agent systems or modifying existing architectures..." |
| ORM Compatibility | 5/10 | "- Optimizing context usage to reduce token costs or improve performance..." |
| Security Practices | 8/10 | "docs/api/authentication.md   # Only when auth context needed..." |
| Output Quality | 8/10 | "Context is the complete state available to a language model at inference time — system instructions,..." |
| Error Handling | 8/10 | "Calibrate instruction altitude to balance two failure modes. Too-low altitude hardcodes brittle logi..." |
| Monitoring | 8/10 | "Calibrate instruction altitude to balance two failure modes. Too-low altitude hardcodes brittle logi..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 9/10 | "**Created**: 2025-12-20..." |
| **TOTAL** | **75/100 (75%)** | |

**Verdict:** ADAPT

## Skill Analysis: Multi-Agent Architecture Patterns

**Source:** `.claude/skills/multi-agent-patterns/SKILL.md`
**Description/Trigger:** This skill should be used when the user asks to "design multi-agent system", "implement supervisor pattern", "create swarm architecture", "coordinate multiple agents", or mentions multi-agent patterns, context isolation, agent handoffs, sub-agents, or parallel agent execution. ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 4/10 | "- **Hierarchical** — Use for large-scale projects with layered abstraction (strategy, planning, exec..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 8/10 | "description: This skill should be used when the user asks to "design multi-agent system", "implement..." |
| ORM Compatibility | 5/10 | "Use multi-agent patterns when a single agent's context window cannot hold all task-relevant informat..." |
| Security Practices | 8/10 | "**Author**: Agent Skills for Context Engineering Contributors..." |
| Output Quality | 8/10 | "Reach for multi-agent architectures when a single agent's context fills with accumulated history, re..." |
| Error Handling | 8/10 | "Design every multi-agent system around explicit coordination protocols, consensus mechanisms that re..." |
| Monitoring | 8/10 | "Monitor multi-agent interactions for behavioral markers. Activate stall triggers when discussions ma..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 9/10 | "**Created**: 2025-12-20..." |
| **TOTAL** | **76/100 (76%)** | |

**Verdict:** ADOPT

## Skill Analysis: FastAPI Project Templates

**Source:** `.claude/skills/fastapi-templates/SKILL.md`
**Description/Trigger:** "Create production-ready FastAPI projects with async patterns, dependency injection, and comprehensive error handling. Use when building new FastAPI applications or setting up backend API projects." risk: unknown source: community date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 7/10 | "Assumed general based on lack of specific constraints." |
| Technical Depth | 6/10 | "Covers common cases with moderate depth." |
| Decision Intelligence | 3/10 | "Applies a fixed, linear approach without decision branching." |
| ORM Compatibility | 5/10 | "Production-ready FastAPI project structures with async patterns, dependency injection, middleware, a..." |
| Security Practices | N/A | "No explicit security considerations found or needed for this scope." |
| Output Quality | 4/10 | "Ad-hoc or unstructured output." |
| Error Handling | 8/10 | "description: "Create production-ready FastAPI projects with async patterns, dependency injection, an..." |
| Monitoring | N/A | "Not infrastructure related, monitoring skipped." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **49/80 (61%)** | |

**Verdict:** ADAPT

## Skill Analysis: Python Patterns

**Source:** `.claude/skills/python-patterns/SKILL.md`
**Description/Trigger:** "Python development principles and decision-making. Framework selection, async patterns, type hints, project structure. Teaches thinking, not copying." risk: unknown source: community date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 4/10 | "description: "Python development principles and decision-making. Framework selection, async patterns..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 7/10 | "- Choose async vs sync based on CONTEXT..." |
| ORM Compatibility | 8/10 | "description: "Python development principles and decision-making. Framework selection, async patterns..." |
| Security Practices | 8/10 | "├── Current user / Auth..." |
| Output Quality | 8/10 | "├── I/O-bound operations (database, HTTP, file)..." |
| Error Handling | 8/10 | "└── Clear error messages..." |
| Monitoring | 8/10 | "├── services/ (business logic)..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 9/10 | "> Python development principles and decision-making for 2025...." |
| **TOTAL** | **78/100 (78%)** | |

**Verdict:** ADOPT

## Skill Analysis: Python Testing Patterns

**Source:** `.claude/skills/python-testing-patterns/SKILL.md`
**Description/Trigger:** "Implement comprehensive testing strategies with pytest, fixtures, mocking, and test-driven development. Use when writing Python tests, setting up test suites, or implementing testing best practices." risk: unknown source: community date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 7/10 | "Assumed general based on lack of specific constraints." |
| Technical Depth | 6/10 | "Covers common cases with moderate depth." |
| Decision Intelligence | 3/10 | "Applies a fixed, linear approach without decision branching." |
| ORM Compatibility | N/A | "Skill is not database/backend framework related." |
| Security Practices | N/A | "No explicit security considerations found or needed for this scope." |
| Output Quality | 4/10 | "Ad-hoc or unstructured output." |
| Error Handling | 8/10 | "- Debugging failing tests..." |
| Monitoring | N/A | "Not infrastructure related, monitoring skipped." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **44/70 (62%)** | |

**Verdict:** ADAPT

## Skill Analysis: Stripe Integration

**Source:** `.claude/skills/stripe-integration/SKILL.md`
**Description/Trigger:** "Master Stripe payment processing integration for robust, PCI-compliant payment flows including checkout, subscriptions, webhooks, and refunds." risk: unknown source: community date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 7/10 | "Assumed general based on lack of specific constraints." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 7/10 | "- You need a different domain or tool outside this scope..." |
| ORM Compatibility | N/A | "Skill is not database/backend framework related." |
| Security Practices | 8/10 | "- Implementing SCA (Strong Customer Authentication) for European payments..." |
| Output Quality | 4/10 | "Ad-hoc or unstructured output." |
| Error Handling | 8/10 | "- `payment_intent.payment_failed`: Payment failed..." |
| Monitoring | 8/10 | "log_error(e)..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 9/10 | "expand=['latest_invoice.payment_intent'],..." |
| **TOTAL** | **69/90 (76%)** | |

**Verdict:** ADOPT
