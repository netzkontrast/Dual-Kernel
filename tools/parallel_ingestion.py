"""
parallel_ingestion.py -- Parallel document ingestion orchestrator.

Discovers all markdown files in Markdown-docs/, splits them into equal batches,
and dispatches one worker agent per batch using ProcessPoolExecutor.  Each worker
runs in its own OS process with a dedicated spaCy model instance, so the scan
scales linearly with CPU cores.

Usage examples
--------------
# Scan all 94 docs with 4 workers (default)
python tools/parallel_ingestion.py

# Use 8 workers on a beefier machine
python tools/parallel_ingestion.py --workers 8

# Only ingest a specific sub-set of files
python tools/parallel_ingestion.py --docs-dir Markdown-docs --pattern "Aegis*.md"

# Write to a custom path instead of tools/output/source-inventory.json
python tools/parallel_ingestion.py --output tools/output/my-inventory.json
"""

import math
import os
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from glob import glob
from typing import Any

import click
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.table import Table

# Ensure tools/ is importable both when run as a script and when spawned
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common import (
    DomainEnum,
    EntityExport,
    FileMentionsExport,
    INVENTORY_PATH,
    SourceInventoryExport,
    console,
    ensure_output_dir,
)
from ingest_worker import _worker_init, process_batch


# ── Helpers ───────────────────────────────────────────────────────────────────


def _split_batches(files: list[str], n: int) -> list[list[str]]:
    """Divide *files* into *n* roughly equal batches."""
    size = math.ceil(len(files) / n)
    return [files[i : i + size] for i in range(0, len(files), size)]


def _merge_worker_results(results: list[dict[str, Any]]) -> dict[str, Any]:
    """Combine per-worker entity dicts into one unified structure.

    The same entity name can appear across workers (it may be mentioned in
    files owned by different workers), but each file_id is owned by exactly
    one worker, so file-level mentions never collide.
    """
    merged: dict[str, Any] = {}
    all_errors: list[dict[str, str]] = []

    for r in results:
        all_errors.extend(r.get("errors", []))
        for name, data in r["entities"].items():
            if name not in merged:
                merged[name] = {
                    "is_known": data["is_known"],
                    "domain": data["domain"],
                    "files": {},
                }
            for file_id, mentions in data["files"].items():
                merged[name]["files"][file_id] = mentions

    return {"entities": merged, "errors": all_errors}


def _build_export(merged: dict[str, Any], files_scanned: int) -> SourceInventoryExport:
    """Convert the merged dict into a validated ``SourceInventoryExport`` model."""
    entity_details: dict[str, EntityExport] = {}

    for name, data in merged["entities"].items():
        if not data.get("files"):
            continue

        files_export: dict[str, FileMentionsExport] = {}
        total_mentions = 0

        for file_id, mentions in data["files"].items():
            mention_dicts = [
                {"line": m["line_number"], "context": m["context_text"]}
                for m in mentions
            ]
            files_export[file_id] = FileMentionsExport(
                mention_count=len(mention_dicts),
                mentions=mention_dicts,
            )
            total_mentions += len(mention_dicts)

        # Normalise domain: workers return the string value
        raw_domain = data.get("domain")
        try:
            domain = DomainEnum(raw_domain) if raw_domain else DomainEnum.FUNDAMENT
        except ValueError:
            domain = DomainEnum.FUNDAMENT

        entity_details[name] = EntityExport(
            total_mentions=total_mentions,
            estimated_domain=domain,
            files=files_export,
        )

    return SourceInventoryExport(
        files_scanned=files_scanned,
        unique_entities_found=len(entity_details),
        total_mentions=sum(e.total_mentions for e in entity_details.values()),
        entity_details=entity_details,
    )


# ── CLI entry point ────────────────────────────────────────────────────────────


