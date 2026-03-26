import re
import click
import spacy
import json
import os
import glob
from collections import defaultdict
from rich.console import Console
from rich.table import Table
from datetime import datetime

from common import (
    load_known_entities, DomainEnum, guess_domain,
    SourceInventoryExport, EntityExport, FileMentionsExport
)
from pydantic import ValidationError

console = Console()

def get_context(lines, index, context_size=2):
    start = max(0, index - context_size)
    end = min(len(lines), index + context_size + 1)
    return "\n".join(lines[start:end])

def scan_file(filepath, nlp, known_regex, known_entities, inventory_data):
    """Scannt eine einzelne Datei und fügt die Mentions zum Inventar hinzu."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    filename = os.path.basename(filepath)

    # 1. Bestehende Mentions für diese Datei entfernen
    for entity_name, entity_data in inventory_data.entity_details.items():
        if filename in entity_data.files:
            del entity_data.files[filename]
            # Mentions aktualisieren
            total = sum(f.mention_count for f in entity_data.files.values())
            entity_data.total_mentions = total

    # Bereinigen von Entitäten ohne Dateien
    entities_to_remove = [k for k, v in inventory_data.entity_details.items() if not v.files]
    for k in entities_to_remove:
        del inventory_data.entity_details[k]

    new_mentions_count = 0
    entities = defaultdict(lambda: {"is_known": False, "mentions": []})

    # 1. Regex Pass (Known Entities)
    for i, line in enumerate(lines):
        for match in known_regex.finditer(line):
            entity_name = match.group(0)
            context = get_context(lines, i)
            entities[entity_name]["is_known"] = True
            entities[entity_name]["mentions"].append({
                "line_number": i + 1,
                "context_text": context,
            })

    # 2. SpaCy Pass (Unknown Entities)
    doc = nlp(content)
    char_to_line = {}
    current_char = 0
    for i, line in enumerate(lines):
        for j in range(len(line) + 1):
            char_to_line[current_char + j] = i + 1
        current_char += len(line) + 1

    for ent in doc.ents:
        if ent.label_ in ["PER", "LOC", "ORG"]:
            entity_name = ent.text.strip().strip('.,;:!?()[]{}"\'')
            if not entity_name or entity_name in entities or entity_name in known_entities:
                continue

            line_idx = char_to_line.get(ent.start_char, 1) - 1
            context = get_context(lines, line_idx)
            entities[entity_name]["is_known"] = False
            entities[entity_name]["mentions"].append({
                "line_number": line_idx + 1,
                "context_text": context,
            })

    # In das Inventar mergen
    for name, data in entities.items():
        if not data["mentions"]:
            continue

        mentions_dicts = [{"line": m["line_number"], "context": m["context_text"]} for m in data["mentions"]]
        new_mentions_count += len(data["mentions"])

        if name not in inventory_data.entity_details:
            inventory_data.entity_details[name] = EntityExport(
                total_mentions=0,
                estimated_domain=None,
                files={}
            )

        entity_export = inventory_data.entity_details[name]

        file_export = FileMentionsExport(
            mention_count=len(data["mentions"]),
            mentions=mentions_dicts
        )

        entity_export.files[filename] = file_export
        entity_export.total_mentions += file_export.mention_count

    return new_mentions_count

def evaluate_domains(inventory_data):
    """Berechnet die Domäne neu für alle Entitäten."""
    for name, entity_data in inventory_data.entity_details.items():
        all_contexts = []
        for file_data in entity_data.files.values():
            for mention in file_data.mentions:
                all_contexts.append(mention["context"])

        combined_context = "\n".join(all_contexts)
        estimated = guess_domain(combined_context)
        entity_data.estimated_domain = estimated

@click.command()
@click.option('--dir', type=click.Path(exists=True, file_okay=False, dir_okay=True), help='Directory to scan for markdown files')
@click.option('--file-list', type=click.Path(exists=True, dir_okay=False), help='Text file with list of files to scan')
def scan(dir, file_list):
    if not dir and not file_list:
        console.print("[bold red]Please provide either --dir or --file-list[/bold red]")
        return

    files_to_scan = []
    if dir:
        files_to_scan = glob.glob(os.path.join(dir, '**/*.md'), recursive=True)
        # ignoriere Dateien, die nicht zum Projekt gehören oder READMEs sind, wenn nötig.
    if file_list:
        with open(file_list, 'r', encoding='utf-8') as f:
            for line in f:
                path = line.strip()
                if os.path.exists(path) and path.endswith('.md'):
                    files_to_scan.append(path)

    if not files_to_scan:
        console.print("[bold yellow]No markdown files found to scan.[/bold yellow]")
        return

    console.print(f"[bold blue]Scanning {len(files_to_scan)} files...[/bold blue]")

    inventory_file = 'tools/output/source-inventory.json'
    inventory_data = None

    if os.path.exists(inventory_file):
        try:
            with open(inventory_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            inventory_data = SourceInventoryExport(**data)
            console.print("[green]Loaded existing inventory.[/green]")
        except (json.JSONDecodeError, ValidationError) as e:
            console.print(f"[yellow]Warning: Could not parse existing inventory ({e}). Starting fresh.[/yellow]")
            inventory_data = SourceInventoryExport(files_scanned=0, unique_entities_found=0, total_mentions=0, entity_details={})
    else:
        inventory_data = SourceInventoryExport(files_scanned=0, unique_entities_found=0, total_mentions=0, entity_details={})

    nlp = spacy.load("de_core_news_lg", disable=["parser", "lemmatizer", "tagger", "attribute_ruler"])

    known_entities = load_known_entities()
    known_entities_sorted = sorted(known_entities, key=len, reverse=True)
    if known_entities_sorted:
        regex_pattern = r'\b(' + '|'.join(map(re.escape, known_entities_sorted)) + r')\b'
        known_regex = re.compile(regex_pattern)
    else:
        known_regex = re.compile(r'(?!)') # matches nothing

    scanned_count = 0
    for filepath in files_to_scan:
        console.print(f"Scanning: {filepath}")
        scan_file(filepath, nlp, known_regex, known_entities, inventory_data)
        scanned_count += 1

    # Evaluieren der Domänen nach dem Scanning
    evaluate_domains(inventory_data)

    # Globale Stats updaten
    inventory_data.files_scanned = len(files_to_scan) # Or update cumulatively if needed
    inventory_data.unique_entities_found = len(inventory_data.entity_details)
    inventory_data.total_mentions = sum(e.total_mentions for e in inventory_data.entity_details.values())
    inventory_data.scan_date = datetime.utcnow()

    os.makedirs('tools/output', exist_ok=True)
    with open(inventory_file, 'w', encoding='utf-8') as f:
        f.write(inventory_data.model_dump_json(indent=2))

    # Terminal Output
    table = Table(title="Updated Inventory Stats")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")

    table.add_row("Files scanned this run", str(scanned_count))
    table.add_row("Total Unique Entities", str(inventory_data.unique_entities_found))
    table.add_row("Total Mentions", str(inventory_data.total_mentions))

    console.print(table)
    console.print(f"[bold green]Saved inventory to {inventory_file}[/bold green]")

if __name__ == '__main__':
    scan()
