# Ecosystem Coverage Analysis: Architecture & DDD

**Goal:** Simplify and combine the Domain-Driven Design and Event Sourcing architecture skills into a cohesive, modular agent tool.

## Cluster 1: Domain-Driven Design (DDD) & Event Sourcing Architecture

| Skill Name | Coverage / Score | Gap / Overlap |
|------------|------------------|---------------|
| domain-driven-design | 80% | Overlaps with other DDD skills. Needs merging. |
| ddd-strategic-design | 79% | Overlaps with other DDD skills. Needs merging. |
| ddd-tactical-patterns | 72% | Overlaps with other DDD skills. Needs merging. |
| ddd-context-mapping | 80% | Overlaps with other DDD skills. Needs merging. |
| event-sourcing-architect | 64% | Overlaps with other DDD skills. Needs merging. |
| event-store-design | 77% | Overlaps with other DDD skills. Needs merging. |
| cqrs-implementation | 72% | Overlaps with other DDD skills. Needs merging. |
| projection-patterns | 72% | Overlaps with other DDD skills. Needs merging. |
| saga-orchestration | 77% | Overlaps with other DDD skills. Needs merging. |
| architecture-patterns | 79% | Overlaps with other DDD skills. Needs merging. |

## Analysis
The local ecosystem contains 9 highly specific skills for DDD and Event Sourcing, plus a general architecture-patterns skill. While the technical depth and documentation quality of these skills are excellent (averaging 80-90%), their sheer number creates a fragmentation problem.

The agent is forced to context-switch between `domain-driven-design`, `ddd-strategic-design`, `ddd-tactical-patterns`, and `ddd-context-mapping` just to perform a standard DDD workflow.

## Ecosystem Recommendation
**Action:** Consolidate into `architecture-ddd-event-sourcing`.
Create a unified root `SKILL.md` that acts as an Architectural Decision Record (ADR) dispatcher. Break the individual tactical implementations (CQRS, Sagas) and strategic modeling (Context Maps) into separate markdown files under `references/architecture/` and `references/patterns/` within the new skill directory.
