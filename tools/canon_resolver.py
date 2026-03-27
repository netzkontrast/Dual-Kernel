"""Semi-automated canon status resolution based on source evidence and consensus."""
import os
import re
import click
from datetime import datetime
from collections import defaultdict
from common import (
    console, KG_DIR, VALID_CANON_STATUSES, load_all_entities
)


def compute_source_score(entity_data):
    """Score entity based on source evidence strength (0.0 to 1.0)."""
    sources = entity_data.get('sources', [])
    if not sources or not isinstance(sources, list):
        return 0.0
    return min(len(sources) / 5.0, 1.0)


def compute_conflict_severity(entity_data):
    """Score conflict severity (0.0 = none, 1.0 = severe)."""
    conflicts = entity_data.get('conflicts')
    if not conflicts or not isinstance(conflicts, list):
        return 0.0

    conflict_types = 0
    total_variants = 0
    for conflict in conflicts:
        if isinstance(conflict, dict):
            conflict_types += 1
            total_variants += len(conflict.get('variants', []))

    if conflict_types == 0:
        return 0.0
    return min((conflict_types * 0.3) + (total_variants * 0.1), 1.0)


def suggest_canon_status(entity_data):
    """Suggest a canon status based on evidence analysis.

    Returns (suggested_status, confidence, reasoning).
    """
    source_score = compute_source_score(entity_data)
    conflict_severity = compute_conflict_severity(entity_data)

    if conflict_severity == 0 and source_score >= 0.4:
        return 'confirmed', 0.8 + source_score * 0.2, \
            [f"No conflicts, {len(entity_data.get('sources', []))} source(s)"]

    if conflict_severity == 0:
        return 'provisional', 0.5, ["No conflicts but limited source evidence"]

    if conflict_severity <= 0.3:
        reason = f"Minor conflicts (severity {conflict_severity:.2f})"
        if source_score >= 0.6:
            return 'provisional', 0.6, [reason, "Strong source base may resolve conflicts"]
        return 'disputed', 0.5, [reason]

    return 'disputed', 0.7, [f"Significant conflicts (severity {conflict_severity:.2f})"]


STATUS_EMOJI = {
    'confirmed': '✓', 'provisional': '~', 'disputed': '⚠',
    'uncertain': '?', 'decanonized': '✗',
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

    if status_filter:
        allowed = {s.strip() for s in status_filter.split(',')}
        entities = {
            k: v for k, v in entities.items()
            if v['data'].get('canon_status') in allowed
        }

    console.print(f"[bold blue]Analyzing {len(entities)} entities for canon resolution...[/bold blue]\n")

    resolutions = []
    for entity_name, entity_info in sorted(entities.items()):
        suggestion, confidence, reasons = suggest_canon_status(entity_info['data'])
        current = entity_info['data'].get('canon_status', '?')
        resolutions.append({
            'entity': entity_name,
            'current': current,
            'suggested': suggestion,
            'confidence': confidence,
            'reasons': reasons,
            'changed': current != suggestion,
            'emoji': STATUS_EMOJI.get(suggestion, '?'),
        })

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

    status_dist = defaultdict(int)
    for r in resolutions:
        status_dist[r['suggested']] += 1

    console.print("\n[bold cyan]Suggested Status Distribution:[/bold cyan]")
    for status in sorted(VALID_CANON_STATUSES):
        count = status_dist.get(status, 0)
        if count > 0:
            console.print(f"  {status:15} {'█' * count} {count}")

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
            content = re.sub(
                r'canon_status:\s*"[^"]*"',
                f'canon_status: "{r["suggested"]}"',
                entity_info['raw']
            )

            with open(entity_info['path'], 'w', encoding='utf-8') as f:
                f.write(content)

            applied_count += 1
            console.print(f"  [green]Applied:[/green] {r['entity']} → {r['suggested']}")

        console.print(
            f"\n[bold green]Applied {applied_count} changes[/bold green]"
            f" ({skipped_count} skipped below confidence threshold)"
        )

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
        for status in sorted(VALID_CANON_STATUSES):
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
