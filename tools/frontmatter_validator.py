import os
import yaml
import glob
from rich.console import Console

console = Console()

def validate_frontmatter():
    files = glob.glob('knowledge-graph/**/*.md', recursive=True)
    # Ignore READMEs and generation_todo.md
    files = [f for f in files if not f.endswith('README.md') and not f.endswith('generation_todo.md')]

    valid_domains = ["character", "alter-system", "world", "physics", "aegis", "narrative", "style", "philosophy", "theme", "mechanic", "juna", "fundament", "mathematics"]
    valid_canon_statuses = ["confirmed", "provisional", "disputed", "uncertain", "decanonized"]

    invalid_files = []
    warnings = []

    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()

        if not content.startswith('---'):
            invalid_files.append((file, "No frontmatter found"))
            continue

        end_idx = content.find('---', 3)
        if end_idx == -1:
            invalid_files.append((file, "Unclosed frontmatter"))
            continue

        yaml_content = content[3:end_idx]
        try:
            data = yaml.safe_load(yaml_content)
        except yaml.YAMLError as e:
            invalid_files.append((file, f"Invalid YAML: {e}"))
            continue

        # Basic schema validation
        required_keys = ['title', 'id', 'domain', 'canon_status', 'sources']
        for key in required_keys:
            if key not in data:
                invalid_files.append((file, f"Missing required key: {key}"))

        if data.get('domain') not in valid_domains:
            invalid_files.append((file, f"Invalid domain: {data.get('domain')}"))

        if data.get('canon_status') not in valid_canon_statuses:
            invalid_files.append((file, f"Invalid canon_status: {data.get('canon_status')}"))

        # Check for disputed canon status without conflicts
        if data.get('canon_status') == 'disputed':
            conflicts = data.get('conflicts')
            if not conflicts or len(conflicts) == 0:
                warnings.append((file, "Warning: canon_status is 'disputed' but 'conflicts' field is empty."))

    if warnings:
        for file, warning in warnings:
            console.print(f"[yellow]{warning} in file: {file}[/yellow]")

    if invalid_files:
        console.print("[bold red]Frontmatter Validation Failed![/bold red]")
        for file, error in invalid_files:
            console.print(f"  - {file}: {error}")
    else:
        console.print("[bold green]All Markdown files have valid YAML frontmatter compliant with the schema![/bold green]")

if __name__ == '__main__':
    validate_frontmatter()
