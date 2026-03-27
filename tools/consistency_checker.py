"""Validate narrative consistency across knowledge graph and source documents."""
import os
import re
import click
from collections import defaultdict
from common import (
    console, KG_DIR, DomainEnum, WIKILINK_REGEX, load_all_entities
)


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
    def has_errors(self):
        return len(self.errors) > 0


def check_character_stability(entities, report):
    """Check that character attributes are consistent across sources."""
    for name, info in entities.items():
        if info['data'].get('domain') != DomainEnum.CHARACTER.value:
            continue
        conflicts = info['data'].get('conflicts')
        if not conflicts or not isinstance(conflicts, list):
            continue
        for conflict in conflicts:
            if not isinstance(conflict, dict) or conflict.get('id') != 'state-conflict':
                continue
            variants = conflict.get('variants', [])
            if len(variants) > 2:
                report.error(
                    "character-stability", name,
                    f"High instability: {len(variants)} contradicting states found"
                )
            elif len(variants) > 1:
                report.warning(
                    "character-stability", name,
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
                        "timeline", name,
                        f"first_appearance_chapter ({first}) > last_referenced_chapter ({last})"
                    )
            for ch_val, ch_name in [(first, 'first_appearance'), (last, 'last_referenced')]:
                if isinstance(ch_val, int) and (ch_val < 0 or ch_val > 39):
                    report.warning(
                        "timeline", name,
                        f"{ch_name}_chapter ({ch_val}) outside expected range 0-39"
                    )


def check_location_consistency(entities, report):
    """Check that world/location entities have bidirectional references."""
    world_entities = {
        name: info for name, info in entities.items()
        if info['data'].get('domain') == DomainEnum.WORLD.value
    }

    location_relations = defaultdict(set)
    for name, info in world_entities.items():
        related = info['data'].get('related', [])
        if not related:
            continue
        for rel in related:
            if isinstance(rel, str):
                match = WIKILINK_REGEX.search(rel)
                if match:
                    location_relations[name].add(match.group(1).partition('|')[0])

    for loc_a, relations in location_relations.items():
        for loc_b in relations:
            if loc_b in world_entities and loc_a not in location_relations.get(loc_b, set()):
                report.warning(
                    "location-link", loc_a,
                    f"One-directional link to {loc_b} (not reciprocated)"
                )


def check_physics_consistency(entities, report):
    """Check that physics/mechanic entities have consistent numerical data and sources."""
    physics_domains = {DomainEnum.PHYSICS.value, DomainEnum.MECHANIC.value}
    for name, info in entities.items():
        if info['data'].get('domain') not in physics_domains:
            continue
        data = info['data']

        conflicts = data.get('conflicts')
        if conflicts and isinstance(conflicts, list):
            for c in conflicts:
                if isinstance(c, dict) and c.get('id') == 'number-conflict':
                    report.error(
                        "physics-consistency", name,
                        "Numerical inconsistency in physics/mechanic entity"
                    )
                    break

        if not data.get('sources'):
            report.warning(
                "physics-consistency", name,
                "Physics/mechanic entity has no source references"
            )


def check_relationship_symmetry(entities, report):
    """Check that entity relationships are bidirectional where expected."""
    relations = {}
    for name, info in entities.items():
        related = info['data'].get('related', [])
        targets = set()
        if related:
            for rel in related:
                if isinstance(rel, str):
                    match = WIKILINK_REGEX.search(rel)
                    if match:
                        targets.add(match.group(1).partition('|')[0])
        relations[name] = targets

    for entity_a, targets_a in relations.items():
        for target in targets_a:
            if target in relations and entity_a not in relations[target]:
                report.note(
                    "relationship-symmetry", entity_a,
                    f"Links to {target} but {target} does not link back"
                )


def check_orphan_conflicts(entities, report):
    """Check for mismatches between conflict data and canon_status."""
    for name, info in entities.items():
        data = info['data']
        canon = data.get('canon_status', '')
        conflicts = data.get('conflicts')
        has_conflicts = conflicts and isinstance(conflicts, list) and len(conflicts) > 0

        if has_conflicts and canon == 'confirmed':
            report.error(
                "canon-conflict", name,
                "Status is 'confirmed' but entity has unresolved conflicts"
            )
        if not has_conflicts and canon == 'disputed':
            report.warning(
                "canon-conflict", name,
                "Status is 'disputed' but no conflict data attached"
            )


def check_domain_placement(entities, report):
    """Check that entities are in the correct domain directory."""
    for name, info in entities.items():
        declared_domain = info['data'].get('domain', '')
        path_parts = info['path'].replace('\\', '/').split('/')
        if len(path_parts) >= 2:
            dir_domain = path_parts[-2]
            if dir_domain != declared_domain and dir_domain != '_index':
                report.error(
                    "domain-placement", name,
                    f"File in '{dir_domain}/' but domain declared as '{declared_domain}'"
                )


CHECKS = {
    'character-stability': check_character_stability,
    'timeline': check_timeline_consistency,
    'location': check_location_consistency,
    'physics': check_physics_consistency,
    'relationships': check_relationship_symmetry,
    'canon-conflicts': check_orphan_conflicts,
    'domain-placement': check_domain_placement,
}


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

    checks = dict(CHECKS)
    if category:
        allowed = {c.strip() for c in category.split(',')}
        checks = {k: v for k, v in checks.items() if k in allowed}

    console.print(f"[bold blue]Running {len(checks)} consistency checks on {len(entities)} entities...[/bold blue]\n")

    for check_fn in checks.values():
        check_fn(entities, report)

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

    if not report.errors and not report.warnings:
        console.print("\n[bold green]All consistency checks passed![/bold green]")
    else:
        is_fail = report.has_errors or (strict and report.warnings)
        status = "FAIL" if is_fail else "WARN"
        color = "red" if is_fail else "yellow"
        console.print(f"\n[bold {color}]Result: {status} — {len(report.errors)} errors, {len(report.warnings)} warnings, {len(report.info)} notes[/bold {color}]")

    if output:
        md_lines = ["# Narrative Consistency Report\n"]
        md_lines.append(f"**Entities checked:** {len(entities)}")
        md_lines.append(f"**Checks run:** {', '.join(checks.keys())}")
        md_lines.append(f"**Errors:** {len(report.errors)} | **Warnings:** {len(report.warnings)} | **Notes:** {len(report.info)}\n")

        for label, items in [("Errors", report.errors), ("Warnings", report.warnings), ("Notes", report.info)]:
            if items:
                md_lines.append(f"\n## {label}\n")
                for cat, entity, msg in items:
                    md_lines.append(f"- **[{cat}]** {entity}: {msg}")

        md_lines.append("\n_Automatisch generiert von `consistency_checker.py`._\n")

        os.makedirs(os.path.dirname(output), exist_ok=True)
        with open(output, 'w', encoding='utf-8') as f:
            f.write("\n".join(md_lines))
        console.print(f"[bold green]Report saved to:[/bold green] {output}")


if __name__ == '__main__':
    check()
