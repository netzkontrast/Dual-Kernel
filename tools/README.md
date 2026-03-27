# Tools — CLI Reference

Python-based ETL pipeline for extracting, validating, and analyzing entities from the `Markdown-docs/` corpus into the `knowledge-graph/`.

All tools require the virtual environment:

```bash
source .venv/bin/activate
cd <repo-root>   # always run from repo root so relative paths resolve
```

---

## Pipeline Overview

```
Phase 1 — Extract
  source_scanner.py  →  xref_finder.py  →  conflict_diff.py  →  entity_generator.py

Phase 2 — Validate (run in parallel, all must pass before Phase 3)
  frontmatter_validator.py
  wikilink_checker.py
  consistency_checker.py

Phase 3 — Analyze & Report (run after validation passes)
  entity_stats.py
  relationship_graph.py
  chapter_mapper.py
  glossary_generator.py
  canon_resolver.py
```

---

## Phase 1: Extract

### `source_scanner.py`

Scans a single markdown file for entity mentions. Runs two-pass detection: regex for known entities (longest-first), then spaCy NER for unknowns. Overwrites `tools/output/source-inventory.json` on each run.

```bash
python tools/source_scanner.py --file Markdown-docs/<filename>.md
```

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--file PATH` | Yes | — | Markdown file to scan |

**Input:** Single `.md` file from `Markdown-docs/`
**Output:** `tools/output/source-inventory.json`

> Note: Runs one file at a time. For the full corpus use `parallel_ingestion.py` (see below).

---

### `xref_finder.py`

Reads the current inventory and detects potential conflicts: entities that appear with different numeric values or contradictory state descriptions across contexts.

```bash
python tools/xref_finder.py
```

No options. Reads from `tools/output/source-inventory.json`.

**Input:** `tools/output/source-inventory.json`
**Output:** `tools/output/cross-references.json`

---

### `conflict_diff.py`

Displays all detected conflicts in a formatted side-by-side view. Optionally saves each conflict as a markdown file for manual review.

```bash
python tools/conflict_diff.py [--save]
```

| Option | Description |
|--------|-------------|
| `--save` | Save each conflict report to `tools/output/diffs/<entity>-conflict.md` |

**Input:** `tools/output/cross-references.json`
**Output:** Console display; optionally `tools/output/diffs/*.md`

---

### `entity_generator.py`

Generates entity markdown files with YAML frontmatter from the current inventory. Detects related entities via co-occurrence in mention context. Overwrites existing entity files for entities in the current inventory.

```bash
python tools/entity_generator.py
```

No options.

**Input:** `tools/output/source-inventory.json` + `tools/output/cross-references.json`
**Output:** `knowledge-graph/<domain>/<kebab-case-id>.md` + domain `README.md` (MOC)

**Canon status rules applied:**
- Known entity with no conflicts → `confirmed`
- Entity in cross-references → `disputed`
- Unknown entity with no conflicts → `provisional`

---

## Phase 2: Validate

All three validators must pass (exit 0) before proceeding to Phase 3 or committing changes.

### `frontmatter_validator.py`

Validates YAML frontmatter schema on every entity file in `knowledge-graph/`.

```bash
python tools/frontmatter_validator.py knowledge-graph/
```

No options (argument ignored; uses `KG_DIR` constant internally).

**Checks:**
- Required fields: `title`, `id`, `domain`, `canon_status`, `sources`
- `domain` is a valid `DomainEnum` value
- `canon_status` is one of: `confirmed`, `provisional`, `disputed`, `uncertain`, `decanonized`

---

### `wikilink_checker.py`

Checks integrity of all `[[wikilinks]]` in the knowledge graph. Reports broken links and orphaned entities (no links point to them).

```bash
python tools/wikilink_checker.py knowledge-graph/
```

No options (argument ignored; uses `KG_DIR` constant internally).

**Checks:**
- All `[[target]]` links resolve to an existing entity file (slugified)
- Supports `[[Target|Alias]]` Obsidian syntax (alias after `|` is ignored)
- Orphan report: entities no other file links to (warning only, not an error)

---

### `consistency_checker.py`

Runs narrative consistency checks across all knowledge graph entities.

```bash
python tools/consistency_checker.py [--strict] [--output FILE] [--category LIST]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--strict` | off | Treat warnings as errors (non-zero exit) |
| `--output, -o FILE` | — | Save report to file instead of console |
| `--category, -c LIST` | all | Run only specific checks (comma-separated) |

**Check categories:**
- `character` — attribute stability across sources
- `timeline` — chronological ordering
- `location` — bidirectionality of location references
- `physics` — uniform physics entity domain placement
- `relationship` — symmetry of entity relationships
- `conflict` — orphaned disputed entities
- `domain` — entities placed in wrong domain

---

## Phase 3: Analyze & Report

### `entity_stats.py`

Generates a statistics report summarizing the current state of the knowledge graph and extraction pipeline.

```bash
python tools/entity_stats.py
```

No options.

**Input:** `knowledge-graph/` + `tools/output/source-inventory.json`
**Output:** `knowledge-graph/_index/extraction-report.md` + console

---

### `relationship_graph.py`

Generates an entity relationship visualization from `related` wikilinks in the knowledge graph.

```bash
python tools/relationship_graph.py [--output FILE] [--format mermaid|html] [--domain-filter LIST]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--output, -o FILE` | `knowledge-graph/_index/relationship-graph.md` | Output path |
| `--format mermaid\|html` | `mermaid` | Output format |
| `--domain-filter, -d LIST` | all | Comma-separated list of domains to include |

**Output:** Mermaid diagram or HTML page with entity relationships

---

### `chapter_mapper.py`

Maps entities to the chapters in which they appear, based on the chapter matrix source document.

```bash
python tools/chapter_mapper.py [--chapter-file PATH] [--update] [--output FILE]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--chapter-file PATH` | `Markdown-docs/KoharenzProtokoll39KapitelMatrix.md` | Chapter matrix source |
| `--update` | off | Write `first_appearance_chapter` / `last_referenced_chapter` back to entity files |
| `--output, -o FILE` | `knowledge-graph/_index/chapter-entity-matrix.md` | Output path |

---

### `glossary_generator.py`

Generates a bilingual German-English glossary from the built-in term list and optionally from discovered knowledge graph entities.

```bash
python tools/glossary_generator.py [--discover] [--output FILE]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--discover` | off | Augment built-in glossary with entity titles from `knowledge-graph/` |
| `--output, -o FILE` | `knowledge-graph/_index/glossary.md` | Output path |

---

### `canon_resolver.py`

Analyzes entity evidence and conflict severity to suggest (or auto-apply) canon status changes.

```bash
python tools/canon_resolver.py [--apply] [--min-confidence FLOAT] [--output FILE] [--status-filter STATUS]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--apply` | off | Write suggested status changes directly to entity files |
| `--min-confidence FLOAT` | `0.6` | Minimum confidence score (0.0–1.0) to apply a change |
| `--output, -o FILE` | — | Save resolution report to file |
| `--status-filter STATUS` | all | Only process entities with this current status (e.g., `disputed`) |

**Scoring:**
- Source score: 0.0–1.0 based on number of source references (capped at 5)
- Conflict severity: 0.0–1.0 based on conflict count and variant count

---

## Parallel Ingestion (Corpus-Scale)

### `parallel_ingestion.py`

Runs `source_scanner.py`-equivalent scanning across the full `Markdown-docs/` corpus in parallel using OS worker processes. Use this instead of the manual `for file in Markdown-docs/*.md` loop for large batches.

```bash
python tools/parallel_ingestion.py [--docs-dir DIR] [--workers N] [--output FILE] [--pattern GLOB]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--docs-dir DIR` | `Markdown-docs` | Directory containing source markdown files |
| `--workers N` | `4` | Number of parallel worker processes (1–32) |
| `--output FILE` | `tools/output/source-inventory.json` | Output path for merged inventory |
| `--pattern GLOB` | `*.md` | Glob pattern to select files within `--docs-dir` |

### `ingest_worker.py`

Internal worker process used by `parallel_ingestion.py`. Not intended for direct invocation.

---

## Shared Module

### `common.py`

Not a CLI tool. Provides shared Pydantic v2 models, constants, and helpers imported by all tools.

| Export | Type | Purpose |
|--------|------|---------|
| `DomainEnum` | Enum | Valid entity domains |
| `VALID_DOMAINS` | frozenset | Set of valid domain strings |
| `VALID_CANON_STATUSES` | frozenset | Valid canon status strings |
| `KNOWN_ENTITIES` | frozenset | Pre-defined entity names |
| `KNOWN_ENTITIES_REGEX` | Pattern | Compiled longest-first regex for entity matching |
| `DOMAIN_MAPPING` | dict | Entity name → domain overrides |
| `slugify(name)` | function | Convert entity name to kebab-case file ID |
| `guess_domain(name, tag)` | function | Infer domain from name/spaCy tag |
| `parse_frontmatter(path)` | function | Extract YAML frontmatter from a markdown file |
| `load_all_entities()` | function | Load all knowledge graph entities into a dict |
| `list_entity_files()` | function | Return all entity file paths (excludes READMEs and `_index/`) |
| `load_inventory(path)` | function | Load `source-inventory.json` |
| `load_conflicts(path)` | function | Load `cross-references.json` |
| `INVENTORY_PATH` | str | `tools/output/source-inventory.json` |
| `CONFLICTS_PATH` | str | `tools/output/cross-references.json` |
| `KG_DIR` | str | `knowledge-graph` |

---

## Output Files Reference

| File | Generated By | Purpose |
|------|-------------|---------|
| `tools/output/source-inventory.json` | `source_scanner.py` / `parallel_ingestion.py` | Entity mentions per scanned file |
| `tools/output/cross-references.json` | `xref_finder.py` | Detected entity conflicts |
| `tools/output/diffs/*.md` | `conflict_diff.py --save` | Per-entity conflict diff reports |
| `knowledge-graph/<domain>/<id>.md` | `entity_generator.py` | Entity files with YAML frontmatter |
| `knowledge-graph/<domain>/README.md` | `entity_generator.py` | Map of Content per domain |
| `knowledge-graph/_index/extraction-report.md` | `entity_stats.py` | Extraction statistics |
| `knowledge-graph/_index/relationship-graph.md` | `relationship_graph.py` | Entity relationship Mermaid diagram |
| `knowledge-graph/_index/chapter-entity-matrix.md` | `chapter_mapper.py` | Chapter-entity appearance matrix |
| `knowledge-graph/_index/glossary.md` | `glossary_generator.py` | Bilingual DE-EN glossary |

> `tools/output/` is gitignored. Do not commit pipeline intermediates.
