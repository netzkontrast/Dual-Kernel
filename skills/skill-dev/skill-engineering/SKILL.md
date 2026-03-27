---
name: skill-engineering
description: "MANDATORY: Use this skill when the user wants to create, update, improve, refactor, or test an agent skill, or when engaging in Kaizen (continuous improvement) of the agent's workflows."
category: meta
risk: unknown
source: community
date_added: "2024-03-27"
triggers: skill creation, skill improvement, kaizen, writing skills, new skill, refactor skill, optimize skill
---

<!--
Refactoring Note: This `skill-engineering` skill is a comprehensive merger of four previously distinct skills: `skill-creator`, `writing-skills`, `skill-developer`, and `kaizen`.
By bringing them together, we create a single "source of truth" for the AI when performing any meta-task related to modifying its own behaviors, templates, or hooks.
The overlap between the previous skills (e.g., skill-creator acting as a generator and writing-skills providing the templates/standards) is resolved here by grouping content logically under `references/`.
-->

# Skill Engineering & Kaizen

You are acting as an expert **Agentic Engineer**. This skill is the central dispatcher for creating, refining, debugging, and continuously improving (Kaizen) AI agent skills and workflows.

## ⚡ Quick Decision Tree

### 1. Creating a NEW Skill
- Is it simple (single file, <200 lines)? → Review [Tier 1 Architecture](references/architecture/README.md) (Simple)
- Is it complex (multi-concept, 200-1000 lines)? → Review [Tier 2 Architecture](references/architecture/README.md) (Expanded)
- Is it a massive platform (10+ products)? → Review [Tier 3 Architecture](references/architecture/README.md) (Platform)
- *If you need an automated workflow/script to generate this, refer to [Workflows](references/workflows/workflows.md).*

### 2. Improving an EXISTING Skill (Kaizen)
- **Too long/Monolithic?** → Modularize using [Progressive Disclosure](references/templates/tier-3-platform.md).
- **AI ignores the rules?** → Apply [Anti-Rationalization techniques](references/anti-rationalization/README.md) and strict [Standards](references/standards/README.md).
- **Agents aren't triggering it?** → Optimize using [CSO (Claude Search Optimization)](references/cso/README.md) and [Trigger Types](references/triggers_and_hooks/TRIGGER_TYPES.md).
- **Need general process improvement?** → Apply [Kaizen Principles](references/kaizen/kaizen_principles.md).

### 3. Debugging & Testing
- Use [Troubleshooting Guide](references/kaizen/TROUBLESHOOTING.md) to fix broken hooks or misfiring skills.
- Use [Testing Guide](references/testing/README.md) and [Subagents Testing](references/testing/testing-skills-with-subagents.md) to verify compliance.

## 📚 Component Index

| Domain | Purpose | Key References |
|--------|---------|----------------|
| **Kaizen & Rules** | Continuous improvement of project/codebase. | [Kaizen Principles](references/kaizen/kaizen_principles.md), [Anthropic Best Practices](references/standards/anthropic-best-practices.md) |
| **Triggers & Hooks** | How to ensure skills fire exactly when needed. | [Hook Mechanisms](references/triggers_and_hooks/HOOK_MECHANISMS.md), [CSO](references/cso/README.md) |
| **Templates** | Standardized structures for different skill types. | [Technique](references/templates/technique.md), [Discipline](references/templates/discipline.md), [Pattern](references/templates/pattern.md) |
| **Workflows** | Interactive processes for generating/deploying skills. | [Workflows](references/workflows/workflows.md), [Output Patterns](references/workflows/output-patterns.md) |

## ✅ Pre-Deploy Checklist (MANDATORY)

Before deploying or updating any skill, verify:
1. `name` field in YAML matches the directory name exactly (kebab-case).
2. `SKILL.md` filename is ALL CAPS.
3. Description starts with "Use when..." or clearly defines the purpose.
4. `triggers` in YAML has 3+ relevant keywords.
5. The core `SKILL.md` file is < 500 lines (use progressive disclosure via `references/` for extra content).
6. Required Frontmatter exists:
   ```yaml
   ---
   name: [skill-name]
   description: Use when [specific situation occurs].
   ---
   ```

## 🛠️ Execution

When asked to create or improve a skill, follow the **RED-GREEN-REFACTOR** cycle for prompt engineering:
1. Identify the goal or failure mode (Kaizen).
2. Select the right template and standards.
3. Apply CSO for discoverability.
4. Add Anti-Rationalization rules if it's a disciplinary skill.
5. Test functionality using subagents or dummy tasks.
