import json
import os
import re
import yaml
from collections import defaultdict
from rich.console import Console
from datetime import datetime

console = Console()

MIN_CO_OCCURRENCE = 2
MIN_TOTAL_MENTIONS = 2

def generate_entities():
    inventory_file = 'tools/output/source-inventory.json'
    if not os.path.exists(inventory_file):
        console.print(f"[bold red]Inventory file not found:[/bold red] {inventory_file}")
        return

    with open(inventory_file, 'r', encoding='utf-8') as f:
        inventory = json.load(f)

    try:
        with open('tools/output/cross-references.json', 'r', encoding='utf-8') as f:
            conflicts = json.load(f)
    except FileNotFoundError:
        conflicts = {}

    output_dir = "knowledge-graph"
    index_dir = os.path.join(output_dir, "_index")
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(index_dir, exist_ok=True)

    todo_file = os.path.join(index_dir, "generation_todo.md")

    # Store links for MOCs
    moc_data = {}

    for entity_name, data in inventory['entity_details'].items():
        domain = data.get('estimated_domain') or 'fundament'
        domain_dir = os.path.join(output_dir, domain)
        os.makedirs(domain_dir, exist_ok=True)

        if domain not in moc_data:
            moc_data[domain] = []

        file_id = entity_name.replace(' ', '-').lower()
        filepath = os.path.join(domain_dir, f"{file_id}.md")

        # Collect new sources
        new_sources_list = []
        for filename in data['files'].keys():
            new_sources_list.append(filename)

        # 1. State-Check (Existierende Dateien)
        if os.path.exists(filepath):
            # Lade bestehendes YAML-Frontmatter
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            if content.startswith('---'):
                end_idx = content.find('---', 3)
                if end_idx != -1:
                    yaml_content = content[3:end_idx]
                    try:
                        existing_data = yaml.safe_load(yaml_content)
                        existing_sources = []
                        if 'sources' in existing_data and existing_data['sources']:
                            for src in existing_data['sources']:
                                if isinstance(src, dict) and 'file' in src:
                                    existing_sources.append(src['file'])
                                elif isinstance(src, str): # Fallback
                                    existing_sources.append(src)

                        # Check for new sources
                        missing_sources = [src for src in new_sources_list if src not in existing_sources]

                        if missing_sources:
                            # Schreibe TODO Eintrag
                            date_str = datetime.now().strftime("%Y-%m-%d")
                            todo_entry = f"[{date_str}] - [ ] **[[{entity_name}]]**: Neue Quellen in '{', '.join(missing_sources)}' gefunden.\n"
                            with open(todo_file, 'a', encoding='utf-8') as tf:
                                tf.write(todo_entry)
                            console.print(f"[yellow]Added TODO for [[{entity_name}]][/yellow] - New sources: {', '.join(missing_sources)}")

                    except yaml.YAMLError as e:
                        console.print(f"[red]Error parsing YAML for {filepath}: {e}[/red]")

            # WICHTIG: Überschreibe die Datei NICHT!
            moc_data[domain].append(f"[[{entity_name}]]")
            continue

        # Determine Canon Status
        canon_status = "provisional"
        is_known = inventory.get('is_known', False)
        if entity_name in conflicts:
            canon_status = "disputed"
        elif is_known:
            canon_status = "confirmed"

        # Find related entities (Smart Links)
        related_counts = defaultdict(int)

        for filename, file_data in data['files'].items():
            for mention in file_data['mentions']:
                context_lower = mention['context'].lower()
                for other_entity, other_data in inventory['entity_details'].items():
                    if other_entity != entity_name:
                        # Bedingung 3 (KG-Check)
                        if other_data.get('total_mentions', 0) >= MIN_TOTAL_MENTIONS:
                            # Bedingung 1: Gleicher Kontext-String
                            if other_entity.lower() in context_lower:
                                related_counts[other_entity] += 1

        # Bedingung 2 (Cutoff)
        related = set()
        for other, count in related_counts.items():
            if count >= MIN_CO_OCCURRENCE:
                related.add(f"[[{other}]]")

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

        yaml_output = f"""---
title: "{entity_name}"
id: "{file_id}"
domain: "{domain}"
canon_status: "{canon_status}"
aliases: []
tags: []
related:
{chr(10).join(f'  - "{r}"' for r in sorted(related)) if related else '  []'}
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
            f.write(yaml_output)

        moc_data[domain].append(f"[[{entity_name}]]")
        console.print(f"[bold blue]Generated:[/bold blue] {filepath}")

    # Generate MOCs (README.md in each domain folder)
    for domain, links in moc_data.items():
        readme_path = os.path.join(output_dir, domain, "README.md")
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(f"# Map of Content: {domain.capitalize()}\n\n")
            f.write("Automatisch generierte Übersicht aller Entitäten in dieser Domäne:\n\n")
            for link in sorted(set(links)): # Ensure unique links in MOC
                f.write(f"- {link}\n")
        console.print(f"[bold green]Generated MOC:[/bold green] {readme_path}")

if __name__ == '__main__':
    generate_entities()
