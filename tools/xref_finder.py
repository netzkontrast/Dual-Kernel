import json
import os
import re
from collections import defaultdict
from rich.console import Console

console = Console()

def find_conflicts(inventory_file='tools/output/source-inventory.json'):
    with open(inventory_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    conflicts = {}

    number_pattern = re.compile(r'\b(\d+)\b')
    state_pattern = re.compile(r'(ist\s+tot|ist\s+lebendig|Status:\s+\w+|geschwächt|stark|unbeugsam)', re.IGNORECASE)

    for entity_name, entity_data in data['entity_details'].items():
        found_values = defaultdict(list)

        for file_id, file_data in entity_data['files'].items():
            for mention in file_data['mentions']:
                context = mention['context']
                line_number = mention['line']

                # Check for numbers
                numbers = number_pattern.findall(context)
                for num in numbers:
                    found_values['numbers'].append({
                        "value": num,
                        "source": f"{file_id}:~{line_number}",
                        "context": context.replace("\n", " ").strip()
                    })

                # Check for states
                states = state_pattern.findall(context)
                for state in states:
                    found_values['states'].append({
                        "value": state.lower(),
                        "source": f"{file_id}:~{line_number}",
                        "context": context.replace("\n", " ").strip()
                    })

        entity_conflicts = []

        # Determine number conflicts (e.g., "11" vs "13")
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

        # Determine state conflicts (e.g., "geschwächt" vs "stark")
        unique_states = {v['value'] for v in found_values['states']}
        # Simple heuristic for testing: if multiple distinct states exist
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

    os.makedirs('tools/output', exist_ok=True)
    with open('tools/output/cross-references.json', 'w', encoding='utf-8') as f:
        json.dump(conflicts, f, indent=2, ensure_ascii=False)

    console.print(f"[bold green]Found {len(conflicts)} entities with potential conflicts.[/bold green]")
    console.print(f"Saved conflicts to tools/output/cross-references.json")

if __name__ == '__main__':
    find_conflicts()
