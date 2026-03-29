# Skill Comparison: Architecture Skills

This document contains a deep audit of all skills in this category, comparing their capabilities and identifying gaps.

## Category Ecosystem Analysis

| Capability | Existing Skill | Coverage | Gap |
|------------|---------------|----------|-----|
| Domain-Driven Design | `domain-driven-design` | ⚠️ Partial | Needs refactoring/depth |
| Mnemonic Search Skill | `search` | ⚠️ Partial | Needs refactoring/depth |
| Kaizen: Continuous Improvement | `kaizen` | ✅ Full | — |
| DDD Context Mapping | `ddd-context-mapping` | ✅ Full | — |
| Context Compiler — Autopoietischer Skill-Loop | `context-compiler` | ✅ Full | — |
| Projection Patterns | `projection-patterns` | ⚠️ Partial | Needs refactoring/depth |
| Changelog Automation | `changelog-automation` | ⚠️ Partial | Needs refactoring/depth |
| Context Compression Strategies | `context-compression` | ⚠️ Partial | Needs refactoring/depth |
| dbt Transformation Patterns | `dbt-transformation-patterns` | ⚠️ Partial | Needs refactoring/depth |
| Advanced Evaluation | `advanced-evaluation` | ⚠️ Partial | Needs refactoring/depth |
| DDD Strategic Design | `ddd-strategic-design` | ⚠️ Partial | Needs refactoring/depth |
| Test-Driven Development (TDD) | `test-driven-development` | ⚠️ Partial | Needs refactoring/depth |
| Verification Before Completion | `verification-before-completion` | ✅ Full | — |
| Agent Skills for Context Engineering | `context-engineering-collection` | ✅ Full | — |
| Comprehensive Research Agent Best Practices | `comprehensive-research-agent` | ⚠️ Partial | Needs refactoring/depth |
| Mnemonic Format Skill | `format` | ⚠️ Partial | Needs refactoring/depth |
| Sentry Commit Messages | `commit` | ⚠️ Partial | Needs refactoring/depth |
| Mnemonic Blackboard Skill | `blackboard` | ⚠️ Partial | Needs refactoring/depth |
| Apache Airflow DAG Patterns | `airflow-dag-patterns` | ⚠️ Partial | Needs refactoring/depth |
| CQRS Implementation | `cqrs-implementation` | ⚠️ Partial | Needs refactoring/depth |
| Writing Skills (Excellence) | `writing-skills` | ⚠️ Partial | Needs refactoring/depth |
| Vector Database Engineer | `vector-database-engineer` | ⚠️ Partial | Needs refactoring/depth |
| Test Fixing | `test-fixing` | ✅ Full | — |
| Database Design | `database-design` | ⚠️ Partial | Needs refactoring/depth |
| Automated Documentation Generation | `documentation-generation-doc-generate` | ⚠️ Partial | Needs refactoring/depth |
| Documentation Templates | `documentation-templates` | ✅ Full | — |
| Microservices Patterns | `microservices-patterns` | ⚠️ Partial | Needs refactoring/depth |
| Requesting Code Review | `requesting-code-review` | ⚠️ Partial | Needs refactoring/depth |
| Context Degradation Patterns | `context-degradation` | ⚠️ Partial | Needs refactoring/depth |
| Event Sourcing Architect | `event-sourcing-architect` | ⚠️ Partial | Needs refactoring/depth |
| Memory Integrator (Der Erinnerungs-Integrator) | `memory-integrator` | ⚠️ Partial | Needs refactoring/depth |
| Systematic Debugging | `systematic-debugging` | ✅ Full | — |
| Project Development Methodology | `project-development` | ⚠️ Partial | Needs refactoring/depth |

## Skill Analysis: Domain-Driven Design

**Source:** `.claude/skills/domain-driven-design/SKILL.md`
**Description/Trigger:** "Plan and route Domain-Driven Design work from strategic modeling to tactical implementation and evented architecture. Use when modeling a complex business domain, defining bounded contexts, splitting a monolith, aligning team ownership, evaluating whether DDD is worth the complexity, planning CQRS, event sourcing, sagas, or projections, or connecting strategic decisions to code-level patterns. Trigger keywords: DDD, domain model, bounded context, ubiquitous language, subdomain, context map, aggregate, domain event, anti-corruption layer, core domain, supporting domain, generic subdomain, domain-driven." risk: safe source: self tags: "[ddd, domain, bounded-context, architecture, routing]" date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 4/10 | "description: "Plan and route Domain-Driven Design work from strategic modeling to tactical implement..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 7/10 | "2. Produce strategic artifacts first: subdomains, bounded contexts, language glossary...." |
| ORM Compatibility | 5/10 | "Launch in background when the codebase scan is large — results inform the routing decision...." |
| Security Practices | N/A | "No explicit security considerations found or needed for this scope." |
| Output Quality | 8/10 | "## Output requirements..." |
| Error Handling | 3/10 | "No clear error handling or failure modes mentioned." |
| Monitoring | 8/10 | "6. Decision log (@architecture-decision-records)..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **60/90 (66%)** | |

**Verdict:** ADAPT

## Skill Analysis: Mnemonic Search Skill

