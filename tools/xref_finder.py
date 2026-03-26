import json
import os
import re
from rich.console import Console

console = Console()

def generate_llm_prompts(inventory_file='tools/output/source-inventory.json'):
    if not os.path.exists(inventory_file):
        console.print(f"[bold red]Inventory file not found:[/bold red] {inventory_file}")
        return

    with open(inventory_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    prompts = []
    SYSTEM_PROMPT = "Finde logische Widersprüche (Zahlen, Rollen, Zustände) zwischen den Quellen dieser Entität."

    for entity_name, entity_data in data['entity_details'].items():
        # Filtere Entitäten, die in mehr als einer Datei auftauchen
        if len(entity_data['files']) > 1:
            sources = []
            for file_id, file_data in entity_data['files'].items():

                # Kompaktiere alle Kontexte aus dieser Datei
                compact_contexts = []
                for mention in file_data['mentions']:
                    # Entferne redundante Leerzeichen, Tabs und Newlines
                    context = re.sub(r'\s+', ' ', mention['context']).strip()
                    compact_contexts.append(context)

                combined_context = " ".join(compact_contexts)

                sources.append({
                    "file": file_id,
                    "context": combined_context
                })

            prompt_obj = {
                "entity": entity_name,
                "system_prompt": SYSTEM_PROMPT,
                "sources": sources
            }
            prompts.append(prompt_obj)

    os.makedirs('tools/output', exist_ok=True)
    output_file = 'tools/output/llm_conflict_prompts.jsonl'

    with open(output_file, 'w', encoding='utf-8') as f:
        for p in prompts:
            f.write(json.dumps(p, ensure_ascii=False) + '\n')

    console.print(f"[bold green]Generated {len(prompts)} LLM conflict prompts.[/bold green]")
    console.print(f"Saved JSON-Lines output to {output_file}")

if __name__ == '__main__':
    generate_llm_prompts()
