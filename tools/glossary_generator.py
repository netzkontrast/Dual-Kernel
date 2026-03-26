"""Build a bilingual (German-English) term glossary from the knowledge graph."""
import os
import re
import glob
import yaml
import click
from collections import defaultdict
from common import console, KG_DIR, KNOWN_ENTITIES_LIST

# Core bilingual term mappings for the Kohärenz Protokoll universe.
# These are manually curated terms that appear across the narrative.
TERM_GLOSSARY = {
    # Physics & Mechanics
    "Riss": "Rift / Tear / Fragmentation",
    "Risse": "Rifts / Tears",
    "Kohärenz": "Coherence",
    "Kohärenz-Kernel": "Coherence Kernel (K₁)",
    "Kollaps-Kernel": "Collapse Kernel (K₀)",
    "Dual-Kernel": "Dual Kernel (DKT core concept)",
    "DKT": "Dual Kernel Theory",
    "Coheron": "Coheron (coherence particle)",
    "Coherons": "Coherons (coherence particles)",
    "Erason": "Erason (erasure particle)",
    "Erasonen": "Erasons (erasure particles)",
    "Persistenzgleichung": "Persistence Equation",
    "Landauer-Prinzip": "Landauer Principle",
    "Unitarität": "Unitarity",
    "Entropie": "Entropy",
    "Negentropie": "Negentropy",
    "Holographisches Prinzip": "Holographic Principle",
    "Bekenstein Bound": "Bekenstein Bound (information limit)",
    "Schwarzschild-Protokoll": "Schwarzschild Protocol",
    "Phase Alignment Lock": "Phase Alignment Lock (PAL)",
    "Qualia": "Qualia (subjective experience)",
    "Vakuum": "Vacuum",
    "Bootstrap": "Bootstrap (self-referencing process)",

    # World & Locations
    "Kernwelt": "Core World",
    "KW1": "Core World 1 (Konstrukt-Stadt)",
    "KW2": "Core World 2 (Mnemosyne's realm)",
    "KW3": "Core World 3",
    "KW4": "Core World 4",
    "Konstrukt-Stadt": "Construct City (KW1 location)",
    "Konstrukt": "Construct",
    "Nexus": "Nexus (central hub)",
    "Archiv": "Archive",
    "Schwelle": "Threshold",
    "Labyrinth": "Labyrinth",
    "Nullpunkt": "Zero Point / Origin",
    "Lethe": "Lethe (river of forgetting)",
    "Void": "Void",
    "Nichts-Rauschen": "Nothingness-Noise / Void Static",
    "Logos-Prime": "Logos Prime",
    "Dead Universe": "Dead Universe",

    # Characters & Systems
    "Kael": "Kael (protagonist, host identity)",
    "Juna": "Juna (external/real connection)",
    "AEGIS": "AEGIS (superintelligence antagonist)",
    "Lex": "Lex (analytical alter/ANP)",
    "Komponente 734": "Component 734",
    "Primal Directive": "Primal Directive (AEGIS core directive)",
    "Integrity Guardian": "Integrity Guardian (AEGIS subsystem)",
    "Genesis-Krise": "Genesis Crisis",
    "Mnemosyne": "Mnemosyne (memory guardian)",
    "Cerberus": "Cerberus (gatekeeper)",
    "Kairos": "Kairos (time guardian)",
    "Sophia": "Sophia (wisdom guardian)",
    "LogOS": "LogOS (logic operating system)",

    # Mechanics & Concepts
    "Riss-Mandat": "Rift Mandate",
    "K-J Verbindung": "K-J Connection (Kael-Juna link)",
    "Computational Class": "Computational Class",
    "Somatic Rulebook": "Somatic Rulebook",
    "Moonshine-Link": "Moonshine Link (mathematical bridge)",
    "Triadische Währung": "Triadic Currency",
    "Ratchet-Prinzip": "Ratchet Principle",
    "Amnestic Barrier": "Amnestic Barrier",
    "Witness Function": "Witness Function",
    "Algorithmische Melancholie": "Algorithmic Melancholy",
    "Wächter-Dilemma": "Guardian Dilemma",

    # Psychology (TSDP/DID)
    "TSDP": "Theory of Structural Dissociation of the Personality",
    "IFS": "Internal Family Systems",
    "ANP": "Apparently Normal Part (functional alter)",
    "EP": "Emotional Part (trauma-holding alter)",
    "DID": "Dissociative Identity Disorder",
    "Funktionale Multiplizität": "Functional Multiplicity",
    "Cache Kohärenz": "Cache Coherence (system metaphor)",
    "Phobische Vermeidung": "Phobic Avoidance",

    # Narrative Theory
    "Dramatica": "Dramatica (narrative theory framework)",
    "Heldinnenreise": "Heroine's Journey",
    "Throughline": "Throughline (narrative thread)",
    "Signpost": "Signpost (narrative milestone)",
    "Story Driver": "Story Driver",
    "Zyklus": "Cycle",
    "Mosaikstruktur": "Mosaic Structure",

    # Philosophy
    "Kohärenztheorie": "Coherence Theory (of truth)",
    "Korrespondenztheorie": "Correspondence Theory (of truth)",
    "Dialetheismus": "Dialetheism (true contradictions)",
    "Parakonsistente Logik": "Paraconsistent Logic",
    "Parakonsistenz": "Paraconsistency",
    "Autopoiesis": "Autopoiesis (self-creation)",
    "Agential Realism": "Agential Realism (Barad)",
    "Agential Cut": "Agential Cut (Barad)",
    "Dasein": "Dasein (being-there, Heidegger)",
    "Existenz": "Existence",
    "Gödel-Unvollständigkeit": "Gödel Incompleteness",
    "Gödel-Gambit": "Gödel Gambit",
    "Living Gödel": "Living Gödel",

    # Mathematics
    "Monstergruppe": "Monster Group",
    "Babymonstergruppe": "Baby Monster Group",
    "Sporadische Gruppen": "Sporadic Groups",
    "Leech-Gitter": "Leech Lattice",
    "Moonshine Conjecture": "Moonshine Conjecture (Conway)",

    # Style
    "Stilebene": "Style Level / Register",
    "Polyphonische Prosa": "Polyphonic Prose",
    "Chorische Stimme": "Choral Voice",
    "Wir-Stimme": "We-Voice (collective narrator)",
    "Staccato": "Staccato (short, sharp style)",
    "Strange Attractor": "Strange Attractor",
    "Fundament": "Foundation / Bedrock",
    "Panopticon": "Panopticon (surveillance concept)",
}


