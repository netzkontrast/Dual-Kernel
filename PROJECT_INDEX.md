# Project Index: Kohärenz Protokoll

Generated: 2026-03-29

**Narrative fiction project** with a Python-based knowledge graph extraction pipeline.
Primary content language: **German**. Tooling/docs: English.

---

## Project Structure

```
Dual-Kernel/
├── Markdown-docs/          # 94 German source documents (READ-ONLY)
├── knowledge-graph/        # 177 generated entity files (YAML frontmatter + MD)
│   ├── _index/             # Generated reports (glossary, chapter matrix, graph)
│   ├── aegis/              # 39 entities — AEGIS AI antagonist system
│   ├── character/          # 53 entities — Characters (Kael, Juna, Lex, etc.)
│   ├── fundament/          # 43 entities — Core concepts (Riss, DKT, K0/K1)
│   ├── world/              # 36 entities — Settings (KW1-4, zones, locations)
│   ├── mechanic/           # 2 entities  — Story mechanics
│   ├── physics/            # 1 entity
│   └── narrative/          # 1 entity
├── tools/                  # 15 Python pipeline scripts
│   └── output/             # Runtime-only generated artifacts (gitignored)
├── Markdown-docs/README.md # Source document index
├── docs/                   # PDF backups (do not modify)
├── _episodic/              # Mnemonic memory (MIF Level 3 format)
├── refactor/               # Active refactoring planning docs
├── schemas/                # MIF Level 3 YAML schema
└── .claude/                # Claude Code config: hooks, skills, settings
```

---

## Entry Points

| Script | CLI Command | Purpose |
|--------|-------------|---------|
| `tools/source_scanner.py` | `python tools/source_scanner.py --file <path>` | Phase 1: Scan MD for entities |
| `tools/parallel_ingestion.py` | `python tools/parallel_ingestion.py` | Phase 1 (parallel): All 94 docs |
| `tools/xref_finder.py` | `python tools/xref_finder.py` | Phase 1: Detect conflicts |
| `tools/conflict_diff.py` | `python tools/conflict_diff.py` | Phase 1: Interactive conflict review |
| `tools/entity_generator.py` | `python tools/entity_generator.py` | Phase 1→2: Generate entity files |
| `tools/frontmatter_validator.py` | `python tools/frontmatter_validator.py knowledge-graph/` | Phase 2: Validate YAML schema |
| `tools/wikilink_checker.py` | `python tools/wikilink_checker.py knowledge-graph/` | Phase 2: Check link integrity |
| `tools/consistency_checker.py` | `python tools/consistency_checker.py knowledge-graph/` | Phase 2: Narrative consistency |
| `tools/entity_stats.py` | `python tools/entity_stats.py` | Phase 3: Stats report |
| `tools/relationship_graph.py` | `python tools/relationship_graph.py` | Phase 3: Mermaid graph |
| `tools/chapter_mapper.py` | `python tools/chapter_mapper.py` | Phase 3: Chapter matrix |
| `tools/glossary_generator.py` | `python tools/glossary_generator.py --discover` | Phase 3: DE-EN glossary |
| `tools/canon_resolver.py` | `python tools/canon_resolver.py --apply` | Phase 3: Auto-resolve canon |

Setup: `./setup.sh` (creates `.venv`, installs deps, downloads `de_core_news_lg`)

---

## Core Modules

### `tools/common.py` — Shared infrastructure
- **Pydantic models:** `ScannedFile`, `Entity`, `Mention`, `FileMentionsExport`, `EntityExport`, `SourceInventoryExport`
- **Enums:** `DomainEnum` (13 domains), `VALID_CANON_STATUSES` (5 statuses)
- **Constants:** `KG_DIR`, `OUTPUT_DIR`, `INVENTORY_PATH`, `CONFLICTS_PATH`, `KNOWN_ENTITIES_LIST` (~120 entities), `KNOWN_ENTITIES_REGEX`
- **Functions:** `guess_domain()`, `slugify()`, `get_context()`, `build_mention()`, `load_inventory()`, `load_conflicts()`, `parse_frontmatter()`, `list_entity_files()`, `load_all_entities()`
- **NLP:** spaCy `de_core_news_lg` — two-pass detection (regex → NER, longest-first greedy)

### `tools/source_scanner.py` — Entity extraction
- Scans single markdown file, outputs `tools/output/source-inventory.json`
- Uses `bisect_right` on `line_offsets` for O(log N) character-to-line mapping

### `tools/ingest_worker.py` — Parallel worker
- Per-process worker for `parallel_ingestion.py`, mirrors scanner logic

### `tools/parallel_ingestion.py` — Batch orchestrator
- `ProcessPoolExecutor` over all 94 docs, merges worker results

---

## ETL Pipeline (3 Phases)

