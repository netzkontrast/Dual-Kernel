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

KNOWN_ENTITIES = [
    "Kael", "Michael", "Michaels", "Lex", "Alex", "Rhys", "Selene", "Nyx", "Kiko", "Lia",
    "Isabelle", "Moros", "Argus", "Nox", "Echo", "Limina", "Praetor", "Nova", "Silas",
    "Oblivion", "Flicker", "Eos", "Elara", "Sentinel", "Juna", "Komponente 734", "AEGIS",
    "Primal Directive", "Genesis-Krise", "Algorithmische Melancholie", "LogOS", "Mnemosyne",
    "Cerberus", "Kairos", "Sophia", "Guardian", "ZTEM", "RTSV", "BPoF", "EIC",
    "Integrity Guardian", "Cognitive Firewall", "Consensus Enforcer", "SIS",
    "Entropic Management", "RIVE", "PMAS", "SARM", "RCV", "SVI", "AFP", "PKP", "OSR",
    "CFT", "PMC", "FDE", "CAS", "ECQ", "VOA", "BFT", "PSE", "DKT", "Dual-Kernel",
    "Dual Kernel", "Kohärenz-Kernel", "Kollaps-Kernel", "K₁", "K₀", "K1", "K0", "Coheron",
    "Coherons", "Erason", "Erasonen", "Persistenzgleichung", "Landauer", "Landauer-Prinzip",
    "Gödel", "Gödel-Unvollständigkeit", "Gödel-Satz", "Gödel-Gambit", "Living Gödel",
    "Bekenstein", "Bekenstein Bound", "Schwarzschild", "Schwarzschild-Protokoll",
    "Unitarität", "Entropie", "Qualia", "Negentropie", "Phase Alignment Lock", "PAL",
    "Holographisches Prinzip", "Dead Universe", "Dead Universe Theory", "Vakuum", "Bootstrap",
    "Kernwelt", "KW1", "KW2", "KW3", "KW4", "Logos-Prime", "Konstrukt", "Konstrukt-Stadt",
    "Co₁", "Co1", "McL", "Babymonster", "Baby-Monster", "Lyons", "Theta-9", "Nexus",
    "Archiv", "Schwelle", "Labyrinth", "Nullpunkt", "Lethe", "Void", "Nichts-Rauschen",
    "Riss-Mandat", "Computational Class", "Somatic Rulebook", "Moonshine-Link", "Moonshine",
    "Triadische Währung", "Ratchet-Prinzip", "Amnestic Barrier", "Witness Function",
    "K-J Verbindung", "K-J", "Riss", "Risse", "TSDP", "IFS", "ANP", "EP", "DID",
    "Funktionale Multiplizität", "Cache Kohärenz", "Phobische Vermeidung", "Dramatica",
    "Heldinnenreise", "Throughline", "Signpost", "Story Driver", "Optionlock", "MC Resolve",
    "Zyklus", "Mosaikstruktur", "NCP", "Kohärenztheorie", "Korrespondenztheorie",
    "Dialetheismus", "Parakonsistente Logik", "Parakonsistenz", "Autopoiesis",
    "Agential Realism", "Agential Cut", "Dasein", "Existenz", "Monstergruppe",
    "Babymonstergruppe", "Sporadische Gruppen", "Conway", "Leech", "Leech-Gitter", "Golay",
    "Moonshine Conjecture", "Stilebene", "Polyphonische Prosa", "polyphon", "Chorische Stimme",
    "chorisch", "We-Voice", "Wir-Stimme", "Staccato", "Fundament", "Strange Attractor",
    "Gardener", "Gardeners Axiom", "Wächter-Dilemma", "Panopticon"
]

DOMAIN_MAPPING = {
    "Kael": DomainEnum.CHARACTER,
    "Lex": DomainEnum.CHARACTER,
    "Juna": DomainEnum.CHARACTER,
    "Dr. Xylophon": DomainEnum.CHARACTER,
    "AEGIS": DomainEnum.AEGIS,
    "Integrity Guardian": DomainEnum.AEGIS,
    "Kohärenz-Kernel": DomainEnum.PHYSICS,
    "Holographisches Prinzip": DomainEnum.PHYSICS,
    "Riss-Mandat": DomainEnum.MECHANIC,
    "K-J Verbindung": DomainEnum.MECHANIC,
    "Genesis-Krise": DomainEnum.NARRATIVE,
    "Primal Directive": DomainEnum.AEGIS,
    "Konstrukt-Stadt": DomainEnum.WORLD,
    "Nexus": DomainEnum.WORLD,
    "Komponente 734": DomainEnum.CHARACTER,
    "Alters": DomainEnum.ALTER_SYSTEM
}

def guess_domain(entity_name: str, spacy_tag: Optional[str] = None) -> DomainEnum:
    if entity_name in DOMAIN_MAPPING:
        return DOMAIN_MAPPING[entity_name]

    if spacy_tag == "PER":
        return DomainEnum.CHARACTER
    elif spacy_tag == "LOC":
        return DomainEnum.WORLD
    elif spacy_tag == "ORG":
        return DomainEnum.AEGIS

    return DomainEnum.FUNDAMENT
