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
│   ├── _index/                # Reports, glossary, relationship graph
│   ├── character/             # Kael, Juna, Lex, Komponente 734
│   ├── aegis/                 # AEGIS, Guardians, Primal Directive
│   ├── world/                 # Nexus, Konstrukt-Stadt
│   ├── mechanic/              # K-J Verbindung, Riss-Mandat
│   ├── physics/               # Kohärenz-Kernel
│   ├── narrative/             # Genesis-Krise
│   └── fundament/             # Riss (foundational concept)
│
├── tools/                     # Knowledge graph extraction & analysis pipeline (Python)
│   ├── common.py              # Shared models, entities, domain mapping (Pydantic v2)
│   ├── source_scanner.py      # Scan markdown files for entity mentions
│   ├── xref_finder.py         # Cross-reference and conflict detection
│   ├── conflict_diff.py       # Side-by-side diff viewer for conflicts
│   ├── entity_generator.py    # Generate entity markdown files
│   ├── frontmatter_validator.py # Validate YAML frontmatter schema
│   ├── wikilink_checker.py    # Check wikilink integrity
│   ├── entity_stats.py        # Generate extraction statistics
│   ├── relationship_graph.py  # Mermaid entity relationship visualization
│   ├── chapter_mapper.py      # Map entities to chapter appearances
│   ├── consistency_checker.py # Narrative consistency validation
│   ├── glossary_generator.py  # Bilingual DE-EN term glossary
│   └── canon_resolver.py      # Semi-automated canon status resolution
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

## Memory Architecture (Mnemonic)

The project heavily utilizes a **[MIF Level 3](https://mif-spec.dev/) filesytem-based memory system**, driven by the [zircote/mnemonic](https://github.com/zircote/mnemonic) protocol. This system guarantees that our autopoietic, multi-agent loop retains an *append-only*, immutable history of its decisions, failures, and context-engineering iterations.

The Memory system uses a cognitive triad of namespaces:
- **`_semantic/`**: Organizational-wide facts, architectural decisions, and knowledge.
- **`_episodic/`**: Iteration histories, sessions, blockers, and incidents (e.g., `iteration-history.memory.md`).
- **`_procedural/`**: Context-compiler patterns, runbooks, and migrations.

The `Memory Integrator` skill ensures that at the end of every agent iteration, variables and lessons learned are permanently appended to the ledger via `/mnemonic:capture`, avoiding memory degradation and loss of the system's evolutionary trajectory.

## ETL Pipeline

The project includes a Python-based knowledge graph extraction and analysis pipeline:

```
Markdown-docs/ (94 files) → source_scanner → xref_finder → conflict_diff
                                                              ↓
knowledge-graph/ ← entity_generator ← manual review ← canon_resolver
       ↓
frontmatter_validator + wikilink_checker + consistency_checker  (parallel)
       ↓
entity_stats + relationship_graph + chapter_mapper + glossary_generator
```

## Quick Start

```bash
# 1. Set up the environment
./setup.sh

# 2. Activate the virtual environment
source .venv/bin/activate

# 3. Run the extraction pipeline
python tools/source_scanner.py --file Markdown-docs/<file>.md
python tools/xref_finder.py
python tools/entity_generator.py

# 4. Validate
python tools/frontmatter_validator.py
python tools/wikilink_checker.py
python tools/consistency_checker.py

# 5. Generate reports & visualizations
python tools/entity_stats.py
python tools/relationship_graph.py
python tools/chapter_mapper.py
python tools/glossary_generator.py --discover
python tools/canon_resolver.py
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
| [project.md](project.md) | Detailed domain cluster overview of all 94 research documents |
| [Plan.md](Plan.md) | Full extraction plan with tool specs, phases, and quality checks |
| [SETUP.md](SETUP.md) | Environment setup and troubleshooting |
| [CLAUDE.md](CLAUDE.md) | Agent conventions, project rules, and coding guidelines |
| [agents.md](agents.md) | Agent architecture, workflows, and implemented tools |
| [Markdown-docs/README.md](Markdown-docs/README.md) | Navigational index for all 94 research documents |

### Generated Reports (in `knowledge-graph/_index/`)

| Report | Generated By |
|--------|-------------|
| [extraction-report.md](knowledge-graph/_index/extraction-report.md) | `entity_stats.py` |
| [relationship-graph.md](knowledge-graph/_index/relationship-graph.md) | `relationship_graph.py` |
| [chapter-entity-matrix.md](knowledge-graph/_index/chapter-entity-matrix.md) | `chapter_mapper.py` |
| [glossary.md](knowledge-graph/_index/glossary.md) | `glossary_generator.py` |

## License

This is a private creative/research project.
