from common import console, VALID_DOMAINS, VALID_CANON_STATUSES, list_entity_files, parse_frontmatter


def validate_frontmatter():
    files = list_entity_files()

    invalid_files = []

    for file in files:
        data, _ = parse_frontmatter(file)

        if data is None:
            invalid_files.append((file, "No valid frontmatter found"))
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
