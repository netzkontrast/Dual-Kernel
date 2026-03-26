import re
import click
import spacy
import json
import os
from collections import defaultdict
from rich.console import Console
from rich.table import Table
from datetime import datetime

from common import (
    KNOWN_ENTITIES, DOMAIN_MAPPING, DomainEnum, guess_domain,
    SourceInventoryExport, EntityExport, FileMentionsExport
)

console = Console()

def get_context(lines, index, context_size=2):
    start = max(0, index - context_size)
    end = min(len(lines), index + context_size + 1)
    return "\n".join(lines[start:end])

@click.command()
@click.option('--file', required=True, type=click.Path(exists=True), help='Markdown file to scan')
def scan(file):
    console.print(f"[bold blue]Scanning file:[/bold blue] {file}")

    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    nlp = spacy.load("de_core_news_lg", disable=["parser", "lemmatizer", "tagger", "attribute_ruler"])

    # Compile known entities into regex
    known_entities_sorted = sorted(KNOWN_ENTITIES, key=len, reverse=True)
    regex_pattern = r'\b(' + '|'.join(map(re.escape, known_entities_sorted)) + r')\b'
    known_regex = re.compile(regex_pattern)

    entities = defaultdict(lambda: {"is_known": False, "domain": None, "mentions": []})

    # 1. Regex Pass (Known Entities)
    for i, line in enumerate(lines):
        for match in known_regex.finditer(line):
            entity_name = match.group(0)
            context = get_context(lines, i)

            if not entities[entity_name]["domain"]:
                entities[entity_name]["domain"] = guess_domain(entity_name)
                entities[entity_name]["is_known"] = True

            entities[entity_name]["mentions"].append({
                "mention_id": f"{entity_name}_{i+1}_{len(entities[entity_name]['mentions'])}",
                "entity_name": entity_name,
                "file_id": os.path.basename(file),
                "line_number": i + 1,
                "context_text": context,
                "is_bold": False
            })

    # 2. SpaCy Pass (Unknown Entities)
    doc = nlp(content)
    # Map token start character to line number
    char_to_line = {}
    current_char = 0
    for i, line in enumerate(lines):
        for j in range(len(line) + 1): # +1 for newline
            char_to_line[current_char + j] = i + 1
        current_char += len(line) + 1

    for ent in doc.ents:
        if ent.label_ in ["PER", "LOC", "ORG"]:
            entity_name = ent.text.strip()
            # Clean punctuation from edges
            entity_name = entity_name.strip('.,;:!?()[]{}"\'')

            if not entity_name or entity_name in entities or entity_name in KNOWN_ENTITIES:
                continue

            line_idx = char_to_line.get(ent.start_char, 1) - 1
            context = get_context(lines, line_idx)

            entities[entity_name]["domain"] = guess_domain(entity_name, ent.label_)
            entities[entity_name]["is_known"] = False

            entities[entity_name]["mentions"].append({
                "mention_id": f"{entity_name}_{line_idx+1}_{len(entities[entity_name]['mentions'])}",
                "entity_name": entity_name,
                "file_id": os.path.basename(file),
                "line_number": line_idx + 1,
                "context_text": context,
                "is_bold": False
            })

    # Export using Pydantic Models structure
    export_data = SourceInventoryExport(
        files_scanned=1,
        unique_entities_found=len(entities),
        total_mentions=sum(len(e["mentions"]) for e in entities.values()),
        entity_details={}
    )

    filename = os.path.basename(file)

    for name, data in entities.items():
        if not data["mentions"]:
            continue

        mentions_dicts = [{"line": m["line_number"], "context": m["context_text"]} for m in data["mentions"]]

        file_export = FileMentionsExport(
            mention_count=len(data["mentions"]),
            mentions=mentions_dicts
        )

        export_data.entity_details[name] = EntityExport(
            total_mentions=len(data["mentions"]),
            estimated_domain=data["domain"],
            files={filename: file_export}
        )

    os.makedirs('tools/output', exist_ok=True)
    with open('tools/output/source-inventory.json', 'w', encoding='utf-8') as f:
        f.write(export_data.model_dump_json(indent=2))

    # Terminal Output
    table = Table(title="Extracted Entities")
    table.add_column("Entity", style="cyan")
    table.add_column("Domain", style="magenta")
    table.add_column("Known", style="green")
    table.add_column("Mentions", style="yellow")

    for name, data in entities.items():
        if data["mentions"]:
            table.add_row(
                name,
                data["domain"].value if data["domain"] else "Unknown",
                "Yes" if data["is_known"] else "No",
                str(len(data["mentions"]))
            )

    console.print(table)
    console.print(f"[bold green]Saved inventory to tools/output/source-inventory.json[/bold green]")

if __name__ == '__main__':
    scan()
