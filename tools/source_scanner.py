import os
import re
import urllib.parse
from typing import List, Dict, Tuple, Set, Optional
from collections import defaultdict

import click
import spacy
from rich.progress import track
from rich.console import Console
from rich.table import Table

# Import Pydantic models and helpers from common.py
from common import (
    DomainEnum,
    ScannedFile,
    Entity,
    Mention,
    FileMentionsExport,
    EntityExport,
    SourceInventoryExport,
    load_known_entities
)

console = Console()

def generate_mention_id(file_id: str, line_number: int, entity_name: str) -> str:
    """Generates a URL-safe, readable mention ID."""
    clean_name = urllib.parse.quote(entity_name.lower().replace(" ", "-"))
    return f"{file_id}_{line_number}_{clean_name}"

def extract_context(lines: List[str], line_idx: int) -> str:
    """Extracts ±2 lines of context, strips newlines, and joins with space."""
    start_idx = max(0, line_idx - 2)
    end_idx = min(len(lines), line_idx + 3)

    context_lines = []
    for i in range(start_idx, end_idx):
        context_lines.append(lines[i].strip())

    # Filter out empty strings and join
    return " ".join([line for line in context_lines if line])

def check_is_bold(line: str, start: int, end: int) -> bool:
    """Checks if the matched string is surrounded by ** or __."""
    if start >= 2 and end <= len(line) - 2:
        before = line[start-2:start]
        after = line[end:end+2]
        if (before == '**' and after == '**') or (before == '__' and after == '__'):
            return True
    return False

def check_overlap(regex_matches: List[Tuple[int, int]], spacy_start: int, spacy_end: int) -> bool:
    """Checks if a spacy match overlaps with any regex match."""
    for r_start, r_end in regex_matches:
        # Overlap condition: r_start < spacy_end AND r_end > spacy_start
        if r_start < spacy_end and r_end > spacy_start:
            return True
    return False

def determine_domain(context_texts: List[str]) -> Optional[DomainEnum]:
    """Heuristic to determine the domain based on keyword frequency in context."""
    # Case-sensitive for nouns, except for specific pronouns if we wanted, but sticking to nouns
    domain_keywords = {
        DomainEnum.CHARACTER: ["Alter", "System", "Trauma", "ANP", "EP"],
        DomainEnum.PHYSICS: ["Energie", "Kernel", "DKT", "Berechnung", "K1", "K0", "Kohärenz"],
        DomainEnum.AEGIS: ["Protokoll", "Verhinderung", "Primal", "Melancholie"],
        DomainEnum.WORLD: ["Stadt", "Sektor", "Zone", "Simulation", "Kernwelt"]
    }

    combined_context = " ".join(context_texts)

    domain_scores = defaultdict(int)
    for domain, keywords in domain_keywords.items():
        for keyword in keywords:
            # Case-sensitive search for whole words (optional, but requested case-sensitive)
            # using \b for word boundaries might fail for K1, K0 if they are part of K1-System etc.
            # We'll use a simple count in the string for robustness, or regex with lookarounds.
            pattern = rf"(?<!\w){re.escape(keyword)}(?!\w)"
            matches = re.findall(pattern, combined_context)
            domain_scores[domain] += len(matches)

    if not domain_scores:
        return None

    # Get domain with highest score
    best_domain = max(domain_scores.items(), key=lambda x: x[1])
    if best_domain[1] > 0:
        return best_domain[0]
    return None


