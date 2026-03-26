import json
import os
import re
from rich.console import Console

console = Console()

def generate_entities():
    with open('tools/output/source-inventory.json', 'r', encoding='utf-8') as f:
        inventory = json.load(f)

    try:
        with open('tools/output/cross-references.json', 'r', encoding='utf-8') as f:
            conflicts = json.load(f)
    except FileNotFoundError:
        conflicts = {}

    output_dir = "knowledge-graph"
    os.makedirs(output_dir, exist_ok=True)

    # Store links for MOCs
    moc_data = {}

    for entity_name, data in inventory['entity_details'].items():
        domain = data.get('estimated_domain', 'fundament')
        domain_dir = os.path.join(output_dir, domain)
        os.makedirs(domain_dir, exist_ok=True)

        if domain not in moc_data:
            moc_data[domain] = []

        file_id = entity_name.replace(' ', '-').lower()
        filepath = os.path.join(domain_dir, f"{file_id}.md")

        # Determine Canon Status
        canon_status = "provisional"
        is_known = inventory.get('is_known', False)
        if entity_name in conflicts:
            canon_status = "disputed"
        elif is_known:
            canon_status = "confirmed"

        # Find related entities (simple co-occurrence in mentions)
        related = set()
        for filename, file_data in data['files'].items():
            for mention in file_data['mentions']:
                for other_entity in inventory['entity_details']:
                    if other_entity != entity_name and other_entity in mention['context']:
                        related.add(f"[[{other_entity}]]")

        # Build Source entry
        sources = []
        for filename, file_data in data['files'].items():
            lines = [m['line'] for m in file_data['mentions']]
            source_entry = f"""  - file: "{filename}"\n    lines: "{min(lines)}-{max(lines)}"\n    relevance: "primary" """
            sources.append(source_entry)

        # Build Conflicts entry
        conflicts_yaml = "[]"
        if entity_name in conflicts:
            conflicts_yaml = "\n"
            for conflict in conflicts[entity_name]:
                conflicts_yaml += f"  - id: \"{conflict['id']}\"\n"
                conflicts_yaml += f"    description: \"{conflict['description']}\"\n"
                conflicts_yaml += "    variants:\n"
                for variant in conflict['variants']:
                    conflicts_yaml += f"      - claim: \"{variant['claim']}\"\n"
                    conflicts_yaml += f"        source: \"{variant['source']}\"\n"

        yaml = f"""---
title: "{entity_name}"
id: "{file_id}"
domain: "{domain}"
canon_status: "{canon_status}"
aliases: []
tags: []
related:
{chr(10).join(f'  - "{r}"' for r in related) if related else '  []'}
sources:
{chr(10).join(sources)}
conflicts: {conflicts_yaml}
first_appearance_chapter: null
last_referenced_chapter: null
---

# {entity_name}

_Automatisch generierter Eintrag aus der Test-Pipeline._
"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(yaml)

        moc_data[domain].append(f"[[{entity_name}]]")
        console.print(f"[bold blue]Generated:[/bold blue] {filepath}")

    # Generate MOCs (README.md in each domain folder)
    for domain, links in moc_data.items():
        readme_path = os.path.join(output_dir, domain, "README.md")
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(f"# Map of Content: {domain.capitalize()}\n\n")
            f.write("Automatisch generierte Übersicht aller Entitäten in dieser Domäne:\n\n")
            for link in sorted(links):
                f.write(f"- {link}\n")
        console.print(f"[bold green]Generated MOC:[/bold green] {readme_path}")

if __name__ == '__main__':
    generate_entities()
