# Kohärenz Studio — Implementation Roadmap

## Phase Overview

```
Phase 1: Plugin Foundation        (Claude Code core)
Phase 2: Writing Agents           (Claude Code craft skills)
Phase 3: Web UI                   (Next.js, Vercel)
Phase 4: Web Write Integration    (git write-back)
```

Each phase is independently shippable. Phase 1 delivers immediate value.

---

## Phase 1 — Plugin Foundation

**Goal:** Replace the 15-script manual workflow with a unified `kp` CLI + Claude Code plugin.
**Deliverable:** `/kp:entity`, `/kp:ask`, `/kp:state` working in Claude Code.

### Tasks

#### 1.1 — kp/ Python Package
- [ ] `kp/pyproject.toml` — entry point `kp = "kp.cli:main"`
- [ ] `kp/entity.py` — CRUD wrapping existing `knowledge-graph/` YAML files
  - `entity_lookup(id)`, `entity_search(query, domain, canon)`, `entity_create(data)`, `entity_relate(a, b)`
  - Uses `common.parse_frontmatter()` and `common.load_all_entities()`
- [ ] `kp/graph.py` — NetworkX graph from `related:` fields
  - `graph_neighbors(id, depth)`, `orphan_scan()`, `deadlink_scan()`
- [ ] `kp/pipeline.py` — subprocess wrappers for existing tools/
  - `run_validate()`, `run_ingest(file)`, `run_report(type)`
- [ ] `kp/state.py` — `writing-state.json` R/W
  - `WritingState.load()`, `WritingState.save()`, `.get_active()`, `.set_beat(ch, beat, status)`
- [ ] `kp/search.py` — `qmd` subprocess wrapper
  - `qmd_search(query, collection)` → JSON results
  - Collections: `kp-entities`, `kp-sources`, `kp-drafts`
- [ ] `kp/cli.py` — Click app with subcommands
  - `kp entity [search|get|create|relate]`
  - `kp graph [show|orphans|deadlinks]`
  - `kp validate`, `kp ingest`, `kp report`
  - `kp state [show|set]`
  - `kp search "<query>"`
  - All support `--json` flag for headless use

#### 1.2 — MCP Server
- [ ] `.claude/mcp/kp-server/server.py` — FastMCP app
  - Register all 14 tool functions
  - Import from `kp/` package
- [ ] `.claude/settings.json` — register `kp-server` MCP

#### 1.3 — Core Skills
- [ ] `.claude/skills/kp-entity/SKILL.md`
  - CRUD operations, guided creation wizard, search
- [ ] `.claude/skills/kp-ask/SKILL.md`
  - qmd semantic query + graph traversal
- [ ] `.claude/skills/kp-state/SKILL.md`
  - Writing dashboard, chapter status, beat progress

#### 1.4 — Hooks
- [ ] `.claude/hooks/session-start.sh` — writing dashboard
- [ ] `.claude/hooks/pre-commit-check.sh` — Phase 2 gate
- [ ] `.claude/hooks/hooks.json` — hook registry

#### 1.5 — Schema & Infrastructure
- [ ] Extend YAML schema: `voice_profile` field for character entities
- [ ] Extend YAML schema: `narrator_layer` for scene entities
- [ ] Create `scene-registry` domain in `knowledge-graph/`
- [ ] Create `writing-state.json` with current chapter state
- [ ] Create `style-guide.md` template (author to fill)
- [ ] Create `drafts/` directory structure
- [ ] Create `state/` directory + `state/current/` symlink
- [ ] Register qmd collections: `kp-entities`, `kp-sources`
- [ ] `pip install -e kp/` in `.venv`

#### 1.6 — Validation
- [ ] `kp validate` passes on current knowledge-graph/
- [ ] `/kp:entity search "riss"` returns results in Claude Code
- [ ] `/kp:ask "what is K0's role in chapter 7"` returns sourced answer
- [ ] Session start hook shows dashboard

---

## Phase 2 — Writing Agents

**Goal:** Full LangGraph agent pipeline for scene drafting.
**Deliverable:** `/kp:scene` produces a validated German prose draft.

### Tasks

#### 2.1 — LangGraph Orchestrator
- [ ] `kp/agents/orchestrator.py` — `StateGraph` definition
  - `WritingState` TypedDict schema
  - Node definitions for all 7 agents
  - Conditional routing (continuity fail → re-draft, max 3 retries)
  - Human-in-loop gate after Strukturist (optional, controlled by env var)

#### 2.2 — Agent Implementations
- [ ] `kp/agents/drafter.py` — Szenenschreiber
  - Context assembly: `assemble_scene_context(scene, narrator_layer)`
  - Subjective vs. objective branching logic
  - XML-tagged system prompt with voice samples
  - Writes to `drafts/chapter-N/beat-M.md`
- [ ] `kp/agents/continuity.py` — Kontinuitätswächter
  - Extended thinking: ON (`budget_tokens=8000`)
  - Structured output: `ContinuityReport` Pydantic model
  - Exemption detection for `narrator_layer=subjective`