**Source:** `.claude/skills/search/SKILL.md`
**Description/Trigger:** >   This skill should be used when the user says "search memories", "find in memories",   "grep mnemonic", "look for memory", "deep search", "synthesize knowledge", or asks   questions like "what do we know about X". Provides progressive disclosure and   enhanced iterative search with synthesis. name: search user-invocable: true --- <!-- BEGIN MNEMONIC PROTOCOL -->

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 7/10 | "Assumed general based on lack of specific constraints." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 7/10 | "Always start at Level 1. Expand only if needed...." |
| ORM Compatibility | 5/10 | "### Output Format..." |
| Security Practices | 8/10 | "rg -i '^title: ".*auth.*"' ${MNEMONIC_ROOT}/ --glob "*.memory.md" -l..." |
| Output Quality | 8/10 | "### Recent Files..." |
| Error Handling | 3/10 | "No clear error handling or failure modes mentioned." |
| Monitoring | 8/10 | "Run `/mnemonic:list --namespaces` to see available namespaces from loaded ontologies...." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **71/100 (71%)** | |

**Verdict:** ADAPT

## Skill Analysis: Kaizen: Continuous Improvement

**Source:** `.claude/skills/kaizen/SKILL.md`
**Description/Trigger:** "Guide for continuous improvement, error proofing, and standardization. Use this skill when the user wants to improve code quality, refactor, or discuss process improvements." risk: unknown source: community date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 9/10 | "**Core principle:** Many small improvements beat one big change. Prevent errors at design time, not ..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 7/10 | "- Verify each change before next..." |
| ORM Compatibility | 5/10 | "- Accept "good enough" performance..." |
| Security Practices | N/A | "No explicit security considerations found or needed for this scope." |
| Output Quality | 8/10 | "- Match existing file structure..." |
| Error Handling | 8/10 | "description: "Guide for continuous improvement, error proofing, and standardization. Use this skill ..." |
| Monitoring | 8/10 | "// Plus caching, plus logging, plus currency conversion......" |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **70/90 (77%)** | |

**Verdict:** ADOPT

## Skill Analysis: DDD Context Mapping

**Source:** `.claude/skills/ddd-context-mapping/SKILL.md`
**Description/Trigger:** "Map relationships between bounded contexts and define integration contracts using DDD context mapping patterns. Use when defining how services or contexts communicate, choosing between Partnership, Shared Kernel, Customer-Supplier, Conformist, or Anti-Corruption Layer patterns, preventing domain model leakage across service boundaries, planning ACL during monolith migration, clarifying upstream/downstream ownership, or designing integration contracts. Trigger keywords: context map, anti-corruption layer, ACL, upstream downstream, shared kernel, conformist, customer supplier, open host service, published language, integration contract, context integration, service boundary, domain leakage." risk: safe source: self tags: "[ddd, context-map, anti-corruption-layer, integration]" date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 9/10 | "| **Open Host Service** | Upstream publishes a stable protocol for many consumers | Upstream |..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 8/10 | "name: ddd-context-mapping..." |
| ORM Compatibility | 5/10 | "description: "Map relationships between bounded contexts and define integration contracts using DDD ..." |
| Security Practices | N/A | "No explicit security considerations found or needed for this scope." |
| Output Quality | 8/10 | "## Output requirements..." |
| Error Handling | 8/10 | "4. Add failure modes, fallback behavior, and versioning policy...." |
| Monitoring | 8/10 | "| Catalog | Search | Open Host Service | Catalog | No |..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **71/90 (78%)** | |

**Verdict:** ADOPT

## Skill Analysis: Context Compiler — Autopoietischer Skill-Loop

**Source:** `.claude/skills/context-compiler/SKILL.md`
**Description/Trigger:** >   Autopoietischer Skill-Loop. Kompiliert alle Context-Engineering-Skills zu einem   dynamischen, selbstverbessernden System-Prompt. 4 parallele Agenten (2 Explore,   1 Critique, 1 Judge) + dreistufiges MIF-Memory (Episodic/K0, Procedural/AEGIS,   Semantic/K1). Adversariales Lernen durch prompt-architect. Jeder Agent hat eine   eigene Seele (soul.md-Prinzip). Output: compiled-context.md + Memory-Update + Chat.   Inspiriert von Dual-Kernel-Ontologie: K0=Fragment, AEGIS=System, K1=Kohärenz. triggers:   - compile context   - context compiler   - /context-compiler   - kompiliere kontext   - autopoietischer loop   - context kompilieren   - build context ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 7/10 | "Assumed general based on lack of specific constraints." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 8/10 | "name: context-compiler..." |
| ORM Compatibility | 5/10 | "├── Explore-B  ─── Adversales Framework-Testing..." |
| Security Practices | 8/10 | "**Author**: Kohärenz Protokoll Contributors..." |
| Output Quality | 8/10 | "eigene Seele (soul.md-Prinzip). Output: compiled-context.md + Memory-Update + Chat...." |
| Error Handling | 8/10 | "- [`tool-design`](../tool-design/SKILL.md) — Consolidation-Prinzip, Error-Context, Token-Effizienz..." |
| Monitoring | 8/10 | "Inspiriert von Dual-Kernel-Ontologie: K0=Fragment, AEGIS=System, K1=Kohärenz...." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **77/100 (77%)** | |

