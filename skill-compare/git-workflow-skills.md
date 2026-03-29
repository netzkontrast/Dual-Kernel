# Skill Comparison: Git Workflow Skills

This document contains a deep audit of all skills in this category, comparing their capabilities and identifying gaps.

## Category Ecosystem Analysis

| Capability | Existing Skill | Coverage | Gap |
|------------|---------------|----------|-----|
| Git Push Workflow | `git-pushing` | ⚠️ Partial | Needs refactoring/depth |
| Alias: create-pr | `create-pr` | ⚠️ Partial | Needs refactoring/depth |

## Skill Analysis: Git Push Workflow

**Source:** `.claude/skills/git-pushing/SKILL.md`
**Description/Trigger:** "Stage all changes, create a conventional commit, and push to the remote branch. Use when explicitly asks to push changes (\"push this\", \"commit and push\"), mentions saving work to remote (\"save to github\", \"push to remote\"), or completes a feature and wants to share it." risk: unknown source: community date_added: "2026-02-27" ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 7/10 | "Assumed general based on lack of specific constraints." |
| Technical Depth | 6/10 | "Covers common cases with moderate depth." |
| Decision Intelligence | 3/10 | "Applies a fixed, linear approach without decision branching." |
| ORM Compatibility | N/A | "Skill is not database/backend framework related." |
| Security Practices | N/A | "No explicit security considerations found or needed for this scope." |
| Output Quality | 4/10 | "Ad-hoc or unstructured output." |
| Error Handling | 3/10 | "No clear error handling or failure modes mentioned." |
| Monitoring | N/A | "Not infrastructure related, monitoring skipped." |
| Documentation | 5/10 | "Reasonable documentation but lacks deep structure." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **35/70 (50%)** | |

**Verdict:** BUILD FROM SCRATCH

## Skill Analysis: Alias: create-pr

**Source:** `.claude/skills/create-pr/SKILL.md`
**Description/Trigger:** Alias for sentry-skills:pr-writer. Use when users explicitly ask for "create-pr" or reference the legacy skill name. Redirects to the canonical PR writing workflow. risk: unknown source: community ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 7/10 | "Assumed general based on lack of specific constraints." |
| Technical Depth | 3/10 | "Surface-level instructions only." |
| Decision Intelligence | 3/10 | "Applies a fixed, linear approach without decision branching." |
| ORM Compatibility | N/A | "Skill is not database/backend framework related." |
| Security Practices | N/A | "No explicit security considerations found or needed for this scope." |
| Output Quality | 4/10 | "Ad-hoc or unstructured output." |
| Error Handling | 3/10 | "No clear error handling or failure modes mentioned." |
| Monitoring | N/A | "Not infrastructure related, monitoring skipped." |
| Documentation | 5/10 | "Reasonable documentation but lacks deep structure." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **32/70 (45%)** | |

**Verdict:** BUILD FROM SCRATCH
