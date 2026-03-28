# Skill Comparison: Testing Quality Skills

This document contains a deep audit of all skills in this category, comparing their capabilities and identifying gaps.

## Category Ecosystem Analysis

| Capability | Existing Skill | Coverage | Gap |
|------------|---------------|----------|-----|
| Concise Planning | `concise-planning` | ⚠️ Partial | Needs refactoring/depth |
| Git Advanced Workflows | `git-advanced-workflows` | ⚠️ Partial | Needs refactoring/depth |
| QMD Setup Skill | `qmd-setup` | ⚠️ Partial | Needs refactoring/depth |
| A/B Test Setup | `ab-test-setup` | ⚠️ Partial | Needs refactoring/depth |
| Code Review Checklist | `code-review-checklist` | ✅ Full | — |

## Skill Analysis: Concise Planning

**Source:** `.claude/skills/concise-planning/SKILL.md`
**Description/Trigger:** "Use when a user asks for a plan for a coding task, to generate a clear, actionable, and atomic checklist." risk: unknown source: community date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 4/10 | "- Ask **at most 1–2 questions** and only if truly blocking...." |
| Technical Depth | 6/10 | "Covers common cases with moderate depth." |
| Decision Intelligence | 8/10 | "### 1. Scan Context..." |
| ORM Compatibility | 5/10 | "- Identify constraints (language, frameworks, tests)...." |
| Security Practices | N/A | "No explicit security considerations found or needed for this scope." |
| Output Quality | 8/10 | "description: "Use when a user asks for a plan for a coding task, to generate a clear, actionable, an..." |
| Error Handling | 3/10 | "No clear error handling or failure modes mentioned." |
| Monitoring | 8/10 | "- **Atomic**: Each step should be a single logical unit of work...." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **58/90 (64%)** | |

**Verdict:** ADAPT

## Skill Analysis: Git Advanced Workflows

**Source:** `.claude/skills/git-advanced-workflows/SKILL.md`
**Description/Trigger:** "Master advanced Git techniques to maintain clean history, collaborate effectively, and recover from any situation with confidence." risk: unknown source: community date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 4/10 | "- Applying specific commits across branches..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 7/10 | "- You need a different domain or tool outside this scope..." |
| ORM Compatibility | N/A | "Skill is not database/backend framework related." |
| Security Practices | 8/10 | "git checkout feature/user-auth..." |
| Output Quality | 8/10 | "# Output shows:..." |
| Error Handling | 8/10 | "# If tests fail..." |
| Monitoring | 8/10 | "### 5. Reflog..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **68/90 (75%)** | |

**Verdict:** ADAPT

## Skill Analysis: QMD Setup Skill

**Source:** `.claude/skills/qmd-setup/SKILL.md`
**Description/Trigger:** Set up @tobilu/qmd semantic search for mnemonic memories. Registers collections, builds indexes, and generates embeddings. Run this once per machine. name: qmd-setup user-invocable: true ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 4/10 | "- `.claude/mnemonic/` → collection `mnemonic-project`..." |
| Technical Depth | 6/10 | "Covers common cases with moderate depth." |
| Decision Intelligence | 3/10 | "Applies a fixed, linear approach without decision branching." |
| ORM Compatibility | N/A | "Skill is not database/backend framework related." |
| Security Practices | 8/10 | "qmd search "auth" -c mnemonic-zircote    # org memories only..." |
| Output Quality | 4/10 | "Ad-hoc or unstructured output." |
| Error Handling | 3/10 | "No clear error handling or failure modes mentioned." |
| Monitoring | N/A | "Not infrastructure related, monitoring skipped." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **44/80 (55%)** | |

**Verdict:** ADAPT

## Skill Analysis: A/B Test Setup

**Source:** `.claude/skills/ab-test-setup/SKILL.md`
**Description/Trigger:** "Structured guide for setting up A/B tests with mandatory gates for hypothesis, metrics, and execution readiness." risk: unknown source: community date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 4/10 | "- Single, specific change..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 8/10 | "- Provide context..." |
| ORM Compatibility | N/A | "Skill is not database/backend framework related." |
| Security Practices | N/A | "No explicit security considerations found or needed for this scope." |
| Output Quality | 4/10 | "Ad-hoc or unstructured output." |
| Error Handling | 8/10 | "- Do NOT override guardrail failures..." |
| Monitoring | 8/10 | "description: "Structured guide for setting up A/B tests with mandatory gates for hypothesis, metrics..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **57/80 (71%)** | |

**Verdict:** ADAPT

## Skill Analysis: Code Review Checklist

**Source:** `.claude/skills/code-review-checklist/SKILL.md`
**Description/Trigger:** "Comprehensive checklist for conducting thorough code reviews covering functionality, security, performance, and maintainability" risk: unknown source: community date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 9/10 | "- Are there any logical errors?..." |
| Technical Depth | 9/10 | "Extensive instructions and edge cases covered." |
| Decision Intelligence | 7/10 | "Provide a systematic checklist for conducting thorough code reviews. This skill helps reviewers ensu..." |
| ORM Compatibility | 5/10 | "description: "Comprehensive checklist for conducting thorough code reviews covering functionality, s..." |
| Security Practices | 8/10 | "description: "Comprehensive checklist for conducting thorough code reviews covering functionality, s..." |
| Output Quality | 8/10 | "- What files were changed and why?..." |
| Error Handling | 8/10 | "Provide a systematic checklist for conducting thorough code reviews. This skill helps reviewers ensu..." |
| Monitoring | 8/10 | "- Are there any logical errors?..." |
| Documentation | 9/10 | "Clear phases, trade-offs explained, well-structured." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **78/100 (78%)** | |

**Verdict:** ADOPT
