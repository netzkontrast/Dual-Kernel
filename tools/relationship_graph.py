"""Generate entity relationship visualization as Mermaid graph."""
import os
import re
import glob
import yaml
import click
from collections import defaultdict
from common import console, slugify, KG_DIR, VALID_DOMAINS


def parse_frontmatter(filepath):
    """Extract YAML frontmatter from a markdown file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if not content.startswith('---'):
        return None
    end_idx = content.find('---', 3)
    if end_idx == -1:
        return None
    try:
        return yaml.safe_load(content[3:end_idx])
    except yaml.YAMLError:
        return None


def load_all_entities():
    """Load all entity frontmatter from the knowledge graph."""
    entities = {}
    files = glob.glob(f'{KG_DIR}/**/*.md', recursive=True)
    for f in files:
        if f.endswith('README.md'):
            continue
        data = parse_frontmatter(f)
        if data and 'title' in data:
            entities[data['title']] = data
    return entities


DOMAIN_COLORS = {
    "character": "#4A90D9",
    "alter-system": "#9B59B6",
    "world": "#27AE60",
    "physics": "#E67E22",
    "aegis": "#E74C3C",
    "narrative": "#F1C40F",
    "style": "#1ABC9C",
    "philosophy": "#8E44AD",
    "theme": "#D35400",
    "mechanic": "#2980B9",
    "juna": "#E91E63",
    "fundament": "#607D8B",
    "mathematics": "#795548",
}

DOMAIN_SHAPES = {
    "character": ("([", "])"),
    "aegis": ("{{", "}}"),
    "physics": ("[[", "]]"),
    "world": (">", "]"),
    "mechanic": ("[/", "/]"),
}


def sanitize_id(name):
    """Create a valid Mermaid node ID from an entity name."""
    return re.sub(r'[^a-zA-Z0-9]', '_', name)


@click.command()
@click.option('--output', '-o', default=None,
              help='Output file path (default: knowledge-graph/_index/relationship-graph.md)')
@click.option('--format', 'fmt', type=click.Choice(['mermaid', 'html']), default='mermaid',
              help='Output format')
@click.option('--domain-filter', '-d', default=None,
              help='Filter to specific domain (comma-separated)')
def graph(output, fmt, domain_filter):
    """Generate an entity relationship graph from knowledge-graph files."""
    entities = load_all_entities()

    if not entities:
        console.print("[bold red]No entities found in knowledge graph.[/bold red]")
        return

    # Apply domain filter
    if domain_filter:
        allowed = {d.strip() for d in domain_filter.split(',')}
        entities = {k: v for k, v in entities.items() if v.get('domain') in allowed}

    # Build adjacency data
    link_pattern = re.compile(r'\[\[(.*?)\]\]')
    edges = []
    edge_set = set()
    domain_groups = defaultdict(list)

    for name, data in entities.items():
        domain = data.get('domain', 'fundament')
        domain_groups[domain].append(name)

        related = data.get('related', [])
        if not related or related == []:
            continue

        for rel in related:
            if isinstance(rel, str):
                match = link_pattern.search(rel)
                if match:
                    target = match.group(1).partition('|')[0]
                    # Only include edges where both nodes exist
                    if target in entities:
                        edge_key = tuple(sorted([name, target]))
                        if edge_key not in edge_set:
                            edge_set.add(edge_key)
                            edges.append((name, target))

    # Build conflict hotspots
    conflict_nodes = set()
    for name, data in entities.items():
        conflicts = data.get('conflicts')
        if conflicts and conflicts != [] and conflicts != '[]':
            conflict_nodes.add(name)

    # Generate Mermaid
    lines = ["graph TD"]

    # Style definitions
    for domain, color in DOMAIN_COLORS.items():
        lines.append(f"    classDef {domain.replace('-', '_')} fill:{color},stroke:#333,color:#fff")
    lines.append("    classDef conflict stroke:#ff0000,stroke-width:3px,stroke-dasharray: 5 5")

    # Domain subgraphs
    for domain in sorted(domain_groups.keys()):
        members = domain_groups[domain]
        lines.append(f"    subgraph {domain.replace('-', '_')}_group [\"{domain.upper()}\"]")
        for name in sorted(members):
            node_id = sanitize_id(name)
            shape_open, shape_close = DOMAIN_SHAPES.get(domain, ("[", "]"))
            label = name.replace('"', "'")
            lines.append(f"        {node_id}{shape_open}\"{label}\"{shape_close}")
        lines.append("    end")

    # Edges
    for src, tgt in edges:
        src_id = sanitize_id(src)
        tgt_id = sanitize_id(tgt)
        lines.append(f"    {src_id} --- {tgt_id}")

    # Apply domain classes
    for domain, members in domain_groups.items():
        ids = ",".join(sanitize_id(m) for m in members)
        if ids:
            lines.append(f"    class {ids} {domain.replace('-', '_')}")

    # Mark conflict nodes
    if conflict_nodes:
        ids = ",".join(sanitize_id(n) for n in conflict_nodes if n in entities)
        if ids:
            lines.append(f"    class {ids} conflict")

    mermaid_code = "\n".join(lines)

    # Compute statistics
    total_nodes = len(entities)
    total_edges = len(edges)
    total_conflicts = len(conflict_nodes)
    domains_used = len(domain_groups)

    # Density: ratio of edges to max possible edges
    max_edges = total_nodes * (total_nodes - 1) / 2 if total_nodes > 1 else 1
    density = total_edges / max_edges

    # Connection counts per entity
    connection_counts = defaultdict(int)
    for src, tgt in edges:
        connection_counts[src] += 1
        connection_counts[tgt] += 1

    hub_entities = sorted(connection_counts.items(), key=lambda x: x[1], reverse=True)[:5]

    if fmt == 'html':
        content = f"""<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<title>Kohärenz Protokoll - Entity Relationship Graph</title>
