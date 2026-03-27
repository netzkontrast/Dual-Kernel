---
name: architecture-ddd-event-sourcing
description: "Unified skill for Domain-Driven Design (DDD) and event-driven architecture. Covers strategic modeling, tactical patterns, context mapping, event sourcing, CQRS, projections, sagas, and event store design."
risk: safe
source: self
tags: "[ddd, event-sourcing, cqrs, saga, projection, bounded-context, architecture]"
date_added: "2026-03-27"
triggers: domain-driven design, DDD, bounded context, aggregate, event sourcing, CQRS, saga, projection, event store, context map, ubiquitous language, subdomain, value object, domain event, anti-corruption layer
---

# Architecture: DDD & Event Sourcing

Unified dispatcher for Domain-Driven Design and event-driven architecture work.
Replaces: `domain-driven-design`, `ddd-strategic-design`, `ddd-tactical-patterns`, `ddd-context-mapping`, `event-sourcing-architect`, `event-store-design`, `cqrs-implementation`, `projection-patterns`, `saga-orchestration`.

## ⚡ Decision Tree — What are you doing?

### 1. Starting from scratch / assessing DDD fit
Run the **viability check** first. Use full DDD only when ≥2 of these are true:
- Business rules are complex or fast-changing
- Multiple teams are causing model collisions
- Integration contracts are unstable
- Auditability and explicit invariants are critical

Then produce strategic artifacts in order: subdomains → bounded contexts → ubiquitous language glossary.

### 2. Strategic design — bounded contexts & subdomains
- Classify subdomains as core / supporting / generic
- Define context boundaries around consistency and team ownership
- Build a ubiquitous language glossary; define anti-terms
- Capture boundary decisions in ADRs before writing code

**Required artifacts:** subdomain classification table · bounded context catalog · glossary · boundary rationale

### 3. Context integration — how contexts talk to each other
- List all context pairs and dependency direction (upstream / downstream)
- Choose relationship patterns: Partnership, Customer-Supplier, Conformist, ACL, Open Host, Published Language
- Define translation rules and contract ownership
- Add failure modes, fallback behavior, and versioning policy

**Required artifacts:** context relationship map · contract ownership matrix · ACL decisions · coupling risks

### 4. Tactical code design — aggregates, entities, value objects
1. Identify invariants first; design aggregates to enforce them
2. Model immutable value objects for validated concepts
3. Keep domain behavior in domain objects, not controllers
4. Emit domain events for meaningful state transitions
5. Keep repositories at aggregate root boundaries

```typescript
class Order {
  private status: "draft" | "submitted" = "draft";
  submit(itemsCount: number): void {
    if (itemsCount === 0) throw new Error("Order cannot be submitted empty");
    if (this.status !== "draft") throw new Error("Order already submitted");
    this.status = "submitted";
  }
}
```

### 5. Event sourcing — events as source of truth
Use when: complete audit trail needed · temporal queries ("state at time X") · undo/redo · complex compensating workflows.

**Implementation order:**
1. Identify aggregate boundaries and event streams
2. Design events as immutable facts (never mutate or delete committed events)
3. Implement command handlers and event application
4. Build projections for query requirements
5. Design saga/process managers for cross-aggregate workflows
6. Implement snapshotting for long-lived aggregates
7. Set up event versioning strategy from day one

**Safety:** Never mutate or delete committed events in production. Rebuild projections in staging before running in production.

### 6. Event store — persistence infrastructure
Technology comparison:

| Technology   | Best For                  | Limitations                      |
|--------------|---------------------------|----------------------------------|
| EventStoreDB | Pure event sourcing       | Single-purpose                   |
| PostgreSQL   | Existing Postgres stack   | Manual implementation            |
| Kafka        | High-throughput streaming | Not ideal for per-stream queries |
| DynamoDB     | Serverless / AWS-native   | Query limitations                |

Minimum schema requirements: append-only · per-stream ordering · optimistic concurrency (version) · subscription support · idempotent writes.

### 7. CQRS — separating reads from writes
Use when: read/write scaling requirements differ · complex query scenarios · different read/write data models · high-performance reporting.

Implementation steps:
1. Separate command handlers (write side) from query handlers (read side)
2. Commands validate and apply domain rules; emit events
3. Events feed projections that build read models
4. Read models are rebuilt from events — they are disposable caches

### 8. Projections — read models from event streams
- Build per-use-case read models; don't share projections across features
- Implement idempotent event handlers (handle replays safely)
- Use correlation IDs for tracing across projections
- Plan for full rebuild: projections must be rebuildable from scratch

### 9. Sagas — distributed transactions & long-running workflows
Use when: a business process spans multiple aggregates or services and requires compensating actions on failure.

Patterns:
- **Choreography:** each service reacts to events; no central coordinator
- **Orchestration:** a saga process manager issues commands and tracks state

Rules: sagas must be idempotent · always define compensation steps · use durable execution for crash resilience.

## Do not use this skill when

- The problem is simple CRUD with low business complexity
- You only need localized bug fixes
- There is no access to domain knowledge and no proxy product expert
- Strong immediate consistency is required everywhere and eventual consistency is unacceptable

## Output requirements

Always return:
- Scope and assumptions
- Current stage (strategic / tactical / evented)
- Explicit artifacts or code produced
- Open risks and next step recommendation
