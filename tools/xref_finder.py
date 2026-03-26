import json
import re
from collections import defaultdict
from common import console, load_inventory, ensure_output_dir, CONFLICTS_PATH


def find_conflicts(inventory_file=None):
    data = load_inventory(inventory_file) if inventory_file else load_inventory()

    conflicts = {}

    number_pattern = re.compile(r'\b(\d+)\b')
    state_pattern = re.compile(r'(ist\s+tot|ist\s+lebendig|Status:\s+\w+|geschwächt|stark|unbeugsam)', re.IGNORECASE)

    for entity_name, entity_data in data['entity_details'].items():
        found_values = defaultdict(list)

        for file_id, file_data in entity_data['files'].items():
            for mention in file_data['mentions']:
                context = mention['context'].replace("\n", " ").strip()
                line_number = mention['line']
                source = f"{file_id}:~{line_number}"

                for num in number_pattern.findall(context):
                    found_values['numbers'].append({"value": num, "source": source})

                for state in state_pattern.findall(context):
                    found_values['states'].append({"value": state.lower(), "source": source})

        entity_conflicts = []

        unique_numbers = {v['value'] for v in found_values['numbers']}
        if len(unique_numbers) > 1:
            entity_conflicts.append({
                "id": "number-conflict",
                "description": f"Unterschiedliche Zahlenwerte im Kontext von {entity_name}",
                "variants": [
                    {"claim": v['value'], "source": v['source']}
                    for v in found_values['numbers']
                ]
            })

        unique_states = {v['value'] for v in found_values['states']}
        if len(unique_states) > 1:
            entity_conflicts.append({
                "id": "state-conflict",
                "description": f"Unterschiedliche Zustände für {entity_name}",
                "variants": [
                    {"claim": v['value'], "source": v['source']}
                    for v in found_values['states']
                ]
            })

        if entity_conflicts:
            conflicts[entity_name] = entity_conflicts

    ensure_output_dir()
    with open(CONFLICTS_PATH, 'w', encoding='utf-8') as f:
        json.dump(conflicts, f, indent=2, ensure_ascii=False)

    console.print(f"[bold green]Found {len(conflicts)} entities with potential conflicts.[/bold green]")
    console.print(f"Saved conflicts to {CONFLICTS_PATH}")

if __name__ == '__main__':
    find_conflicts()