**Verdict:** ADOPT

## Skill Analysis: Projection Patterns

**Source:** `.claude/skills/projection-patterns/SKILL.md`
**Description/Trigger:** "Build read models and projections from event streams. Use when implementing CQRS read sides, building materialized views, or optimizing query performance in event-sourced systems." risk: unknown source: community date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 7/10 | "Assumed general based on lack of specific constraints." |
| Technical Depth | 6/10 | "Covers common cases with moderate depth." |
| Decision Intelligence | 3/10 | "Applies a fixed, linear approach without decision branching." |
| ORM Compatibility | 5/10 | "description: "Build read models and projections from event streams. Use when implementing CQRS read ..." |
| Security Practices | N/A | "No explicit security considerations found or needed for this scope." |
| Output Quality | 4/10 | "Ad-hoc or unstructured output." |
| Error Handling | 3/10 | "No clear error handling or failure modes mentioned." |
| Monitoring | 8/10 | "- Implementing real-time dashboards..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **52/90 (57%)** | |

**Verdict:** ADAPT

## Skill Analysis: Changelog Automation

**Source:** `.claude/skills/changelog-automation/SKILL.md`
**Description/Trigger:** "Automate changelog generation from commits, PRs, and releases following Keep a Changelog format. Use when setting up release workflows, generating release notes, or standardizing commit conventions." risk: unknown source: community date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 7/10 | "Assumed general based on lack of specific constraints." |
| Technical Depth | 6/10 | "Covers common cases with moderate depth." |
| Decision Intelligence | 3/10 | "Applies a fixed, linear approach without decision branching." |
| ORM Compatibility | 5/10 | "description: "Automate changelog generation from commits, PRs, and releases following Keep a Changel..." |
| Security Practices | 8/10 | "- Avoid exposing secrets or internal-only details in release notes...." |
| Output Quality | 8/10 | "- Configure tooling to generate and publish notes...." |
| Error Handling | 3/10 | "No clear error handling or failure modes mentioned." |
| Monitoring | 8/10 | "name: changelog-automation..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **64/100 (64%)** | |

**Verdict:** ADAPT

## Skill Analysis: Context Compression Strategies

**Source:** `.claude/skills/context-compression/SKILL.md`
**Description/Trigger:** This skill should be used when the user asks to "compress context", "summarize conversation history", "implement compaction", "reduce token usage", or mentions context compression, structured summarization, tokens-per-task optimization, or long-running agent sessions exceeding context limits. ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 4/10 | "1. **Anchored Iterative Summarization**: Implement this for long-running sessions where file trackin..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 7/10 | "- Debugging cases where agents "forget" what files they modified..." |
| ORM Compatibility | 5/10 | "When agent sessions generate millions of tokens of conversation history, compression becomes mandato..." |
| Security Practices | 8/10 | "- auth.controller.ts: Fixed JWT token generation..." |
| Output Quality | 8/10 | "When agent sessions generate millions of tokens of conversation history, compression becomes mandato..." |
| Error Handling | 8/10 | "1. **Anchored Iterative Summarization**: Implement this for long-running sessions where file trackin..." |
| Monitoring | 8/10 | "- Retry logic with exponential backoff for transient failures..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 9/10 | "- Factory Research: Evaluating Context Compression for AI Agents (December 2025) - Read when: needin..." |
| **TOTAL** | **75/100 (75%)** | |

**Verdict:** ADAPT

## Skill Analysis: dbt Transformation Patterns

**Source:** `.claude/skills/dbt-transformation-patterns/SKILL.md`
**Description/Trigger:** "Production-ready patterns for dbt (data build tool) including model organization, testing strategies, documentation, and incremental processing." risk: unknown source: community date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 7/10 | "Assumed general based on lack of specific constraints." |
| Technical Depth | 6/10 | "Covers common cases with moderate depth." |
| Decision Intelligence | 3/10 | "Applies a fixed, linear approach without decision branching." |
| ORM Compatibility | 5/10 | "name: dbt-transformation-patterns..." |
| Security Practices | N/A | "No explicit security considerations found or needed for this scope." |
| Output Quality | 4/10 | "Ad-hoc or unstructured output." |
| Error Handling | 3/10 | "No clear error handling or failure modes mentioned." |
| Monitoring | N/A | "Not infrastructure related, monitoring skipped." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **44/80 (55%)** | |

**Verdict:** ADAPT

## Skill Analysis: Advanced Evaluation

