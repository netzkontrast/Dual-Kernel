# Kohärenz Protokoll - Knowledge-Graph ETL-Pipeline

Dieses Repository enthält die Codebasis und Dokumentation für das **Kohärenz Protokoll** – ein interdisziplinäres narratives Projekt, das tiefgreifende philosophische Konzepte (Identität, Realität, Systemtheorie) und harte Science-Fiction (Quantenphysik, Topologie) verbindet.

Der Fokus dieses Repositories liegt auf der **Knowledge-Graph ETL-Pipeline**, die narrative Elemente, Weltbeschreibungen und Charaktere aus den Markdown-Designdokumenten extrahiert, vernetzt und als strukturierten Graphen bereitstellt.

---

## 🚀 Die ETL-Pipeline (`tools/`)

Die Custom-Skripte im Verzeichnis `tools/` fungieren als automatisierte Pipeline, um Rohtexte in einen strukturierten, maschinenlesbaren Wissensgraphen zu überführen.

**Hauptfunktionen:**
*   **Entitätsextraktion:** Nutzt Natural Language Processing (`spaCy` mit dem Modell `de_core_news_lg`) zur Identifikation von Schlüsselelementen (Charaktere, AEGIS-Protokolle, physikalische Konzepte etc.).
*   **Strikte Validierung:** Verwendet Pydantic v2 zur Durchsetzung relationaler Datenmodelle und zur Validierung von YAML Frontmatter in den generierten Dateien.
*   **Konfliktdokumentation:** Die Pipeline löst narrative Konflikte (z.B. abweichende Altersangaben oder Zustände eines Charakters) **nicht** automatisch auf. Stattdessen werden alle Varianten gleichberechtigt mit spezifischen Kanon-Status (z.B. `disputed`, `uncertain`) in den Metadaten dokumentiert.

### Voraussetzungen & Setup

Das Projekt erfordert Python >= 3.10. Alle Abhängigkeiten (inklusive `spaCy`, `pyyaml`, `rich`, `click` und `pydantic>=2.0`) werden über ein automatisiertes Skript verwaltet.

So richten Sie die Umgebung ein:

```bash
# 1. Ausführen des Setup-Skripts (erstellt die .venv und lädt das spaCy-Modell)
bash setup.sh

# 2. Aktivieren der virtuellen Umgebung
source .venv/bin/activate
```

### Ausführen der Pipeline

Um die Python-Tools auszuführen, stellen Sie sicher, dass die virtuelle Umgebung aktiviert ist und der Python-Pfad auf das `tools/`-Verzeichnis zeigt:

```bash
# Beispiel: Ausführen des Source-Scanners
PYTHONPATH=./tools .venv/bin/python tools/source_scanner.py

# Beispiel: Ausführen des Entity-Generators
PYTHONPATH=./tools .venv/bin/python tools/entity_generator.py
```

---

## 📂 Generierte Inhalte (`knowledge-graph/`)

Die Ergebnisse der Pipeline werden im Verzeichnis `knowledge-graph/` als strukturierte Markdown-Dateien mit YAML Frontmatter gespeichert.

### Beispiel: Generierte Entitätsdatei

Wenn die Pipeline einen Konflikt im Rohtext erkennt (z.B. abweichende Beschreibungen des Charakters "Kael"), generiert sie eine Datei (wie `knowledge-graph/character/kael.md`) mit folgender Struktur:

```yaml
---
title: "Kael"
id: "kael"
domain: "character"
canon_status: "disputed"
aliases: []
tags: []
related:
  - "[[Riss-Mandat]]"
  - "[[Kohärenz-Kernel]]"
  - "[[AEGIS]]"
sources:
  - file: "test-kael-konflikt.md"
    lines: "3-16"
    relevance: "primary"
conflicts:
  - id: "state-conflict"
    description: "Unterschiedliche Zustände für Kael"
    variants:
      - claim: "stark"
        source: "test-kael-konflikt.md:~3"
      - claim: "geschwächt"
        source: "test-kael-konflikt.md:~12"
---

# Kael

_Automatisch generierter Eintrag aus der Test-Pipeline._
```

Wie im Beispiel zu sehen, wird der `canon_status` auf `disputed` gesetzt und die exakten Quellen des Konflikts im Array `conflicts` festgehalten.

---

## 🔗 Übersicht der Entitäten (Domains)

Die extrahierten Daten werden nach Domänen (`Domains`) kategorisiert. Hier gelangen Sie zu den Übersichten der generierten Knotenpunkte:

*   **[Charaktere (Character)](knowledge-graph/character/)** - Protagonisten, Fragmente und Persönlichkeiten (z.B. Kael, Lex, Juna).
*   **[AEGIS (Aegis)](knowledge-graph/aegis/)** - Protokolle, Entitäten und Wächter (z.B. Integrity Guardian, Primal Directive).
*   **[Physik & Konzepte (Physics)](knowledge-graph/physics/)** - Hard Sci-Fi Elemente (z.B. Kohärenz-Kernel, Holographisches Prinzip).
*   **[Welt & Orte (World)](knowledge-graph/world/)** - Zonen und Konstrukte (z.B. Konstrukt-Stadt, Nexus).
*   **[Mechaniken (Mechanic)](knowledge-graph/mechanic/)** - Interaktionsgesetze und Phänomene (z.B. Riss-Mandat).
*   **[Fundament & Narrativ (Fundament / Narrative)](knowledge-graph/fundament/)** - Abstrakte oder storytreibende Konzepte.

_Zusätzliche Reports (wie Extraktions-Zusammenfassungen) finden sich im [`_index/`](knowledge-graph/_index/) Verzeichnis._