<script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
<style>
body {{ font-family: sans-serif; margin: 2em; background: #1a1a2e; color: #eee; }}
h1 {{ color: #4A90D9; }}
.stats {{ background: #16213e; padding: 1em; border-radius: 8px; margin: 1em 0; }}
.mermaid {{ background: #0f3460; padding: 1em; border-radius: 8px; }}
</style>
</head><body>
<h1>Entity Relationship Graph</h1>
<div class="stats">
<p><strong>Nodes:</strong> {total_nodes} | <strong>Edges:</strong> {total_edges} | <strong>Domains:</strong> {domains_used} | <strong>Conflicts:</strong> {total_conflicts} | <strong>Density:</strong> {density:.3f}</p>
</div>
<div class="mermaid">
{mermaid_code}
</div>
<script>mermaid.initialize({{startOnLoad:true, theme:'dark'}});</script>
</body></html>"""
    else:
        content = f"""# Entity Relationship Graph

**Generated:** Automatisch generiert aus `knowledge-graph/`

## Statistics

| Metric | Value |
|--------|-------|
| Entities | {total_nodes} |
| Relationships | {total_edges} |
| Domains | {domains_used} |
| Conflict Hotspots | {total_conflicts} |
| Graph Density | {density:.3f} |

## Hub Entities (Most Connected)

"""
        for name, count in hub_entities:
            domain = entities[name].get('domain', '?')
            conflict_marker = " ⚠️" if name in conflict_nodes else ""
            content += f"- **{name}** ({domain}): {count} connections{conflict_marker}\n"

        content += f"""
## Relationship Graph

```mermaid
{mermaid_code}
```

## Domain Legend

"""
        for domain in sorted(domain_groups.keys()):
            count = len(domain_groups[domain])
            color = DOMAIN_COLORS.get(domain, '#999')
            content += f"- **{domain}**: {count} entities ({color})\n"

        content += "\n_Automatisch generiert von `relationship_graph.py`._\n"

    # Write output
    if output is None:
        ext = '.html' if fmt == 'html' else '.md'
        index_dir = os.path.join(KG_DIR, '_index')
        os.makedirs(index_dir, exist_ok=True)
        output = os.path.join(index_dir, f'relationship-graph{ext}')

    os.makedirs(os.path.dirname(output), exist_ok=True)
    with open(output, 'w', encoding='utf-8') as f:
        f.write(content)

    console.print(f"[bold green]Generated relationship graph:[/bold green] {output}")
    console.print(f"  Entities: {total_nodes} | Edges: {total_edges} | Domains: {domains_used} | Conflicts: {total_conflicts}")

    if hub_entities:
        console.print("\n[bold cyan]Hub Entities:[/bold cyan]")
        for name, count in hub_entities:
            console.print(f"  - {name}: {count} connections")


if __name__ == '__main__':
    graph()
