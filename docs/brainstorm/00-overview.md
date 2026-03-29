# Kohärenz Studio — Brainstorm Overview

**Session date:** 2026-03-29
**Status:** Architecture finalized, ready for implementation

## What This Is

**Kohärenz Studio** is a Claude Code plugin + web UI that transforms the Dual-Kernel repository into a fully integrated novel authoring environment. Claude Code remains the primary interface. Everything is a plugin.

## The Problem It Solves

| Current | After |
|---------|-------|
| 15 independent scripts invoked separately | One `kp` CLI + 12 slash commands |
| No entity search or browse | qmd-powered semantic search |
| No writing assistance | 7 specialized writing agents |
| No unified session context | Writing dashboard at every session start |
| No draft infrastructure | `drafts/chapter-N/beat-M.md` + state tracking |
| No web visualization | Next.js knowledge graph + entity browser |

## Document Index

| File | Contents |
|------|---------|
| `01-architecture.md` | Complete system architecture |
| `02-agent-pipeline.md` | 7 writing agents, LangGraph orchestration, prompt patterns |
| `03-plugin-design.md` | Claude Code plugin: skills, hooks, MCP server |
| `04-web-ui.md` | Next.js app, qmd search, Vercel deployment |
| `05-implementation-roadmap.md` | 4 build phases, task breakdown |
| `06-research-findings.md` | Full research report: agentic writing, RAG, KG for fiction |

## Key Design Decisions

| Decision | Choice | Reason |
|----------|--------|--------|
| Primary interface | Claude Code | Already in use; plugin approach zero-friction |
| Agent model | claude-sonnet-4-6 + full entity files | No chunking needed — entities fit in context |
| Search | `@tobilu/qmd` (hybrid BM25 + vector) | Already in project, indexes markdown natively |
| Web framework | Next.js → Vercel | API routes + React, single deploy |
| Auth | WRITING_SECRET single password | Single author, no OAuth overhead |
| Persistence | Git repo | Every write = commit, no database |
| Orchestration | LangGraph | State machine matches existing conditional pipeline logic |
| Memory | Mnemonic `_episodic/` | Already integrated, persists across sessions |
| Language | Python (kp/ core) + TypeScript (web/) | Matches existing stack |

## Critical Research Finding

> KG entity grounding works well for physics/AEGIS/world scenes.
> For Kael's interior/psychological scenes, style-guide retrieval outperforms entity lookup.
> These require different context assembly strategies.

This distinction drives the `narrator_layer: subjective|objective` field in the YAML schema and the `assemble_scene_context()` branching logic.
