# Dual-Kernel: Kohärenz Protokoll

> An interdisciplinary narrative fiction project exploring identity, consciousness, trauma, and artificial intelligence through the lens of quantum physics, mathematical topology, and systems theory.

## Overview

**Kohärenz Protokoll** (Coherence Protocol) is a deeply complex science-fiction novel project centered on the conflict between simulation and the true self. The story follows **Kael**, a protagonist with a fragmented identity system (modeled on TSDP/IFS/ANP-EP frameworks), and their confrontation with **AEGIS**, an artificial superintelligence maintaining a simulated multiverse.

The central tension -- the **K-J Paradox** -- explores the incompatibility between Kael's path toward integration/healing and AEGIS's control mechanisms. The project weaves together:

- **Psychological depth** -- Dissociative identity structures, trauma processing, functional multiplicity
- **Hard science fiction** -- Quantum coherence, Landauer principle, Bekenstein bound, holographic principle
- **Mathematical topology** -- Monster group, sporadic groups, Moonshine conjecture
- **Philosophy & systems theory** -- Paraconsistent logic, autopoiesis, agential realism, Gödel incompleteness
- **Narrative design** -- 39-40 chapter arc using Dramatica theory, polyphonic prose, mosaic structure

## Project Structure

```
Dual-Kernel/
├── README.md                  # This file
├── CLAUDE.md                  # Agent conventions and project guidelines
├── agents.md                  # Agent architecture and workflows
├── project.md                 # Detailed project overview with domain clusters
├── Plan.md                    # Knowledge graph extraction workflow
├── SETUP.md                   # Environment setup guide
│
├── Markdown-docs/             # 94 research & design documents (primarily German)
│   └── README.md              # Clustered navigation index
│
├── knowledge-graph/           # Structured entity knowledge base
│   ├── _index/                # Statistics and registry
│   ├── character/             # Kael, Juna, Lex, Komponente 734
│   ├── aegis/                 # AEGIS, Guardians, Primal Directive
│   ├── world/                 # Nexus, Konstrukt-Stadt
│   ├── mechanic/              # K-J Verbindung, Riss-Mandat
│   ├── physics/               # Kohärenz-Kernel
│   ├── narrative/             # Genesis-Krise
│   └── fundament/             # Riss (foundational concept)
│
├── tools/                     # Knowledge graph extraction pipeline (Python)
│   ├── common.py              # Shared models, entities, domain mapping (Pydantic v2)
│   ├── source_scanner.py      # Scan markdown files for entity mentions
│   ├── xref_finder.py         # Cross-reference and conflict detection
│   ├── conflict_diff.py       # Side-by-side diff viewer for conflicts
│   ├── entity_generator.py    # Generate entity markdown files
│   ├── frontmatter_validator.py # Validate YAML frontmatter schema
│   ├── wikilink_checker.py    # Check wikilink integrity
│   └── entity_stats.py        # Generate extraction statistics
│
└── docs/                      # PDF versions of research documents
```

## Knowledge Domains

| Domain | Description | Key Entities |
|--------|-------------|--------------|
| **Character** | Protagonists, alter personas, psychological profiles | Kael, Juna, Lex, Komponente 734 |
| **Alter-System** | Dissociative identity structures (TSDP, IFS) | ANP/EP models, functional multiplicity |
| **AEGIS** | Superintelligence protocols, guardians, core systems | AEGIS, Primal Directive, Integrity Guardian |
| **World** | Reality layers, simulated worlds, locations | KW1-4, Konstrukt-Stadt, Nexus, Archiv |
| **Physics** | Quantum mechanics, information theory | DKT, Kohärenz-Kernel, Landauer, Gödel |
| **Narrative** | Plot structure, dramaturgy, chapter planning | 39-40 chapters, Genesis-Krise, Dramatica |
| **Philosophy** | Epistemology, ontology, metaphysics | Paraconsistent logic, autopoiesis, Dasein |
| **Mathematics** | Topology, group theory, symmetry | Monster group, Moonshine conjecture |
| **Fundament** | Core concepts underlying all domains | Riss (rift/tear), coherence vs. collapse |
| **Mechanic** | Narrative/world mechanics and rules | K-J Verbindung, Riss-Mandat, Ratchet-Prinzip |

## ETL Pipeline

The project includes a Python-based knowledge graph extraction pipeline:

```
Markdown-docs/ (94 files) → source_scanner → xref_finder → conflict_diff
                                                              ↓
knowledge-graph/ ← entity_generator ← manual review ← conflict resolution
       ↓
frontmatter_validator + wikilink_checker → entity_stats → extraction-report.md
```

## Quick Start

```bash
# 1. Set up the environment
./setup.sh

# 2. Activate the virtual environment
source .venv/bin/activate

# 3. Run the extraction pipeline
python tools/source_scanner.py Markdown-docs/
python tools/xref_finder.py
python tools/entity_generator.py
python tools/frontmatter_validator.py knowledge-graph/
python tools/wikilink_checker.py knowledge-graph/
python tools/entity_stats.py
```

See [SETUP.md](SETUP.md) for detailed environment setup and [Plan.md](Plan.md) for the full extraction workflow.

## Tech Stack

- **Python 3.10+** with Pydantic v2 for data models
- **spaCy** (`de_core_news_lg`) for German NLP / named entity recognition
- **PyYAML** for Obsidian-compatible YAML frontmatter
- **Rich** for formatted console output
- **Click** for CLI interfaces

## Documentation

| Document | Purpose |
|----------|---------|
| [project.md](project.md) | Detailed domain cluster overview with 92 referenced documents |
| [Plan.md](Plan.md) | Full extraction plan with tool specs, phases, and quality checks |
| [SETUP.md](SETUP.md) | Environment setup and troubleshooting |
| [CLAUDE.md](CLAUDE.md) | Agent conventions, project rules, and coding guidelines |
| [agents.md](agents.md) | Agent architecture, workflows, and improvement suggestions |
| [Markdown-docs/README.md](Markdown-docs/README.md) | Navigational index for all 94 research documents |

## License

This is a private creative/research project.
