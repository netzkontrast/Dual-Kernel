# Original Request: Tool Specifications

Create all tools in `tools/` BEFORE starting the extraction. Actively use them during work.

## 5.1 `source_scanner.py`
**Purpose**: Creates an inventory of all source files and entity candidates within them.
**Input**: Path to `Markdown-docs/`
**Output**: `tools/output/source-inventory.json`
**Actions**: Read every `.md` file, extract headings with line numbers, identify entity candidates via bold text, capitalized names, recurring technical terms, and known keywords (Kael, AEGIS, Juna, DKT, Kernwelt, etc.). Output includes filename, line numbers, surrounding context (±2 lines), and estimated domain.

## 5.2 `xref_finder.py`
**Purpose**: Finds entities in multiple files and identifies potential conflicts via diverging descriptions.
**Input**: `tools/output/source-inventory.json`
**Output**: `tools/output/cross-references.json`
**Actions**: For each entity in >1 file, collect context passages, search for defining sentences, compare definitions for surface contradictions (numbers, names, properties). Marks conflicts with Confidence-Score: HIGH, MEDIUM, LOW.

## 5.3 `conflict_diff.py`
**Purpose**: Shows passages from all sources side-by-side as a diff-view for manual inspection for a specific entity.
**Input**: Entity name + Path to `Markdown-docs/`
**Output**: Formatted console output + optional `tools/output/diffs/ENTITY.md`

## 5.4 `frontmatter_validator.py`
**Purpose**: Checks all generated entity files for valid YAML frontmatter and schema conformity.
**Input**: Path to `knowledge-graph/`
**Output**: Validation report on the console
**Checks**: YAML validity, required fields (`title`, `id`, `domain`, `canon_status`), valid values, `sources` array, `related` wikilinks, `tags`.

## 5.5 `wikilink_checker.py`
**Purpose**: Checks the integrity of all wikilinks in the Knowledge Graph.
**Input**: Path to `knowledge-graph/`
**Output**: Report on the console
**Checks**: Broken links, orphaned files, bidirectionality (warning), duplicate titles.

## 5.6 `entity_stats.py`
**Purpose**: Generates a statistics report after extraction completion.
**Input**: Path to `knowledge-graph/` + `tools/output/`
**Output**: `knowledge-graph/_index/extraction-report.md` + console

---

## 6. YAML-Frontmatter-Schema
A specific YAML schema is required containing fields like `title`, `id`, `domain` (character, world, physics, etc.), `canon_status` (confirmed, disputed, uncertain, etc.), `sources` (with `file`, `lines`, `relevance`), and `conflicts`.

---

## 7. Workflow
- **Phase 0**: Build tools, create `tools/README.md`, test scanner/xref.
- **Phase 1**: Run scanner, run xref_finder, run conflict_diff for frequent entities.
- **Phase 2**: Create directory structure under `knowledge-graph/`, create entity files with specific markdown sections (Summary, Sources, Conflicts, Relationships).
- **Phase 3**: Run frontmatter_validator, wikilink_checker, create MOC READMEs, create hub README.
- **Phase 4**: Create JSON registry indices, run entity_stats, check the extraction report.

---

## 8. Quality Checks
- All 6 tools exist and are executable.
- `tools/output/source-inventory.json` exists.
- Every entity file has valid YAML frontmatter.
- Validators report 0 errors/broken links.
- `conflict-registry.json` and `entity-registry.json` are valid JSON.
- No `decanonized` status without explicit source proof.
- No files contain invented content.
- Entity Stats Report exists.

---
# Knowledge Graph Extraction Plan

This document details the comprehensive strategy and workflow for extracting entities from the `Markdown-docs/` directory and constructing a structured knowledge graph in the `knowledge-graph/` directory.

## 1. Project Setup and Dependencies

### Prerequisites
- **Python**: version 3.10 or higher.
- **Dependencies**: Listed in `requirements.txt`.
  - `spacy>=3.7,<4.0`: NLP operations (NER, POS-Tagging).
  - `de_core_news_lg>=3.7`: German language model for spaCy.
  - `pyyaml>=6.0`: Reading and writing YAML frontmatter.
  - `rich>=13.0`: Formatted console output.
  - `click>=8.0`: CLI interfaces for the tools.

### Installation Script (`setup.sh`)
An installation script will set up a virtual environment, install dependencies, and download the required spaCy model. It will also create necessary directories like `tools/output`, `tools/output/diffs`, and `tools/fixtures`.

### .gitignore
Must be updated to ignore build and cache artifacts:
```
.venv/
tools/output/
__pycache__/
*.pyc
```

## 2. Shared Library (`tools/common.py`)

A common utility module shared across all tools. It includes:
- **Constants**: `VALID_DOMAINS`, `VALID_CANON_STATUS`, `REQUIRED_FRONTMATTER`, and paths.
- **Known Entities**: A comprehensive seed list of domain-specific named entities (e.g., Kael, AEGIS, Dual Kernel, Kernwelt, Juna, etc.) to aid extraction where NLP models might miss fictional terms.
- **NLP Setup**: Caches and loads the `de_core_news_lg` spaCy model with unneeded pipes disabled for performance.
- **Frontmatter Parsing/Writing**: Uses PyYAML to read/write Obsidian-compatible YAML frontmatter.
- **Markdown Helpers**: Functions to extract headings, bold terms, and surrounding context/paragraphs given a line number.
- **Entity Detection**: A hybrid approach using regex for `KNOWN_ENTITIES` and spaCy NER for general entities.
- **Output Helpers**: Utilities for writing JSON files and generating kebab-case IDs.

