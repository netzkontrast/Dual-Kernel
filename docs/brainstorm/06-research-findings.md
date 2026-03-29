# Research Findings: Agentic Writing for Complex Novels

*Research conducted 2026-03-29. Sources listed at end.*

---

## 1. Existing Agentic Writing Tools

### Commercial Landscape

**Sudowrite** — Most mature multi-phase pipeline: braindump → synopsis → characters → worldbuilding → outline → scenes. Runs a multi-model stack (GPT-4.1, Claude Opus, Gemini Pro 2.5). Story Bible feature closest to a structured context store. Weakness: English-centric, no German support.

**NovelCrafter + The Codex** — Most architecturally relevant. The Codex is a wiki-like story bible where each entry (character, location, lore) is automatically cross-referenced with manuscript text. Constructs AI context by pulling relevant Codex entries alongside the current scene — essentially structured RAG using the author's world bible. Supports BYOK (Claude, GPT, Gemini, Ollama). Tracks "Progressions" — character attributes change per chapter position.

**NovelAI** — Lorebook + Memory system, flexible models. No structured plotting. Better for exploratory non-linear fiction; requires heavy manual steering for canon compliance.

### Open-Source CLI Tools

| Tool | Description | Relevance |
|------|-------------|-----------|
| StoryCraftr | Python CLI, generates worldbuilding/outline/chapters | Direct CLI + novel writing match |
| GPTAuthor | Multi-chapter fiction from prompt, sequential | Too simple |
| SILK | CLI workflow with LLM integration, context optimization | Useful patterns |
| Novel-OS | Three-layer context injection (Standards/Novel/Manuscripts) | Mirrors CLAUDE.md approach |
| **Book-Agent / Claude Book** | Multi-agent pipeline, most technically complete | **Adopt as reference** |

### Book-Agent / Claude Book (Priority Reference)

Most directly applicable open-source architecture:
- **Planner agent** (Opus) → chapter beats from synopsis
- **Writer agent** (Opus) → full chapters from beats
- **Perplexity Gate** (Ministral 8B) → flags predictable text (PPL < 22 threshold)
- **Reviewer agents** (Sonnet, parallel) → style, character, continuity validation
- **State Updater** → extracts per-chapter character state into versioned snapshots
- File pattern: `state/current/` symlink always points to latest validated state

This pipeline maps directly to the Kohärenz Studio agent design.

---

## 2. Writing Process Stages for Complex Novels

### Standard 7-Stage Process

| Stage | Description | AI Role |
|-------|-------------|---------|
| Premise/Logline | Core idea + stakes | Validator, alternative generator |
| World-Building | Settings, rules, history | Consistency checker, expander |
| Character Architecture | Arcs, psychology, voice | Role-player, arc designer |
| Structural Outline | Act structure, scene-by-scene | Beat generator, pacing analyst |
| Scene Drafting | Chapter-level prose | Drafter, style enforcer |
| Continuity Checking | Timeline, relationship consistency | Automated validator |
| Revision/Editing | Voice, pacing, line polish | Style enforcer, compression agent |

### What Complex Novels Require Differently

**Multi-arc DID protagonist**: Each alter has an independent arc that must be internally consistent while causally linked to the host system's arc. Requires per-alter state tracking throughout all 39 chapters.

**Unreliable narrator**: Two-layer truth model required:
- Layer 1: narrator's subjective truth (what Kael/active alter experiences)
- Layer 2: canonical objective truth (what the KG says is actually true)

Continuity Checker must flag violations but exempt intentional unreliability (`narrator_layer=subjective`).

**Non-linear timelines**: Scenes must carry both narrative position (chapter N) and chronological position. The state snapshot infrastructure handles this.

**Philosophical/scientific themes**: Physics claims (DKT, Landauer, Gödel, Monster group) must trace to canonical entity definitions. A dedicated physics validation pass is needed beyond the structural consistency_checker.py.

**Multiple POVs**: Each POV requires its own vocabulary register, sentence length distribution, emotional baseline, forbidden words. This is the `voice_profile` extension to the entity schema.

---

## 3. RAG and Knowledge Graph Approaches

### The Optimal Pattern (Three-Layer)

