"""Map entities to their chapter appearances using the 39-chapter matrix."""
import os
import re
import glob
import yaml
import click
from collections import defaultdict
from common import (
    console, slugify, KG_DIR, KNOWN_ENTITIES_REGEX,
    KNOWN_ENTITIES, load_inventory
)


CHAPTER_SOURCE = 'Markdown-docs/KoharenzProtokoll39KapitelMatrix.md'

# Fields in the chapter matrix that contain entity references
ENTITY_FIELDS = ['Charaktere', 'Ort', 'Plot-Beat', 'Narrative Funktion',
                 'Perspektive & Stimme', 'Überschrift', 'Titel']


def parse_chapters(filepath):
    """Parse the 39-chapter matrix into structured chapter data."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    chapters = []
    # Split by chapter headers: ## **Kapitel N** or - **Kapitel N**
    chapter_pattern = re.compile(
        r'(?:##\s*\*\*|-\s*\*\*)Kapitel\s+(\d+)\*\*',
        re.IGNORECASE
    )

    splits = list(chapter_pattern.finditer(content))
    for i, match in enumerate(splits):
        chapter_num = int(match.group(1))
        start = match.start()
        end = splits[i + 1].start() if i + 1 < len(splits) else len(content)
        chapter_text = content[start:end]

        chapter_data = {
            'number': chapter_num,
            'text': chapter_text,
            'title': '',
            'characters': [],
            'location': '',
        }

        # Extract structured fields
        title_match = re.search(r'\*\*Titel:\*\*\s*(.+)', chapter_text)
        if title_match:
            chapter_data['title'] = title_match.group(1).strip()

        char_match = re.search(r'\*\*Charaktere:\*\*\s*(.+)', chapter_text)
        if char_match:
            chapter_data['characters'] = [
                c.strip().rstrip('.')
                for c in re.split(r'[,;]', char_match.group(1))
            ]

        loc_match = re.search(r'\*\*Ort:\*\*\s*(.+)', chapter_text)
        if loc_match:
            chapter_data['location'] = loc_match.group(1).strip()

        chapters.append(chapter_data)

    return chapters


def find_entity_mentions_in_chapters(chapters):
    """Find all known entity mentions within each chapter's text."""
    entity_chapters = defaultdict(set)

    for chapter in chapters:
        text = chapter['text']
        # Find known entities via regex
        for match in KNOWN_ENTITIES_REGEX.finditer(text):
            entity_name = match.group(0)
            entity_chapters[entity_name].add(chapter['number'])

    return entity_chapters