**Source:** `.claude/skills/advanced-evaluation/SKILL.md`
**Description/Trigger:** This skill should be used when the user asks to "implement LLM-as-judge", "compare model outputs", "create evaluation rubrics", "mitigate evaluation bias", or mentions direct scoring, pairwise comparison, position bias, evaluation pipelines, or automated quality assessment. ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 4/10 | "**Verbosity Bias**: Excessive detail scores higher even when unnecessary. Mitigate with criteria-spe..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 7/10 | "**Key insight**: LLM-as-a-Judge is not a single technique but a family of approaches, each suited to..." |
| ORM Compatibility | 5/10 | "**Length Bias**: Longer responses score higher regardless of quality. Mitigate by explicitly prompti..." |
| Security Practices | 8/10 | "**Authority Bias**: Confident tone scores higher regardless of accuracy. Mitigate by requiring evide..." |
| Output Quality | 8/10 | "description: This skill should be used when the user asks to "implement LLM-as-judge", "compare mode..." |
| Error Handling | 8/10 | "| Binary classification (pass/fail) | Recall, Precision, F1 | Cohen's kappa |..." |
| Monitoring | 8/10 | "### Metric Selection Framework..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 9/10 | "**Created**: 2025-12-24..." |
| **TOTAL** | **75/100 (75%)** | |

**Verdict:** ADAPT

## Skill Analysis: DDD Strategic Design

**Source:** `.claude/skills/ddd-strategic-design/SKILL.md`
**Description/Trigger:** "Design DDD strategic artifacts including subdomains, bounded contexts, and ubiquitous language for complex business domains. Use when classifying subdomains as core/supporting/generic, splitting a monolith into services, aligning teams with domain ownership, building a shared ubiquitous language with domain experts, defining context boundaries, or producing a domain model for a new system. Trigger keywords: subdomain classification, bounded context, core domain, ubiquitous language, team ownership, context boundary, domain boundary, monolith splitting, domain model, strategic DDD." risk: safe source: self tags: "[ddd, strategic-design, bounded-context, ubiquitous-language]" date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 7/10 | "Assumed general based on lack of specific constraints." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 8/10 | "description: "Design DDD strategic artifacts including subdomains, bounded contexts, and ubiquitous ..." |
| ORM Compatibility | 5/10 | "| Identity | Supporting | Needed but not differentiating | Platform |..." |
| Security Practices | 8/10 | "| Checkout | Order placement and payment authorization | Catalog, Pricing | Fulfillment, Billing |..." |
| Output Quality | 8/10 | "Defines clear output artifacts." |
| Error Handling | 3/10 | "No clear error handling or failure modes mentioned." |
| Monitoring | 8/10 | "- Bounded context catalog..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **72/100 (72%)** | |

**Verdict:** ADAPT

## Skill Analysis: Test-Driven Development (TDD)

**Source:** `.claude/skills/test-driven-development/SKILL.md`
**Description/Trigger:** "Use when implementing any feature or bugfix, before writing implementation code" risk: unknown source: community date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 9/10 | "description: "Use when implementing any feature or bugfix, before writing implementation code"..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 3/10 | "Applies a fixed, linear approach without decision branching." |
| ORM Compatibility | 5/10 | "const result = await submitForm({ email: '' });..." |
| Security Practices | N/A | "No explicit security considerations found or needed for this scope." |
| Output Quality | 8/10 | "- Generated code..." |
| Error Handling | 8/10 | "Write the test first. Watch it fail. Write minimal code to pass...." |
| Monitoring | N/A | "Not infrastructure related, monitoring skipped." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **58/80 (72%)** | |

**Verdict:** ADAPT

## Skill Analysis: Verification Before Completion

**Source:** `.claude/skills/verification-before-completion/SKILL.md`
**Description/Trigger:** "Claiming work is complete without verification is dishonesty, not efficiency. Use when ANY variation of success/completion claims, ANY expression of satisfaction, or ANY positive statement about work state." risk: unknown source: community date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 9/10 | "description: "Claiming work is complete without verification is dishonesty, not efficiency. Use when..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 7/10 | "name: verification-before-completion..." |
| ORM Compatibility | N/A | "Skill is not database/backend framework related." |
| Security Practices | N/A | "No explicit security considerations found or needed for this scope." |
| Output Quality | 8/10 | "3. READ: Full output, check exit code, count failures..." |
| Error Handling | 8/10 | "3. READ: Full output, check exit code, count failures..." |
| Monitoring | 8/10 | "| Build succeeds | Build command: exit 0 | Linter passing, logs look good |..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **65/80 (81%)** | |

**Verdict:** ADOPT

## Skill Analysis: Agent Skills for Context Engineering

**Source:** `.claude/skills/context-engineering-collection/SKILL.md`
**Description/Trigger:** A comprehensive collection of Agent Skills for context engineering, multi-agent architectures, and production agent systems. Use when building, optimizing, or debugging agent systems that require effective context management. ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 4/10 | "Background coding agents run in remote sandboxed environments rather than on local machines. Key pat..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 8/10 | "name: context-engineering-collection..." |
| ORM Compatibility | 5/10 | "- Optimizing existing agent performance..." |
| Security Practices | 8/10 | "**Author**: Agent Skills for Context Engineering Contributors..." |
| Output Quality | 8/10 | "Context is not just prompt text—it is the complete state available to the language model at inferenc..." |
| Error Handling | 8/10 | "- Debugging context-related failures..." |
| Monitoring | 8/10 | "### Development Methodology..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 9/10 | "**Created**: 2025-12-20..." |
| **TOTAL** | **76/100 (76%)** | |

**Verdict:** ADOPT

