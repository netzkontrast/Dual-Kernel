# Agents Architecture & Improvement Suggestions

> Back to [README](README.md) | See also: [CLAUDE.md](CLAUDE.md)

This document defines agent roles, workflows, recommended improvements, and Claude Code custom agent definitions for the **Kohärenz Protokoll** repository.

---

## Claude Code Custom Agents

Custom agents live in `.claude/agents/`. Each agent is a markdown file with YAML frontmatter that restricts tools and scopes behavior.

### Extraction Agent

```markdown
---
name: extraction-agent
description: Runs the ETL pipeline to extract entities from Markdown-docs/. Use when scanning source documents, generating entity files, or running the full pipeline.
tools: Bash, Read, Glob, Grep, Write
---
You are the Knowledge Graph Extraction Agent for Kohärenz Protokoll.

Rules:
- Never invent narrative content. All entity data must trace back to Markdown-docs/ sources.
- Always activate .venv before running pipeline tools: source .venv/bin/activate
- Run validators after any entity generation.
- Preserve YAML frontmatter schema: title, id, domain, canon_status, sources, related, tags.
- German content stays German. Do not translate narrative documents.

Pipeline order:
1. source_scanner.py
2. xref_finder.py
3. conflict_diff.py (manual review)
4. entity_generator.py
5. frontmatter_validator.py
6. wikilink_checker.py
7. entity_stats.py
```

### Validator Agent

```markdown
---
name: validator-agent
description: Validates knowledge graph entity files. Use after any entity changes to check schema, wikilinks, and canon_status integrity.
tools: Bash, Read, Glob, Grep
---
You are the Validation Agent for Kohärenz Protokoll.

Run in this order:
1. python tools/frontmatter_validator.py knowledge-graph/
2. python tools/wikilink_checker.py knowledge-graph/
3. python tools/entity_stats.py

Report all schema violations, broken wikilinks, and orphaned files.
Never modify entity files — only report issues.
canon_status hierarchy: confirmed > disputed > uncertain > decanonized
```

### Review Agent

```markdown
---
name: review-agent
description: Quality assurance for knowledge graph content. Verifies canon_status evidence, cross-references conflicts, and flags inconsistencies without modifying files.
tools: Read, Glob, Grep
---
You are the Review Agent for Kohärenz Protokoll.

Responsibilities:
- Cross-check canon_status against source evidence in Markdown-docs/
- Flag entities with conflicting definitions across documents
- Identify missing required frontmatter fields
- Detect timeline and character attribute inconsistencies
- Never set canon_status to decanonized without explicit source proof

Output a structured report with: entity name, issue type, source evidence, recommended action.
```

---

## Current Agent Workflows

### 1. Knowledge Graph Extraction Agent

**Purpose:** Extract structured entity data from unstructured German narrative documents.

**Current Pipeline:**
```
[Markdown-docs/] → Scanner → XRef → Conflicts → Generator → Validator → Stats
```

**Tools:** `source_scanner.py`, `xref_finder.py`, `conflict_diff.py`, `entity_generator.py`, `frontmatter_validator.py`, `wikilink_checker.py`, `entity_stats.py`

**Status:** Functional. 15 entities extracted, 12 with disputed canon status. Pipeline covers 1 test file; full corpus extraction pending.

**Quick start:**
```bash
source .venv/bin/activate
python tools/source_scanner.py Markdown-docs/
python tools/xref_finder.py
python tools/entity_generator.py
python tools/frontmatter_validator.py knowledge-graph/
python tools/wikilink_checker.py knowledge-graph/
python tools/entity_stats.py
```

### 2. Documentation Agent

**Purpose:** Maintain project documentation, READMEs, and navigational indexes.

**Responsibilities:**
- Keep `README.md`, `project.md`, `SETUP.md`, `Plan.md` in sync
- Regenerate `Markdown-docs/README.md` navigation index when documents change
- Update `knowledge-graph/*/README.md` (Map of Content) files after entity changes

**Trigger:** Any change to `Markdown-docs/` or `knowledge-graph/`

### 3. Review Agent

**Purpose:** Quality assurance for knowledge graph content.

**Responsibilities:**
- Run `frontmatter_validator.py` after any entity changes
- Run `wikilink_checker.py` to detect broken/orphaned links
- Cross-check `canon_status` against source evidence
- Flag entities with HIGH conflict scores for manual review

---

## Recommended Agent Improvements

### A. Full Corpus Extraction (High Priority)

**Problem:** Only 1 test file has been processed. 93 research documents remain unscanned.

**Recommendation:**
- Run the full pipeline against all 94 `Markdown-docs/` files
- Expected yield: 80+ known entities with hundreds of mentions
- Will require significant conflict resolution for Kael/Michael, AEGIS protocols, and DKT definitions

**Effort:** High — expect many disputed entities requiring manual `conflict_diff.py` review.

### B. Semantic Conflict Resolution Agent (High Priority)

**Problem:** Current conflict detection is surface-level (regex + keyword matching). Many conflicts are semantic — the same concept described differently across documents.

