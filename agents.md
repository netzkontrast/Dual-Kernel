# AGENTS.md — Kohärenz Protokoll

For detailed project context, see [`CLAUDE.md`](CLAUDE.md). This file documents agent workflows, tools, and quality gates for the **Kohärenz Protokoll** (Coherence Protocol) knowledge graph extraction pipeline.

---

## Project Overview

| Property | Value |
|----------|-------|
| **Language** | Python 3.10+ |
| **Build System** | `tools/common.py` with Pydantic v2 + Click CLI |
| **Content** | 94 German narrative documents + YAML entity files |
| **Domains** | `character`, `alter-system`, `world`, `physics`, `aegis`, `narrative`, `style`, `philosophy`, `theme`, `mechanic`, `juna`, `fundament`, `mathematics` |
| **Entry Point** | `.venv/bin/activate` then `python tools/<script>.py` |
| **Validators** | `frontmatter_validator.py`, `wikilink_checker.py`, `entity_stats.py` |

---

## Verified Agent Commands

| Agent | Command | Purpose | Verified |
|-------|---------|---------|----------|
| Extraction | `source .venv/bin/activate && python tools/source_scanner.py Markdown-docs/` | Scan narratives for entity mentions | ✓ |
| Extraction | `python tools/xref_finder.py` | Find cross-references and conflicts | ✓ |
| Extraction | `python tools/entity_generator.py` | Generate entity files from scan results | ✓ |
| Validator | `python tools/frontmatter_validator.py knowledge-graph/` | Validate YAML schema | ✓ |
| Validator | `python tools/wikilink_checker.py knowledge-graph/` | Check link integrity | ✓ |
| Stats | `python tools/entity_stats.py` | Generate statistics report | ✓ |
| Conflict | `python tools/conflict_diff.py` | Manual conflict review (interactive) | ✓ |

---

## ETL Pipeline (Sequential Order)

```bash
source .venv/bin/activate
python tools/source_scanner.py Markdown-docs/
python tools/xref_finder.py
# [Manual review of conflicts via conflict_diff.py if needed]
python tools/entity_generator.py
python tools/frontmatter_validator.py knowledge-graph/
python tools/wikilink_checker.py knowledge-graph/
python tools/entity_stats.py
```

**Exit on first failure.** Validators must pass before committing entity changes.

---

## File Pointers (Do Not Duplicate)

| What | Where |
|------|-------|
| Critical project rules | [`CLAUDE.md`](CLAUDE.md) — **read first** |
| Project documentation | [`README.md`](README.md), [`project.md`](project.md), [`SETUP.md`](SETUP.md), [`Plan.md`](Plan.md) |
| Domain taxonomy | [`tools/common.py`](tools/common.py) — `DomainEnum` class |
| Entity schema | [`tools/common.py`](tools/common.py) — `DomainEnum` + Plan.md section 6 |
| Key entities | [`CLAUDE.md`](CLAUDE.md) — Key Entities Reference table |
| Test fixture | [`tools/fixtures/test-source.md`](tools/fixtures/test-source.md) |
| Entity files | [`knowledge-graph/<domain>/`](knowledge-graph/) — live YAML files |
| Source narratives | [`Markdown-docs/`](Markdown-docs/) — **read-only** |

---

## Extraction Workflow

### 1. Scan Documents
```bash
python tools/source_scanner.py Markdown-docs/
```
**Input:** All `.md` files in `Markdown-docs/`
**Output:** Entity mention list + conflict map
**Next:** Review conflicts via `conflict_diff.py`

### 2. Find Cross-References
```bash
python tools/xref_finder.py
```
**Input:** Scanner output
**Output:** Cross-reference graph
**Next:** Analyze for connection patterns

### 3. Resolve High-Conflict Entities
```bash
python tools/conflict_diff.py
```
**Input:** Conflict data from xref_finder
**Output:** Conflict resolution decisions
**Manual step:** Review > 5 conflicting definitions per entity

### 4. Generate Entities
```bash
python tools/entity_generator.py
```
**Input:** Scanner + conflict resolutions
**Output:** `knowledge-graph/<domain>/*.md` entity files with YAML frontmatter
**Next:** Validate schema

### 5. Validate Frontmatter
```bash
python tools/frontmatter_validator.py knowledge-graph/
```
**Input:** Entity files
**Output:** Pass/fail report
**Fails on:** Missing required fields, invalid domains, malformed YAML

### 6. Check Wikilinks
```bash
python tools/wikilink_checker.py knowledge-graph/
```
**Input:** Entity files
**Output:** Broken link report
**Fails on:** Dead wikilinks, orphaned files

### 7. Generate Statistics
```bash
python tools/entity_stats.py
```
**Input:** Entity files
**Output:** Coverage report, domain distribution, conflict summary

---

## Quality Gates (Before Commit)