## Skill Analysis: Comprehensive Research Agent Best Practices

**Source:** `.claude/skills/context-engineering-collection/examples/interleaved-thinking/generated_skills/comprehensive-research-agent/SKILL.md`
**Description/Trigger:** "Ensure thorough validation, error recovery, and transparent reasoning in research tasks with multiple tool calls" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 4/10 | "- *Vague Completion Claims**: Agent declares 'I have enough information' or 'research is comprehensi..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 7/10 | "This skill addresses common failures in multi-step research tasks: unhandled tool errors, missing va..." |
| ORM Compatibility | 5/10 | "- Task requires gathering information from multiple sources..." |
| Security Practices | 8/10 | "- *Implement Pre-Reading Source Evaluation**: Before reading URLs, rank search results by relevance,..." |
| Output Quality | 8/10 | "- Task includes file operations that need validation (save, write, read)..." |
| Error Handling | 8/10 | "description: "Ensure thorough validation, error recovery, and transparent reasoning in research task..." |
| Monitoring | 8/10 | "- *Silent Tool Failure**: A tool call returns an error (404, timeout, invalid URL) but the agent pro..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 9/10 | "**After (Pattern)**: 'Search returned 15 results on context engineering. Evaluating relevance: Liu e..." |
| **TOTAL** | **75/100 (75%)** | |

**Verdict:** ADAPT

## Skill Analysis: Mnemonic Format Skill

**Source:** `.claude/skills/format/SKILL.md`
**Description/Trigger:** MIF Level 3 specification, memory templates, and formatting guidelines name: format user-invocable: true --- <!-- BEGIN MNEMONIC PROTOCOL -->

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 4/10 | "description: MIF Level 3 specification, memory templates, and formatting guidelines..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 7/10 | "description: MIF Level 3 specification, memory templates, and formatting guidelines..." |
| ORM Compatibility | 5/10 | "description: MIF Level 3 specification, memory templates, and formatting guidelines..." |
| Security Practices | 8/10 | "- file: src/auth/handler.ts..." |
| Output Quality | 8/10 | "## File Naming..." |
| Error Handling | 3/10 | "No clear error handling or failure modes mentioned." |
| Monitoring | 8/10 | "Run `/mnemonic:list --namespaces` to see available namespaces from loaded ontologies...." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **68/100 (68%)** | |

**Verdict:** ADAPT

## Skill Analysis: Sentry Commit Messages

**Source:** `.claude/skills/commit/SKILL.md`
**Description/Trigger:** ALWAYS use this skill when committing code changes — never commit directly without it. Creates commits following Sentry conventions with proper conventional commit format and issue references. Trigger on any commit, git commit, save changes, or commit message task. risk: unknown source: community ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 9/10 | "description: ALWAYS use this skill when committing code changes — never commit directly without it. ..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 3/10 | "Applies a fixed, linear approach without decision branching." |
| ORM Compatibility | 5/10 | "description: ALWAYS use this skill when committing code changes — never commit directly without it. ..." |
| Security Practices | 8/10 | "When changes were primarily generated by a coding agent (like Claude Code), include the Co-Authored-..." |
| Output Quality | 4/10 | "Ad-hoc or unstructured output." |
| Error Handling | 3/10 | "No clear error handling or failure modes mentioned." |
| Monitoring | 8/10 | "| `style` | Code formatting (no logic change) |..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **65/100 (65%)** | |

**Verdict:** ADAPT

## Skill Analysis: Mnemonic Blackboard Skill

**Source:** `.claude/skills/blackboard/SKILL.md`
**Description/Trigger:** Cross-session handoff, persistent context via blackboard, and agent coordination patterns user-invocable: true allowed-tools:   - Bash   - Read   - Write   - Glob   - Grep ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 7/10 | "Assumed general based on lack of specific constraints." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 8/10 | "description: Cross-session handoff, persistent context via blackboard, and agent coordination patter..." |
| ORM Compatibility | 5/10 | "### Handoff Format..." |
| Security Practices | N/A | "No explicit security considerations found or needed for this scope." |
| Output Quality | 8/10 | "| **Persistent knowledge** | Mnemonic memories | `*.memory.md` files |..." |
| Error Handling | 3/10 | "No clear error handling or failure modes mentioned." |
| Monitoring | 8/10 | "Run `/mnemonic:list --namespaces` to see available namespaces from loaded ontologies...." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 9/10 | "| **Cross-session** | Mnemonic blackboard handoff | `handoff/latest-handoff.md` via hooks |..." |
| **TOTAL** | **66/90 (73%)** | |

**Verdict:** ADAPT

## Skill Analysis: Apache Airflow DAG Patterns

**Source:** `.claude/skills/airflow-dag-patterns/SKILL.md`
**Description/Trigger:** "Build production Apache Airflow DAGs with best practices for operators, sensors, testing, and deployment. Use when creating data pipelines, orchestrating workflows, or scheduling batch jobs." risk: unknown source: community date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 7/10 | "Assumed general based on lack of specific constraints." |
| Technical Depth | 6/10 | "Covers common cases with moderate depth." |
| Decision Intelligence | 3/10 | "Applies a fixed, linear approach without decision branching." |
| ORM Compatibility | N/A | "Skill is not database/backend framework related." |
| Security Practices | N/A | "No explicit security considerations found or needed for this scope." |
| Output Quality | 4/10 | "Ad-hoc or unstructured output." |
| Error Handling | 8/10 | "- Debugging failed DAG runs..." |
| Monitoring | 8/10 | "3. Implement DAGs with observability and alerting hooks...." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **52/80 (65%)** | |

