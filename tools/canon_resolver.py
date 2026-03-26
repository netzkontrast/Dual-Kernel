"""Semi-automated canon status resolution based on source evidence and consensus."""
import os
import re
import glob
import yaml
import click
from datetime import datetime
from collections import defaultdict
from common import (
    console, KG_DIR, VALID_CANON_STATUSES,
    load_inventory, load_conflicts, slugify
)


def parse_frontmatter(filepath):
    """Extract YAML frontmatter from a markdown file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if not content.startswith('---'):
        return None, content
    end_idx = content.find('---', 3)
    if end_idx == -1:
        return None, content
    try:
        data = yaml.safe_load(content[3:end_idx])
        return data, content
    except yaml.YAMLError:
        return None, content


def load_all_entities():
    """Load all entity files with their paths and frontmatter."""
    entities = {}
    files = glob.glob(f'{KG_DIR}/**/*.md', recursive=True)
    for f in files:
        if f.endswith('README.md'):
            continue
        data, raw = parse_frontmatter(f)
        if data and 'title' in data:
            entities[data['title']] = {
                'path': f,
                'data': data,
                'raw': raw,
            }
    return entities


def compute_source_score(entity_data):
    """Score an entity based on its source evidence strength.

    Scoring factors:
    - Number of distinct source files (more files = stronger consensus)
    - Number of mentions across files
    - Whether the entity is in the known entities list
    """
    sources = entity_data.get('sources', [])
    if not sources:
        return 0.0

    source_count = len(sources) if isinstance(sources, list) else 0
    # Base score from number of sources
    score = min(source_count / 5.0, 1.0)  # Cap at 5 sources = 1.0
    return score


def compute_conflict_severity(entity_data):
    """Score conflict severity (0 = no conflicts, 1 = severe)."""
    conflicts = entity_data.get('conflicts')
    if not conflicts or not isinstance(conflicts, list):
        return 0.0

    total_variants = 0
    conflict_types = 0
    for conflict in conflicts:
        if isinstance(conflict, dict):
            conflict_types += 1
            variants = conflict.get('variants', [])
            total_variants += len(variants)

    if conflict_types == 0:
        return 0.0

    # More conflict types and more variants = more severe
    severity = min((conflict_types * 0.3) + (total_variants * 0.1), 1.0)
    return severity


def suggest_canon_status(entity_name, entity_data):
    """Suggest a canon status based on evidence analysis.

    Returns (suggested_status, confidence, reasoning).
    """
    current_status = entity_data.get('canon_status', 'uncertain')
    source_score = compute_source_score(entity_data)
    conflict_severity = compute_conflict_severity(entity_data)

    reasons = []

    # No conflicts + good sources = confirmed
    if conflict_severity == 0 and source_score >= 0.4:
        reasons.append(f"No conflicts, {len(entity_data.get('sources', []))} source(s)")
        return 'confirmed', 0.8 + source_score * 0.2, reasons

    # No conflicts but weak sources = provisional
    if conflict_severity == 0 and source_score < 0.4:
        reasons.append("No conflicts but limited source evidence")
        return 'provisional', 0.5, reasons

    # Has conflicts but they're minor (1-2 variants)
    if 0 < conflict_severity <= 0.3:
        reasons.append(f"Minor conflicts (severity {conflict_severity:.2f})")
        if source_score >= 0.6:
            reasons.append("Strong source base may resolve conflicts")
            return 'provisional', 0.6, reasons
        return 'disputed', 0.5, reasons

    # Significant conflicts
    if conflict_severity > 0.3:
        reasons.append(f"Significant conflicts (severity {conflict_severity:.2f})")
        return 'disputed', 0.7, reasons

    return current_status, 0.3, ["Insufficient data for determination"]


def format_resolution_report(entity_name, entity_info, suggestion, confidence, reasons):
    """Format a single entity resolution recommendation."""
    data = entity_info['data']
    current = data.get('canon_status', '?')
    path = entity_info['path']

    status_emoji = {
        'confirmed': '✓',
        'provisional': '~',
        'disputed': '⚠',
        'uncertain': '?',
        'decanonized': '✗',
    }

    return {
        'entity': entity_name,
        'current': current,
        'suggested': suggestion,
        'confidence': confidence,
        'reasons': reasons,
        'path': path,
        'changed': current != suggestion,
        'emoji': status_emoji.get(suggestion, '?'),
    }


@click.command()
@click.option('--apply', is_flag=True,
              help='Apply suggested canon status changes to entity files')
@click.option('--min-confidence', default=0.6, type=float,
              help='Minimum confidence threshold for applying changes (0.0-1.0)')
@click.option('--output', '-o', default=None,
              help='Save resolution report to file')
@click.option('--status-filter', default=None,
              help='Only process entities with specific status (e.g., "disputed")')
def resolve(apply, min_confidence, output, status_filter):
    """Analyze and suggest canon status resolutions for knowledge graph entities."""
    entities = load_all_entities()

    if not entities:
        console.print("[bold red]No entities found in knowledge graph.[/bold red]")
        return

    # Filter by status
    if status_filter:
        allowed = {s.strip() for s in status_filter.split(',')}
        entities = {
            k: v for k, v in entities.items()
            if v['data'].get('canon_status') in allowed
        }

    console.print(f"[bold blue]Analyzing {len(entities)} entities for canon resolution...[/bold blue]\n")

    resolutions = []
    for entity_name, entity_info in sorted(entities.items()):
        suggestion, confidence, reasons = suggest_canon_status(
            entity_name, entity_info['data']
        )
        resolution = format_resolution_report(
            entity_name, entity_info, suggestion, confidence, reasons
        )
        resolutions.append(resolution)

    # Display results
    changed = [r for r in resolutions if r['changed']]
    unchanged = [r for r in resolutions if not r['changed']]

    if changed:
        console.print(f"[bold yellow]Suggested Changes ({len(changed)}):[/bold yellow]\n")
        for r in changed:
            conf_bar = '█' * int(r['confidence'] * 10) + '░' * (10 - int(r['confidence'] * 10))
            console.print(
                f"  {r['emoji']} [bold]{r['entity']}[/bold]: "
                f"[red]{r['current']}[/red] → [green]{r['suggested']}[/green] "
                f"[{conf_bar}] {r['confidence']:.0%}"
            )
            for reason in r['reasons']:
                console.print(f"    └ {reason}")
    else:
        console.print("[bold green]No status changes suggested.[/bold green]")

    if unchanged:
        unchanged_list = ", ".join(r['entity'] for r in unchanged)
        console.print(f"\n[dim]Unchanged ({len(unchanged)}): {unchanged_list}[/dim]")

    # Summary statistics
    status_dist = defaultdict(int)
    for r in resolutions:
        status_dist[r['suggested']] += 1

    console.print("\n[bold cyan]Suggested Status Distribution:[/bold cyan]")
    for status in ['confirmed', 'provisional', 'disputed', 'uncertain', 'decanonized']:
        count = status_dist.get(status, 0)
        if count > 0:
            bar = '█' * count
            console.print(f"  {status:15} {bar} {count}")

    # Apply changes if requested
    if apply:
        applied_count = 0
        skipped_count = 0

        for r in changed:
            if r['confidence'] < min_confidence:
                console.print(
                    f"  [dim]Skipped {r['entity']}: confidence {r['confidence']:.0%} "
                    f"< threshold {min_confidence:.0%}[/dim]"
                )
                skipped_count += 1
                continue

            entity_info = entities[r['entity']]
            filepath = entity_info['path']
            content = entity_info['raw']

            # Update canon_status in frontmatter
            content = re.sub(
                r'canon_status:\s*"[^"]*"',
                f'canon_status: "{r["suggested"]}"',
                content
            )

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            applied_count += 1
            console.print(
                f"  [green]Applied:[/green] {r['entity']} → {r['suggested']}"
            )

        console.print(
            f"\n[bold green]Applied {applied_count} changes[/bold green]"
            f" ({skipped_count} skipped below confidence threshold)"
        )

    # Save report
    if output:
        md_lines = ["# Canon Resolution Report\n"]
        md_lines.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        md_lines.append(f"**Entities analyzed:** {len(resolutions)}")
        md_lines.append(f"**Changes suggested:** {len(changed)}")
        if apply:
            md_lines.append(f"**Changes applied:** {sum(1 for r in changed if r['confidence'] >= min_confidence)}")
        md_lines.append("")

        if changed:
            md_lines.append("## Suggested Changes\n")
            md_lines.append("| Entity | Current | Suggested | Confidence | Reason |")
            md_lines.append("|--------|---------|-----------|------------|--------|")
            for r in changed:
                reason_str = "; ".join(r['reasons'])
                md_lines.append(
                    f"| {r['entity']} | {r['current']} | {r['suggested']} "
                    f"| {r['confidence']:.0%} | {reason_str} |"
                )

        md_lines.append("\n## Status Distribution\n")
        md_lines.append("| Status | Count |")
        md_lines.append("|--------|-------|")
        for status in ['confirmed', 'provisional', 'disputed', 'uncertain', 'decanonized']:
            count = status_dist.get(status, 0)
            if count > 0:
                md_lines.append(f"| {status} | {count} |")

        md_lines.append("\n_Automatisch generiert von `canon_resolver.py`._\n")

        os.makedirs(os.path.dirname(output), exist_ok=True)
        with open(output, 'w', encoding='utf-8') as f:
            f.write("\n".join(md_lines))
        console.print(f"[bold green]Report saved to:[/bold green] {output}")


if __name__ == '__main__':
    resolve()
