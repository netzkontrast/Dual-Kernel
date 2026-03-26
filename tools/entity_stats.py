import json
import os
from datetime import datetime
from rich.console import Console

console = Console()

def generate_stats():
    with open('tools/output/source-inventory.json', 'r', encoding='utf-8') as f:
        inventory = json.load(f)

    try:
        with open('tools/output/cross-references.json', 'r', encoding='utf-8') as f:
            conflicts = json.load(f)
    except FileNotFoundError:
        conflicts = {}

    total_entities = inventory['unique_entities_found']
    total_mentions = inventory['total_mentions']

    known_count = sum(1 for e in inventory['entity_details'].values() if e.get('is_known', False))
    unknown_count = total_entities - known_count

    conflict_count = len(conflicts)

    domains = {}
    for data in inventory['entity_details'].values():
        domain = data.get('estimated_domain', 'fundament')
        domains[domain] = domains.get(domain, 0) + 1

    md_content = f"""# Knowledge Graph Extraction Report

**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Files Scanned:** 1
**Total Entities:** {total_entities}
**Total Mentions:** {total_mentions}

## Breakdown

- **Known Entities:** {known_count}
- **Newly Discovered (Provisional):** {unknown_count}
- **Entities with Conflicts (Disputed):** {conflict_count}

## Domain Distribution

"""
    for domain, count in sorted(domains.items(), key=lambda x: x[1], reverse=True):
        md_content += f"- **{domain}**: {count}\n"

    os.makedirs('knowledge-graph/_index', exist_ok=True)
    report_path = 'knowledge-graph/_index/extraction-report.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(md_content)

    console.print(f"[bold green]Generated extraction report at:[/bold green] {report_path}")

if __name__ == '__main__':
    generate_stats()