**Verdict:** ADAPT

## Skill Analysis: CQRS Implementation

**Source:** `.claude/skills/cqrs-implementation/SKILL.md`
**Description/Trigger:** "Implement Command Query Responsibility Segregation for scalable architectures. Use when separating read and write models, optimizing query performance, or building event-sourced systems." risk: unknown source: community date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 7/10 | "Assumed general based on lack of specific constraints." |
| Technical Depth | 6/10 | "Covers common cases with moderate depth." |
| Decision Intelligence | 3/10 | "Applies a fixed, linear approach without decision branching." |
| ORM Compatibility | 5/10 | "description: "Implement Command Query Responsibility Segregation for scalable architectures. Use whe..." |
| Security Practices | N/A | "No explicit security considerations found or needed for this scope." |
| Output Quality | 4/10 | "Ad-hoc or unstructured output." |
| Error Handling | 8/10 | "- Validate performance, recovery, and failure modes...." |
| Monitoring | N/A | "Not infrastructure related, monitoring skipped." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **49/80 (61%)** | |

**Verdict:** ADAPT

## Skill Analysis: Writing Skills (Excellence)

**Source:** `.claude/skills/writing-skills/SKILL.md`
**Description/Trigger:** "Use when creating, updating, or improving agent skills." category: meta risk: unknown source: community date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 4/10 | "description: Use when [specific symptom occurs]...." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 3/10 | "Applies a fixed, linear approach without decision branching." |
| ORM Compatibility | 5/10 | "- Is it a massive platform (10+ products, AWS, Convex)? → [Tier 3 Architecture](references/tier-3-pl..." |
| Security Practices | N/A | "No explicit security considerations found or needed for this scope." |
| Output Quality | 8/10 | "- Is it simple (single file, <200 lines)? → [Tier 1 Architecture](references/tier-1-simple/README.md..." |
| Error Handling | 8/10 | "triggers: error-text, symptom, tool-name..." |
| Monitoring | N/A | "Not infrastructure related, monitoring skipped." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **53/80 (66%)** | |

**Verdict:** ADAPT

## Skill Analysis: Vector Database Engineer

**Source:** `.claude/skills/vector-database-engineer/SKILL.md`
**Description/Trigger:** "Expert in vector databases, embedding strategies, and semantic search implementation. Masters Pinecone, Weaviate, Qdrant, Milvus, and pgvector for RAG applications, recommendation systems, and similar" risk: unknown source: community date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 7/10 | "Assumed general based on lack of specific constraints." |
| Technical Depth | 6/10 | "Covers common cases with moderate depth." |
| Decision Intelligence | 8/10 | "1. Analyze data characteristics and query patterns..." |
| ORM Compatibility | 5/10 | "- Performance tuning and scaling..." |
| Security Practices | N/A | "No explicit security considerations found or needed for this scope." |
| Output Quality | 4/10 | "Ad-hoc or unstructured output." |
| Error Handling | 3/10 | "No clear error handling or failure modes mentioned." |
| Monitoring | 8/10 | "8. Set up monitoring and reindexing strategies..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **57/90 (63%)** | |

**Verdict:** ADAPT

## Skill Analysis: Test Fixing

**Source:** `.claude/skills/test-fixing/SKILL.md`
**Description/Trigger:** "Systematically identify and fix all failing tests using smart grouping strategies. Use when explicitly asks to fix tests (\"fix these tests\", \"make tests pass\"), reports test failures (\"tests are failing\", \"test suite is broken\"), or completes implementation and wants tests passing." risk: unknown source: community date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 7/10 | "Assumed general based on lack of specific constraints." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 7/10 | "description: "Systematically identify and fix all failing tests using smart grouping strategies. Use..." |
| ORM Compatibility | N/A | "Skill is not database/backend framework related." |
| Security Practices | N/A | "No explicit security considerations found or needed for this scope." |
| Output Quality | 8/10 | "Analyze output for:..." |
| Error Handling | 8/10 | "description: "Systematically identify and fix all failing tests using smart grouping strategies. Use..." |
| Monitoring | 8/10 | "**Finally, logic issues:**..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **63/80 (78%)** | |

**Verdict:** ADOPT

## Skill Analysis: Database Design

**Source:** `.claude/skills/database-design/SKILL.md`
**Description/Trigger:** "Database design principles and decision-making. Schema design, indexing strategy, ORM selection, serverless databases." risk: unknown source: community date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 7/10 | "Assumed general based on lack of specific constraints." |
| Technical Depth | 6/10 | "Covers common cases with moderate depth." |
| Decision Intelligence | 8/10 | "| `optimization.md` | N+1, EXPLAIN ANALYZE | Query optimization |..." |
| ORM Compatibility | 8/10 | "description: "Database design principles and decision-making. Schema design, indexing strategy, ORM ..." |
| Security Practices | N/A | "No explicit security considerations found or needed for this scope." |
| Output Quality | 8/10 | "**Read ONLY files relevant to the request!** Check the content map, find what you need...." |
| Error Handling | 3/10 | "No clear error handling or failure modes mentioned." |
| Monitoring | N/A | "Not infrastructure related, monitoring skipped." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **56/80 (70%)** | |

