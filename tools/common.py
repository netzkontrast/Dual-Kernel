import re
import os
from datetime import datetime
from typing import Optional, List, Dict
from enum import Enum
from pydantic import BaseModel, Field

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

# -- Relationale Modelle (Interner State) --

class ScannedFile(BaseModel):
    file_id: str = Field(..., description="Dateiname (z.B. 'Kapitel1.md')")
    filepath: str = Field(..., description="Relativer Pfad")
    line_count: int = 0

class Entity(BaseModel):
    name: str = Field(..., description="Name der Entität (Primary Key)")
    is_known: bool = Field(default=False)
    estimated_domain: Optional[DomainEnum] = None
    total_mentions: int = 0

class Mention(BaseModel):
    mention_id: str = Field(..., description="Hash aus file_id + line_number + entity_name")
    entity_name: str = Field(..., description="Fremdschlüssel -> Entity.name")
    file_id: str = Field(..., description="Fremdschlüssel -> ScannedFile.file_id")
    line_number: int = Field(..., ge=1)
    context_text: str = Field(..., description="Textausschnitt (±2 Zeilen)")
    is_bold: bool = Field(default=False)

# -- Export Modelle (Für JSON Output) --

class FileMentionsExport(BaseModel):
    mention_count: int
    mentions: List[Dict[str, str | int]] # Liste von {"line": int, "context": str}

class EntityExport(BaseModel):
    total_mentions: int
    estimated_domain: Optional[DomainEnum]
    files: Dict[str, FileMentionsExport] # Key ist file_id

class SourceInventoryExport(BaseModel):
    scan_date: datetime = Field(default_factory=datetime.utcnow)
    files_scanned: int
    unique_entities_found: int
    total_mentions: int
    entity_details: Dict[str, EntityExport]


def load_known_entities(filepath: str = "known_entities.txt") -> List[str]:
    """Lädt bekannte Entitäten aus einer Datei, ignoriert leere Zeilen und Kommentare."""
    entities = []
    if not os.path.exists(filepath):
        # Versuche relativen Pfad vom tools Ordner aus, falls von dort aufgerufen
        alt_filepath = os.path.join(os.path.dirname(__file__), "..", filepath)
        if os.path.exists(alt_filepath):
            filepath = alt_filepath
        else:
            print(f"Warnung: {filepath} nicht gefunden.")
            return []

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                entities.append(line)
    return entities