```
Layer 1: Structured entity lookup
  → knowledge-graph/ YAML files
  → Fast, exact, for canonical facts

Layer 2: Hybrid semantic search (qmd)
  → knowledge-graph/ + Markdown-docs/ + drafts/
  → BM25 + vector, for thematic context

Layer 3: Graph traversal (future)
  → NetworkX in-memory, LightRAG for multi-hop
  → "How does AEGIS's Primal Directive relate to K-J Verbindung?"
```

### CRITICAL FINDING: KG Grounding Depends on Scene Type

*From 2025 Scientific Reports KG-RAG paper + narrative AI research:*

> KG-assisted generation improves factual consistency for action-oriented and structured narratives but **declines** for introspective/emotional narratives.

**For Kohärenz Protokoll:**
- Physics/AEGIS/world scenes → entity lookup dominant
- Kael/alter interior scenes → style-guide + voice retrieval dominant
- This is the `narrator_layer` distinction and drives the `assemble_scene_context()` branching

### qmd as Search Backend

`@tobilu/qmd` (npm, Node.js ≥ 22):
- Collections: directories of markdown files
- `qmd update` → BM25 index
- `qmd embed` → vector embeddings (downloads ~2GB GGUF models once)
- `qmd search "query"` → BM25 keyword
- `qmd vsearch "query"` → semantic vector
- `qmd query "query"` → hybrid (best for writing context assembly)
- `--json` flag for programmatic use
- Already integrated in project via `qmd-setup` and `qmd-reindex` skills

**Collections for this project:**
```bash
qmd collection add knowledge-graph/ --name kp-entities
qmd collection add Markdown-docs/   --name kp-sources
qmd collection add drafts/          --name kp-drafts
```

### LightRAG (Future Phase)

For multi-hop queries ("what does Kael know about the Riss and how does AEGIS's Primal Directive relate?"): LightRAG builds entity/relationship hierarchies from raw text. Lighter than Microsoft GraphRAG, local-first, supports open-source LLMs. Deferred — qmd handles Phase 1-3 search needs.

---

## 4. Multi-Agent Pipeline Architecture

### Recommended: LangGraph (not CrewAI)

