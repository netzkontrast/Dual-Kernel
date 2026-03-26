import json
import click
import os
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

@click.command()
@click.option('--save', is_flag=True, help='Save diffs as Markdown files')
def diff(save):
    with open('tools/output/cross-references.json', 'r', encoding='utf-8') as f:
        conflicts = json.load(f)

    if not conflicts:
        console.print("[bold green]No conflicts found.[/bold green]")
        return

    os.makedirs('tools/output/diffs', exist_ok=True)

    for entity, entity_conflicts in conflicts.items():
        console.print(f"\n[bold red]Conflict detected for Entity:[/bold red] {entity}")

        md_content = f"# Conflict Report: {entity}\n\n"

        for conflict in entity_conflicts:
            md_content += f"## {conflict['id']}\n"
            md_content += f"**Description:** {conflict['description']}\n\n"

            panel_text = Text(f"Description: {conflict['description']}\n\n")
            for variant in conflict['variants']:
                panel_text.append(f"Claim: {variant['claim']}\n", style="bold yellow")
                panel_text.append(f"Source: {variant['source']}\n\n", style="cyan")

                md_content += f"- **Claim:** {variant['claim']}\n"
                md_content += f"  - **Source:** {variant['source']}\n"

            console.print(Panel(panel_text, title=f"Conflict: {conflict['id']}"))
            md_content += "\n"

        if save:
            filename = f"tools/output/diffs/{entity.replace(' ', '-').lower()}-conflict.md"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(md_content)
            console.print(f"[bold green]Saved diff to:[/bold green] {filename}")

if __name__ == '__main__':
    diff()
