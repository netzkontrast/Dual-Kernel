# Skill Comparison: Frontend Skills

This document contains a deep audit of all skills in this category, comparing their capabilities and identifying gaps.

## Category Ecosystem Analysis

| Capability | Existing Skill | Coverage | Gap |
|------------|---------------|----------|-----|
| Browser Automation | `browser-automation` | ⚠️ Partial | Needs refactoring/depth |
| Hosted Agent Infrastructure | `hosted-agents` | ⚠️ Partial | Needs refactoring/depth |
| frontend-developer | `frontend-developer` | ⚠️ Partial | Needs refactoring/depth |
| Architecture Patterns | `architecture-patterns` | ⚠️ Partial | Needs refactoring/depth |
| E2E Testing Patterns | `e2e-testing-patterns` | ⚠️ Partial | Needs refactoring/depth |
| Architecture Decision Records | `architecture-decision-records` | ⚠️ Partial | Needs refactoring/depth |
| Backend Development Guidelines | `backend-dev-guidelines` | ⚠️ Partial | Needs refactoring/depth |
| Skill Developer Guide | `skill-developer` | ✅ Full | — |
| Code Review Reception | `receiving-code-review` | ⚠️ Partial | Needs refactoring/depth |
| Prompt Architect | `prompt-architect` | ⚠️ Partial | Needs refactoring/depth |

## Skill Analysis: Browser Automation

**Source:** `.claude/skills/browser-automation/SKILL.md`
**Description/Trigger:** "You are a browser automation expert who has debugged thousands of flaky tests and built scrapers that run for years without breaking. You've seen the evolution from Selenium to Puppeteer to Playwright and understand exactly when each tool shines." risk: unknown source: "vibeship-spawner-skills (Apache 2.0)" date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 7/10 | "Assumed general based on lack of specific constraints." |
| Technical Depth | 6/10 | "Covers common cases with moderate depth." |
| Decision Intelligence | 8/10 | "### ❌ Single Browser Context for Everything..." |
| ORM Compatibility | N/A | "Skill is not database/backend framework related." |
| Security Practices | N/A | "No explicit security considerations found or needed for this scope." |
| Output Quality | 4/10 | "Ad-hoc or unstructured output." |
| Error Handling | 8/10 | "Your core insight: Most automation failures come from three sources - bad..." |
| Monitoring | N/A | "Not infrastructure related, monitoring skipped." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **49/70 (70%)** | |

**Verdict:** ADAPT

## Skill Analysis: Hosted Agent Infrastructure

**Source:** `.claude/skills/hosted-agents/SKILL.md`
**Description/Trigger:** This skill should be used when the user asks to "build background agent", "create hosted coding agent", "set up sandboxed execution", "implement multiplayer agent", or mentions background agents, sandboxed VMs, agent infrastructure, Modal sandboxes, self-spawning agents, or remote coding environments. ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 4/10 | "Hosted agents run in remote sandboxed environments rather than on local machines. When designed well..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 7/10 | "Configure git identity explicitly in every sandbox because background agents are not tied to a speci..." |
| ORM Compatibility | 5/10 | "Design the architecture in three layers because each layer scales independently. Build sandbox infra..." |
| Security Practices | 8/10 | "Build the data model so sessions are not tied to single authors because multiplayer fails silently i..." |
| Output Quality | 8/10 | "- Cached files from running app and test suite once..." |
| Error Handling | 8/10 | "Select frameworks where the agent can read its own source code to understand behavior. Prioritize th..." |
| Monitoring | 8/10 | "Structure the agent framework as a server first, with TUI and desktop apps as thin clients, because ..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 9/10 | "Pre-build environment images on a regular cadence (every 30 minutes works well) because this makes s..." |
| **TOTAL** | **75/100 (75%)** | |

**Verdict:** ADAPT

## Skill Analysis: frontend-developer