def parse_frontmatter(filepath):
    """Extract YAML frontmatter from a markdown file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if not content.startswith('---'):
        return None
    end_idx = content.find('---', 3)
    if end_idx == -1:
        return None
    try:
        return yaml.safe_load(content[3:end_idx])
    except yaml.YAMLError:
        return None


def discover_terms_from_kg():
    """Discover additional terms from knowledge graph entity files."""
    discovered = {}
    files = glob.glob(f'{KG_DIR}/**/*.md', recursive=True)
    for f in files:
        if f.endswith('README.md'):
            continue
        data = parse_frontmatter(f)
        if data and 'title' in data:
            title = data['title']
            domain = data.get('domain', 'fundament')
            if title not in TERM_GLOSSARY:
                discovered[title] = f"[{domain}] (auto-discovered from knowledge graph)"
    return discovered


def categorize_terms(terms):
    """Group terms by thematic category."""
    categories = defaultdict(list)

    category_keywords = {
        "Physics & Mechanics": ["kernel", "kohärenz", "kollaps", "dual", "dkt", "coheron",
                                "erason", "persistenz", "landauer", "unitarität", "entropie",
                                "negentropie", "holograph", "bekenstein", "schwarzschild",
                                "phase", "qualia", "vakuum", "bootstrap", "pal"],
        "World & Locations": ["kernwelt", "kw1", "kw2", "kw3", "kw4", "konstrukt", "nexus",
                              "archiv", "schwelle", "labyrinth", "nullpunkt", "lethe", "void",
                              "nichts", "logos-prime", "dead universe", "stadt"],
        "Characters & Systems": ["kael", "juna", "aegis", "lex", "komponente", "primal",
                                 "integrity", "genesis", "mnemosyne", "cerberus", "kairos",
                                 "sophia", "logos", "guardian"],
        "Mechanics & Concepts": ["riss", "verbindung", "computational", "somatic", "moonshine",
                                 "triadisch", "ratchet", "amnestic", "witness", "algorithmi",
                                 "wächter", "währung", "mandat"],
        "Psychology": ["tsdp", "ifs", "anp", "ep", "did", "multiplizität", "cache",
                       "phobisch", "dissoziativ"],
        "Narrative Theory": ["dramatica", "heldinnenreise", "throughline", "signpost",
                             "driver", "zyklus", "mosaik", "optionlock"],
        "Philosophy": ["kohärenztheorie", "korrespondenz", "dialetheismus", "parakonsist",
                       "autopoiesis", "agential", "dasein", "existenz", "gödel"],
        "Mathematics": ["monster", "baby", "sporadisch", "leech", "moonshine", "conway",
                        "golay", "gruppen"],
        "Style": ["stilebene", "polyphon", "chorisch", "wir-stimme", "staccato",
                  "strange attractor", "fundament", "panopticon"],
    }

    for term, translation in sorted(terms.items()):
        term_lower = term.lower()
        placed = False
        for cat, keywords in category_keywords.items():
            if any(kw in term_lower for kw in keywords):
                categories[cat].append((term, translation))
                placed = True
                break
        if not placed:
            categories["Other"].append((term, translation))

    return categories


@click.command()
@click.option('--output', '-o', default=None,
              help='Output file path (default: knowledge-graph/_index/glossary.md)')
@click.option('--discover', is_flag=True,
              help='Include auto-discovered terms from knowledge graph')
def glossary(output, discover):
    """Generate a bilingual German-English glossary of key terms."""
    terms = dict(TERM_GLOSSARY)

    if discover:
        discovered = discover_terms_from_kg()
        console.print(f"[cyan]Discovered {len(discovered)} additional terms from knowledge graph[/cyan]")
        terms.update(discovered)

    categories = categorize_terms(terms)

    # Build glossary markdown
    lines = ["# Glossar / Glossary"]
    lines.append("")
    lines.append("Zweisprachiges Glossar der Schlüsselbegriffe des Kohärenz Protokolls.")
    lines.append("Bilingual glossary of key terms from the Coherence Protocol universe.")
    lines.append("")
    lines.append(f"**Einträge / Entries:** {len(terms)}")
    lines.append("")

    # Quick reference table (all terms alphabetically)
    lines.append("## Schnellreferenz / Quick Reference")
    lines.append("")
    lines.append("| Deutsch | English |")
    lines.append("|---------|---------|")
    for term in sorted(terms.keys(), key=str.lower):
        translation = terms[term]
        lines.append(f"| {term} | {translation} |")

    # Categorized sections
    lines.append("")
    lines.append("---")
    lines.append("")

    category_order = [
        "Physics & Mechanics", "World & Locations", "Characters & Systems",
        "Mechanics & Concepts", "Psychology", "Narrative Theory",
        "Philosophy", "Mathematics", "Style", "Other"
    ]

    for cat in category_order:
        if cat not in categories:
            continue
        cat_terms = categories[cat]
        lines.append(f"## {cat}")
        lines.append("")
        for term, translation in sorted(cat_terms, key=lambda x: x[0].lower()):
            lines.append(f"- **{term}** — {translation}")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("_Automatisch generiert von `glossary_generator.py`._")

    content = "\n".join(lines) + "\n"

    # Write output
    if output is None:
        index_dir = os.path.join(KG_DIR, '_index')
        os.makedirs(index_dir, exist_ok=True)
        output = os.path.join(index_dir, 'glossary.md')

    os.makedirs(os.path.dirname(output), exist_ok=True)
    with open(output, 'w', encoding='utf-8') as f:
        f.write(content)

    console.print(f"[bold green]Generated glossary:[/bold green] {output}")
    console.print(f"  Terms: {len(terms)} | Categories: {len(categories)}")


if __name__ == '__main__':
    glossary()