**Why LangGraph:**
- State machine model matches existing conditional logic (Phase 2 must pass before Phase 3, decanonized requires proof, violations block drafting)
- Existing Pydantic schemas compatible
- Explicit conditional routing (fail → re-route vs. CrewAI's opinionated flow)
- The existing tools/ scripts become LangGraph tool nodes

**Why not CrewAI:**
- Opinionated design requires workarounds at every step
- Adds abstraction overhead conflicting with existing Pydantic architecture

### Agent Roles Consensus

| Agent | Model Tier | Think |
|-------|-----------|-------|
| Orchestrator | Sonnet 4.6 | OFF |
| Weltbauer | Sonnet 4.6 | ON |
| Strukturist | Sonnet 4.6 | OFF |
| Szenenschreiber | Sonnet 4.6 | OFF (overthinking harms prose) |
| Kontinuitätswächter | Sonnet 4.6 | ON |
| Stimmprüfer | Sonnet 4.6 | OFF |
| Perplexity Gate | Haiku | N/A |
| Zustandsupdate | Sonnet 4.6 | OFF |

**Note on extended thinking:** Research confirms extended thinking should be OFF for prose generation. Structured reasoning tasks (continuity, world-building logic) benefit from ON.

### File-System Handoff Pattern (from Book-Agent)

Each agent writes structured output to a specific path. The next agent reads that path as primary input. Combined with `state/current/` symlink, this creates a durable pipeline that survives interruptions.

```
beats/chapter-N.json              ← Strukturist output
drafts/chapter-N/beat-M.md        ← Szenenschreiber output
reviews/chapter-N/continuity.json ← Kontinuitätswächter output
reviews/chapter-N/style.json      ← Stimmprüfer output
state/ch-N/snapshot.json          ← Zustandsupdate output
state/current/ → state/ch-N/      ← symlink to latest
```

---

## 5. Claude-Specific Writing Capabilities

### Extended Thinking Usage

| Use | Setting | Reason |
|-----|---------|--------|
| World-building consistency | ON (4k-8k budget) | Multi-entity reasoning |
| Continuity checking | ON (8k budget) | Cross-reference multiple entities |
| Prose drafting | OFF | Overthinking produces stilted prose |
| Style checking | OFF | Pattern matching, not reasoning |
| Beat planning | OFF | Structured output, not creative |

### Prompt Architecture for Character Voice

**4 key techniques (research consensus):**

1. **Few-shot voice locking** — 3-5 example sentences before any generation. Per-alter voice samples are mandatory, not optional.

2. **XML-tagged context** — use explicit `<character_state>`, `<scene_beat>`, `<forbidden_elements>`, `<voice_constraints>`. Claude responds to predictable scaffolding with higher consistency.

3. **Pass-based workflow** — never draft AND check continuity in one pass.
   Order: beat generation → draft → continuity → style → perplexity → compress

4. **Decisions log** — running log of canonical rules injected at session top. This is the `style-guide.md` + `writing-state.json` pattern.

### The 3 Claude Personas

| Persona | System Prompt Mode | Used For |
|---------|-------------------|----------|
| Author | "Du schreibst Kohärenz Protokoll..." | Szenenschreiber |
| Assistant | "Analysiere diesen Entwurf auf Widersprüche..." | Kontinuitätswächter |
| Critic | "Du bist Lektor. Diene den Themen des Romans..." | Stimmprüfer |

### Context Window Strategy

Claude's 200K context means full entity files fit (no chunking needed). The key is **selective loading**:
- Use `chapter_mapper.py` output to filter to ~15-20 entities per scene
- Don't load all 177 entities per generation call
- Interior scenes: load only the active alter + style-guide (< 10K tokens total)
- Physics scenes: load relevant domain entities + Markdown-docs extracts

---

## 6. Project-Specific Recommendations

### German-Language Model Choice

Claude Sonnet 4.6 is ranked in the top tier for German-language literary quality on current benchmarks (Artificial Analysis multilingual benchmark). Opus 4.6 is top-ranked but cost 15× more. Given that Sonnet 4.6 handles entity files directly (no chunking overhead), it's the right choice for this project.

For cost-sensitive auxiliary tasks (perplexity gate, style checking), Haiku is appropriate.

### DID Themes — Special Handling

The alter system (54 character entities) requires:
1. Per-alter voice profiles (the `voice_profile` YAML extension)
2. Alter-switch tracking in state snapshots (which alter was active when)
3. The knowledge restriction field: each alter knows only what their system position allows them to know
4. The Kontinuitätswächter must validate alter knowledge states, not just canonical facts

### Unreliable Narrator — Implementation

```yaml
# In scene-registry entities
narrator_layer: subjective  # Kontinuitätswächter exempts these violations
```

The pipeline must distinguish:
- Accidental continuity error → flag and re-draft
- Intentional unreliability → confirm and pass

This is one of the most technically interesting constraints in the system.

### Physics Validation Gap

Current `consistency_checker.py` validates structural rules, not semantic physics consistency. A dedicated physics validation tool is needed that:
- Validates all DKT/Landauer/Gödel/Monster-group references against physics domain entities
- Uses the 2 existing physics entities + Markdown-docs/DualKernelAiAndNarrativeCollapse.md as authority
- Should be part of Phase 2 agent pipeline (Kontinuitätswächter tool)

---

## Sources

- [Claude Book: Multi-Agent Framework for Writing Novels](https://hackernoon.com/claude-book-a-multi-agent-framework-for-writing-novels-with-claude-code)
- [Book-Agent: Generating Epistemically Controlled Long-Form Fiction](https://forum.level1techs.com/t/my-ai-powered-novel-writing-pipeline-book-agent/243193)
- [Guiding Generative Storytelling with Knowledge Graphs (arXiv 2025)](https://arxiv.org/html/2505.24803v2)
- [GraphRAG: Unlocking LLM discovery on narrative private data (Microsoft Research)](https://www.microsoft.com/en-us/research/blog/graphrag-unlocking-llm-discovery-on-narrative-private-data/)
- [LightRAG (GitHub)](https://github.com/hkuds/lightrag)
- [KG-RAG model research (Scientific Reports 2025)](https://www.nature.com/articles/s41598-025-21222-z)
- [NovelCrafter Codex Feature](https://www.novelcrafter.com/features/codex)
- [LangGraph vs CrewAI comparison (ZenML)](https://www.zenml.io/blog/langgraph-vs-crewai)
- [Claude extended thinking tips](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/extended-thinking-tips)
- [German AI Models Benchmark (Artificial Analysis)](https://artificialanalysis.ai/models/multilingual/german)
- [@tobilu/qmd — project qmd-setup skill (this repo)](../.claude/skills/qmd-setup/SKILL.md)
