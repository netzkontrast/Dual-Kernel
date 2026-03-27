"""
ingest_worker.py -- Per-process worker agent for parallel document ingestion.

Each worker process loads the spaCy model once (via initializer) and then
processes an assigned batch of markdown files, returning serializable results
that the orchestrator (parallel_ingestion.py) merges into a unified inventory.
"""

import os
import sys
from bisect import bisect_right
from collections import defaultdict
from typing import Any

# Ensure tools/ is on the path for both fork and spawn start methods
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common import KNOWN_ENTITIES, KNOWN_ENTITIES_REGEX, guess_domain

# Module-level spaCy handle; populated by _worker_init() in the worker process
_nlp = None


def _worker_init() -> None:
    """
    Initializer for ProcessPoolExecutor workers.
    Loads the spaCy model once per worker process so every task in that
    process reuses the same in-memory model instead of reloading it.
    """
    import spacy

    global _nlp
    _nlp = spacy.load(
        "de_core_news_lg",
        disable=["parser", "lemmatizer", "tagger", "attribute_ruler"],
    )


def _get_context(lines: list[str], index: int, context_size: int = 2) -> str:
    start = max(0, index - context_size)
    end = min(len(lines), index + context_size + 1)
    return "\n".join(lines[start:end])


def _build_mention(
    entity_name: str,
    file_id: str,
    line_number: int,
    context: str,
    seq: int,
) -> dict[str, Any]:
    return {
        "mention_id": f"{entity_name}_{line_number}_{seq}",
        "entity_name": entity_name,
        "file_id": file_id,
        "line_number": line_number,
        "context_text": context,
        "is_bold": False,
    }


def scan_file(filepath: str) -> dict[str, Any]:
    """
    Scan a single markdown file for entity mentions.

    Returns a dict::

        {
          "file_id": str,
          "entities": {
              entity_name: {
                  "is_known": bool,
                  "domain": str,          # DomainEnum.value
                  "mentions": [mention, ...]
              }
          }
        }
    """
    if _nlp is None:
        # Fallback: lazy-load when called outside a worker pool (e.g. tests)
        _worker_init()

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")
    file_id = os.path.basename(filepath)
    entities: dict[str, Any] = defaultdict(
        lambda: {"is_known": False, "domain": None, "mentions": []}
    )

    # ── Pass 1: regex scan for known entities ─────────────────────────────────
    for i, line in enumerate(lines):
        for match in KNOWN_ENTITIES_REGEX.finditer(line):
            name = match.group(0)
            if entities[name]["domain"] is None:
                domain = guess_domain(name)
                entities[name]["domain"] = domain.value if domain else None
                entities[name]["is_known"] = True
            entities[name]["mentions"].append(
                _build_mention(name, file_id, i + 1, _get_context(lines, i), len(entities[name]["mentions"]))
            )

    # ── Pass 2: spaCy NER for previously unseen names ─────────────────────────
    doc = _nlp(content)

    # Build line-start char-offsets for O(log N) line-number lookup
    line_offsets: list[int] = []
    offset = 0
    for line in lines:
        line_offsets.append(offset)
        offset += len(line) + 1

    for ent in doc.ents:
        if ent.label_ not in ("PER", "LOC", "ORG"):
            continue
        name = ent.text.strip().strip('.,;:!?()[]{}"\'')
        if not name or name in entities or name in KNOWN_ENTITIES:
            continue
        line_idx = bisect_right(line_offsets, ent.start_char) - 1
        domain = guess_domain(name, ent.label_)
        entities[name]["domain"] = domain.value if domain else None
        entities[name]["is_known"] = False
        entities[name]["mentions"].append(
            _build_mention(name, file_id, line_idx + 1, _get_context(lines, line_idx), len(entities[name]["mentions"]))
        )

    return {"file_id": file_id, "entities": dict(entities)}


def process_batch(filepaths: list[str], worker_id: int) -> dict[str, Any]:
    """
    Process a batch of markdown files.

    Called by ``ProcessPoolExecutor`` workers; returns a serializable dict::

        {
          "worker_id":       int,
          "files_processed": int,
          "entities": {
              entity_name: {
                  "is_known": bool,
                  "domain":   str,
                  "files": {
                      file_id: [mention, ...]
                  }
              }
          },
          "errors": [{"file": str, "error": str}, ...]
        }
    """
    merged: dict[str, Any] = {}
    errors: list[dict[str, str]] = []

    for filepath in filepaths:
        try:
            result = scan_file(filepath)
            for name, data in result["entities"].items():
                if not data["mentions"]:
                    continue
                if name not in merged:
                    merged[name] = {
                        "is_known": data["is_known"],
                        "domain": data["domain"],
                        "files": {},
                    }
                file_id = result["file_id"]
                if file_id not in merged[name]["files"]:
                    merged[name]["files"][file_id] = data["mentions"]
                else:
                    # De-duplicate by line number
                    seen = {m["line_number"] for m in merged[name]["files"][file_id]}
                    for m in data["mentions"]:
                        if m["line_number"] not in seen:
                            merged[name]["files"][file_id].append(m)
                            seen.add(m["line_number"])
        except Exception as exc:  # noqa: BLE001
            errors.append({"file": filepath, "error": str(exc)})

    return {
        "worker_id": worker_id,
        "files_processed": len(filepaths),
        "entities": merged,
        "errors": errors,
    }
