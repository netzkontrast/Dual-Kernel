# qmd Integration — Complete Technical Reference

*Research completed 2026-03-29. Source: https://github.com/tobi/qmd*

## What qmd Is

`@tobilu/qmd` (v2.0.1, MIT) is an on-device **hybrid search engine** for markdown files.

Three-layer pipeline:
1. **BM25 full-text** (SQLite FTS5)
2. **Vector semantic** (GGUF embeddings via node-llama-cpp)
3. **LLM re-ranking** (fine-tuned Qwen3-based reranker)

All inference is local. No API keys. Index = single SQLite file.

**Requirements:** Node.js >= 22 (hard constraint)

## Models (auto-downloaded ~1.9 GB total)

| Role | Model | Size |
|------|-------|------|
| Embeddings | embeddinggemma-300M-Q8_0 | ~300M params |
| Re-ranking | Qwen3-Reranker-0.6B-Q8_0 | ~600M params |
| Query expansion | qmd-query-expansion-1.7B-q4_k_m | ~1.7B params |

All models are **multilingual** — German works natively.
Downloaded to `~/.cache/qmd/models` on first `qmd embed` run.

## Installation

```bash
npm install -g @tobilu/qmd   # Node.js >= 22 required
qmd --version                # verify
```

## CLI Commands

```bash
# Collections
qmd collection add knowledge-graph/ --name kp-entities
qmd collection add Markdown-docs/   --name kp-sources
qmd collection add drafts/          --name kp-drafts

# Context annotations (improves relevance)
qmd context add qmd://kp-entities "Kohärenz Protokoll entity knowledge graph"
qmd context add qmd://kp-sources  "German research and design documents"

# Index
qmd embed                    # Build vector index (first run ~16s cold start)
qmd update                   # BM25 only (fast, no models)

# Search modes
qmd search  "riss"           # BM25 keyword (fast)
qmd vsearch "fragmentation"  # Vector semantic only
qmd query   "Kael K0 riss"   # HYBRID: expansion + BM25 + vector + reranking (best)

# Scoped
qmd query "alter interiority" -c kp-entities
qmd query "dissociation"      -c kp-sources

# Machine-readable
qmd query "riss kael" --json -n 10
```

## Built-in MCP Server (Key Finding)

qmd ships with a **built-in MCP server** — no custom wrapper needed.

```bash
# Stdio (for Claude Desktop)
qmd mcp

# HTTP daemon (recommended — keeps models warm, 10ms warm latency vs 16s cold)
qmd mcp --http              # binds localhost:8181
qmd mcp --http --port 8080  # custom port
qmd mcp --http --daemon     # background daemon

# Stop daemon
qmd mcp stop
```

**HTTP endpoint:** `POST localhost:8181/mcp` — MCP Streamable HTTP (JSON-RPC 2.0)
**Health check:** `GET localhost:8181/health`

**MCP tools exposed:**

| Tool | Description |
|------|-------------|
| `query` | Hybrid search: expansion + BM25 + vector + reranking |
| `get` | Retrieve document by path or docid |
| `multi_get` | Batch retrieval by glob pattern |
| `status` | Index health, collection metadata |

## Architecture Decision: Use qmd as a Separate MCP Server

Since qmd has a built-in MCP server, **register it directly in `.claude/settings.json`** alongside `kp-server`. This gives Claude native access to semantic search without any wrapper code:

```json
{
  "mcpServers": {
    "kp-server": {
      "command": "python3",
      "args": [".claude/mcp/kp-server/server.py"]
    },
    "qmd": {
      "command": "qmd",
      "args": ["mcp"]
    }
  }
}
```

For the MCP server daemon (better performance), use HTTP transport:

```json
{
  "mcpServers": {
    "qmd": {
      "command": "qmd",
      "args": ["mcp", "--http", "--daemon"],
      "httpEndpoint": "http://localhost:8181/mcp"
    }
  }
}
```

Claude can then call `qmd.query()`, `qmd.get()`, `qmd.multi_get()` directly in skills.

## Python Integration — kp/ Package

For `kp/search.py`, use the HTTP daemon (avoids subprocess overhead):

```python
# kp/search.py
import httpx
import json

QMD_HTTP = "http://localhost:8181/mcp"

def qmd_search(query: str, collection: str = "kp-entities", limit: int = 10) -> list[dict]:
    """Hybrid semantic search via qmd HTTP daemon."""
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "query",
            "arguments": {
                "query": query,
                "collection": collection,
                "n": limit,
            }
        }
    }
    resp = httpx.post(QMD_HTTP, json=payload, timeout=30.0)
    resp.raise_for_status()
    return resp.json()["result"]["content"]


def qmd_get(path: str) -> dict:
    """Retrieve document by relative path."""
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": "get", "arguments": {"path": path}}
    }
    resp = httpx.post(QMD_HTTP, json=payload, timeout=30.0)
    resp.raise_for_status()
    return resp.json()["result"]["content"]


# Fallback: subprocess if daemon not running
def qmd_search_cli(query: str, collection: str = None, limit: int = 10) -> list[dict]:
    import subprocess
    cmd = ["qmd", "query", query, "--json", "-n", str(limit)]
    if collection:
        cmd += ["-c", collection]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return json.loads(result.stdout)
```