@click.command()
@click.argument('docs_dir', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('--output', '-o', default='tools/output/source-inventory.json', help='Output JSON file path.')
def main(docs_dir: str, output: str):
    """Scans Markdown files for entities and generates a knowledge graph inventory."""
    console.print(f"[bold blue]Starte Source Scanner in Verzeichnis:[/] {docs_dir}")

    # 1. Setup & Extract
    known_entities_list = load_known_entities("known_entities.txt")

    # Compile regex patterns
    regex_patterns = []
    for entity in known_entities_list:
        # (?<!\w) ... (?!\w) is safer than \b for things with special chars
        escaped_entity = re.escape(entity)
        pattern_str = rf"(?<!\w){escaped_entity}(?!\w)"

        if len(entity) <= 3:
            # Case-sensitive for short words
            regex_patterns.append((entity, re.compile(pattern_str)))
        else:
            # Case-insensitive for long words
            regex_patterns.append((entity, re.compile(pattern_str, re.IGNORECASE)))

    console.print(f"[green]✓[/] {len(known_entities_list)} bekannte Entitäten geladen und kompiliert.")

    # Load spaCy
    console.print("[yellow]Lade spaCy Modell (de_core_news_lg)...[/]")
    try:
        nlp = spacy.load("de_core_news_lg", disable=["parser", "lemmatizer"])
        console.print("[green]✓[/] spaCy Modell geladen.")
    except Exception as e:
        console.print(f"[red]Fehler beim Laden von spaCy:[/] {e}")
        console.print("Bitte stelle sicher, dass das Modell installiert ist: python -m spacy download de_core_news_lg")
        return

    # Initialize State
    scanned_files: Dict[str, ScannedFile] = {}
    entities: Dict[str, Entity] = {}
    mentions: List[Mention] = []

    # Find Markdown files
    md_files = []
    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))

    # 2. Transform (Hybride Detection)
    for filepath in track(md_files, description="Scanne Dateien..."):
        filename = os.path.basename(filepath)
        file_id = filename

        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        scanned_file = ScannedFile(file_id=file_id, filepath=filepath, line_count=len(lines))
        scanned_files[file_id] = scanned_file

        full_text = "".join(lines)

        # spaCy analysis on full text
        doc = nlp(full_text)

        # We need to map spaCy entites to line numbers for conflict resolution
        # Let's track line offsets
        line_offsets = []
        current_offset = 0
        for line in lines:
            line_offsets.append((current_offset, current_offset + len(line)))
            current_offset += len(line)

        def get_line_idx(char_offset: int) -> int:
            for idx, (start, end) in enumerate(line_offsets):
                if start <= char_offset < end:
                    return idx
            return len(lines) - 1

        # Group spacy matches by line_idx for easier conflict resolution
        spacy_matches_by_line = defaultdict(list)
        for ent in doc.ents:
            if ent.label_ in ["PER", "LOC", "ORG"] and len(ent.text) >= 3:
                line_idx = get_line_idx(ent.start_char)
                # Calculate relative start/end within the line
                line_start_offset = line_offsets[line_idx][0]
                rel_start = ent.start_char - line_start_offset
                rel_end = ent.end_char - line_start_offset
                spacy_matches_by_line[line_idx].append((ent.text, rel_start, rel_end))

        # Scan line by line with Regex
        for line_idx, line in enumerate(lines):
            line_number = line_idx + 1
            regex_matches_in_line: List[Tuple[int, int]] = []

            # Regex Scan
            for entity_name, pattern in regex_patterns:
                for match in pattern.finditer(line):
                    start, end = match.span()
                    regex_matches_in_line.append((start, end))

                    # Create/Update Entity
                    if entity_name not in entities:
                        entities[entity_name] = Entity(name=entity_name, is_known=True)
                    entities[entity_name].total_mentions += 1

                    # Create Mention
                    context_text = extract_context(lines, line_idx)
                    is_bold = check_is_bold(line, start, end)
                    mention_id = generate_mention_id(file_id, line_number, entity_name)

                    mentions.append(Mention(
                        mention_id=mention_id,
                        entity_name=entity_name,
                        file_id=file_id,
                        line_number=line_number,
                        context_text=context_text,
                        is_bold=is_bold
                    ))

            # spaCy Scan (resolve conflicts)
            if line_idx in spacy_matches_by_line:
                for spacy_text, spacy_start, spacy_end in spacy_matches_by_line[line_idx]:
                    if not check_overlap(regex_matches_in_line, spacy_start, spacy_end):
                        # No conflict, add spaCy entity

                        # Clean spacy text (remove newlines if any)
                        clean_spacy_text = spacy_text.replace("\n", " ").strip()
                        if not clean_spacy_text:
                            continue

                        # Create/Update Entity
                        if clean_spacy_text not in entities:
                            entities[clean_spacy_text] = Entity(name=clean_spacy_text, is_known=False)
                        entities[clean_spacy_text].total_mentions += 1

                        # Create Mention
                        context_text = extract_context(lines, line_idx)
                        is_bold = check_is_bold(line, spacy_start, spacy_end)
                        mention_id = generate_mention_id(file_id, line_number, clean_spacy_text)

                        mentions.append(Mention(
                            mention_id=mention_id,
                            entity_name=clean_spacy_text,
                            file_id=file_id,
                            line_number=line_number,
                            context_text=context_text,
                            is_bold=is_bold
                        ))

    # 3. Transform (Domain Heuristik)
    console.print("[yellow]Führe Domain-Heuristik aus...[/]")

    # Group contexts by entity
    entity_contexts = defaultdict(list)
    for mention in mentions:
        entity_contexts[mention.entity_name].append(mention.context_text)

    for entity_name, entity in entities.items():
        if entity_name in entity_contexts:
            entity.estimated_domain = determine_domain(entity_contexts[entity_name])

    # 4. Load (Export)
    console.print("[yellow]Generiere Export-Daten...[/]")

    export_entities: Dict[str, EntityExport] = {}

    # Group mentions by entity and file
    mentions_by_entity_and_file = defaultdict(lambda: defaultdict(list))
    for mention in mentions:
        mentions_by_entity_and_file[mention.entity_name][mention.file_id].append({
            "line": mention.line_number,
            "context": mention.context_text
        })

    for entity_name, entity in entities.items():
        files_export: Dict[str, FileMentionsExport] = {}
        for file_id, file_mentions in mentions_by_entity_and_file.get(entity_name, {}).items():
            files_export[file_id] = FileMentionsExport(
                mention_count=len(file_mentions),
                mentions=file_mentions
            )

        export_entities[entity_name] = EntityExport(
            total_mentions=entity.total_mentions,
            estimated_domain=entity.estimated_domain,
            files=files_export
        )

    source_inventory = SourceInventoryExport(
        files_scanned=len(scanned_files),
        unique_entities_found=len(entities),
        total_mentions=len(mentions),
        entity_details=export_entities
    )

    # Save to output file
    os.makedirs(os.path.dirname(output), exist_ok=True)
    with open(output, 'w', encoding='utf-8') as f:
        f.write(source_inventory.model_dump_json(indent=2))

    console.print(f"[green]✓[/] Ergebnisse in [bold]{output}[/] gespeichert.")

    # Print Summary Table
    table = Table(title="Source Scanner Zusammenfassung")
    table.add_column("Metrik", style="cyan")
    table.add_column("Wert", style="magenta")

    table.add_row("Gescannte Dateien", str(len(scanned_files)))
    table.add_row("Gefundene Entitäten", str(len(entities)))
    table.add_row("Gesamte Erwähnungen", str(len(mentions)))

    console.print(table)

    # Print Top 5 Entities
    top_entities = sorted(entities.values(), key=lambda x: x.total_mentions, reverse=True)[:5]
    if top_entities:
        top_table = Table(title="Top 5 Entitäten")
        top_table.add_column("Entität", style="cyan")
        top_table.add_column("Erwähnungen", justify="right", style="green")
        top_table.add_column("Domain", style="yellow")

        for ent in top_entities:
            domain_str = ent.estimated_domain.value if ent.estimated_domain else "None"
            top_table.add_row(ent.name, str(ent.total_mentions), domain_str)

        console.print(top_table)

if __name__ == '__main__':
    main()
