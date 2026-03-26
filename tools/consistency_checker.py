"""Validate narrative consistency across knowledge graph and source documents."""
import os
import re
import glob
import yaml
import click
from collections import defaultdict
from common import (
    console, KG_DIR, VALID_DOMAINS, VALID_CANON_STATUSES,
    load_inventory, load_conflicts, slugify
)


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
    """Load all entity files with their paths and frontmatter."""
    entities = {}
    files = glob.glob(f'{KG_DIR}/**/*.md', recursive=True)
    for f in files:
        if f.endswith('README.md'):
            continue
        data = parse_frontmatter(f)
        if data and 'title' in data:
            entities[data['title']] = {'path': f, 'data': data}
    return entities


class ConsistencyReport:
    """Accumulates consistency check results."""

    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []

    def error(self, category, entity, message):
        self.errors.append((category, entity, message))

    def warning(self, category, entity, message):
        self.warnings.append((category, entity, message))

    def note(self, category, entity, message):
        self.info.append((category, entity, message))

    @property
    def total_issues(self):
        return len(self.errors) + len(self.warnings)


def check_character_stability(entities, report):
    """Check that character attributes are consistent across sources."""
    character_entities = {
        name: info for name, info in entities.items()
        if info['data'].get('domain') == 'character'
    }

    for name, info in character_entities.items():
        data = info['data']
        conflicts = data.get('conflicts')

        # Check for state conflicts (character attribute instability)
        if conflicts and isinstance(conflicts, list):
            state_conflicts = [c for c in conflicts if isinstance(c, dict)
                               and c.get('id') == 'state-conflict']
            if state_conflicts:
                for conflict in state_conflicts:
                    variants = conflict.get('variants', [])
                    if len(variants) > 2:
                        report.error(
                            "character-stability",
                            name,
                            f"High instability: {len(variants)} contradicting states found"
                        )
                    elif len(variants) > 1:
                        report.warning(
                            "character-stability",
                            name,
                            f"State conflict: {', '.join(v.get('claim', '?') for v in variants)}"
                        )


def check_timeline_consistency(entities, report):
    """Check that chapter appearances don't create timeline contradictions."""
    for name, info in entities.items():
        data = info['data']
        first = data.get('first_appearance_chapter')
        last = data.get('last_referenced_chapter')

        if first is not None and last is not None:
            if isinstance(first, int) and isinstance(last, int):
                if first > last:
                    report.error(
                        "timeline",
                        name,
                        f"first_appearance_chapter ({first}) > last_referenced_chapter ({last})"
                    )
            # Check that chapters are in valid range (0-39)
            for ch_val, ch_name in [(first, 'first_appearance'), (last, 'last_referenced')]:
                if isinstance(ch_val, int) and (ch_val < 0 or ch_val > 39):
                    report.warning(
                        "timeline",
                        name,
                        f"{ch_name}_chapter ({ch_val}) outside expected range 0-39"
                    )


def check_location_consistency(entities, report):
    """Check that world/location entities are consistently described."""
    world_entities = {
        name: info for name, info in entities.items()
        if info['data'].get('domain') == 'world'
    }

    # Check for overlapping location descriptions via related entities
    location_relations = defaultdict(set)
    for name, info in world_entities.items():
        related = info['data'].get('related', [])
        if related and related != []:
            for rel in related:
                if isinstance(rel, str):
                    match = re.search(r'\[\[(.*?)\]\]', rel)
                    if match:
                        target = match.group(1).partition('|')[0]
                        location_relations[name].add(target)

    # Check bidirectional references
    for loc_a, relations in location_relations.items():
        for loc_b in relations:
            if loc_b in world_entities:
                if loc_a not in location_relations.get(loc_b, set()):
                    report.warning(
                        "location-link",
                        loc_a,
                        f"One-directional link to {loc_b} (not reciprocated)"
                    )


def check_physics_consistency(entities, report):
    """Check that physics rules (DKT, Landauer) are applied uniformly."""
    physics_entities = {
        name: info for name, info in entities.items()
        if info['data'].get('domain') == 'physics'
    }
    mechanic_entities = {
        name: info for name, info in entities.items()
        if info['data'].get('domain') == 'mechanic'
    }

    combined = {**physics_entities, **mechanic_entities}

    for name, info in combined.items():
        data = info['data']
        conflicts = data.get('conflicts')

        if conflicts and isinstance(conflicts, list):
            number_conflicts = [c for c in conflicts if isinstance(c, dict)
                                and c.get('id') == 'number-conflict']
            if number_conflicts:
                report.error(
                    "physics-consistency",
                    name,
                    f"Numerical inconsistency in physics/mechanic entity"
                )

        # Check that physics entities have proper sources
        sources = data.get('sources', [])
        if not sources:
            report.warning(
                "physics-consistency",
                name,
                "Physics/mechanic entity has no source references"
            )


def check_relationship_symmetry(entities, report):
    """Check that entity relationships are bidirectional where expected."""
    link_pattern = re.compile(r'\[\[(.*?)\]\]')
    relations = {}

    for name, info in entities.items():
        related = info['data'].get('related', [])
        targets = set()
        if related and related != []:
            for rel in related:
                if isinstance(rel, str):
                    match = link_pattern.search(rel)
                    if match:
                        targets.add(match.group(1).partition('|')[0])
        relations[name] = targets

    for entity_a, targets_a in relations.items():
        for target in targets_a:
            if target in relations:
                if entity_a not in relations[target]:
                    report.note(
                        "relationship-symmetry",
                        entity_a,
                        f"Links to {target} but {target} does not link back"
                    )


