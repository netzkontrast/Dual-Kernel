import glob
import yaml
from common import console, VALID_DOMAINS, VALID_CANON_STATUSES, KG_DIR


def validate_frontmatter():
    files = glob.glob(f'{KG_DIR}/**/*.md', recursive=True)
    files = [f for f in files if not f.endswith('README.md')]

    invalid_files = []

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

        required_keys = ['title', 'id', 'domain', 'canon_status', 'sources']
        for key in required_keys:
            if key not in data:
                invalid_files.append((file, f"Missing required key: {key}"))

        if data.get('domain') not in VALID_DOMAINS:
            invalid_files.append((file, f"Invalid domain: {data.get('domain')}"))

        if data.get('canon_status') not in VALID_CANON_STATUSES:
            invalid_files.append((file, f"Invalid canon_status: {data.get('canon_status')}"))

    if invalid_files:
        console.print("[bold red]Frontmatter Validation Failed![/bold red]")
        for file, error in invalid_files:
            console.print(f"  - {file}: {error}")
    else:
        console.print("[bold green]All Markdown files have valid YAML frontmatter compliant with the schema![/bold green]")

if __name__ == '__main__':
    validate_frontmatter()
