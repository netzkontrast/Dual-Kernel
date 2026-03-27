---
name: ddd-context-mapping
description: "Map relationships between bounded contexts and define integration contracts using DDD context mapping patterns. Use when defining how services or contexts communicate, choosing between Partnership, Shared Kernel, Customer-Supplier, Conformist, or Anti-Corruption Layer patterns, preventing domain model leakage across service boundaries, planning ACL during monolith migration, clarifying upstream/downstream ownership, or designing integration contracts. Trigger keywords: context map, anti-corruption layer, ACL, upstream downstream, shared kernel, conformist, customer supplier, open host service, published language, integration contract, context integration, service boundary, domain leakage."
risk: safe
source: self
tags: "[ddd, context-map, anti-corruption-layer, integration]"
date_added: "2026-02-27"
---

# DDD Context Mapping

## Prerequisite

Bounded contexts must be defined via `@ddd-strategic-design` before mapping their relationships.

## Use this skill when

- Defining integration patterns between bounded contexts.
- Preventing domain model leakage across service boundaries.
- Planning anti-corruption layers during migration.
- Clarifying upstream and downstream ownership for contracts.
- Deciding whether to use a Conformist, ACL, or Open Host pattern.

## Do not use this skill when

- You have a single-context system with no integrations.
- You only need internal class design within one context.
- You are selecting cloud infrastructure tooling.

## Instructions

1. List all context pairs and dependency direction.
2. Choose a relationship pattern for each pair (see patterns below).
3. Define translation rules and ownership boundaries.
4. Add failure modes, fallback behavior, and versioning policy.
5. Hand off to `@ddd-tactical-patterns` to implement ACL and domain objects.

## Relationship patterns

| Pattern | When to use | Contract owner |
|---------|-------------|----------------|
| **Partnership** | Two contexts evolve together, joint planning | Both |
| **Shared Kernel** | Shared code explicitly owned and versioned | Both (high coordination cost) |
| **Customer-Supplier** | Downstream depends on upstream; upstream plans for downstream | Upstream |
| **Conformist** | Downstream accepts upstream model as-is | Upstream (no negotiation) |
| **Anti-Corruption Layer** | Downstream must protect its model from upstream | Downstream |
| **Open Host Service** | Upstream publishes a stable protocol for many consumers | Upstream |
| **Published Language** | Shared schema/format decoupled from either context model | Neutral |

## Subagents

| Task | Agent type | What to ask |
|------|------------|-------------|
| Find all cross-context dependencies | `Explore` | "Find all API calls, event subscriptions, shared database tables, and shared models between services in `[path]`. List direction of dependency." |
| Identify hidden couplings | `Explore` | "Search `[path]` for direct ORM model imports, shared constants, or inline HTTP calls that cross service boundaries." |
| Design the context map | `Plan` | "Given these service dependencies: `[list]`, assign a relationship pattern to each pair (Partnership, Customer-Supplier, Conformist, ACL, Open Host Service) with rationale." |

Run the two `Explore` scans in parallel before starting the mapping session.

## Mapping template

| Upstream context | Downstream context | Pattern | Contract owner | ACL needed |
|------------------|--------------------|---------|----------------|------------|
| Billing | Checkout | Customer-Supplier | Billing | Yes |
| Identity | Checkout | Conformist | Identity | No |
| Catalog | Search | Open Host Service | Catalog | No |

## ACL implementation checklist

- Define canonical domain model for the receiving context.
- Translate external terms into local ubiquitous language — never let external terms into the domain core.
- Keep ACL code at the boundary layer, not inside domain logic.
- Add contract tests for all mapped behavior.
- Document translation rules — what changes in upstream break the ACL.

## Output requirements

- Relationship map for all context pairs
- Contract ownership matrix
- Translation and anti-corruption decisions
- Known coupling risks and mitigation plan

## Examples

```text
Use @ddd-context-mapping to define how Checkout integrates with Billing,
Inventory, and Fraud contexts, including ACL and contract ownership.
```

## Next step

After defining contracts and ACL boundaries, use `@ddd-tactical-patterns`
to implement aggregates, domain events, and repositories inside each context.

## Limitations

- This skill does not replace API-level schema design.
- It does not guarantee organizational alignment by itself.
- It should be revisited when team ownership changes.
