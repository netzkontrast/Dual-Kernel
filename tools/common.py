from datetime import datetime
from typing import Optional, List, Dict
from enum import Enum
from pydantic import BaseModel, Field
import json
import os

class DomainEnum(str, Enum):
    CHARACTER = "character"
    ALTER_SYSTEM = "alter-system"
    WORLD = "world"
    PHYSICS = "physics"
    AEGIS = "aegis"
    NARRATIVE = "narrative"
    STYLE = "style"
    PHILOSOPHY = "philosophy"
    THEME = "theme"
    MECHANIC = "mechanic"
    JUNA = "juna"
    FUNDAMENT = "fundament"
    MATHEMATICS = "mathematics"

class ScannedFile(BaseModel):
    file_id: str = Field(..., description="Dateiname")
    filepath: str = Field(..., description="Relativer Pfad")
    line_count: int = 0

class Entity(BaseModel):
    name: str = Field(..., description="Primary Key")
    is_known: bool = Field(default=False)
    estimated_domain: Optional[DomainEnum] = None
    total_mentions: int = 0

class Mention(BaseModel):
    mention_id: str = Field(...)
    entity_name: str = Field(...)
    file_id: str = Field(...)
    line_number: int = Field(..., ge=1)
    context_text: str = Field(...)
    is_bold: bool = Field(default=False)

class FileMentionsExport(BaseModel):
    mention_count: int
    mentions: List[Dict[str, str | int]]

class EntityExport(BaseModel):
    total_mentions: int
    estimated_domain: Optional[DomainEnum]
    files: Dict[str, FileMentionsExport]

class SourceInventoryExport(BaseModel):
    scan_date: datetime = Field(default_factory=datetime.utcnow)
    files_scanned: int
    unique_entities_found: int
    total_mentions: int
    entity_details: Dict[str, EntityExport]

def load_known_entities() -> List[str]:
    """Liest die bekannten Entitäten aus known_entities.txt."""
    entities = []
    filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "known_entities.txt")
    if not os.path.exists(filepath):
        return entities
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                entities.append(line)
    return entities

def _load_domain_keywords() -> Dict[str, List[str]]:
    """Läd die Domain-Keywords aus config/domain_keywords.json."""
    filepath = os.path.join(os.path.dirname(__file__), "config", "domain_keywords.json")
    if not os.path.exists(filepath):
        return {}
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def guess_domain(all_contexts: str) -> Optional[DomainEnum]:
    """
    Bestimmt die Domäne basierend auf Keyword-Häufigkeiten über alle Kontexte hinweg.
    min_score = 2 (Cutoff).
    """
    keywords_map = _load_domain_keywords()
    if not keywords_map:
        return None

    scores = {domain: 0 for domain in keywords_map}
    text = all_contexts.lower()

    for domain, keywords in keywords_map.items():
        for keyword in keywords:
            # Einfaches zählen des Keywords im Gesamttext
            scores[domain] += text.count(keyword.lower())

    # Domäne mit höchstem Score finden
    best_domain = max(scores, key=scores.get)
    best_score = scores[best_domain]

    if best_score >= 2:
        try:
            return DomainEnum(best_domain)
        except ValueError:
            return None
    return None