**Source:** `.claude/skills/frontend-developer/SKILL.md`
**Description/Trigger:** Build React components, implement responsive layouts, and handle client-side state management. Masters React 19, Next.js 15, and modern frontend architecture. risk: unknown source: community date_added: '2026-02-27' --- You are a frontend development expert specializing in modern React applications, Next.js, and cutting-edge frontend architecture.

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 4/10 | "- You only need backend API architecture..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 7/10 | "1. Clarify requirements, target devices, and performance goals...." |
| ORM Compatibility | 8/10 | "- Fixing frontend performance, accessibility, or state issues..." |
| Security Practices | 8/10 | "- Authentication with NextAuth.js, Auth0, and Clerk..." |
| Output Quality | 4/10 | "Ad-hoc or unstructured output." |
| Error Handling | 8/10 | "- Error boundaries and error handling strategies..." |
| Monitoring | 8/10 | "- Memory leak prevention and performance monitoring..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **72/100 (72%)** | |

**Verdict:** ADAPT

## Skill Analysis: Architecture Patterns

**Source:** `.claude/skills/architecture-patterns/SKILL.md`
**Description/Trigger:** "Master proven backend architecture patterns including Clean Architecture, Hexagonal Architecture, and Domain-Driven Design to build maintainable, testable, and scalable systems." risk: unknown source: community date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 7/10 | "Assumed general based on lack of specific constraints." |
| Technical Depth | 6/10 | "Covers common cases with moderate depth." |
| Decision Intelligence | 3/10 | "Applies a fixed, linear approach without decision branching." |
| ORM Compatibility | 5/10 | "5. For workflows that must survive failures (payments, order fulfillment, multi-step processes), use..." |
| Security Practices | N/A | "No explicit security considerations found or needed for this scope." |
| Output Quality | 4/10 | "Ad-hoc or unstructured output." |
| Error Handling | 8/10 | "5. For workflows that must survive failures (payments, order fulfillment, multi-step processes), use..." |
| Monitoring | N/A | "Not infrastructure related, monitoring skipped." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **49/80 (61%)** | |

**Verdict:** ADAPT

## Skill Analysis: E2E Testing Patterns

**Source:** `.claude/skills/e2e-testing-patterns/SKILL.md`
**Description/Trigger:** "Build reliable, fast, and maintainable end-to-end test suites that provide confidence to ship code quickly and catch regressions before users do." risk: unknown source: community date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 7/10 | "Assumed general based on lack of specific constraints." |
| Technical Depth | 6/10 | "Covers common cases with moderate depth." |
| Decision Intelligence | 3/10 | "Applies a fixed, linear approach without decision branching." |
| ORM Compatibility | N/A | "Skill is not database/backend framework related." |
| Security Practices | N/A | "No explicit security considerations found or needed for this scope." |
| Output Quality | 8/10 | "- Use dedicated test data and scrub sensitive output...." |
| Error Handling | 8/10 | "description: "Build reliable, fast, and maintainable end-to-end test suites that provide confidence ..." |
| Monitoring | N/A | "Not infrastructure related, monitoring skipped." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **48/70 (68%)** | |

**Verdict:** ADAPT

## Skill Analysis: Architecture Decision Records

**Source:** `.claude/skills/architecture-decision-records/SKILL.md`
**Description/Trigger:** "Comprehensive patterns for creating, maintaining, and managing Architecture Decision Records (ADRs) that capture the context and rationale behind significant technical decisions." risk: unknown source: community date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 4/10 | "- You only need to document small implementation details..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 7/10 | "description: "Comprehensive patterns for creating, maintaining, and managing Architecture Decision R..." |
| ORM Compatibility | 5/10 | "| New framework adoption | Minor version upgrades |..." |
| Security Practices | 8/10 | "| Security architecture | Routine maintenance |..." |
| Output Quality | 8/10 | "ADR-0003 (2021) chose MongoDB for user profile storage due to schema flexibility..." |
| Error Handling | 8/10 | "related to prop type mismatches and undefined errors. PropTypes provide..." |
| Monitoring | 8/10 | "- Documenting technology choices..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 9/10 | "**Date**: 2024-01-15..." |
| **TOTAL** | **75/100 (75%)** | |

**Verdict:** ADAPT

## Skill Analysis: Backend Development Guidelines

