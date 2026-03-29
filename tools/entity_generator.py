import os
import re
from common import (
    console, load_inventory, load_conflicts, slugify,
    KG_DIR, DomainEnum
)


def generate_entities():
    inventory = load_inventory()
    conflicts = load_conflicts()

    os.makedirs(KG_DIR, exist_ok=True)

    moc_data = {}
    all_entity_names = list(inventory['entity_details'].keys())

    # Pre-compile a single regex for co-occurrence detection
    if all_entity_names:
        entity_pattern = re.compile(
            r'\b(' + '|'.join(re.escape(n) for n in sorted(all_entity_names, key=len, reverse=True)) + r')\b'
        )
    else:
        entity_pattern = None

    created_dirs = set()

    for entity_name, data in inventory['entity_details'].items():
        domain = data.get('estimated_domain', DomainEnum.FUNDAMENT.value)
        domain_dir = os.path.join(KG_DIR, domain)

        if domain_dir not in created_dirs:
            os.makedirs(domain_dir, exist_ok=True)
            created_dirs.add(domain_dir)

        if domain not in moc_data:
            moc_data[domain] = []

        file_id = slugify(entity_name)
        filepath = os.path.join(domain_dir, f"{file_id}.md")

        canon_status = "provisional"
        is_known = data.get('is_known', False)
        if entity_name in conflicts:
            canon_status = "disputed"
        elif is_known:
            canon_status = "confirmed"

        # Find related entities via single regex scan over all mention contexts
        related = set()
        for filename, file_data in data['files'].items():
            for mention in file_data['mentions']:
                if entity_pattern:
                    for match in entity_pattern.finditer(mention['context']):
                        found = match.group(0)
                        if found != entity_name:
                            related.add(f"[[{found}]]")

        sources = []
        for filename, file_data in data['files'].items():
            lines = [m['line'] for m in file_data['mentions']]
            source_entry = f"""  - file: "{filename}"\n    lines: "{min(lines)}-{max(lines)}"\n    relevance: "primary" """
            sources.append(source_entry)

        conflicts_parts = []
        if entity_name in conflicts:
            conflicts_parts.append("\n")
            for conflict in conflicts[entity_name]:
                conflicts_parts.append(f"  - id: \"{conflict['id']}\"\n")
                conflicts_parts.append(f"    description: \"{conflict['description']}\"\n")
                conflicts_parts.append("    variants:\n")
                for variant in conflict['variants']:
                    conflicts_parts.append(f"      - claim: \"{variant['claim']}\"\n")
                    conflicts_parts.append(f"        source: \"{variant['source']}\"\n")
            conflicts_yaml = "".join(conflicts_parts)
        else:
            conflicts_yaml = "[]"

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

    for domain, links in moc_data.items():
        readme_path = os.path.join(KG_DIR, domain, "README.md")
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(f"# Map of Content: {domain.capitalize()}\n\n")
            f.write("Automatisch generierte Übersicht aller Entitäten in dieser Domäne:\n\n")
            for link in sorted(links):
                f.write(f"- {link}\n")
        console.print(f"[bold green]Generated MOC:[/bold green] {readme_path}")

if __name__ == '__main__':
    generate_entities()
