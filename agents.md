# Agents Architecture & Improvement Suggestions

> Back to [README](README.md) | See also: [CLAUDE.md](CLAUDE.md)

This document defines agent roles, workflows, and recommended improvements for working with the Kohärenz Protokoll repository.

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

### 2. Documentation Agent

**Purpose:** Maintain project documentation, READMEs, and navigational indexes.

**Responsibilities:**
- Keep `README.md`, `project.md`, `SETUP.md`, `Plan.md` in sync
- Regenerate `Markdown-docs/README.md` navigation index when documents change
- Update `knowledge-graph/*/README.md` (Map of Content) files after entity changes

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
- Will require significant conflict resolution for entities like Kael/Michael, AEGIS protocols, and DKT definitions

### B. Semantic Conflict Resolution Agent (High Priority)

**Problem:** Current conflict detection is surface-level (regex + keyword matching). Many conflicts are semantic -- the same concept described differently across documents.

**Recommendation:**
- Add embedding-based similarity scoring (e.g., sentence-transformers with a German model)
- Implement a "conflict resolution workspace" that presents grouped conflicts for batch review
- Auto-suggest `canon_status` based on document recency and consensus across sources

### C. Relationship Graph Visualization (Medium Priority)

**Problem:** Entity relationships exist as wikilinks in YAML but have no visual representation.

**Recommendation:**
- Generate a Mermaid or D3.js relationship graph from `knowledge-graph/` entity files
- Show domain clustering, conflict hotspots, and connection density
- Integrate as a GitHub Pages site or Obsidian canvas

### D. Chapter-Entity Mapping Agent (Medium Priority)

**Problem:** The `first_appearance_chapter` and `last_referenced_chapter` fields in YAML frontmatter are mostly empty.

**Recommendation:**
- Create a tool that maps entities to their chapter appearances using the 40-chapter structure in `40ChapterPlotModule.md`
- Generate a chapter-entity matrix showing which entities appear in which chapters
- Enable narrative arc analysis per entity

### E. Narrative Consistency Checker (Medium Priority)

**Problem:** With 94 documents and 39-40 chapters, consistency errors are inevitable (timeline contradictions, character attribute conflicts, location mismatches).

**Recommendation:**
- Build a rule-based consistency checker that validates:
  - Character attributes remain stable (or changes are documented)
  - Timeline events don't contradict across chapters
  - Location descriptions are consistent
  - Physics rules (DKT, Landauer) are applied uniformly

### F. Interactive Query Agent (Low Priority)

**Problem:** Finding information across 94 documents requires manual searching.

**Recommendation:**
- Build a RAG (Retrieval-Augmented Generation) interface over the corpus
- Allow natural language queries like "What is the relationship between Kael and Juna?" or "How does the Landauer Principle apply in KW3?"
- Index both `Markdown-docs/` and `knowledge-graph/` for comprehensive answers

### G. Multi-Language Documentation Agent (Low Priority)

**Problem:** Research documents are in German, tooling docs are in English. No systematic translation layer.

**Recommendation:**
- Auto-generate English summaries for each German research document
- Maintain a bilingual glossary of key terms (e.g., Riss = rift, Kernwelt = core world)
- Keep the glossary in `knowledge-graph/_index/glossary.md`

---

## Agent Interaction Patterns

### Sequential Pipeline (Current)
```
Scanner → XRef → Generator → Validator → Stats
```
Each step depends on the previous. Run in order.

### Parallel Review Pattern (Recommended)
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
Use file watchers to trigger validation on save. Useful during manual entity editing.

---

## Proposed New Tools

| Tool | Purpose | Input | Output |
|------|---------|-------|--------|
| `relationship_graph.py` | Generate entity relationship visualization | `knowledge-graph/` | SVG/HTML graph |
| `chapter_mapper.py` | Map entities to chapter appearances | `knowledge-graph/` + chapter docs | Chapter-entity matrix |
| `consistency_checker.py` | Validate narrative consistency rules | `knowledge-graph/` + `Markdown-docs/` | Consistency report |
| `glossary_generator.py` | Build bilingual term glossary | `knowledge-graph/` + `Markdown-docs/` | `_index/glossary.md` |
| `canon_resolver.py` | Semi-automated canon status resolution | Conflict data + sources | Updated entity files |

---

## Metrics & Quality Gates

### Current State
- **Entities extracted:** 15 / ~80+ expected
- **Corpus coverage:** 1/94 files (1%)
- **Conflict resolution:** 12 disputed, 0 confirmed
- **Wikilink integrity:** Not fully validated on full corpus

### Target State
- **Entities extracted:** 80+ core entities fully documented
- **Corpus coverage:** 94/94 files (100%)
- **Conflict resolution:** <10% disputed after manual review
- **Wikilink integrity:** 0 broken links, 0 orphaned files
- **Chapter mapping:** All entities mapped to chapter appearances

---

## Contributing as an Agent

When working on this repository:

1. **Always read `CLAUDE.md` first** -- it contains critical rules about content invention, schema, and German language preservation
2. **Run validators after changes** -- never commit entity files without passing `frontmatter_validator.py`
3. **Trace everything to sources** -- every claim in the knowledge graph must reference specific files and line numbers in `Markdown-docs/`
4. **Respect the domain taxonomy** -- use only valid domains from `DomainEnum` in `tools/common.py`
5. **Document your work** -- update `Process.log` with extraction steps and decisions
