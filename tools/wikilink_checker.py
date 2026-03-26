import os
import re
import glob
from collections import defaultdict
from rich.console import Console

console = Console()

def check_links():
    files = glob.glob('knowledge-graph/**/*.md', recursive=True)
    all_entities = [os.path.basename(f)[:-3] for f in files if not f.endswith('README.md')]

    link_pattern = re.compile(r'\[\[(.*?)\]\]')

    broken_links = []
    orphans = []

    linked_to = set()

    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()

        links = link_pattern.findall(content)

        for link in links:
            clean_link = link.split('|')[0] # handle aliases if any
            target_id = clean_link.replace(' ', '-').lower()

            if target_id not in all_entities and target_id != "readme":
                broken_links.append((file, link))
            else:
                linked_to.add(target_id)

    for entity in all_entities:
        if entity not in linked_to:
            orphans.append(entity)

    if broken_links:
        console.print("[bold red]Broken Links Found![/bold red]")
        for file, link in broken_links:
            console.print(f"  - In {file}: {link}")
    else:
        console.print("[bold green]No broken links found![/bold green]")

    if orphans:
        console.print("\n[bold yellow]Orphaned Entities (no links pointing to them):[/bold yellow]")
        for orphan in orphans:
            console.print(f"  - {orphan}")

if __name__ == '__main__':
    check_links()