```
Phase 1: Extract
  Markdown-docs/*.md → source_scanner / parallel_ingestion
  → tools/output/source-inventory.json
  → xref_finder → tools/output/cross-references.json
  → conflict_diff (interactive) → tools/output/conflicts-resolved.json
  → entity_generator → knowledge-graph/<domain>/*.md

Phase 2: Validate (EXIT ON FIRST FAILURE — do not proceed to Phase 3)
  frontmatter_validator  → YAML schema compliance
  wikilink_checker       → [[entity]] link integrity
  consistency_checker    → Narrative rules

Phase 3: Analyze (run after validation passes)
  entity_stats           → tools/output/extraction-report.md
  relationship_graph     → knowledge-graph/_index/relationship-graph.md
  chapter_mapper         → knowledge-graph/_index/chapter-entity-matrix.md
  glossary_generator     → knowledge-graph/_index/glossary.md
  canon_resolver         → suggests/applies canon_status changes
```

---

## Entity Schema (YAML Frontmatter)

Every `knowledge-graph/<domain>/<id>.md` requires:

```yaml
title: string
id: kebab-case (must match filename)
domain: character|alter-system|world|physics|aegis|narrative|style|
        philosophy|theme|mechanic|juna|fundament|mathematics
canon_status: confirmed > provisional > disputed > uncertain > decanonized
sources:
  - Markdown-docs/file.md:42
related:
  - entity-id (no .md)
tags: []
```

---

## Key Entities

| Entity | Domain | Role |
|--------|--------|------|
| Kael | character | Protagonist, fragmented identity (TSDP) |
| Juna | character | External anchor / real-world connection |
| AEGIS | aegis | Superintelligence antagonist |
| Primal Directive | aegis | AEGIS core directive |
| Riss | fundament | Central concept: rift/fragmentation |
| DKT / Dual-Kernel | physics | Dual Kernel Theory |
| K1 (Kohärenz-Kernel) | physics | Coherence kernel |
| K0 (Kollaps-Kernel) | physics | Collapse kernel |
| Monster group | mathematics | Topological narrative framework |
| K-J Verbindung | mechanic | Kael-Juna connection mechanism |

---

## Configuration

| File | Purpose |
|------|---------|
| `requirements.txt` | Python deps: spacy, PyYAML, rich, click |
| `setup.sh` | One-time venv + dep setup |
| `.gitignore` | Excludes `.venv/`, `tools/output/`, `__pycache__/`, caches |
| `.claude/settings.json` | Claude Code permissions + hooks |
| `.claude/hooks/session-start.sh` | Auto-setup on Claude Code web sessions |
| `skills-lock.json` | Pinned Claude Code skill versions |
| `schemas/mif_level3_agent_trace.yaml` | MIF Level 3 memory schema |

---

## Documentation

| File | Topic |
|------|-------|
| `README.md` | Project overview and quick start |
| `CLAUDE.md` | Claude Code instructions (canonical dev guide) |
| `project.md` | Full narrative project summary (German) |
| `SETUP.md` | Detailed setup instructions |
| `EXTRACTION_LOG.md` | ETL run history |
| `Process.log` | Detailed process log |
| `agents.md` | AGENTS.md convention file |
| `Markdown-docs/README.md` | Index of all 94 source documents |
| `knowledge-graph/_index/glossary.md` | DE-EN term glossary |
| `knowledge-graph/_index/relationship-graph.md` | Mermaid entity graph |
| `knowledge-graph/_index/chapter-entity-matrix.md` | Chapter×entity matrix |
| `knowledge-graph/_index/extraction-report.md` | Extraction statistics |
| `refactor/` | Active refactoring planning (4 docs) |

---

## Quick Start

```bash
# Setup (once)
./setup.sh
source .venv/bin/activate

# Run full pipeline
python tools/parallel_ingestion.py       # Extract all 94 docs
python tools/xref_finder.py              # Detect conflicts
python tools/conflict_diff.py            # Resolve conflicts interactively
python tools/entity_generator.py         # Generate entity files

# Validate (must pass before commit)
python tools/frontmatter_validator.py knowledge-graph/
python tools/wikilink_checker.py knowledge-graph/
python tools/consistency_checker.py knowledge-graph/

# Analyze & report
python tools/entity_stats.py
python tools/relationship_graph.py
python tools/chapter_mapper.py
python tools/glossary_generator.py --discover
python tools/canon_resolver.py --apply

# Single file scan
python tools/source_scanner.py --file Markdown-docs/<filename>.md
```

---

## Critical Rules

1. `Markdown-docs/` is **read-only** — never modify without explicit instruction
2. All entity data must trace back to `Markdown-docs/` sources with line numbers
3. Never set `canon_status: decanonized` without explicit source proof
4. German narrative content stays German — do not translate
5. Phase 2 validators must pass before commit or Phase 3

---

## Memory System

Mnemonic filesystem at `_episodic/`, `_semantic/`, `_procedural/` (MIF Level 3 format).
Commands: `/mnemonic:capture {namespace} "{title}"` | `/mnemonic:search`
