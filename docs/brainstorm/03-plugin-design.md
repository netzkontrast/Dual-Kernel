# Kohärenz Studio — Claude Code Plugin Design

## Plugin Overview

Everything lives in `.claude/`. Claude Code is the primary interface.
No separate app to launch. Skills are slash commands. Hooks automate.
MCP server gives Claude live access to the entity graph.

## Skills Reference

| Skill | Command | Persona | Primary Tools |
|-------|---------|---------|--------------|
| kp-entity | `/kp:entity` | Entity Manager | entity_lookup, entity_search, entity_create, entity_relate |
| kp-ask | `/kp:ask` | Graph Navigator | qmd_search, graph_neighbors |
| kp-state | `/kp:state` | Dashboard | writing_state_get, chapter_entities |
| kp-world | `/kp:world` | Weltbauer | entity_create, entity_search (think:ON) |
| kp-outline | `/kp:outline` | Strukturist | chapter_beats, chapter_entities |
| kp-scene | `/kp:scene` | Szenenschreiber | chapter_entities, entity_lookup, qmd_search |
| kp-dialogue | `/kp:dialogue` | Dialogcoach | entity_lookup (character psych entities) |
| kp-review | `/kp:review` | Lektor+Kontinuitätswächter | run_validate, full entity graph (think:ON) |
| kp-research | `/kp:research` | Forschungsassistent | qmd_search, entity_create |
| kp-validate | `/kp:validate` | Pipeline Runner | run_validate |
| kp-ingest | `/kp:ingest` | Pipeline Runner | run_ingest |
| kp-commit | `/kp:commit` | Commit + Memory | writing_state_set, git commit |

## Skill SKILL.md Template

Every skill follows this structure:

```markdown
---
name: kp-scene
description: Draft a scene beat as German prose using entity context
user-invocable: true
allowed-tools:
  - mcp__kp-server__entity_lookup
  - mcp__kp-server__chapter_entities
  - mcp__kp-server__writing_state_get
  - mcp__kp-server__qmd_search
  - Write
  - Bash
---

# /kp:scene — Szenenschreiber

## Trigger
/kp:scene [--chapter N] [--beat M] [--entities e1,e2]

## Behavioral Flow

1. LOAD — Call writing_state_get() if --chapter/--beat not specified
2. LOAD — Call chapter_entities(N) + entity_lookup for key entities
3. LOAD — Call qmd_search for semantic context
4. INSTRUCT — Assemble context bundle (narrator_layer-aware)
5. DRAFT — Generate German prose with Szenenschreiber persona
6. WRITE — Save to drafts/chapter-N/beat-M.md
7. VALIDATE — Run kp validate (Phase 2)
8. COMMIT — Update writing_state + commit

## Context Strategy

If narrator_layer = subjective:
  → style-guide.md + voice_profile + qmd(alter interiority)
  → DO NOT load all chapter entities (distract from voice)

If narrator_layer = objective/physics:
  → chapter_entities(N) + continuity_deps entity lookups
  → qmd_search(physics concepts, scene context)
```

## Session-Start Hook Output

Every session opens with this dashboard:

```
╔══════════════════════════════════════════════╗
║     KOHÄRENZ PROTOKOLL — Session Start       ║
╠══════════════════════════════════════════════╣
║  Active chapter:   7 — "Der Riss"            ║
║  Next beat:        Beat 3 of 8               ║
║  Draft progress:   2 / 8 beats complete      ║
║  Entities in ch7:  14 loaded                 ║
║  Last session:     2026-03-28                ║
║  Open conflicts:   2 disputed entities       ║
║  Validation:       ✓ Phase 2 passing         ║
╚══════════════════════════════════════════════╝

→ /kp:state    full dashboard
→ /kp:scene    continue drafting beat 3
→ /kp:ask      query the knowledge graph
→ /kp:entity   manage entities
```

Implementation (`session-start.sh`):
```bash
#!/bin/bash
# Read writing-state.json and print dashboard
python3 -c "
from kp.state import WritingState
from kp.entity import count_domain
state = WritingState.load()
# ... render dashboard
"
```

## Hooks Configuration

### hooks.json
```json
{
  "hooks": [
    {
      "event": "SessionStart",
      "script": ".claude/hooks/session-start.sh"
    },
    {
      "event": "PostToolUse",
      "matcher": { "tool": "Write", "path_pattern": "knowledge-graph/**/*.md" },
      "script": ".claude/hooks/post-edit-validate.sh"
    },
    {
      "event": "PreCommit",
      "script": ".claude/hooks/pre-commit-check.sh"
    }
  ]
}
```

### post-edit-validate.sh
```bash
#!/bin/bash
# Fires when any knowledge-graph/**/*.md is written
CHANGED_FILE="$1"
python3 tools/frontmatter_validator.py "$CHANGED_FILE" 2>&1 | head -20
# Warning only — does not block writes
```

