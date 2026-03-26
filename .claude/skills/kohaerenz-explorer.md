# Kohärenz Explorer

Interactive skill for exploring and managing the Kohärenz Protokoll knowledge base.

## Usage

`/kohaerenz-explorer [command] [args]`

## Commands

When this skill is invoked, determine which command the user wants based on their input and execute accordingly:

### `search <term>` -- Search across all documents and entities
Search for a term across `Markdown-docs/` and `knowledge-graph/`. Show:
- File matches with context (2 lines before/after)
- Entity matches from the knowledge graph
- Related entities via wikilinks
- Domain classification

### `entity <name>` -- Show entity details
Look up an entity in `knowledge-graph/`. Display:
- Full YAML frontmatter (domain, canon_status, aliases, tags)
- Summary content
- All sources with file references
- Conflicts and their severity
- Related entities
- If the entity doesn't exist in the knowledge graph, search `Markdown-docs/` for mentions and suggest creating it.

### `domain <domain-name>` -- List all entities in a domain
Show all entities within a given domain (character, aegis, world, physics, etc.).
Read the domain's README.md and list all entity files with their canon_status.

### `conflicts` -- Show all unresolved conflicts
Scan `knowledge-graph/` for entities with `canon_status: disputed` or `uncertain`.
Group by severity and suggest resolution paths.

### `stats` -- Show project statistics
Report:
- Total entities in knowledge-graph (count files per domain)
- Total research documents in Markdown-docs/
- Coverage: which domains have good coverage, which are sparse
- Conflict count by status

### `validate` -- Run validation checks
Execute the validation pipeline:
1. Check all entity files for valid YAML frontmatter
2. Verify wikilink integrity
3. Report any schema violations or broken links
4. Suggest fixes for common issues

### `glossary <term>` -- Explain a project-specific term
Look up the term in the codebase. Search `tools/common.py` KNOWN_ENTITIES, `Markdown-docs/`, and `knowledge-graph/`. Provide:
- German term and English translation (if applicable)
- Domain classification
- Brief explanation based on source documents
- Related terms

### `map` -- Show entity relationship overview
Read all entity files in `knowledge-graph/` and build a relationship map from `related` fields in YAML frontmatter. Present as a structured text diagram showing connections between entities grouped by domain.

### `chapter <number>` -- Show chapter details
Search for chapter-related content in `Markdown-docs/40ChapterPlotModule.md` and related narrative documents. Show:
- Chapter title and summary
- Key entities appearing in the chapter
- Plot points and narrative beats

### Default (no command)
If invoked without a specific command, show a welcome message with available commands and current project stats (entity count, document count, conflict count).

## Implementation Notes

- Always read `CLAUDE.md` before making any changes
- Use Grep and Glob tools for searching, not bash grep
- Entity names may contain German characters (umlauts, etc.)
- Present results in clean, formatted markdown
- For `validate`, read the actual Python tool files and describe what they check, or run them if .venv is available
