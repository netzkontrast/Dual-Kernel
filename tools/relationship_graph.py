"""Generate entity relationship visualization as Mermaid graph."""
import os
import re
import click
from collections import defaultdict
from common import console, KG_DIR, load_all_entities, WIKILINK_REGEX, DomainEnum


DOMAIN_COLORS = {d.value: c for d, c in {
    DomainEnum.CHARACTER: "#4A90D9",
    DomainEnum.ALTER_SYSTEM: "#9B59B6",
    DomainEnum.WORLD: "#27AE60",
    DomainEnum.PHYSICS: "#E67E22",
    DomainEnum.AEGIS: "#E74C3C",
    DomainEnum.NARRATIVE: "#F1C40F",
    DomainEnum.STYLE: "#1ABC9C",
    DomainEnum.PHILOSOPHY: "#8E44AD",
    DomainEnum.THEME: "#D35400",
    DomainEnum.MECHANIC: "#2980B9",
    DomainEnum.JUNA: "#E91E63",
    DomainEnum.FUNDAMENT: "#607D8B",
    DomainEnum.MATHEMATICS: "#795548",
}.items()}

DOMAIN_SHAPES = {
    DomainEnum.CHARACTER.value: ("([", "])"),
    DomainEnum.AEGIS.value: ("{{", "}}"),
    DomainEnum.PHYSICS.value: ("[[", "]]"),
    DomainEnum.WORLD.value: (">", "]"),
    DomainEnum.MECHANIC.value: ("[/", "/]"),
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
    all_entities = load_all_entities()
    entities = {name: info['data'] for name, info in all_entities.items()}

    if not entities:
        console.print("[bold red]No entities found in knowledge graph.[/bold red]")
        return

    if domain_filter:
        allowed = {d.strip() for d in domain_filter.split(',')}
        entities = {k: v for k, v in entities.items() if v.get('domain') in allowed}

    edges = []
    edge_set = set()
    domain_groups = defaultdict(list)
    conflict_nodes = set()

    for name, data in entities.items():
        domain = data.get('domain', DomainEnum.FUNDAMENT.value)
        domain_groups[domain].append(name)

        conflicts = data.get('conflicts')
        if conflicts and conflicts != [] and conflicts != '[]':
            conflict_nodes.add(name)

        related = data.get('related', [])
        if not related:
            continue

        for rel in related:
            if isinstance(rel, str):
                match = WIKILINK_REGEX.search(rel)
                if match:
                    target = match.group(1).partition('|')[0]
                    if target in entities:
                        edge_key = tuple(sorted([name, target]))
                        if edge_key not in edge_set:
                            edge_set.add(edge_key)
                            edges.append((name, target))

    # Generate Mermaid
    lines = ["graph TD"]

    for domain, color in DOMAIN_COLORS.items():
        lines.append(f"    classDef {domain.replace('-', '_')} fill:{color},stroke:#333,color:#fff")
    lines.append("    classDef conflict stroke:#ff0000,stroke-width:3px,stroke-dasharray: 5 5")

    for domain in sorted(domain_groups.keys()):
        members = domain_groups[domain]
        lines.append(f"    subgraph {domain.replace('-', '_')}_group [\"{domain.upper()}\"]")
        for name in sorted(members):
            node_id = sanitize_id(name)
            shape_open, shape_close = DOMAIN_SHAPES.get(domain, ("[", "]"))
            label = name.replace('"', "'")
            lines.append(f"        {node_id}{shape_open}\"{label}\"{shape_close}")
        lines.append("    end")

    for src, tgt in edges:
        lines.append(f"    {sanitize_id(src)} --- {sanitize_id(tgt)}")

    for domain, members in domain_groups.items():
        ids = ",".join(sanitize_id(m) for m in members)
        if ids:
            lines.append(f"    class {ids} {domain.replace('-', '_')}")

    if conflict_nodes:
        ids = ",".join(sanitize_id(n) for n in conflict_nodes if n in entities)
        if ids:
            lines.append(f"    class {ids} conflict")

    mermaid_code = "\n".join(lines)

    # Statistics
    max_edges = len(entities) * (len(entities) - 1) / 2 if len(entities) > 1 else 1
    density = len(edges) / max_edges

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
<p><strong>Nodes:</strong> {len(entities)} | <strong>Edges:</strong> {len(edges)} | <strong>Domains:</strong> {len(domain_groups)} | <strong>Conflicts:</strong> {len(conflict_nodes)} | <strong>Density:</strong> {density:.3f}</p>
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
| Entities | {len(entities)} |
| Relationships | {len(edges)} |
| Domains | {len(domain_groups)} |
| Conflict Hotspots | {len(conflict_nodes)} |
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

    if output is None:
        ext = '.html' if fmt == 'html' else '.md'
        index_dir = os.path.join(KG_DIR, '_index')
        os.makedirs(index_dir, exist_ok=True)
        output = os.path.join(index_dir, f'relationship-graph{ext}')

    os.makedirs(os.path.dirname(output), exist_ok=True)
    with open(output, 'w', encoding='utf-8') as f:
        f.write(content)

    console.print(f"[bold green]Generated relationship graph:[/bold green] {output}")
    console.print(f"  Entities: {len(entities)} | Edges: {len(edges)} | Domains: {len(domain_groups)} | Conflicts: {len(conflict_nodes)}")

    if hub_entities:
        console.print("\n[bold cyan]Hub Entities:[/bold cyan]")
        for name, count in hub_entities:
            console.print(f"  - {name}: {count} connections")


if __name__ == '__main__':
    graph()