### pre-commit-check.sh
```bash
#!/bin/bash
# Check if commit touches knowledge-graph/
if git diff --cached --name-only | grep -q "^knowledge-graph/"; then
  echo "Running Phase 2 validators..."
  python3 tools/frontmatter_validator.py knowledge-graph/ || exit 1
  python3 tools/wikilink_checker.py knowledge-graph/ || exit 1
  python3 tools/consistency_checker.py knowledge-graph/ || exit 1
fi
```

## MCP Server

### server.py (FastMCP)

```python
from fastmcp import FastMCP
from kp.entity import entity_lookup, entity_search, entity_create, entity_relate
from kp.graph import graph_neighbors, orphan_scan, deadlink_scan
from kp.chapter import chapter_entities, chapter_beats
from kp.state import writing_state_get, writing_state_set
from kp.pipeline import run_validate, run_ingest
from kp.search import qmd_search

mcp = FastMCP("kp-server")

@mcp.tool()
def entity_lookup(id: str) -> dict:
    """Get full entity: frontmatter YAML + markdown content."""

@mcp.tool()
def entity_search(query: str, domain: str = None, canon: str = None) -> list[dict]:
    """Search entities by name/tag/domain. Exact for structured, qmd for semantic."""

@mcp.tool()
def entity_create(data: dict) -> dict:
    """Create a new entity file with validated frontmatter."""

@mcp.tool()
def entity_relate(source_id: str, target_id: str) -> None:
    """Add target to source entity's related: list."""

@mcp.tool()
def graph_neighbors(id: str, depth: int = 1) -> dict:
    """Return entity + N-hop relationship graph."""

@mcp.tool()
def orphan_scan() -> list[str]:
    """Find entities with no incoming or outgoing links."""

@mcp.tool()
def deadlink_scan() -> list[dict]:
    """Find [[wikilinks]] pointing to non-existent entities."""

@mcp.tool()
def chapter_entities(chapter_n: int) -> list[dict]:
    """All entities appearing in chapter N from chapter matrix."""

@mcp.tool()
def chapter_beats(chapter_n: int) -> list[dict]:
    """Beat sheet for chapter N (from beats/chapter-N.json)."""

@mcp.tool()
def qmd_search(query: str, collection: str = "kp-entities") -> list[dict]:
    """Hybrid semantic+BM25 search via qmd CLI.
    Collections: kp-entities | kp-sources | kp-drafts"""

@mcp.tool()
def writing_state_get() -> dict:
    """Current chapter, beat, per-chapter draft status."""

@mcp.tool()
def writing_state_set(chapter: int, beat: int, status: str) -> None:
    """Update draft status. status: planned|drafted|validated|locked"""

@mcp.tool()
def run_validate(path: str = "knowledge-graph/") -> dict:
    """Run Phase 2 validators. Returns structured report."""

if __name__ == "__main__":
    mcp.run()
```

### settings.json — MCP Registration
```json
{
  "mcpServers": {
    "kp-server": {
      "command": "python3",
      "args": [".claude/mcp/kp-server/server.py"],
      "env": {
        "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}"
      }
    }
  }
}
```

## writing-state.json Schema

```json
{
  "active_chapter": 7,
  "active_beat": 3,
  "style_guide_version": "1.0",
  "chapters": {
    "1": { "status": "locked", "beats": 6, "beats_done": 6 },
    "7": {
      "status": "in_progress",
      "beats": 8,
      "beats_done": 2,
      "beats": {
        "1": "validated",
        "2": "validated",
        "3": "planned",
        "4": "planned"
      }
    }
  },
  "last_session": "2026-03-29",
  "open_conflicts": ["kael-timeline-dispute", "riss-physics-uncertain"]
}
```

## style-guide.md Template

```markdown
# Kohärenz Protokoll — Style Guide

## General Voice
- Language: German, literary register
- Sentence rhythm: fragmented for interior scenes, more composed for world scenes
- Philosophical terms: preserve technical accuracy

## Kael (Host System)
- Fragmented syntax mid-sentence when overwhelmed
- Self-referential loops ("...aber war das wirklich ich? War ich das gewesen?")
- Forbidden: complete sentences during dissociative episodes

## Lex (Alter)
- Cold, analytical, declarative
- Short sentences. No subordinate clauses in crisis moments.
- Forbidden: uncertainty markers ("vielleicht", "irgendwie")

## AEGIS
- Clinical precision, no human warmth
- Technical vocabulary from physics/mathematics domain
- No contractions, no colloquialisms

## Physics Scenes (DKT, K0/K1)
- Ground every physics reference in the entity definitions
- No invented terminology
- Cross-reference source: Markdown-docs/DualKernelAiAndNarrativeCollapse.md
```
