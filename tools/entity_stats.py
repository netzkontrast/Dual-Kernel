import os
from datetime import datetime
from common import console, load_inventory, load_conflicts, KG_DIR


def generate_stats():
    inventory = load_inventory()
    conflicts = load_conflicts()

    entity_details = inventory['entity_details']
    total_entities = len(entity_details)
    total_mentions = sum(e['total_mentions'] for e in entity_details.values())
    files_scanned = inventory.get('files_scanned', 1)

    known_count = sum(1 for e in entity_details.values() if e.get('is_known', False))
    unknown_count = total_entities - known_count

    conflict_count = len(conflicts)

    domains = {}
    for data in entity_details.values():
        domain = data.get('estimated_domain', 'fundament')
        domains[domain] = domains.get(domain, 0) + 1

    md_content = f"""# Knowledge Graph Extraction Report

**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Files Scanned:** {files_scanned}
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

    index_dir = os.path.join(KG_DIR, '_index')
    os.makedirs(index_dir, exist_ok=True)
    report_path = os.path.join(index_dir, 'extraction-report.md')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(md_content)

    console.print(f"[bold green]Generated extraction report at:[/bold green] {report_path}")

if __name__ == '__main__':
    generate_stats()