## 3. Tool Specifications

### Phase 1: Scan & Inventory

1. **`source_scanner.py`**
   - **Purpose**: Scans all `.md` files in `Markdown-docs/` to build an inventory of entity mentions.
   - **Process**: Extracts headings, bold terms, and entities using `common.py`. Aggregates mentions by entity, storing file paths, line numbers, mention counts, context, and an estimated domain.
   - **Output**: `tools/output/source-inventory.json`

2. **`xref_finder.py`**
   - **Purpose**: Identifies cross-references for entities appearing in multiple files and flags potential conflicts.
   - **Process**: Uses heuristics to find conflicting definitions (e.g., regex for numbers near entity mentions, keyword matching for definition structures).
   - **Output**: `tools/output/cross-references.json` with conflict severity scores (`HIGH`, `MEDIUM`, `LOW`).

3. **`conflict_diff.py`**
   - **Purpose**: A CLI tool to visually compare conflicting passages across sources for manual review.
   - **Process**: Extracts paragraphs surrounding specific entity mentions and prints them grouped by source file.
   - **Options**: `--save` flag saves the diff output to `tools/output/diffs/<entity>.md`.

### Phase 2: Extraction (Automated Generation)

4. **`entity_generator.py`**
   - **Purpose**: Automatically generates the `knowledge-graph/` directory and markdown files.
   - **Process**: Reads `source-inventory.json` and `cross-references.json`. For each entity:
     - Determines the appropriate `domain` subfolder.
     - Sets `canon_status` based on conflict data.
     - Generates YAML frontmatter, a short summary from context, a sources list, conflicts, and related wikilinks based on co-occurrence.
   - **Output**: Populates `knowledge-graph/` with entity `.md` files and generates Map of Content (MOC) `README.md` files for each subfolder.

### Phase 3: Validation

5. **`frontmatter_validator.py`**
   - **Purpose**: Validates the YAML frontmatter of generated files against the schema.
   - **Checks**: Existence of frontmatter, parseability, required fields, valid domain/canon_status values, structure of sources, and wikilink syntax in related fields.

6. **`wikilink_checker.py`**
   - **Purpose**: Checks the integrity of `[[Link]]` formatted wikilinks.
   - **Checks**: Broken links (targets missing), orphaned files, bidirectional link warnings, and duplicate titles.

### Phase 4: Index & Report

7. **`entity_stats.py`**
   - **Purpose**: Generates final statistical reports and JSON indexes.
   - **Process**: Reads all frontmatters to aggregate data.
   - **Outputs**: `_index/entity-registry.json`, `_index/conflict-registry.json`, and a formatted `_index/extraction-report.md` detailing entity counts, conflicts, and file coverage.

## 4. Testing Strategy

- **Fixture**: A copy of `Markdown-docs/EinleitungGenesisDerExistenz.md` acts as the test source (`tools/fixtures/test-source.md`).
- **Test Script (`test_with_fixture.py`)**: Runs all tools against the fixture to verify expected behavior (e.g., detecting known entities like AEGIS, validating generated frontmatter) before running on the full dataset.

## 5. Execution Workflow

1. Run `./setup.sh` and activate the virtual environment.
2. Run `tools/test_with_fixture.py` to ensure tool correctness.
3. Execute `tools/source_scanner.py` to build the inventory.
4. Execute `tools/xref_finder.py` to identify conflicts.
5. Run `tools/conflict_diff.py --save` for critical entities (e.g., Kael, Michael, AEGIS, Dual Kernel, DKT, Kohärenz, Kernwelt, KW1, Juna, Fundament, Guardian, Kapitel).
6. Execute `tools/entity_generator.py` to build the knowledge graph structure.
7. Validate results with `tools/frontmatter_validator.py` and `tools/wikilink_checker.py`.
8. Generate final reports with `tools/entity_stats.py`.

## 6. Notable Entity Handling

- **Kael / Michael**: "Michael" is noted as a probable early name for the protagonist "Kael". They will be treated with care, documenting the alias/conflict and using `canon_status: uncertain` for Michael.
- **Echo**: Potentially an Alter name or a concept. Context evaluation is needed.
- **Lethe**: Can be a location, concept, or metaphor.
- **AEGIS Acronyms**: Context checking is required as they might not all be operative protocols (e.g., PKP might be "Plot-Kern-Punkte").
- **PAL**: "Phase Alignment Lock", needs verification against all mentions for definition consistency.

---

## What Needs to be Done Next

The above plan details exactly what was initially asked of me. Here's a summary of the next steps to actually implement it:

1.  **Create the actual tool scripts**: The python files listed above (`common.py`, `source_scanner.py`, `xref_finder.py`, `conflict_diff.py`, `entity_generator.py`, `frontmatter_validator.py`, `wikilink_checker.py`, `entity_stats.py`, `test_with_fixture.py`) need to be populated with their respective logic as outlined in the specifications.
2.  **Ensure requirements and setup**: `setup.sh` and `requirements.txt` have been created, but `.venv` needs to be activated to run the scripts.
3.  **Run the test suite**: Execute `python tools/test_with_fixture.py` to make sure the environment and basic parsing work correctly.
4.  **Execute the workflow**: Run the scripts in the specified order (Phase 1 -> Phase 2 -> Phase 3 -> Phase 4) to generate the knowledge graph.
5.  **Manual Review**: After automatic generation, manually review the complex entities (like AEGIS, Kael, DKT) as the automated summaries might need refinement.
