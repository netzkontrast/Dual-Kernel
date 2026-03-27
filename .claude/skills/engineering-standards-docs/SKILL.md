---
name: engineering-standards-docs
description: "Unified engineering standards skill. Covers documentation generation, ADRs, API design patterns, architecture (Clean/Hexagonal/Microservices), backend guidelines, and senior-level system design."
risk: safe
source: self
tags: "[architecture, documentation, api-design, microservices, adr, backend, standards]"
date_added: "2026-03-27"
triggers: architecture, ADR, architecture decision record, documentation, API design, REST, GraphQL, tRPC, microservices, clean architecture, hexagonal, backend guidelines, system design, openapi, swagger, service mesh, layered architecture
---

# Engineering Standards & Documentation

Unified dispatcher for architecture decisions, API design, documentation, and backend engineering standards.
Replaces: `documentation-generation-doc-generate`, `documentation-templates`, `architecture-decision-records`, `architecture-patterns`, `microservices-patterns`, `backend-dev-guidelines`, `senior-architect`, `senior-fullstack`, `api-patterns`.

## ⚡ Decision Tree — What are you designing?

### 1. Architecture pattern selection

| Complexity | Pattern | When to use |
|------------|---------|-------------|
| Low–Medium | Layered (MVC/routes→services→repos) | CRUD-heavy, small teams, rapid delivery |
| Medium | Clean Architecture | Business logic must be framework-independent |
| Medium–High | Hexagonal (Ports & Adapters) | Multiple I/O adapters, strong testability required |
| High | Microservices | Independent scaling, team autonomy, polyglot |

**Default for new backends:** Layered architecture. Only move to Clean/Hexagonal when testability pain is real, not hypothetical.

**Layered dependency rule:** `routes → controllers → services → repositories → DB`. Never skip layers. Never import upward.

**Clean Architecture rule:** Inner rings (domain, use cases) must not import outer rings (frameworks, DB, HTTP). Dependency injection at boundaries.

### 2. API design

**Protocol selection:**
- REST: default for public APIs, simple CRUD, mobile clients
- GraphQL: complex nested data, multiple clients with different data needs
- tRPC: TypeScript monorepo with shared types, internal services

**REST conventions:**
- Resources are nouns: `/orders`, `/users/{id}` (not `/getOrder`)
- Use standard HTTP verbs and status codes correctly
- POST 201 · GET 200 · PUT/PATCH 200 · DELETE 204 · not found 404 · validation 422 · server error 500
- Pagination: cursor-based for large/real-time datasets; offset for stable, small sets
- Versioning: URI prefix (`/v1/`) for breaking changes; avoid when possible

**Response envelope (errors must be consistent):**
```json
{
  "data": { ... },
  "error": null,
  "meta": { "page": 1, "total": 42 }
}
```

### 3. Architecture Decision Records (ADRs)

Create an ADR whenever: a significant technical decision is made · a decision reverses a previous one · a controversial trade-off is accepted.

**ADR template:**
```markdown
# ADR-NNN: <Title>

## Status
Proposed | Accepted | Deprecated | Superseded by ADR-NNN

## Context
What situation forced this decision?

## Decision
What was decided? Be specific.

## Consequences
**Positive:** ...
**Negative:** ...
**Risks:** ...
```

Store in `docs/adr/` or `architecture/decisions/`. Number sequentially. Never delete; mark as Superseded.

### 4. Microservices design

**Split by:** bounded context / domain capability (not by technical layer).

**Inter-service communication:**
- Synchronous (request/response): REST or gRPC — use for queries needing immediate results
- Asynchronous (events): Kafka / RabbitMQ — use for state changes and workflows

**Resilience patterns:**
- Circuit breaker: stop calling a failing service; fail fast
- Retry with backoff: idempotent operations only; set a limit (3–5 retries max)
- Bulkhead: isolate thread pools per downstream service
- Timeout: every external call must have a timeout

**Data isolation:** each service owns its data store. Never share a database between services.

### 5. Backend development standards (Node.js / Express / TypeScript)

Layer rules:
- **Routes:** HTTP plumbing only; delegate to controllers immediately
- **Controllers:** validate input, call one service method, return response
- **Services:** business logic; no HTTP or DB concerns
- **Repositories:** DB access only; return domain objects, not raw DB records

Code standards:
- All inputs validated at the HTTP boundary (zod / joi / class-validator)
- Errors propagated as typed exceptions; never `throw new Error("string")`
- Logging: structured JSON (`pino` / `winston`); never `console.log` in production
- Env config: all config from environment; fail fast on missing required vars

### 6. Documentation generation

**What to document:**
- Public APIs: OpenAPI 3.x spec (generated from code annotations when possible)
- Architecture: ADRs + diagrams (Mermaid / PlantUML embedded in Markdown)
- Runbooks: operational procedures in `docs/runbooks/`
- Code: only non-obvious *why*, never *what*

**README minimum:**
```markdown
# Project Name
One sentence description.

## Quick start
<3 commands to run locally>

## Architecture
<link to ADR index or inline diagram>

## Contributing
<branch naming, commit format, PR checklist>
```

**This project's docs standard:** German content in `Markdown-docs/`; English in tooling and meta-docs. Entity files in `knowledge-graph/` follow the YAML frontmatter schema defined in `CLAUDE.md`.

## Do not use this skill when
- You need framework-specific implementation details → use `python-backend-engineering` or `frontend-developer`
- You are doing DDD strategic/tactical modeling → use `architecture-ddd-event-sourcing`
- The task is a one-line code change with no design implications