- [ ] `kp/agents/style.py` — Stimmprüfer
  - Voice profile validation per active alter
  - Forbidden word detection
  - Thematic alignment check
- [ ] `kp/agents/perplexity_gate.py` — Quality Gate
  - Uses Haiku for sentence-level scoring
  - Flags sentences below quality threshold
- [ ] `kp/agents/state_updater.py` — Zustandsupdate
  - Structured extraction of entity state changes
  - Updates `knowledge-graph/` YAML files
  - Updates `state/ch-N/snapshot.json`
  - Runs Phase 2 validators post-update

#### 2.3 — Craft Skills
- [ ] `.claude/skills/kp-scene/SKILL.md` — primary drafting skill
- [ ] `.claude/skills/kp-world/SKILL.md` — Weltbauer
- [ ] `.claude/skills/kp-outline/SKILL.md` — Strukturist
- [ ] `.claude/skills/kp-dialogue/SKILL.md` — Dialogcoach
- [ ] `.claude/skills/kp-review/SKILL.md` — Lektor + Kontinuitätswächter
- [ ] `.claude/skills/kp-research/SKILL.md` — Forschungsassistent
- [ ] `.claude/skills/kp-commit/SKILL.md` — commit + memory capture

#### 2.4 — State Infrastructure
- [ ] `beats/` directory — chapter beat sheets as JSON
- [ ] `state/` directory — per-chapter snapshots
- [ ] MCP tools: `chapter_beats()`, `writing_state_set()`

#### 2.5 — Voice Profiles
- [ ] Populate `voice_profile` field for top 10 character entities
  - Kael (host), Lex, Nyx, Alex, Guardian, Kiko (minimum)
  - Extract sample passages from Markdown-docs/TsdpAnalyseKaelsInnereWelt.md
- [ ] Validate voice profile schema in `frontmatter_validator.py`

---

## Phase 3 — Web UI

**Goal:** Vercel-deployed knowledge graph visualization + entity browser.
**Deliverable:** Protected web app accessible at `https://<project>.vercel.app`

### Tasks

#### 3.1 — Next.js App Skeleton
- [ ] `web/` — `npx create-next-app@latest` with TypeScript, App Router
- [ ] NextAuth setup — `WRITING_SECRET` credential provider
- [ ] Protected layout: `(protected)/layout.tsx` with auth check
- [ ] Basic nav: graph | entities | chapters

#### 3.2 — Static Data Export
- [ ] `kp export web` command — generates `web/public/data/`:
  - `entities.json` — all entity summaries
  - `graph.json` — D3 nodes + links
  - `chapters.json` — chapter matrix
  - `writing-state.json` — draft status
- [ ] Pre-commit hook: run `kp export web` before every commit

#### 3.3 — Views
- [ ] `/graph` — `EntityGraph.tsx` with `react-force-graph-2d`
  - Domain colors, node sizing, click → detail
  - Filter controls: domain, canon_status
- [ ] `/entities` — `SearchBar.tsx` + `EntityCard.tsx`
  - Static filter from `entities.json`
  - qmd search via `/api/search` (local dev) or pre-indexed (Vercel)
- [ ] `/chapters` — `ChapterMatrix.tsx`
  - 39×N grid, beat status overlay

#### 3.4 — Vercel Deployment
- [ ] `web/vercel.json` config
- [ ] Environment variables: WRITING_SECRET, NEXTAUTH_SECRET, NEXTAUTH_URL
- [ ] Deploy: `vercel deploy --prod`

---

## Phase 4 — Web Write Integration

**Goal:** Web UI can commit entity edits and draft annotations.
**Deliverable:** Inline entity editing from browser → git commit.

### Tasks
- [ ] Python runtime on Vercel (`@vercel/python` API routes)
- [ ] `/api/entities POST` — write entity via `kp entity create`
- [ ] `/api/entities/[id] PUT` — edit entity via `kp entity edit`
- [ ] Optimistic UI + error rollback
- [ ] Draft annotation in `/write` — comments → git commit

---

## Technology Dependencies

```
# Python (add to requirements.txt)
fastmcp>=0.5
langgraph>=1.0
anthropic>=0.40
networkx>=3.0
pydantic>=2.0
click>=8.0
rich>=13.0
spacy>=3.7

# Node.js (web/)
next@15
next-auth@5
react-force-graph-2d
tailwindcss
typescript

# CLI tools
npm install -g @tobilu/qmd   # Node.js >= 22 required
```

## Suggested Start

```bash
# Install kp package
pip install -e kp/

# Register qmd collections
qmd collection add knowledge-graph/ --name kp-entities
qmd collection add Markdown-docs/ --name kp-sources
qmd update && qmd embed   # ~2GB download on first run

# Test MCP server
python3 .claude/mcp/kp-server/server.py

# Test core skill
# In Claude Code: /kp:entity search "riss"
```
