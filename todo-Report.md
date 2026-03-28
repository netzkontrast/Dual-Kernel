# Comprehensive Todo & Refactoring Report

**Date:** 2026-03-28
**Subject:** Integration of `zircote/mnemonic` with the `Dual-Kernel` (Kohärenz Protokoll) Multi-Agent Architecture

## Executive Summary
Recent iterations successfully introduced the `Memory Integrator` skill to prevent memory degradation and ported the full `zircote/mnemonic` repository into `.claude/mnemonic/` and `.claude/skills/`. The hooks (`SessionStart`, `PreToolUse`, `UserPromptSubmit`, `PostToolUse`, `Stop`) and custom commands (e.g., `/mnemonic:capture`) are registered in `.claude/settings.json`.

However, the rapid integration has surfaced significant structural and architectural inconsistencies between the native Dual-Kernel paradigm and the imported Mnemonic framework. This document details these inconsistencies, poses critical architectural questions, and provides concrete steps to resolve them.

---

## 1. Directory Structure: Flat Namespace vs. Hierarchical Ontology

### Current State & Inconsistency
- **Dual-Kernel Paradigm:** The project specifies a flat memory hierarchy at the root level: `_episodic/`, `_semantic/`, and `_procedural/`.
- **Mnemonic Paradigm:** The Mnemonic tools (especially `setup.md`, `search.md`, and its Python path resolver `lib/paths.py`) aggressively default to an `{org}/{project}/{namespace}` hierarchy (e.g., `default/Dual-Kernel/_semantic/decisions/`).
- **Conflict:** While `capture.md` and `config.py` were hotfixed to use `MNEMONIC_ROOT=.`, running commands like `/mnemonic:setup` or using the `memory-curator` agent will still attempt to construct the `{org}/{project}` nested structure.

### Questions
1. Should we permanently fork Mnemonic's path resolution (`lib/paths.py`) to eliminate the `{org}/{project}` hierarchy entirely for this repository?
2. Or should we accept the Mnemonic V2 structure and move our existing `_episodic/`, `_semantic/`, `_procedural/` folders into a `Kohärenz/Dual-Kernel/` subdirectory?

### How to Resolve
- **Recommendation:** Fork the path resolution. Since this is a self-contained narrative/system-theory project, the enterprise-grade `{org}/{project}` scoping is unnecessary overhead.
- **Action Items:**
  1. Refactor `.claude/mnemonic/lib/paths.py` to remove `_get_v2_memory_dir` and `_get_legacy_memory_dir`, replacing them with a strict flat resolver: `return self.context.memory_root / namespace`.
  2. Refactor `.claude/mnemonic/commands/setup.md` to stop creating `{org}/{project}` directories.

---

## 2. The Two Knowledge Systems: ETL Pipeline vs. Mnemonic

### Current State & Inconsistency
- **The ETL Pipeline (`tools/common.py`):** Extracts narrative entities (Characters, Physics, AEGIS protocols) from the German `Markdown-docs/` into strict YAML-frontmatter files in `knowledge-graph/` using Pydantic v2.
- **Mnemonic Memory System:** Captures meta-agent decisions, session logs, and autopoietic loop reflections into `_semantic/`, `_episodic/`, and `_procedural/` using MIF Level 3 formatting.
- **Conflict:** Both systems generate Markdown files with YAML frontmatter, and both claim to handle "semantic" knowledge. There is a risk that Mnemonic's `ontology-discovery` or `search` agents might accidentally ingest or modify the `knowledge-graph/` files, or vice versa.

### Questions
1. What is the explicit boundary between `knowledge-graph/` and `_semantic/`?
2. Should Mnemonic's `search.md` be restricted from indexing `knowledge-graph/`, or should the two systems eventually merge?

### How to Resolve
- **Recommendation:** Maintain strict separation. `knowledge-graph/` is the **Object Level** (the narrative world), while `_semantic/`, `_episodic/`, and `_procedural/` are the **Meta Level** (the agents building the world).
- **Action Items:**
  1. Update `.claude/mnemonic/commands/search.md` and the `qmd-setup` scripts to explicitly exclude the `knowledge-graph/` and `Markdown-docs/` directories from their glob patterns.
  2. Document this exact boundary in `CLAUDE.md`.

---

## 3. Redundancy: Memory Integrator vs. Mnemonic Core

### Current State & Inconsistency
- **`Memory Integrator`:** A custom skill explicitly designed to force the LLM to reflect on recent commits/friction and append an "Appendix of Lessons Learned" to `_episodic/iteration-history.memory.md`.
- **Mnemonic Core / Custodian:** Provides native tools (`/mnemonic:capture`, `/mnemonic:gc`, `memory-curator`) to handle memory creation, deduplication, and decay.
- **Conflict:** The `Memory Integrator` skill is currently bridging the gap by instructing the LLM to use `/mnemonic:capture`. However, Mnemonic's native `Stop` and `SessionStart` hooks are also trying to do session summarization automatically. This leads to double-capturing or conflicting prompts during the "Stop" phase of an agent loop.

### Questions
1. Does the `Memory Integrator` skill need to exist if Mnemonic's `Stop` hook (`hooks/stop.py`) natively handles session summarization?
2. How do we ensure Mnemonic's automated captures adhere to the *Dual-Kernel ontological mapping* (Psychology, Quantum Physics, Topology)?

### How to Resolve
- **Recommendation:** Merge the `Memory Integrator` logic into Mnemonic's native hook system.
- **Action Items:**
  1. Modify `.claude/mnemonic/hooks/stop.py` (or the `blackboard` skill) to explicitly require the Dual-Kernel ontological mapping (Psychology, Quantum Physics, Systems Theory) when it auto-summarizes a session.
  2. Once the native Mnemonic hooks are generating Dual-Kernel compliant summaries, deprecate the manual `Memory Integrator` skill from `.claude/settings.json`.

---

## 4. The `CLAUDE_PLUGIN_ROOT` Environment Variable

### Current State & Inconsistency
- `session-start.sh` exports `CLAUDE_PLUGIN_ROOT=".claude/mnemonic"`.
- However, Mnemonic's internal scripts (like `lib/ontology.py` and `commands/validate.md`) occasionally assume the plugin is located at `~/.claude/plugins/mnemonic/` or use `$(dirname $(dirname $0))` which can break depending on the shell context.

### Questions
1. Is `.claude/mnemonic` the final home for this framework, or should it be converted into a true Claude Code Plugin in the future?

### How to Resolve
- **Recommendation:** Standardize the relative paths.
- **Action Items:**
  1. Audit all bash scripts in `.claude/mnemonic/commands/` and replace `~/.claude/plugins/mnemonic` fallbacks with `${CLAUDE_PLUGIN_ROOT:-.claude/mnemonic}`.
  2. Ensure Python hooks in `.claude/mnemonic/hooks/` use `pathlib` relative to the project root rather than hardcoded absolute paths.

---

## Summary of Next Steps for the Skill-Engineer

1. Execute a targeted refactor of `.claude/mnemonic/lib/paths.py` to enforce the flat memory architecture.
2. Update Mnemonic's search bounds to ignore `knowledge-graph/`.
3. Port the Dual-Kernel ontological mapping logic from `memory-integrator/SKILL.md` directly into `.claude/mnemonic/hooks/stop.py`.
4. Run `/mnemonic:setup` (after fixing paths) to validate the new unified architecture.