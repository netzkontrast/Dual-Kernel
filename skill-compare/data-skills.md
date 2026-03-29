# Skill Comparison: Data Skills

This document contains a deep audit of all skills in this category, comparing their capabilities and identifying gaps.

## Category Ecosystem Analysis

| Capability | Existing Skill | Coverage | Gap |
|------------|---------------|----------|-----|
| QMD Re-index Skill | `qmd-reindex` | ⚠️ Partial | Needs refactoring/depth |

## Skill Analysis: QMD Re-index Skill

**Source:** `.claude/skills/qmd-reindex/SKILL.md`
**Description/Trigger:** Re-index mnemonic memories for qmd semantic search. Run after capturing new memories or bulk imports. name: qmd-reindex user-invocable: true ---

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Scope & Generality | 4/10 | "# Index only (skip embeddings — faster)..." |
| Technical Depth | 3/10 | "Surface-level instructions only." |
| Decision Intelligence | 3/10 | "Applies a fixed, linear approach without decision branching." |
| ORM Compatibility | N/A | "Skill is not database/backend framework related." |
| Security Practices | N/A | "No explicit security considerations found or needed for this scope." |
| Output Quality | 8/10 | "- `qmd embed` — regenerates vector embeddings for semantic search..." |
| Error Handling | 3/10 | "No clear error handling or failure modes mentioned." |
| Monitoring | N/A | "Not infrastructure related, monitoring skipped." |
| Documentation | 5/10 | "Reasonable documentation but lacks deep structure." |
| Freshness | 7/10 | "Standard local repository maintenance." |
| **TOTAL** | **33/70 (47%)** | |

**Verdict:** BUILD FROM SCRATCH
