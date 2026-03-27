---
description: Skill architecture tiers — when to use Tier 1, 2, or 3.
metadata:
  tags: [tier-1, tier-2, tier-3, architecture, structure]
---

# Skill Architecture Guide

Three tiers of skill complexity. Choose the simplest tier that fits the task.

---

## Tier 1 — Simple (Single File)

**Use when:** Single concept, one technique, one reference. Can be explained in <200 lines.

### Structure
```
my-skill/
└── SKILL.md          # Everything in one file, no references/ needed
```

### Characteristics
- No complex decision logic
- Frequently loaded (small token footprint is critical)
- User knows exactly what they need

### Checklist
- [ ] Fits in <200 lines
- [ ] Single focused purpose
- [ ] No `references/` directory needed
- [ ] Description uses "Use when…" pattern

### Example Frontmatter
```yaml
---
name: flatten-with-flags
description: Use when simplifying deeply nested conditionals with 3+ nesting levels.
triggers:
  - nested if
  - complex conditionals
  - early return
  - deep nesting
---
```

---

## Tier 2 — Expanded (Skill + References)

**Use when:** Multi-concept skill, 200–1000 lines of total content, or multiple workflows that benefit from progressive disclosure.

### Structure
```
my-skill/
├── SKILL.md                    # Core dispatcher (<500 lines)
└── references/
    ├── workflows.md            # Detailed step-by-step guides
    ├── examples.md             # Extended examples
    ├── troubleshooting.md      # Debug guide
    └── patterns.md             # Reference patterns
```

### Characteristics
- SKILL.md acts as a hub: orientates and links to references
- References loaded on-demand (only when needed)
- Clear table of contents in SKILL.md pointing to each reference
- Good for: domain guides, architecture patterns, multi-step workflows

### SKILL.md Pattern for Tier 2
```markdown
# My Skill

Brief 2-3 sentence description.

## Quick Decision
Use [Workflow A](references/workflows.md#a) for X.
Use [Workflow B](references/workflows.md#b) for Y.

## Reference Index
| Need | Read |
|------|------|
| Full workflow | [workflows.md](references/workflows.md) |
| Examples | [examples.md](references/examples.md) |
| Debugging | [troubleshooting.md](references/troubleshooting.md) |
```

### Checklist
- [ ] SKILL.md under 500 lines
- [ ] Each reference file has a table of contents if >100 lines
- [ ] References are loaded only when their section is needed
- [ ] No circular references between files
- [ ] All links in SKILL.md resolve to real files

---

## Tier 3 — Platform (Full Hierarchy + Subagents)

**Use when:** Covers 10+ products/domains, requires codebase analysis before acting, or has independent parallel workflows.

### Structure
```
my-skill/
├── SKILL.md                         # Master orchestrator (<500 lines)
└── references/
    ├── architecture/                # Tier/structure guidance
    ├── templates/                   # Skill templates per type
    ├── standards/                   # Rules and best practices
    ├── workflows/                   # Process guides
    ├── testing/                     # Validation guides
    ├── kaizen/                      # Improvement and debug guides
    ├── triggers_and_hooks/          # Hook mechanics
    ├── cso/                         # Discoverability
    └── anti-rationalization/        # Compliance enforcement
```

### Characteristics
- SKILL.md is a pure dispatcher: classifies intent, launches subagents, links to references
- Subagents handle heavy analysis (codebase scanning, quality audits, planning)
- Multiple parallel research agents before any writing begins
- Never proceeds without a research phase

### Subagent Pattern for Tier 3
```markdown
## Phase A — Research (always run first)

Spawn in parallel:

Agent(Explore, background=false):
  "Scan [target]. Extract [specific data]. Answer: [specific question]."

Agent(Explore, background=true):
  "Find all [X] in [path]. Summarize by [dimension]."

Wait for foreground agents before Phase B.
```

### Checklist
- [ ] SKILL.md under 500 lines (use references for everything else)
- [ ] Every workflow starts with a research/scan phase using subagents
- [ ] Parallel agents for independent queries
- [ ] Background agents only for work that doesn't gate the next step
- [ ] All subagent prompts are concrete and specific (not vague instructions)
- [ ] Includes an AUDIT workflow with scoring criteria
- [ ] Registered in settings.json

---

## Template Selection

After choosing a tier, select the matching content template from [templates/](../templates/):

| Skill type | Template | Use for |
|---|---|---|
| How-to guide | [technique.md](../templates/technique.md) | Step-by-step processes |
| Rule enforcement | [discipline.md](../templates/discipline.md) | Mandatory practices with anti-rationalization |
| Mental model | [pattern.md](../templates/pattern.md) | Recognizing and applying patterns |
| Documentation | [reference.md](../templates/reference.md) | API docs, lookup tables |
| Complex platform | [tier-3-platform.md](../templates/tier-3-platform.md) | Multi-workflow orchestrators |