@click.command()
@click.option(
    "--docs-dir",
    default="Markdown-docs",
    show_default=True,
    type=click.Path(exists=True),
    help="Directory containing the markdown source documents.",
)
@click.option(
    "--workers",
    default=4,
    show_default=True,
    type=click.IntRange(1, 32),
    help="Number of parallel worker agents (OS processes).",
)
@click.option(
    "--output",
    default=None,
    help="Output path for the inventory JSON.  Defaults to tools/output/source-inventory.json.",
)
@click.option(
    "--pattern",
    default="*.md",
    show_default=True,
    help="Glob pattern applied inside --docs-dir to select files.",
)
def ingest(docs_dir: str, workers: int, output: str | None, pattern: str) -> None:
    """
    Run parallel document ingestion across all markdown source files.

    Spawns WORKERS independent agent processes.  Each agent loads the German
    spaCy model (de_core_news_lg) once and scans its assigned file batch for
    entity mentions using both regex (known entities) and NER (new names).
    Results are merged and written as a JSON inventory compatible with the
    rest of the ETL pipeline.
    """
    output_path = output or INVENTORY_PATH

    # ── Discover files ─────────────────────────────────────────────────────────
    files = sorted(glob(os.path.join(docs_dir, pattern)))
    if not files:
        console.print(f"[red]No files matched '{pattern}' in '{docs_dir}'.[/red]")
        raise SystemExit(1)

    num_workers = min(workers, len(files))
    batches = _split_batches(files, num_workers)

    console.print("[bold blue]Parallel Document Ingestion[/bold blue]")
    console.print(f"  Source directory : [cyan]{docs_dir}[/cyan]")
    console.print(f"  Documents found  : [cyan]{len(files)}[/cyan]")
    console.print(f"  Worker agents    : [cyan]{num_workers}[/cyan]")
    console.print(f"  Files per agent  : [cyan]~{math.ceil(len(files) / num_workers)}[/cyan]")
    console.print()

    # ── Dispatch workers ───────────────────────────────────────────────────────
    worker_results: list[dict[str, Any]] = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task_id = progress.add_task("Ingesting documents...", total=num_workers)

        with ProcessPoolExecutor(
            max_workers=num_workers,
            initializer=_worker_init,   # load spaCy once per worker process
        ) as pool:
            future_map = {
                pool.submit(process_batch, batch, wid): wid
                for wid, batch in enumerate(batches)
            }

            for future in as_completed(future_map):
                wid = future_map[future]
                try:
                    result = future.result()
                    worker_results.append(result)
                    console.print(
                        f"  [green]✓[/green] Worker {wid} — "
                        f"{result['files_processed']} files, "
                        f"{len(result['entities'])} entities"
                    )
                except Exception as exc:  # noqa: BLE001
                    console.print(f"  [red]✗[/red] Worker {wid} failed: {exc}")
                finally:
                    progress.advance(task_id)

    # ── Merge & export ─────────────────────────────────────────────────────────
    console.print()
    console.print("[bold blue]Merging results from all agents...[/bold blue]")

    merged = _merge_worker_results(worker_results)

    if merged["errors"]:
        console.print(f"[yellow]⚠ {len(merged['errors'])} file(s) produced errors:[/yellow]")
        for err in merged["errors"][:10]:
            console.print(f"  [yellow]- {err['file']}: {err['error']}[/yellow]")

    export = _build_export(merged, len(files))

    ensure_output_dir()
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(export.model_dump_json(indent=2))

    # ── Summary ────────────────────────────────────────────────────────────────
    table = Table(title="Ingestion Summary", show_header=True)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="yellow", justify="right")
    table.add_row("Files scanned", str(export.files_scanned))
    table.add_row("Unique entities found", str(export.unique_entities_found))
    table.add_row("Total mentions", str(export.total_mentions))
    table.add_row("Worker agents used", str(num_workers))
    table.add_row("Output file", output_path)
    console.print(table)
    console.print(f"\n[bold green]✓ Inventory saved to {output_path}[/bold green]")


if __name__ == "__main__":
    ingest()