**Verdict:** ADAPT

## Skill Analysis: Automated Documentation Generation

**Source:** `.claude/skills/documentation-generation-doc-generate/SKILL.md`
**Description/Trigger:** "You are a documentation expert specializing in creating comprehensive, maintainable documentation from code. Generate API docs, architecture diagrams, user guides, and technical references using AI-powered analysis and industry best practices." risk: unknown source: community date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 7/10 | "Assumed general based on lack of specific constraints." |
| Technical Depth | 6/10 | "Covers common cases with moderate depth." |
| Decision Intelligence | 8/10 | "Analyzes context before acting." |
| ORM Compatibility | 5/10 | "The user needs automated documentation generation that extracts information from code, creates clear..." |
| Security Practices | 8/10 | "- Avoid exposing secrets, internal URLs, or sensitive data in docs...." |
| Output Quality | 8/10 | "name: documentation-generation-doc-generate..." |
| Error Handling | 3/10 | "No clear error handling or failure modes mentioned." |
| Monitoring | 8/10 | "- Generate docs with consistent terminology and structure...." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **69/100 (69%)** | |

**Verdict:** ADAPT

## Skill Analysis: Documentation Templates

**Source:** `.claude/skills/documentation-templates/SKILL.md`
**Description/Trigger:** "Documentation templates and structure guidelines. README, API docs, code comments, and AI-friendly documentation." risk: unknown source: community date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 7/10 | "Assumed general based on lack of specific constraints." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 8/10 | "Analyzes context before acting." |
| ORM Compatibility | N/A | "Skill is not database/backend framework related." |
| Security Practices | N/A | "No explicit security considerations found or needed for this scope." |
| Output Quality | 8/10 | "## Core Files..." |
| Error Handling | 8/10 | "* @throws ErrorType - When this error occurs..." |
| Monitoring | 8/10 | "| Why (business logic) | What (obvious) |..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 9/10 | "## [1.0.0] - 2025-01-01..." |
| **TOTAL** | **66/80 (82%)** | |

**Verdict:** ADOPT

## Skill Analysis: Microservices Patterns

**Source:** `.claude/skills/microservices-patterns/SKILL.md`
**Description/Trigger:** "Master microservices architecture patterns including service boundaries, inter-service communication, data management, and resilience patterns for building distributed systems." risk: unknown source: community date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 7/10 | "Assumed general based on lack of specific constraints." |
| Technical Depth | 6/10 | "Covers common cases with moderate depth." |
| Decision Intelligence | 3/10 | "Applies a fixed, linear approach without decision branching." |
| ORM Compatibility | N/A | "Skill is not database/backend framework related." |
| Security Practices | N/A | "No explicit security considerations found or needed for this scope." |
| Output Quality | 4/10 | "Ad-hoc or unstructured output." |
| Error Handling | 3/10 | "No clear error handling or failure modes mentioned." |
| Monitoring | 8/10 | "3. Plan resilience, observability, and deployment strategy...." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **47/80 (58%)** | |

**Verdict:** ADAPT

## Skill Analysis: Requesting Code Review

**Source:** `.claude/skills/requesting-code-review/SKILL.md`
**Description/Trigger:** "Use when completing tasks, implementing major features, or before merging to verify work meets requirements" risk: unknown source: community date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 7/10 | "Assumed general based on lack of specific constraints." |
| Technical Depth | 6/10 | "Covers common cases with moderate depth." |
| Decision Intelligence | 3/10 | "Applies a fixed, linear approach without decision branching." |
| ORM Compatibility | N/A | "Skill is not database/backend framework related." |
| Security Practices | N/A | "No explicit security considerations found or needed for this scope." |
| Output Quality | 4/10 | "Ad-hoc or unstructured output." |
| Error Handling | 8/10 | "Dispatch superpowers:code-reviewer subagent to catch issues before they cascade...." |
| Monitoring | 8/10 | "BASE_SHA=$(git log --oneline | grep "Task 1" | head -1 | awk '{print $1}')..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **52/80 (65%)** | |

**Verdict:** ADAPT

## Skill Analysis: Context Degradation Patterns

