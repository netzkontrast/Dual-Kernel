# Kohärenz Studio — Web UI Design

## Purpose

The web UI is a read-oriented companion to Claude Code.
Claude Code + plugin = write/craft. Web UI = visualize/browse/navigate.

Write-back from the web is deferred to Phase 4 (git API route).
Phase 3 delivers a protected read-heavy interface deployed on Vercel.

## 4 Core Views

### 1. `/graph` — Knowledge Graph Visualization
- Force-directed graph of all 177+ entities
- Node color = domain (aegis: red, character: blue, fundament: green, etc.)
- Node size = mention count (from extraction-report.md)
- Edge = relationship (from `related:` frontmatter)
- Click node → entity detail panel (slide-in)
- Filters: domain, canon_status, chapter appearance
- Component: `react-force-graph-2d` or `d3-force`

### 2. `/entities` — Entity Browser
- Left: filter sidebar (domain, canon_status, tags)
- Center: entity list with qmd-powered search bar
- Right: entity detail (frontmatter + rendered markdown + mini relation graph)
- Search: hybrid BM25 + vector via `/api/search?q=...`
- URL: `/entities?domain=character&canon=confirmed`
- Component: `EntityCard.tsx`, `SearchBar.tsx`

### 3. `/chapters` — Chapter Matrix
- 39-chapter grid × entity columns (from chapter-entity-matrix.md)
- Color: has entity = filled, absent = empty
- Beat status overlay: planned/drafted/validated/locked per chapter
- Click chapter row → expand to show beat breakdown from writing-state.json
- Component: `ChapterMatrix.tsx`

### 4. `/write` — Draft Viewer
- Read-only rendered markdown of `drafts/chapter-N/beat-M.md`
- Chapter selector + beat selector
- Side panel: entities active in that beat
- Phase 4 only: inline comment mode → git commit

## Authentication

```typescript
// middleware.ts
export { default } from "next-auth/middleware"
export const config = { matcher: ["/(protected)/:path*"] }

// Single-password auth — no OAuth needed for solo author
// .env: WRITING_SECRET=<strong-secret>
//       NEXTAUTH_SECRET=<random>
//       NEXTAUTH_URL=https://your-app.vercel.app
```

```typescript
// app/api/auth/[...nextauth]/route.ts
import CredentialsProvider from "next-auth/providers/credentials"

export const authOptions = {
  providers: [CredentialsProvider({
    credentials: { password: { type: "password" } },
    async authorize({ password }) {
      if (password === process.env.WRITING_SECRET) {
        return { id: "author", name: "Author" }
      }
      return null
    }
  })]
}
```

## API Routes

### `/api/search` — qmd Search
```typescript
// app/api/search/route.ts
import { exec } from "child_process"

export async function GET(req: Request) {
  const { searchParams } = new URL(req.url)
  const q = searchParams.get("q") ?? ""
  const collection = searchParams.get("c") ?? "kp-entities"

  return new Promise((resolve) => {
    exec(`qmd query "${q}" -c ${collection} --json`, (err, stdout) => {
      if (err) resolve(Response.json({ results: [] }))
      else resolve(Response.json({ results: JSON.parse(stdout) }))
    })
  })
}
```

### `/api/entities` — Entity CRUD
```typescript
// app/api/entities/route.ts
// GET: list with filters → calls `kp entity list --json`
// POST: create entity → calls `kp entity create --json`
import { execSync } from "child_process"

export async function GET(req: Request) {
  const { searchParams } = new URL(req.url)
  const domain = searchParams.get("domain")
  const cmd = domain
    ? `python3 -m kp.cli entity list --domain ${domain} --json`
    : `python3 -m kp.cli entity list --json`
  const result = execSync(cmd, { cwd: process.env.REPO_ROOT })
  return Response.json(JSON.parse(result.toString()))
}
```

### `/api/graph` — Graph Data
```typescript
// Returns D3-compatible nodes + links for react-force-graph
// GET /api/graph?depth=1&root=kael
export async function GET(req: Request) {
  const root = req.nextUrl.searchParams.get("root")
  const depth = req.nextUrl.searchParams.get("depth") ?? "1"
  const cmd = `python3 -m kp.cli graph neighbors ${root} --depth ${depth} --json`
  const result = execSync(cmd, { cwd: process.env.REPO_ROOT })
  return Response.json(JSON.parse(result.toString()))
}
```

## Component Sketches

### EntityGraph.tsx
```typescript
import ForceGraph2D from "react-force-graph-2d"

const DOMAIN_COLORS = {
  character: "#4A9EFF",
  aegis: "#FF4A4A",
  fundament: "#4AFF9E",
  world: "#FFD74A",
  physics: "#D74AFF",
}

export function EntityGraph({ nodes, links }) {
  return (
    <ForceGraph2D
      graphData={{ nodes, links }}
      nodeColor={n => DOMAIN_COLORS[n.domain] ?? "#999"}
      nodeRelSize={4}
      nodeVal={n => Math.sqrt(n.mention_count ?? 1) * 2}
      linkDirectionalArrowLength={4}
      onNodeClick={handleNodeClick}
    />
  )
}
```

### SearchBar.tsx
```typescript
export function SearchBar({ onResults }) {
  const [query, setQuery] = useState("")

  const search = useDebouncedCallback(async (q) => {
    const res = await fetch(`/api/search?q=${encodeURIComponent(q)}`)
    const { results } = await res.json()
    onResults(results)
  }, 300)

  return (
    <input
      type="search"
      placeholder="Semantic search... (e.g. 'Kael dissociation K0')"
      onChange={e => search(e.target.value)}
    />
  )
}
```

## Vercel Deployment

```bash
# Environment variables (Vercel dashboard)
WRITING_SECRET=<strong-password>
NEXTAUTH_SECRET=<random-32-chars>
NEXTAUTH_URL=https://kohaerenz.vercel.app
ANTHROPIC_API_KEY=<key>
REPO_ROOT=/var/task   # for API routes calling kp CLI

# Deploy
cd web/
vercel deploy --prod
```

**Note on API routes calling kp CLI:**
Vercel serverless functions can shell out to Python only if the Python runtime is available. Two options:
1. **Local dev only** — API routes work locally, web is read-only on Vercel (reads pre-built JSON exports)
2. **Vercel with Python** — use `@vercel/python` runtime for API routes that need `kp` CLI

Recommended: **Option 1 for Phase 3**, Option 2 for Phase 4. Build a `kp export --json` command that pre-generates static JSON in `web/public/data/` at commit time.

## next.config.ts
```typescript
const nextConfig = {
  experimental: { appDir: true },
  // During dev: proxy API calls to local kp server
  async rewrites() {
    return [
      {
        source: "/api/kp/:path*",
        destination: "http://localhost:8765/:path*",
      },
    ]
  },
}
export default nextConfig
```