def check_orphan_conflicts(entities, report):
    """Check for entities with unresolved conflict data."""
    for name, info in entities.items():
        data = info['data']
        canon = data.get('canon_status', '')
        conflicts = data.get('conflicts')

        has_conflicts = conflicts and isinstance(conflicts, list) and len(conflicts) > 0
        if has_conflicts and canon == 'confirmed':
            report.error(
                "canon-conflict",
                name,
                "Status is 'confirmed' but entity has unresolved conflicts"
            )

        if not has_conflicts and canon == 'disputed':
            report.warning(
                "canon-conflict",
                name,
                "Status is 'disputed' but no conflict data attached"
            )


def check_domain_placement(entities, report):
    """Check that entities are in the correct domain directory."""
    for name, info in entities.items():
        data = info['data']
        path = info['path']
        declared_domain = data.get('domain', '')

        # Extract domain from file path
        path_parts = path.replace('\\', '/').split('/')
        if len(path_parts) >= 2:
            dir_domain = path_parts[-2]
            if dir_domain != declared_domain and dir_domain != '_index':
                report.error(
                    "domain-placement",
                    name,
                    f"File in '{dir_domain}/' but domain declared as '{declared_domain}'"
                )


@click.command()
@click.option('--strict', is_flag=True, help='Treat warnings as errors')
@click.option('--output', '-o', default=None, help='Save report to file')
@click.option('--category', '-c', default=None,
              help='Run only specific checks (comma-separated)')
def check(strict, output, category):
    """Run narrative consistency checks across the knowledge graph."""
    entities = load_all_entities()

    if not entities:
        console.print("[bold red]No entities found in knowledge graph.[/bold red]")
        return

    report = ConsistencyReport()

    checks = {
        'character-stability': check_character_stability,
        'timeline': check_timeline_consistency,
        'location': check_location_consistency,
        'physics': check_physics_consistency,
        'relationships': check_relationship_symmetry,
        'canon-conflicts': check_orphan_conflicts,
        'domain-placement': check_domain_placement,
    }

    # Filter checks if category specified
    if category:
        allowed = {c.strip() for c in category.split(',')}
        checks = {k: v for k, v in checks.items() if k in allowed}

    console.print(f"[bold blue]Running {len(checks)} consistency checks on {len(entities)} entities...[/bold blue]\n")

    for check_name, check_fn in checks.items():
        check_fn(entities, report)

    # Display results
    if report.errors:
        console.print(f"[bold red]ERRORS ({len(report.errors)}):[/bold red]")
        for cat, entity, msg in report.errors:
            console.print(f"  [red]✗[/red] [{cat}] {entity}: {msg}")

    if report.warnings:
        console.print(f"\n[bold yellow]WARNINGS ({len(report.warnings)}):[/bold yellow]")
        for cat, entity, msg in report.warnings:
            console.print(f"  [yellow]![/yellow] [{cat}] {entity}: {msg}")

    if report.info:
        console.print(f"\n[bold cyan]INFO ({len(report.info)}):[/bold cyan]")
        for cat, entity, msg in report.info:
            console.print(f"  [cyan]·[/cyan] [{cat}] {entity}: {msg}")

    # Summary
    if report.total_issues == 0:
        console.print("\n[bold green]All consistency checks passed![/bold green]")
    else:
        status = "FAIL" if (report.errors or (strict and report.warnings)) else "WARN"
        color = "red" if status == "FAIL" else "yellow"
        console.print(f"\n[bold {color}]Result: {status} — {len(report.errors)} errors, {len(report.warnings)} warnings, {len(report.info)} notes[/bold {color}]")

    # Save report if requested
    if output:
        md_lines = ["# Narrative Consistency Report\n"]
        md_lines.append(f"**Entities checked:** {len(entities)}")
        md_lines.append(f"**Checks run:** {', '.join(checks.keys())}")
        md_lines.append(f"**Errors:** {len(report.errors)} | **Warnings:** {len(report.warnings)} | **Notes:** {len(report.info)}\n")

        if report.errors:
            md_lines.append("## Errors\n")
            for cat, entity, msg in report.errors:
                md_lines.append(f"- **[{cat}]** {entity}: {msg}")

        if report.warnings:
            md_lines.append("\n## Warnings\n")
            for cat, entity, msg in report.warnings:
                md_lines.append(f"- **[{cat}]** {entity}: {msg}")

        if report.info:
            md_lines.append("\n## Notes\n")
            for cat, entity, msg in report.info:
                md_lines.append(f"- [{cat}] {entity}: {msg}")

        md_lines.append("\n_Automatisch generiert von `consistency_checker.py`._\n")

        os.makedirs(os.path.dirname(output), exist_ok=True)
        with open(output, 'w', encoding='utf-8') as f:
            f.write("\n".join(md_lines))
        console.print(f"[bold green]Report saved to:[/bold green] {output}")


if __name__ == '__main__':
    check()