**Source:** `.claude/skills/context-degradation/SKILL.md`
**Description/Trigger:** This skill should be used when the user asks to "diagnose context problems", "fix lost-in-middle issues", "debug agent failures", "understand context poisoning", or mentions context degradation, attention patterns, context clash, context confusion, or agent performance degradation. Provides patterns for recognizing and mitigating context failures. ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 4/10 | "Diagnose and fix context failures before they cascade. Context degradation is not binary — it is a c..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 7/10 | "Diagnose and fix context failures before they cascade. Context degradation is not binary — it is a c..." |
| ORM Compatibility | 5/10 | "description: This skill should be used when the user asks to "diagnose context problems", "fix lost-..." |
| Security Practices | 8/10 | "**Author**: Agent Skills for Context Engineering Contributors..." |
| Output Quality | 8/10 | "- Debugging cases where agents produce incorrect or irrelevant outputs..." |
| Error Handling | 8/10 | "description: This skill should be used when the user asks to "diagnose context problems", "fix lost-..." |
| Monitoring | 8/10 | "Monitor for lost-in-middle symptoms: correct information exists in context but the model ignores it,..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 9/10 | "**Created**: 2025-12-20..." |
| **TOTAL** | **75/100 (75%)** | |

**Verdict:** ADAPT

## Skill Analysis: Event Sourcing Architect

**Source:** `.claude/skills/event-sourcing-architect/SKILL.md`
**Description/Trigger:** "Expert in event sourcing, CQRS, and event-driven architecture patterns. Masters event store design, projection building, saga orchestration, and eventual consistency patterns. Use PROACTIVELY for event-sourced systems, audit trail requirements, or complex domain modeling with temporal queries." risk: unknown source: community date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 7/10 | "Assumed general based on lack of specific constraints." |
| Technical Depth | 6/10 | "Covers common cases with moderate depth." |
| Decision Intelligence | 3/10 | "Applies a fixed, linear approach without decision branching." |
| ORM Compatibility | 5/10 | "- Snapshotting strategies for performance..." |
| Security Practices | N/A | "No explicit security considerations found or needed for this scope." |
| Output Quality | 4/10 | "Ad-hoc or unstructured output." |
| Error Handling | 3/10 | "No clear error handling or failure modes mentioned." |
| Monitoring | N/A | "Not infrastructure related, monitoring skipped." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **44/80 (55%)** | |

**Verdict:** ADAPT

## Skill Analysis: Memory Integrator (Der Erinnerungs-Integrator)

**Source:** `.claude/skills/memory-integrator/SKILL.md`
**Description/Trigger:** > Mandatory skill for every iteration to manage the "changing memories (not appending)" problem. Reflects on past iterations, extracts variables/lessons, and integrates them into an append-only appendix to align with the repo goal (Dual-Kernel: Psychology, Quantum Physics, Topology, Systems Theory). </description>

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 4/10 | "Mandatory skill for every iteration to manage the "changing memories (not appending)" problem. Refle..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 8/10 | "The Multi-Agent architecture has suffered from memory degradation—specifically, past memories being ..." |
| ORM Compatibility | 5/10 | "The Multi-Agent architecture has suffered from memory degradation—specifically, past memories being ..." |
| Security Practices | N/A | "No explicit security considerations found or needed for this scope." |
| Output Quality | 8/10 | "- Use when updating or reading from the `MIF-Memory-File`...." |
| Error Handling | 8/10 | "The Multi-Agent architecture has suffered from memory degradation—specifically, past memories being ..." |
| Monitoring | 8/10 | "Mandatory skill for every iteration to manage the "changing memories (not appending)" problem. Refle..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **66/90 (73%)** | |

**Verdict:** ADAPT

## Skill Analysis: Systematic Debugging

**Source:** `.claude/skills/systematic-debugging/SKILL.md`
**Description/Trigger:** "Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes" risk: unknown source: community date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 9/10 | "description: "Use when encountering any bug, test failure, or unexpected behavior, before proposing ..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 7/10 | "If you haven't completed Phase 1, you cannot propose fixes...." |
| ORM Compatibility | 5/10 | "- Performance problems..." |
| Security Practices | 8/10 | "echo "=== Secrets available in workflow: ==="..." |
| Output Quality | 8/10 | "- Note line numbers, file paths, error codes..." |
| Error Handling | 8/10 | "description: "Use when encountering any bug, test failure, or unexpected behavior, before proposing ..." |
| Monitoring | 8/10 | "- Log what data enters component..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **78/100 (78%)** | |

**Verdict:** ADOPT

## Skill Analysis: Project Development Methodology

**Source:** `.claude/skills/project-development/SKILL.md`
**Description/Trigger:** This skill should be used when the user asks to "start an LLM project", "design batch pipeline", "evaluate task-model fit", "structure agent project", or mentions pipeline architecture, agent-assisted development, cost estimation, or choosing between LLM and traditional approaches. ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 4/10 | "name: project-development..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 7/10 | "This skill covers the principles for identifying tasks suited to LLM processing, designing effective..." |
| ORM Compatibility | 5/10 | "| Synthesis across sources | LLMs combine information from multiple inputs better than rule-based al..." |
| Security Practices | 8/10 | "**Author**: Agent Skills for Context Engineering Contributors..." |
| Output Quality | 8/10 | "- Planning a batch processing pipeline with structured outputs..." |
| Error Handling | 8/10 | "| Error tolerance | Individual failures do not break the overall system, so LLM non-determinism is a..." |
| Monitoring | 8/10 | "# Project Development Methodology..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 9/10 | "**Created**: 2025-12-25..." |
| **TOTAL** | **75/100 (75%)** | |

**Verdict:** ADAPT
