# Kohärenz Studio — Writing Agent Pipeline

## The 7 Agents

```
┌─────────────────────────────────────────────────────────────────────┐
│  ORCHESTRATOR — LangGraph state machine (Sonnet 4.6)               │
│  Routes pipeline, manages quality gates, human-in-loop checkpoints  │
└──────────┬──────────────────────────────┬───────────────────────────┘
           │                              │
    ┌──────▼──────┐              ┌────────▼──────────┐
    │  Weltbauer  │              │  Forschungs-       │
    │  (World     │              │  assistent         │
    │  Builder)   │              │  (Researcher)      │
    │  Sonnet 4.6 │              │  Sonnet 4.6        │
    │  think: ON  │              │  think: OFF        │
    └─────────────┘              └───────────────────┘
           │
    ┌──────▼──────┐
    │ Strukturist │
    │ (Planner)   │
    │ Sonnet 4.6  │
    │ think: OFF  │
    └──────┬──────┘
           │  beat sheet
    ┌──────▼──────────────┐
    │  Szenenschreiber    │   Author mode — German prose
    │  (Drafter)          │   Subjective: style-guide focused
    │  Sonnet 4.6         │   Objective: entity-lookup focused
    │  think: OFF         │   (overthinking harms prose generation)
    └──────┬──────────────┘
           │  raw draft
    ┌──────┼──────────────────────┐
    │      │                      │
    ▼      ▼                      ▼
┌──────────────┐  ┌──────────┐  ┌──────────────┐
│Kontinuitäts- │  │Stimm-    │  │Perplexity    │
│wächter       │  │prüfer    │  │Gate (Haiku)  │
│(Continuity)  │  │(Style)   │  │              │
│Sonnet 4.6    │  │Sonnet 4.6│  │PPL < 22 →    │
│think: ON     │  │think:OFF │  │rewrite flag  │
└──────┬───────┘  └────┬─────┘  └──────┬───────┘
       │               │               │
       └───────────────┴───────────────┘
                       │  validated draft
              ┌────────▼────────┐
              │ Zustandsupdate  │
              │ (State Updater) │
              │ Sonnet 4.6      │
              │                 │
              │ → knowledge-graph/ YAML updates
              │ → state/ch-N/snapshot.json
              │ → Phase 2 validators
              │ → git commit
              └─────────────────┘
```

## Agent Definitions

### Orchestrator
- **Role:** State machine — routes between agents, manages quality gates
- **Input:** User intent + writing-state.json
- **Tools:** All MCP tools
- **Routing logic:**
  - Continuity violation → re-route to Drafter with error context
  - Style violation → re-route to Drafter with revision notes
  - Perplexity fail → optional rewrite pass
  - All gates pass → route to State Updater
- **Human gates:** After Strukturist (beat sheet review) — optional

### Weltbauer (World Builder)
- **Role:** Develops new world-building concepts into entity files
- **Extended thinking:** ON — needs to reason about physics/lore consistency
- **Input:** Concept description + related entity files
- **Output:** New `knowledge-graph/<domain>/<id>.md` files
- **Trigger:** `/kp:world "<concept>"`

### Strukturist (Planner)
- **Role:** Generates beat sheets from chapter outlines
- **Extended thinking:** OFF — structured output, not creative
- **Input:** Chapter outline + active entities + open plot threads
- **Output:** `beats/chapter-N.json` — array of beats with metadata
- **Beat schema:**
  ```json
  {
    "beat_id": "ch07-b03",
    "description": "Lex confronts the K0 signal",
    "active_alter": "lex",
    "emotional_register": "hypervigilant",
    "physics_element": "k0",
    "continuity_deps": ["riss", "kael", "k0"],
    "narrator_layer": "subjective"
  }
  ```

### Szenenschreiber (Drafter)
- **Role:** Generates German prose from beat + context
- **Extended thinking:** OFF — overthinking harms prose quality
- **Persona:** "Author mode" — inhabits character perspective
- **Context strategy:** Depends on `narrator_layer`
  - `subjective`: style-guide + voice_profile + qmd(alter interiority)
  - `objective`: all chapter entities + continuity deps
  - `dual`: both — used for scenes with deliberate unreliability
- **Output:** `drafts/chapter-N/beat-M.md`

### Kontinuitätswächter (Continuity Checker)
- **Role:** Validates draft against canonical entity state
- **Extended thinking:** ON — needs to reason across multiple entities
- **Persona:** "Assistant mode" — analytical, not creative
- **Checks:**
  1. Character knowledge violations
  2. Physics consistency (DKT, Landauer, Gödel references)
  3. Timeline violations
  4. Alter system violations
  5. Intentional unreliability exemptions (narrator_layer=subjective)
- **Output:** `reviews/chapter-N/continuity.json`
  ```json
  {
    "violations": [
      {"type": "character_knowledge", "line": 42, "description": "...", "severity": "error"}
    ],
    "exemptions_confirmed": ["kael-subjective-distortion"],
    "overall_pass": true
  }
  ```

### Stimmprüfer (Style Checker)
- **Role:** Validates voice consistency per active alter
- **Extended thinking:** OFF — pattern matching, not reasoning
- **Persona:** "Critic mode" — literary editor
- **Checks:** vocabulary register, sentence length, forbidden words, thematic alignment
- **Output:** `reviews/chapter-N/style.json`

