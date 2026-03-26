import re
import click
import spacy
import json
import os
from bisect import bisect_right
from collections import defaultdict
from rich.table import Table

from common import (
    KNOWN_ENTITIES, KNOWN_ENTITIES_REGEX, guess_domain,
    SourceInventoryExport, EntityExport, FileMentionsExport,
    console, ensure_output_dir, INVENTORY_PATH
)


def get_context(lines, index, context_size=2):
    start = max(0, index - context_size)
    end = min(len(lines), index + context_size + 1)
    return "\n".join(lines[start:end])


def build_mention(entity_name, file_id, line_number, context, mention_count):
    return {
        "mention_id": f"{entity_name}_{line_number}_{mention_count}",
        "entity_name": entity_name,
        "file_id": file_id,
        "line_number": line_number,
        "context_text": context,
        "is_bold": False
    }


@click.command()
@click.option('--file', required=True, type=click.Path(exists=True), help='Markdown file to scan')
def scan(file):
    console.print(f"[bold blue]Scanning file:[/bold blue] {file}")

    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    file_id = os.path.basename(file)
    nlp = spacy.load("de_core_news_lg", disable=["parser", "lemmatizer", "tagger", "attribute_ruler"])

    entities = defaultdict(lambda: {"is_known": False, "domain": None, "mentions": []})

    for i, line in enumerate(lines):
        for match in KNOWN_ENTITIES_REGEX.finditer(line):
            entity_name = match.group(0)
            context = get_context(lines, i)

            if not entities[entity_name]["domain"]:
                entities[entity_name]["domain"] = guess_domain(entity_name)
                entities[entity_name]["is_known"] = True

            entities[entity_name]["mentions"].append(
                build_mention(entity_name, file_id, i + 1, context, len(entities[entity_name]['mentions']))
            )

    doc = nlp(content)

    # Build line-start offsets for O(log N) char-to-line lookup
    line_offsets = []
    offset = 0
    for line in lines:
        line_offsets.append(offset)
        offset += len(line) + 1

    for ent in doc.ents:
        if ent.label_ in ("PER", "LOC", "ORG"):
            entity_name = ent.text.strip().strip('.,;:!?()[]{}"\'')

            if not entity_name or entity_name in entities or entity_name in KNOWN_ENTITIES:
                continue

            line_idx = bisect_right(line_offsets, ent.start_char) - 1
            context = get_context(lines, line_idx)

            entities[entity_name]["domain"] = guess_domain(entity_name, ent.label_)
            entities[entity_name]["is_known"] = False

            entities[entity_name]["mentions"].append(
                build_mention(entity_name, file_id, line_idx + 1, context, len(entities[entity_name]['mentions']))
            )

    export_data = SourceInventoryExport(
        files_scanned=1,
        unique_entities_found=len(entities),
        total_mentions=sum(len(e["mentions"]) for e in entities.values()),
        entity_details={}
    )

    for name, data in entities.items():
        if not data["mentions"]:
            continue

        mentions_dicts = [{"line": m["line_number"], "context": m["context_text"]} for m in data["mentions"]]

        export_data.entity_details[name] = EntityExport(
            total_mentions=len(data["mentions"]),
            estimated_domain=data["domain"],
            files={file_id: FileMentionsExport(
                mention_count=len(data["mentions"]),
                mentions=mentions_dicts
            )}
        )

    ensure_output_dir()
    with open(INVENTORY_PATH, 'w', encoding='utf-8') as f:
        f.write(export_data.model_dump_json(indent=2))

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
    console.print(f"[bold green]Saved inventory to {INVENTORY_PATH}[/bold green]")

if __name__ == '__main__':
    scan()
