---
name: ddd-tactical-patterns
description: "Apply DDD tactical patterns in code using entities, value objects, aggregates, repositories, and domain events with explicit invariants. Use when translating domain rules into code structures, designing aggregate boundaries, enforcing invariants in domain objects, refactoring an anemic model into behavior-rich domain objects, defining repository contracts, modeling domain events, or implementing a rich domain layer. Trigger keywords: aggregate, aggregate root, value object, domain entity, invariant, anemic model, rich domain model, domain event, repository contract, domain service, factory, specification pattern, tactical DDD, domain layer."
risk: safe
source: self
tags: "[ddd, tactical, aggregates, value-objects, domain-events]"
date_added: "2026-02-27"
---

# DDD Tactical Patterns

## Prerequisite

Strategic boundaries must be stable before tactical design. Use `@ddd-strategic-design`
and `@ddd-context-mapping` first, then return here to implement within each context.

## Use this skill when

- Translating domain rules into code structures.
- Designing aggregate boundaries and invariants.
- Refactoring an anemic model into behavior-rich domain objects.
- Defining repository contracts and domain event boundaries.
- Deciding what is an entity vs a value object.

## Do not use this skill when

- You are still defining strategic boundaries.
- The task is only API documentation or UI layout.
- Full DDD complexity is not justified (check viability in `@domain-driven-design`).

## Instructions

1. Identify invariants first — design aggregates around them, not around data.
2. Model immutable value objects for validated domain concepts.
3. Keep domain behavior in domain objects, not controllers or services.
4. Emit domain events for meaningful state transitions.
5. Keep repositories at aggregate root boundaries only.

## Pattern checklist

### Aggregate design
- One aggregate root per transaction boundary
- Invariants enforced inside aggregate methods — never outside
- Avoid cross-aggregate synchronous consistency rules
- Reference other aggregates by ID only, never by direct object reference

### Value objects
- Immutable by default
- Validation at construction — throw on invalid input
- Equality by value, not identity
- Model domain concepts, not just primitives (e.g., `Money`, `Email`, not `number`, `string`)

### Repositories
- Persist and load aggregate roots only
- Expose domain-friendly query methods (e.g., `findByOrderId`, not `findWhere(...)`)
- Avoid leaking ORM entities into the domain layer
- One repository per aggregate root

### Domain events
- Past-tense event names (e.g., `OrderSubmitted`, `PaymentFailed`)
- Include minimal, stable event payloads
- Version event schema before breaking changes
- Raise events inside aggregate methods, dispatch at the boundary

## Examples

```typescript
class Order {
  private status: "draft" | "submitted" = "draft";

  submit(itemsCount: number): void {
    if (itemsCount === 0) throw new Error("Order cannot be submitted empty");
    if (this.status !== "draft") throw new Error("Order already submitted");
    this.status = "submitted";
    this.raise(new OrderSubmitted(this.id));
  }
}
```

```typescript
// Value object — equality by value, validation at construction
class Email {
  readonly value: string;

  constructor(raw: string) {
    if (!raw.includes("@")) throw new Error("Invalid email");
    this.value = raw.toLowerCase();
  }

  equals(other: Email): boolean {
    return this.value === other.value;
  }
}
```

## Next steps

- Use `@python-testing-patterns` or `@e2e-testing-patterns` to cover invariants with tests.
- Use `@cqrs-implementation` when read and write models need to diverge.
- Use `@event-sourcing-architect` when events must be the source of truth.

## Limitations

- This skill does not define deployment architecture.
- It does not choose databases or transport protocols.
- It should be paired with testing patterns for invariant coverage.