### Perplexity Gate
- **Model:** Claude Haiku (fast, cheap)
- **Role:** Flags predictable/formulaic sentences
- **Threshold:** Equivalent to PPL < 22 (adapted for Claude scoring)
- **Output:** `reviews/chapter-N/perplexity.json` — flagged sentences
- **Trigger:** After Szenenschreiber, before Kontinuitätswächter

### Zustandsupdate (State Updater)
- **Role:** Extracts state changes from validated draft, updates KG
- **Extended thinking:** OFF — structured extraction
- **Extracts:** location changes, relationship changes, character knowledge updates, alter switches
- **Output:**
  - Updated `knowledge-graph/<domain>/<entity>.md` files
  - `state/ch-N/snapshot.json`
  - `state/current/` symlink update

## Prompt Patterns

### Drafter System Prompt (subjective scene)
```xml
<persona>
Du schreibst Kohärenz Protokoll auf Deutsch. Du bist gerade in der
subjektiven Perspektive von {active_alter}, einem Fragment von Kaels
dissoziativen System. Schreibe aus tiefer Innenperspektive — verzerrt,
fragmentiert, aber intern kohärent.
</persona>

<voice_samples>
{3-5 sample passages from active_alter's voice_profile.sample_passages}
</voice_samples>

<scene_beat>{beat_description}</scene_beat>

<context>
{prior_scene_summary}
{active_alter entity file — full content}
</context>

<constraints>
{style_guide_forbidden_elements}
Dieser Alter kennt folgendes NICHT: {knowledge_restricted_from_alter}
Narrator Layer: subjective — interne Kohärenz hat Vorrang vor Objektwahrheit.
</constraints>

<task>
Schreibe die Szene auf Deutsch. Ziel: ~{target_word_count} Wörter.
</task>
```

### Continuity Checker Prompt
```xml
<task>Prüfe diesen Entwurf auf Kontinuitätsverletzungen.</task>

<draft>{scene_draft}</draft>

<canon_sources>
  <entities>{relevant_entity_files}</entities>
  <physics>{physics_domain_entities}</physics>
  <timeline>{state/current/snapshot.json}</timeline>
</canon_sources>

<check_types>
  1. Character knowledge violations
  2. Physics consistency (DKT, Landauer, Gödel)
  3. Timeline violations
  4. Alter system violations
  WICHTIG: narrator_layer=subjective Szenen sind ABSICHTLICH unzuverlässig.
  Diese sind keine Fehler — bestätige ihre Präsenz als intended.
</check_types>

<output>JSON: violations[], exemptions_confirmed[], overall_pass: bool</output>
```

### Scene Planner Prompt
```xml
<task>Erstelle ein Beat-Sheet für Kapitel {N}: "{chapter_title}"</task>

<arc_context>
  Aktiver Handlungsbogen: {arc_name}
  Aktiver POV: {pov_character} (Alter: {active_alter})
  Thematisches Mandat: {themes_from_kg}
</arc_context>

<entity_context>{filtered_entities_for_chapter}</entity_context>

<constraints>
  - Beats müssen folgende offene Threads vorantreiben: {open_threads}
  - Diese Auflösungen sind für später reserviert: {reserved_for_later}
  - Physik-Konzepte in dieser Szene: {physics_entities}
</constraints>

<output>JSON-Array von Beats mit: beat_id, description, active_alter,
emotional_register, physics_element, continuity_deps, narrator_layer</output>
```

## State Updater Prompt
```xml
<task>Extrahiere alle kanonischen Zustandsänderungen aus diesem
validierten Kapitel.</task>

<validated_chapter>{chapter_prose}</validated_chapter>
<prior_state>{state/current/snapshot.json}</prior_state>

<extract>
  Für jede Entity im Kapitel:
  - Ortsveränderungen
  - Beziehungsveränderungen
  - Wissenszustandsänderungen (was hat wer erfahren?)
  - Alter-System-Wechsel
  - Physikzustandsänderungen
</extract>

<output>JSON: entity_id → diff. Nur veränderte Entities.</output>
```

## LangGraph State Machine (Simplified)

```python
from langgraph.graph import StateGraph, END

class WritingState(TypedDict):
    chapter: int
    beat: int
    beat_data: dict
    raw_draft: str | None
    continuity_report: dict | None
    style_report: dict | None
    perplexity_report: dict | None
    validated_draft: str | None
    revision_count: int

graph = StateGraph(WritingState)
graph.add_node("planner", run_planner)
graph.add_node("drafter", run_drafter)
graph.add_node("continuity", run_continuity_check)
graph.add_node("style", run_style_check)
graph.add_node("perplexity", run_perplexity_gate)
graph.add_node("state_updater", run_state_updater)

graph.add_conditional_edges("continuity", route_after_continuity, {
    "pass": "style",
    "fail": "drafter",   # re-draft with error context
    "max_retries": END,
})
graph.add_conditional_edges("style", route_after_style, {
    "pass": "perplexity",
    "fail": "drafter",
})
graph.add_edge("perplexity", "state_updater")
graph.add_edge("state_updater", END)
```