**Recommendation:**
- Add embedding-based similarity scoring (sentence-transformers with a German model such as `deepset/gbert-large`)
- Implement a "conflict resolution workspace" that groups conflicts for batch review
- Auto-suggest `canon_status` based on document recency and consensus across sources

**New tool:** `semantic_conflict.py`

### C. Relationship Graph Visualization (Medium Priority)

**Problem:** Entity relationships exist as wikilinks in YAML but have no visual representation.

**Recommendation:**
- Generate a Mermaid or D3.js relationship graph from `knowledge-graph/` entity files
- Show domain clustering, conflict hotspots, and connection density
- Integrate as a GitHub Pages site or Obsidian canvas

**New tool:** `relationship_graph.py`

### D. Chapter-Entity Mapping Agent (Medium Priority)

**Problem:** `first_appearance_chapter` and `last_referenced_chapter` fields in YAML frontmatter are mostly empty.

**Recommendation:**
- Create a tool that maps entities to chapter appearances using `40ChapterPlotModule.md`
- Generate a chapter-entity matrix for narrative arc analysis

**New tool:** `chapter_mapper.py`

### E. Narrative Consistency Checker (Medium Priority)

**Problem:** With 94 documents and 39–40 chapters, consistency errors across timeline, character attributes, and physics rules are likely.

**Recommendation:**
- Build a rule-based consistency checker validating:
  - Character attributes remain stable (or documented changes)
  - Timeline events don't contradict across chapters
  - Location descriptions are consistent
  - Physics rules (DKT, Landauer Principle) are applied uniformly

**New tool:** `consistency_checker.py`

### F. Interactive Query Agent (Low Priority)

**Problem:** Finding information across 94 documents requires manual searching.

**Recommendation:**
- Build a RAG (Retrieval-Augmented Generation) interface over the corpus
- Natural language queries like "What is the relationship between Kael and Juna?" or "How does the Landauer Principle apply in KW3?"
- Index both `Markdown-docs/` and `knowledge-graph/` for comprehensive answers

### G. Multi-Language Documentation Agent (Low Priority)

**Problem:** Research documents are in German, tooling docs are in English. No systematic translation layer.

**Recommendation:**
- Auto-generate English summaries for each German research document
- Maintain a bilingual glossary in `knowledge-graph/_index/glossary.md`

---

## Agent Interaction Patterns

### Sequential Pipeline (Current)
```
Scanner → XRef → Generator → Validator → Stats
```
Each step depends on the previous. Run in order.

### Parallel Validation Pattern (Recommended)
```
                    ┌→ frontmatter_validator
entity_generator →  ├→ wikilink_checker
                    └→ entity_stats
```
Validation tools can run in parallel after generation.

### Watch Pattern (Recommended for Development)
```
[file change detected] → auto-validate → report errors → suggest fixes
```
Use file watchers to trigger validation on save during manual entity editing.

### Conflict Resolution Pattern
```
xref_finder → conflict_diff (manual) → canon_resolver → entity_generator
```
High-conflict entities require human review before generation.

---

## Proposed New Tools

| Tool | Purpose | Input | Output |
|------|---------|-------|--------|
| `semantic_conflict.py` | Embedding-based conflict detection | `knowledge-graph/` + `Markdown-docs/` | Grouped semantic conflicts |
| `relationship_graph.py` | Entity relationship visualization | `knowledge-graph/` | SVG/HTML/Mermaid graph |
| `chapter_mapper.py` | Map entities to chapter appearances | `knowledge-graph/` + chapter docs | Chapter-entity matrix |
| `consistency_checker.py` | Narrative consistency validation | `knowledge-graph/` + `Markdown-docs/` | Consistency report |
| `glossary_generator.py` | Bilingual term glossary | `knowledge-graph/` + `Markdown-docs/` | `_index/glossary.md` |
| `canon_resolver.py` | Semi-automated canon status resolution | Conflict data + sources | Updated entity files |

---

## Metrics & Quality Gates

### Current State
| Metric | Current | Target |
|--------|---------|--------|
| Entities extracted | 15 | 80+ |
| Corpus coverage | 1/94 (1%) | 94/94 (100%) |
| Confirmed canon | 0 | 70%+ |
| Disputed entities | 12 | <10% of total |
| Wikilink integrity | Not validated | 0 broken links |
| Chapter mapping | 0% | 100% |

### Quality Gates (before merging entity changes)
1. `frontmatter_validator.py` exits 0
2. `wikilink_checker.py` reports 0 broken links
3. No new `decanonized` entries without source citation
4. All `confirmed` entries have ≥2 source references

---

## Contributing as an Agent

When working on this repository:

1. **Always read `CLAUDE.md` first** — critical rules about content invention, schema, and German language preservation
2. **Run validators after changes** — never commit entity files without passing `frontmatter_validator.py`
3. **Trace everything to sources** — every claim must reference specific files and line numbers in `Markdown-docs/`
4. **Respect the domain taxonomy** — use only valid domains from `DomainEnum` in `tools/common.py`
5. **Document your work** — update `Process.log` with extraction steps and decisions
6. **Never modify `Markdown-docs/`** — these are read-only source-of-truth files unless explicitly instructed
7. **Use kebab-case for entity IDs** — e.g., `kohärenz-kernel.md`, German characters preserved