| Gate | Command | Required |
|------|---------|----------|
| YAML Schema | `python tools/frontmatter_validator.py knowledge-graph/` | ✓ Exit 0 |
| Wikilinks | `python tools/wikilink_checker.py knowledge-graph/` | ✓ 0 broken links |
| Canon Evidence | Source citation check in conflict_diff review | ✓ No `decanonized` without proof |
| Statistics | `python tools/entity_stats.py` | ✓ Report generated |

**Do not commit** if any quality gate fails.

---

## Domain Taxonomy

See [`tools/common.py`](tools/common.py) for the `DomainEnum` class.

| Domain | Examples | Entities |
|--------|----------|----------|
| `character` | Kael, Juna, Michael, Sophia | Characters, personas, identities |
| `alter-system` | Kael's alters, AEGIS-mirror | Fragmented consciousnesses |
| `world` | Kernwelt, Überwelt, Prototopia | Locations, worlds, dimensions |
| `physics` | DKT (Dual Kernel Theory), Kohärenz-Kernel | Physical laws, theories |
| `aegis` | AEGIS, Primal Directive | AI antagonist and rules |
| `narrative` | Narrative arcs, plot points | Story structure |
| `style` | Writing conventions, tone | Stylistic choices |
| `philosophy` | Consciousness, identity, freedom | Philosophical concepts |
| `theme` | Fragmentation, autonomy, control | Thematic threads |
| `mechanic` | K-J Verbindung, resonance | Narrative mechanics |
| `juna` | Juna connection mechanics | External/real connection |
| `fundament` | Riss (rift), primary concepts | Foundational concepts |
| `mathematics` | Monster group, topological framework | Mathematical structures |

---

## YAML Frontmatter Schema

All entity files require:

```yaml
---
title: Entity Name
id: kebab-case-id
domain: character | alter-system | ... (from DomainEnum)
canon_status: confirmed | disputed | uncertain | decanonized
sources:
  - Markdown-docs/file.md:line
  - Markdown-docs/other.md:line-range
related:
  - related-entity-id
tags:
  - tag1
  - tag2
---
```

**Canon Status Hierarchy:** `confirmed` > `disputed` > `uncertain` > `decanonized`

Never set `decanonized` without source proof.

---

## Recommended Improvements

| Priority | Task | Effort | Status |
|----------|------|--------|--------|
| High | Full corpus extraction (94 files, currently 1) | High | Pending |
| High | Semantic conflict resolution (embeddings) | High | Proposed |
| Medium | Relationship graph visualization (Mermaid) | Medium | Proposed |
| Medium | Chapter-entity mapping (narrative arcs) | Medium | Proposed |
| Medium | Narrative consistency checker (rules) | Medium | Proposed |
| Low | Interactive query agent (RAG over corpus) | High | Proposed |
| Low | Bilingual glossary generator (German/English) | Medium | Proposed |

See [`agents.md`](agents.md) section "Recommended Agent Improvements" for details.

---

## Agent Interaction Patterns

### Sequential Pipeline (Current)
```
Scanner → XRef → Generator → Validator → Stats
```
Each step depends on the previous.

### Parallel Validation (Recommended)
```
                    ┌→ frontmatter_validator
entity_generator →  ├→ wikilink_checker
                    └→ entity_stats
```
Run validators in parallel after generation.

### Conflict Resolution Pattern
```
xref_finder → conflict_diff (manual) → entity_generator
```
High-conflict entities require human review.

---

## Contributing Rules

1. **Read `CLAUDE.md` first** — critical rules about invention, schema, German language
2. **Never invent content** — trace all data to `Markdown-docs/` sources
3. **Run validators** — commit only after `frontmatter_validator.py` passes
4. **Use kebab-case IDs** — e.g., `kohärenz-kernel.md` (German chars preserved)
5. **Respect domain taxonomy** — only use valid domains from `tools/common.py`
6. **Document sources** — every claim needs file + line reference
7. **German narrative, English tooling** — do not translate research documents
8. **`Markdown-docs/` is read-only** — modify only when explicitly instructed

---

## Current Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Entities extracted | 15 | 80+ |
| Corpus coverage | 1/94 (1%) | 94/94 (100%) |
| Confirmed canon | 0 | 70%+ |
| Disputed entities | 12 | <10% |
| Broken wikilinks | TBD | 0 |
| Chapter mapping | 0% | 100% |

---

## References

| File | Purpose |
|------|---------|
| [`CLAUDE.md`](CLAUDE.md) | Project conventions, critical rules |
| [`Plan.md`](Plan.md) | Project roadmap, section 6 has schema details |
| [`tools/common.py`](tools/common.py) | Domain enum, Pydantic models, shared utilities |
| [`knowledge-graph/`](knowledge-graph/) | Entity files organized by domain |
| [`Markdown-docs/`](Markdown-docs/) | Source narratives (read-only) |
| [`tools/fixtures/test-source.md`](tools/fixtures/test-source.md) | Test fixture for validation |
