---
name: ddd-strategic-design
description: "Design DDD strategic artifacts including subdomains, bounded contexts, and ubiquitous language for complex business domains. Use when classifying subdomains as core/supporting/generic, splitting a monolith into services, aligning teams with domain ownership, building a shared ubiquitous language with domain experts, defining context boundaries, or producing a domain model for a new system. Trigger keywords: subdomain classification, bounded context, core domain, ubiquitous language, team ownership, context boundary, domain boundary, monolith splitting, domain model, strategic DDD."
risk: safe
source: self
tags: "[ddd, strategic-design, bounded-context, ubiquitous-language]"
date_added: "2026-02-27"
---

# DDD Strategic Design

## Prerequisite

Run the viability check in `@domain-driven-design` before using this skill. Strategic design is only warranted when at least two of the viability criteria are met.

## Use this skill when

- Defining core, supporting, and generic subdomains.
- Splitting a monolith or service landscape by domain boundaries.
- Aligning teams and ownership with bounded contexts.
- Building a shared ubiquitous language with domain experts.

## Do not use this skill when

- The domain model is stable and already well bounded.
- You need tactical code patterns only.
- The task is purely infrastructure or UI oriented.

## Instructions

1. Extract domain capabilities and classify subdomains.
2. Define bounded contexts around consistency and ownership.
3. Establish a ubiquitous language glossary and anti-terms.
4. Capture context boundaries in ADRs before implementation.
5. Hand off to `@ddd-context-mapping` to define integration patterns between contexts.

## Required artifacts

- Subdomain classification table
- Bounded context catalog
- Glossary with canonical terms and anti-terms
- Boundary decisions with rationale

## Templates

### Subdomain classification

| Capability | Subdomain type | Why | Owner team |
|------------|----------------|-----|------------|
| Pricing | Core | Differentiates business value | Commerce |
| Identity | Supporting | Needed but not differentiating | Platform |
| Email delivery | Generic | Buy, don't build | Infrastructure |

### Bounded context catalog

| Context | Responsibility | Upstream dependencies | Downstream consumers |
|---------|----------------|----------------------|----------------------|
| Catalog | Product data lifecycle | Supplier feed | Checkout, Search |
| Checkout | Order placement and payment authorization | Catalog, Pricing | Fulfillment, Billing |

### Ubiquitous language

| Term | Definition | Context | Anti-terms (do not use) |
|------|------------|---------|--------------------------|
| Order | Confirmed purchase request | Checkout | Cart, Basket |
| Reservation | Temporary inventory hold | Fulfillment | Lock, Block |

## Examples

```text
Use @ddd-strategic-design to map our commerce domain into bounded contexts,
classify subdomains, and propose team ownership.
```

## Next step

After producing strategic artifacts, use `@ddd-context-mapping` to define
integration patterns and contracts between bounded contexts.

## Limitations

- This skill does not produce executable code.
- It cannot infer business truth without stakeholder input.
- It should be followed by context mapping and tactical design before implementation.
