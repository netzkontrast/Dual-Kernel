# Kohärenz Studio — System Architecture

## Repository Layout (Target State)

```
Dual-Kernel/
│
├── .claude/                        # Claude Code plugin (kohärenz-studio)
│   ├── skills/                     # 12 slash command skills
│   ├── hooks/                      # 4 automation hooks
│   ├── mcp/kp-server/              # Local FastMCP server
│   ├── writing-state.json          # Current chapter/beat/draft status
│   ├── style-guide.md              # Prose voice, German style rules
│   └── settings.json               # MCP + hook registration
│
├── kp/                             # Installable Python package
│   ├── pyproject.toml              # Entry point: `kp` CLI
│   └── kp/
│       ├── cli.py                  # Click app
│       ├── entity.py               # CRUD over knowledge-graph/
│       ├── graph.py                # NetworkX relationship graph
│       ├── pipeline.py             # Wraps tools/ scripts
│       ├── state.py                # writing-state.json R/W
│       ├── search.py               # qmd subprocess wrapper
│       └── agents/                 # 7 writing agents (LangGraph)
│           ├── orchestrator.py
│           ├── drafter.py
│           ├── continuity.py
│           ├── style.py
│           ├── perplexity_gate.py
│           └── state_updater.py
│
├── web/                            # Next.js → Vercel
│   ├── app/
│   │   ├── (auth)/login/
│   │   ├── (protected)/
│   │   │   ├── graph/              # Force-directed entity graph
│   │   │   ├── entities/[id]/      # Entity detail + relations
│   │   │   ├── chapters/           # Chapter matrix + draft status
│   │   │   └── write/              # Draft viewer
│   │   └── api/                    # Next.js API routes
│   │       ├── entities/
│   │       ├── search/             # → qmd subprocess
│   │       └── graph/
│   └── components/
│       ├── EntityGraph.tsx         # react-force-graph / D3
│       ├── EntityCard.tsx
│       ├── SearchBar.tsx           # qmd-powered
│       └── ChapterMatrix.tsx
│
├── drafts/                         # NEW — scene drafts (git-tracked)
│   └── chapter-{N}/beat-{M}.md
│
├── state/                          # NEW — chapter state snapshots
│   ├── current -> state/ch-07/     # symlink to latest validated
│   └── ch-{N}/snapshot.json
│
├── knowledge-graph/                # Extended with new domain + fields
│   ├── scene-registry/             # NEW domain — scene-level entities
│   └── ...existing domains
│
├── tools/                          # Existing (wrapped by kp/pipeline.py)
├── Markdown-docs/                  # Existing — read-only source truth
└── _episodic/                      # Mnemonic memory
```

## Data Flow: Scene Drafting

```
/kp:scene --chapter 7 --beat 3
        │
        ▼ SKILL: kp-scene/SKILL.md
        │
        ├── MCP: writing_state_get()          → current chapter/beat
        ├── MCP: chapter_entities(7)           → 14 relevant entity files
        ├── MCP: entity_lookup("riss")         → deep entity context
        └── MCP: qmd_search("K0 Kael ch7")    → semantic context from corpus
        │
        ▼ Context Assembly (narrator_layer-aware)
        │
        ├── If subjective scene:
        │     style-guide.md + voice_profile for active alter
        │     qmd_search(alter interiority) — style retrieval dominant
        │
        └── If objective/physics scene:
              all chapter_entities + entity_lookup(continuity_deps)
              qmd_search(physics concepts) — entity lookup dominant
        │
        ▼ claude-sonnet-4-6 (think: OFF for prose)
        │
        ├── Generates German prose draft
        ├── Write → drafts/chapter-7/beat-3.md
        ├── MCP: writing_state_set(7, 3, "drafted")
        ├── Run validators (Phase 2)
        ├── /mnemonic:capture episodic "chapter 7 beat 3 drafted"
        └── git commit (kp:commit skill)
```

## YAML Schema Extensions

Two new fields added to entity frontmatter:

```yaml
# For character/* entities (especially alters)
voice_profile:
  register: fragmented|clinical|childlike|cold|hypervigilant
  sentence_style: short-burst|dissociative-run-on|measured
  forbidden_words: []
  sample_passages:
    - "Markdown-docs/TsdpAnalyseKaelsInnereWelt.md:142"

# New domain: scene-registry/*
scene_id: ch07-beat03
chapter: 7
beat: 3
narrator_layer: subjective    # subjective | objective | dual
active_alter: lex
draft_status: planned         # planned | drafted | validated | locked
continuity_deps:
  - kael
  - riss
```

## qmd Collection Setup

```bash
# Register all corpus directories as qmd collections
qmd collection add knowledge-graph/ --name kp-entities
qmd collection add Markdown-docs/   --name kp-sources
qmd collection add drafts/          --name kp-drafts

# Build index + embeddings
qmd update && qmd embed

# Usage
qmd query "riss fragmentation chapter 7" -c kp-entities
qmd query "Kael interiority dissociation" -c kp-sources
qmd vsearch "K0 collapse state" -c kp-entities   # vector-only
```

## Technology Stack

| Layer | Technology | Notes |
|-------|-----------|-------|
| Plugin skills | Markdown SKILL.md | Claude Code slash commands |
| Plugin hooks | Bash + hooks.json | Session start, pre-commit |
| MCP server | FastMCP (Python) | Exposes tools to Claude in-context |
| Core library | Python 3.10+ (kp/) | Click CLI + Pydantic v2 |
| Agent orchestration | LangGraph 1.0 | State machine, conditional routing |
| Agent model | claude-sonnet-4-6 | Full entity files as context |
| Search | @tobilu/qmd | BM25 + vector hybrid over markdown |
| Graph analysis | NetworkX | In-memory, sufficient for 177 entities |
| Web framework | Next.js 15 | App Router, API routes |
| Auth | NextAuth.js | WRITING_SECRET env var |
| Deployment | Vercel | Serverless, single command deploy |
| Persistence | Git repo | Every significant write = commit |
| Memory | Mnemonic _episodic/ | MIF Level 3, append-only |
