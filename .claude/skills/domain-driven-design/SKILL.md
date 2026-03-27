---
name: domain-driven-design
description: "Plan and route Domain-Driven Design work from strategic modeling to tactical implementation and evented architecture. Use when modeling a complex business domain, defining bounded contexts, splitting a monolith, aligning team ownership, evaluating whether DDD is worth the complexity, planning CQRS, event sourcing, sagas, or projections, or connecting strategic decisions to code-level patterns. Trigger keywords: DDD, domain model, bounded context, ubiquitous language, subdomain, context map, aggregate, domain event, anti-corruption layer, core domain, supporting domain, generic subdomain, domain-driven."
risk: safe
source: self
tags: "[ddd, domain, bounded-context, architecture, routing]"
date_added: "2026-02-27"
---

# Domain-Driven Design

## Use this skill when

- You need to model a complex business domain with explicit boundaries.
- You want to decide whether full DDD is worth the added complexity.
- You need to connect strategic design decisions to implementation patterns.
- You are planning CQRS, event sourcing, sagas, or projections from domain needs.
- You are splitting a monolith or aligning teams around ownership boundaries.

## Do not use this skill when

- The problem is simple CRUD with low business complexity.
- You only need localized bug fixes.
- There is no access to domain knowledge and no proxy product expert.

## Instructions

1. Run a viability check before committing to full DDD.
2. Produce strategic artifacts first: subdomains, bounded contexts, language glossary.
3. Route to specialized skills based on current task.
4. Define success criteria and evidence for each stage.

### Viability check

Use full DDD only when at least two of these are true:

- Business rules are complex or fast-changing.
- Multiple teams are causing model collisions.
- Integration contracts are unstable.
- Auditability and explicit invariants are critical.

### Sequence

DDD work follows this order — do not skip ahead:

```
1. Viability check (this skill)
        ↓
2. Strategic design (@ddd-strategic-design)
   — subdomains, bounded contexts, ubiquitous language
        ↓
3. Context mapping (@ddd-context-mapping)
   — integration patterns, ACL, contract ownership
        ↓
4. Tactical patterns (@ddd-tactical-patterns)
   — aggregates, value objects, repositories, domain events
        ↓
5. Evented architecture (when complexity warrants)
   — @cqrs-implementation, @event-sourcing-architect, @event-store-design
   — @saga-orchestration, @projection-patterns
        ↓
6. Decision log (@architecture-decision-records)
```

### Routing map

| Task | Skill |
|------|-------|
| Strategic model and boundaries | `@ddd-strategic-design` |
| Cross-context integrations | `@ddd-context-mapping` |
| Tactical code modeling | `@ddd-tactical-patterns` |
| Read/write separation | `@cqrs-implementation` |
| Event history as source of truth | `@event-sourcing-architect`, `@event-store-design` |
| Long-running workflows | `@saga-orchestration` |
| Read models | `@projection-patterns` |
| Decision log | `@architecture-decision-records` |

## Deliverables by stage

### Strategic
- Subdomain map (core, supporting, generic)
- Bounded context map and ownership
- Ubiquitous language glossary
- 1-2 ADRs documenting critical boundary decisions

### Tactical
- Aggregate list with invariants
- Value object list
- Domain events list
- Repository contracts and transaction boundaries

### Evented (only when required)
- Command and query separation rationale
- Event schema versioning policy
- Saga compensation matrix
- Projection rebuild strategy

## Subagents

Delegate discovery and planning work to agents rather than doing it manually:

| Task | Agent type | What to ask |
|------|------------|-------------|
| Scan codebase for existing domain boundaries | `Explore` | "Find all module groupings, service boundaries, and domain concepts in `[path]`. List by capability area." |
| Assess architecture for DDD viability | `Plan` | "Evaluate this codebase for DDD adoption: identify complexity signals, team boundary indicators, and integration instability." |
| Research unfamiliar DDD patterns | `general-purpose` | "Explain [pattern] with a concrete example. When should it be preferred over [alternative]?" |

Launch in background when the codebase scan is large — results inform the routing decision.

## Output requirements

Always return:

- Scope and assumptions
- Current stage (strategic, tactical, or evented)
- Explicit artifacts produced
- Open risks and next step recommendation

## Examples

```text
Use @domain-driven-design to assess if this billing platform should adopt full DDD.
Then route to the right next skill and list artifacts we must produce this week.
```

## Limitations

- This skill does not replace direct workshops with domain experts.
- It does not provide framework-specific code generation.
- It should not be used as a justification to over-engineer simple systems.
