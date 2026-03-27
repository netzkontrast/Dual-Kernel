"""Map entities to their chapter appearances using the 39-chapter matrix."""
import os
import re
import click
from collections import defaultdict
from common import (
    console, KG_DIR, KNOWN_ENTITIES_REGEX, load_all_entities
)


CHAPTER_SOURCE = 'Markdown-docs/KoharenzProtokoll39KapitelMatrix.md'


def parse_chapters(filepath):
    """Parse the 39-chapter matrix into structured chapter data."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    chapters = []
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
        }

        title_match = re.search(r'\*\*Titel:\*\*\s*(.+)', chapter_text)
        if title_match:
            chapter_data['title'] = title_match.group(1).strip()

        chapters.append(chapter_data)

    return chapters


def find_entity_mentions_in_chapters(chapters):
    """Find all known entity mentions within each chapter's text."""
    entity_chapters = defaultdict(set)
    for chapter in chapters:
        for match in KNOWN_ENTITIES_REGEX.finditer(chapter['text']):
            entity_chapters[match.group(0)].add(chapter['number'])
    return entity_chapters


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

    entity_chapters = find_entity_mentions_in_chapters(chapters)
    kg_entities = load_all_entities()

    all_entities_sorted = sorted(entity_chapters.keys())

    # Generate markdown report
    lines = ["# Chapter-Entity Matrix\n"]
    lines.append(f"**Source:** `{chapter_file}`\n")
    lines.append(f"**Chapters:** {len(chapters)} | **Entities Found:** {len(entity_chapters)}\n")

    lines.append("\n## Entity Appearances\n")
    lines.append("| Entity | Chapters | Count | In KG |")
    lines.append("|--------|----------|-------|-------|")

    for entity in all_entities_sorted:
        ch_nums = sorted(entity_chapters[entity])
        ch_str = ", ".join(str(c) for c in ch_nums)
        in_kg = "✓" if entity in kg_entities else "—"
        lines.append(f"| {entity} | {ch_str} | {len(ch_nums)} | {in_kg} |")

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
        first, last = ch_nums[0], ch_nums[-1]
        span = last - first
        bar = ['·'] * 39
        for c in ch_nums:
            if 0 <= c < 39:
                bar[c] = '█'
        arc_str = ''.join(bar[:max(last + 2, 10)])
        arc_data.append((entity, first, last, span, arc_str))

    arc_data.sort(key=lambda x: (-x[3], x[1]))
    for entity, first, last, span, arc_str in arc_data:
        lines.append(f"| {entity} | {first} | {last} | {span} | `{arc_str}` |")

    report_content = "\n".join(lines)
    report_content += "\n\n_Automatisch generiert von `chapter_mapper.py`._\n"

    if output is None:
        index_dir = os.path.join(KG_DIR, '_index')
        os.makedirs(index_dir, exist_ok=True)
        output = os.path.join(index_dir, 'chapter-entity-matrix.md')

    os.makedirs(os.path.dirname(output), exist_ok=True)
    with open(output, 'w', encoding='utf-8') as f:
        f.write(report_content)

    console.print(f"[bold green]Generated chapter-entity matrix:[/bold green] {output}")

    if update:
        updated_count = 0
        for entity_name, ch_nums_set in entity_chapters.items():
            if entity_name not in kg_entities:
                continue

            ch_nums = sorted(ch_nums_set)
            first_ch, last_ch = ch_nums[0], ch_nums[-1]
            entity_info = kg_entities[entity_name]
            content = entity_info['raw']

            content = re.sub(
                r'first_appearance_chapter:\s*\S+',
                f'first_appearance_chapter: {first_ch}',
                content
            )
            content = re.sub(
                r'last_referenced_chapter:\s*\S+',
                f'last_referenced_chapter: {last_ch}',
                content
            )

            with open(entity_info['path'], 'w', encoding='utf-8') as f:
                f.write(content)

            updated_count += 1
            console.print(f"  [cyan]Updated:[/cyan] {entity_name} → chapters {first_ch}-{last_ch}")

        console.print(f"\n[bold green]Updated {updated_count} entity files with chapter data.[/bold green]")

    console.print(f"\n[bold cyan]Top entities by chapter span:[/bold cyan]")
    for entity, first, last, span, _ in arc_data[:10]:
        console.print(f"  {entity}: chapters {first}–{last} (span {span})")


if __name__ == '__main__':
    map_chapters()