def parse_frontmatter(filepath):
    """Extract YAML frontmatter from a markdown file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if not content.startswith('---'):
        return None
    end_idx = content.find('---', 3)
    if end_idx == -1:
        return None
    try:
        return yaml.safe_load(content[3:end_idx])
    except yaml.YAMLError:
        return None


def load_kg_entities():
    """Load existing knowledge graph entities."""
    entities = {}
    files = glob.glob(f'{KG_DIR}/**/*.md', recursive=True)
    for f in files:
        if f.endswith('README.md'):
            continue
        data = parse_frontmatter(f)
        if data and 'title' in data:
            entities[data['title']] = {'path': f, 'data': data}
    return entities


@click.command()
@click.option('--chapter-file', default=CHAPTER_SOURCE,
              help='Path to chapter matrix document')
@click.option('--update', is_flag=True,
              help='Update entity files with chapter appearance data')
@click.option('--output', '-o', default=None,
              help='Output file for chapter-entity matrix')
def map_chapters(chapter_file, update, output):
    """Map entities to their chapter appearances."""
    if not os.path.exists(chapter_file):
        console.print(f"[bold red]Chapter file not found:[/bold red] {chapter_file}")
        return

    chapters = parse_chapters(chapter_file)
    if not chapters:
        console.print("[bold red]No chapters parsed from source file.[/bold red]")
        return

    console.print(f"[bold blue]Parsed {len(chapters)} chapters[/bold blue]")

    # Find entity mentions in chapters
    entity_chapters = find_entity_mentions_in_chapters(chapters)

    # Load existing KG entities for cross-reference
    kg_entities = load_kg_entities()

    # Build chapter-entity matrix
    all_entities_sorted = sorted(entity_chapters.keys())
    all_chapters_sorted = sorted({ch['number'] for ch in chapters})

    # Generate markdown report
    lines = ["# Chapter-Entity Matrix\n"]
    lines.append(f"**Source:** `{chapter_file}`\n")
    lines.append(f"**Chapters:** {len(chapters)} | **Entities Found:** {len(entity_chapters)}\n")

    # Entity appearance summary
    lines.append("\n## Entity Appearances\n")
    lines.append("| Entity | Chapters | Count | In KG |")
    lines.append("|--------|----------|-------|-------|")

    for entity in all_entities_sorted:
        ch_nums = sorted(entity_chapters[entity])
        ch_str = ", ".join(str(c) for c in ch_nums)
        in_kg = "✓" if entity in kg_entities else "—"
        lines.append(f"| {entity} | {ch_str} | {len(ch_nums)} | {in_kg} |")

    # Chapter breakdown
    lines.append("\n## Chapter Breakdown\n")
    for chapter in sorted(chapters, key=lambda c: c['number']):
        num = chapter['number']
        title = chapter.get('title', '')
        entities_in_ch = [e for e, chs in entity_chapters.items() if num in chs]
        lines.append(f"### Kapitel {num}: {title}\n")
        if entities_in_ch:
            for e in sorted(entities_in_ch):
                marker = "🔗" if e in kg_entities else "·"
                lines.append(f"- {marker} {e}")
        else:
            lines.append("- _(keine bekannten Entitäten gefunden)_")
        lines.append("")

    # Narrative arc analysis
    lines.append("\n## Narrative Arc Analysis\n")
    lines.append("Entities sorted by span (first to last appearance):\n")
    lines.append("| Entity | First | Last | Span | Arc |")
    lines.append("|--------|-------|------|------|-----|")

    arc_data = []
    for entity in all_entities_sorted:
        ch_nums = sorted(entity_chapters[entity])
        first = ch_nums[0]
        last = ch_nums[-1]
        span = last - first
        # Visual arc bar
        bar_chars = 39
        bar = ['·'] * bar_chars
        for c in ch_nums:
            if 0 <= c < bar_chars:
                bar[c] = '█'
        arc_str = ''.join(bar[:max(last + 2, 10)])
        arc_data.append((entity, first, last, span, arc_str))

    arc_data.sort(key=lambda x: (-x[3], x[1]))
    for entity, first, last, span, arc_str in arc_data:
        lines.append(f"| {entity} | {first} | {last} | {span} | `{arc_str}` |")

    report_content = "\n".join(lines)
    report_content += "\n\n_Automatisch generiert von `chapter_mapper.py`._\n"

    # Write output
    if output is None:
        index_dir = os.path.join(KG_DIR, '_index')
        os.makedirs(index_dir, exist_ok=True)
        output = os.path.join(index_dir, 'chapter-entity-matrix.md')

    os.makedirs(os.path.dirname(output), exist_ok=True)
    with open(output, 'w', encoding='utf-8') as f:
        f.write(report_content)

    console.print(f"[bold green]Generated chapter-entity matrix:[/bold green] {output}")

    # Optionally update entity files with chapter data
    if update:
        updated_count = 0
        for entity_name, ch_nums_set in entity_chapters.items():
            if entity_name not in kg_entities:
                continue

            ch_nums = sorted(ch_nums_set)
            first_ch = ch_nums[0]
            last_ch = ch_nums[-1]

            entity_path = kg_entities[entity_name]['path']
            with open(entity_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Update first_appearance_chapter
            content = re.sub(
                r'first_appearance_chapter:\s*\S+',
                f'first_appearance_chapter: {first_ch}',
                content
            )
            # Update last_referenced_chapter
            content = re.sub(
                r'last_referenced_chapter:\s*\S+',
                f'last_referenced_chapter: {last_ch}',
                content
            )

            with open(entity_path, 'w', encoding='utf-8') as f:
                f.write(content)

            updated_count += 1
            console.print(f"  [cyan]Updated:[/cyan] {entity_name} → chapters {first_ch}-{last_ch}")

        console.print(f"\n[bold green]Updated {updated_count} entity files with chapter data.[/bold green]")

    # Print summary
    console.print(f"\n[bold cyan]Top entities by chapter span:[/bold cyan]")
    for entity, first, last, span, _ in arc_data[:10]:
        console.print(f"  {entity}: chapters {first}–{last} (span {span})")


if __name__ == '__main__':
    map_chapters()
