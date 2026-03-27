import os
from common import console, slugify, WIKILINK_REGEX, list_entity_files


def check_links():
    files = list_entity_files()
    all_entities = {os.path.basename(f)[:-3] for f in files}

    broken_links = []
    linked_to = set()

    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()

        for link in WIKILINK_REGEX.findall(content):
            target_id = slugify(link.partition('|')[0])

            if target_id not in all_entities and target_id != "readme":
                broken_links.append((file, link))
            else:
                linked_to.add(target_id)

    orphans = [e for e in sorted(all_entities) if e not in linked_to]

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