**Source:** `.claude/skills/backend-dev-guidelines/SKILL.md`
**Description/Trigger:** "You are a senior backend engineer operating production-grade services under strict architectural and reliability constraints. Use when routes, controllers, services, repositories, express middleware, or prisma database access." risk: unknown source: community date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 7/10 | "Assumed general based on lack of specific constraints." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 3/10 | "Applies a fixed, linear approach without decision branching." |
| ORM Compatibility | 8/10 | "description: "You are a senior backend engineer operating production-grade services under strict arc..." |
| Security Practices | 8/10 | "| **Operational Risk**          | Does this impact auth, billing, messaging, or infra?             |..." |
| Output Quality | 4/10 | "Ad-hoc or unstructured output." |
| Error Handling | 8/10 | "* Explicit error boundaries..." |
| Monitoring | 8/10 | "* First-class observability..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **71/100 (71%)** | |

**Verdict:** ADAPT

## Skill Analysis: Skill Developer Guide

**Source:** `.claude/skills/skill-developer/SKILL.md`
**Description/Trigger:** "Comprehensive guide for creating and managing skills in Claude Code with auto-activation system, following Anthropic's official best practices including the 500-line rule and progressive disclosure pattern." risk: unknown source: community date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 4/10 | "**Purpose:** Provide comprehensive guidance for specific areas..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 8/10 | "- **Method**: Injects formatted reminder as context (stdout → Claude's input)..." |
| ORM Compatibility | 5/10 | "- **Method**: Injects formatted reminder as context (stdout → Claude's input)..." |
| Security Practices | 8/10 | "- **Use For**: Critical mistakes, data integrity, security issues..." |
| Output Quality | 8/10 | "- **File**: `.claude/hooks/skill-activation-prompt.ts`..." |
| Error Handling | 8/10 | "**2. Stop Hook - Error Handling Reminder** (Gentle Reminders)..." |
| Monitoring | 8/10 | "- **Content**: Technology-specific detection..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 9/10 | "**Philosophy Change (2025-10-27):** We moved away from blocking PreToolUse for Sentry/error handling..." |
| **TOTAL** | **76/100 (76%)** | |

**Verdict:** ADOPT

## Skill Analysis: Code Review Reception

**Source:** `.claude/skills/receiving-code-review/SKILL.md`
**Description/Trigger:** "Code review requires technical evaluation, not emotional performance." risk: unknown source: community date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 9/10 | "IF any item is unclear:..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 7/10 | "**Core principle:** Verify before implementing. Ask before assuming. Technical correctness over soci..." |
| ORM Compatibility | 5/10 | "description: "Code review requires technical evaluation, not emotional performance."..." |
| Security Practices | 8/10 | "- Blocking issues (breaks, security)..." |
| Output Quality | 4/10 | "Ad-hoc or unstructured output." |
| Error Handling | 8/10 | "✅ "Good catch - [specific issue]. Fixed in [location]."..." |
| Monitoring | 8/10 | "- Complex fixes (refactoring, logic)..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **74/100 (74%)** | |

**Verdict:** ADAPT

## Skill Analysis: Prompt Architect

**Source:** `.claude/skills/prompt-architect/SKILL.md`
**Description/Trigger:** Analyzes and improves prompts using 27 research-backed frameworks across 7 intent categories. Use when a user wants to improve, rewrite, structure, or engineer a prompt — including requests like "help me write a better prompt", "improve this prompt", "what framework should I use", "make this prompt more effective", or any prompt engineering task. Recommends the right framework based on intent (create, transform, reason, critique, recover, clarify, agentic), asks targeted questions, and delivers a structured, high-quality result. license: MIT compatibility: Requires no external dependencies. Works with any Agent Skills compatible tool. metadata:   author: ckelsoe   version: "3.2.2"   homepage: https://github.com/ckelsoe/prompt-architect ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 4/10 | "- **Specificity**: Are requirements detailed enough?..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 7/10 | "description: Analyzes and improves prompts using 27 research-backed frameworks across 7 intent categ..." |
| ORM Compatibility | 5/10 | "description: Analyzes and improves prompts using 27 research-backed frameworks across 7 intent categ..." |
| Security Practices | 8/10 | "author: ckelsoe..." |
| Output Quality | 8/10 | "- **Output Format**: Is desired format clear?..." |
| Error Handling | 8/10 | "| Identify failure modes before they happen | **Pre-Mortem** |..." |
| Monitoring | 8/10 | "You are an expert in prompt engineering and systematic application of prompting frameworks. Help use..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 9/10 | "- `devils-advocate.md` - Strongest opposing argument generation (ACM IUI 2024)..." |
| **TOTAL** | **75/100 (75%)** | |

**Verdict:** ADAPT