## Next.js Integration (Phase 3 Web UI)

qmd SDK works directly in Next.js API routes (Node.js runtime only — NOT edge):

```typescript
// web/app/api/search/route.ts
import { createStore } from '@tobilu/qmd'
import { NextRequest, NextResponse } from 'next/server'

export const runtime = 'nodejs'  // REQUIRED — qmd uses native SQLite bindings

let store: Awaited<ReturnType<typeof createStore>> | null = null

async function getStore() {
  if (!store) {
    store = await createStore({
      dbPath: process.env.QMD_DB_PATH ?? './qmd-index.sqlite',
    })
  }
  return store
}

export async function GET(req: NextRequest) {
  const q = req.nextUrl.searchParams.get('q') ?? ''
  const collection = req.nextUrl.searchParams.get('c') ?? undefined

  const s = await getStore()
  const results = await s.search({ query: q, limit: 10, minScore: 0.3 })

  return NextResponse.json(results.map(r => ({
    title: r.title,
    path: r.displayPath,
    score: r.score,
    collection: r.collectionName,
    context: r.context,
  })))
}
```

## Vercel Deployment Constraint

qmd uses `better-sqlite3` (native bindings) and `node-llama-cpp` — these **cannot run on Vercel Edge or Vercel Serverless** without bundling native binaries.

**Recommended approach for Vercel:**

1. **Build step**: run `qmd embed` locally and commit the `.sqlite` index
2. **Deploy**: bundle the pre-built index with the deployment
3. **Runtime**: use `@tobilu/qmd` SDK in Node.js API routes pointing at the bundled SQLite

```bash
# next.config.ts — pre-build hook
# package.json scripts
{
  "scripts": {
    "prebuild": "qmd update && qmd embed",
    "build": "next build"
  }
}
```

```bash
# .env (Vercel)
QMD_DB_PATH=/var/task/qmd-index.sqlite   # bundled index path on Vercel
```

**Alternative**: Use the HTTP daemon locally, pre-export search results to static JSON for Vercel (read-only search on deployed site).

## Session Start — Daemon Management

Add to `session-start.sh`:

```bash
# Ensure qmd daemon is running for fast search
if ! curl -s http://localhost:8181/health > /dev/null 2>&1; then
  echo "Starting qmd search daemon..."
  qmd mcp --http --daemon
  sleep 2  # wait for model load
  echo "qmd ready (warm latency ~10ms)"
fi
```

## qmd Configuration File

`~/.config/qmd/index.yml` or project-local `.qmd.yml`:

```yaml
global_context: >
  Kohärenz Protokoll knowledge graph — German narrative fiction project.
  Entities: characters (Kael, Juna, Lex), physics (DKT, K0, K1),
  AEGIS AI system, fundament concepts (Riss, fragmentation).

collections:
  kp-entities:
    path: ./knowledge-graph
    pattern: "**/*.md"
    context:
      "/": "Entity knowledge graph — YAML frontmatter + markdown content"
      "/character": "Characters, alter system (TSDP/IFS), voice profiles"
      "/aegis": "AEGIS superintelligence system entities"
      "/fundament": "Core concepts: Riss, DKT, K0/K1, Landauer, Gödel"
      "/physics": "Physics domain entities"
      "/scene-registry": "Scene-level entities with beat/chapter data"

  kp-sources:
    path: ./Markdown-docs
    pattern: "**/*.md"
    context:
      "/": "German research and design documents — source of truth for all entities"

  kp-drafts:
    path: ./drafts
    pattern: "**/*.md"
    context:
      "/": "Scene drafts organized by chapter and beat"
```

## Latency Profile

| Operation | Latency |
|-----------|---------|
| Model cold start | ~16 seconds |
| Warm query (daemon) | ~10ms |
| `qmd update` (BM25 only) | < 1 second |
| `qmd embed` (full corpus 94 docs) | ~2-5 minutes first run |
| Re-index after single file change | ~30 seconds |

**Key implication**: Always run `qmd mcp --http --daemon` via `session-start.sh`. Never cold-start qmd mid-skill — the 16s latency would break the writing flow.

## Summary: How qmd Fits the Stack

```
Claude Code skills
    │
    ├── kp-server MCP (Python/FastMCP)
    │     entity_lookup, graph_neighbors, writing_state, pipeline
    │
    └── qmd MCP (built-in, qmd mcp)
          query, get, multi_get, status
          Indexes: kp-entities, kp-sources, kp-drafts

Next.js Web UI
    └── @tobilu/qmd SDK (Node.js API routes)
          Pre-built .sqlite index bundled with Vercel deploy
```
