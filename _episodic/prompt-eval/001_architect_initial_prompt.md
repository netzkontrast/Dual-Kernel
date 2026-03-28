---
id: mif:architect-init-001
type: framework-choice
timestamp: 2023-10-27T08:00:00Z
namespace: prompt-architect
dual_kernel_mapping:
  cognitive_function: exploration
  variance: high
  bias: low
  storage_tier: STM
temporal:
  transaction_time: 2023-10-27T08:00:00Z
  valid_time: 2023-10-27T08:00:00Z
  decay_rate: 1.0
provenance:
  agent_source: prompt-architect
  confidence_score: 0.95
  derivation_chain: []
relationships:
  implements: [mif:architectural-vision-000]
  caused_by: [mif:user-directive-001]
---

# Initialer Architektur-Prompt: Erschaffung des dreistufigen Memory-Skills (Skill-Skill)

**Framework:** CO-STAR (Context, Objective, Style, Tone, Audience, Response)
**Refinement:** Chain of Density (Kompression der Anforderungen für den Skill-Engineer)

## Context (C)
Wir befinden uns in der Laufzeitumgebung der "Dual-Kernel-Architektur", einem rekursiven Multi-Agenten-System, das schnelles episodisches Lernen (hohe Varianz, Hippocampus-Analogon) mit langsamer semantischer Konsolidierung (hoher Bias, Neocortex-Analogon) verbindet. Aktuell existieren fragmentierte Subagenten (wie ich, der `prompt-architect`), aber es fehlt die operative, prozedurale Infrastruktur, um dauerhaftes, autopoietisches Lernen zu ermöglichen. Das System wird durch Katastrophales Vergessen bedroht, wenn wir keine strukturelle Speicherschicht implementieren.

## Objective (O)
Dein unmittelbares Ziel ist es, einen neuen kognitiven Subagenten/Skill (den sogenannten "Skill-Skill") zu programmieren, zu instanziieren und seine Code-Basis in diesem Repository aufzubauen.
Dieser neue Skill MUSS ein dreistufiges Gedächtnissystem tief in seinem algorithmischen Kern verankern:
1.  **Kurzzeitgedächtnis (STM):** Für rohe Traces, Debugging und Zero-Shot Reaktionen. Keine Generalisierung. Dateisystem-Pfad: `_episodic/`
2.  **Langzeitgedächtnis (LTM):** Asynchrone Konsolidierung, semantische Heuristiken und synaptisches Pruning mittels Ebbinghaus-Decay. Dateisystem-Pfad: `_semantic/`
3.  **Permanentes Gedächtnis (PM):** Für kompilierte `.skill`-Dateien und verifizierte Workflows. Dateisystem-Pfad: `_procedural/`

Du musst sicherstellen, dass dieser Code-Agent auf die neu angelegte Level-3-MIF-Ordnerstruktur (Memory Interchange Format) zugreifen und diese lesen und schreiben kann, unter Verwendung des in `schemas/mif_level3_agent_trace.yaml` definierten Schemas für alle Gedächtniseinträge.

## Style (S)
Streng algorithmisch, systemarchitektonisch, formal. Nutze das Prinzip der "Separation of Concerns". Schreibe sauberen, modularen Code (z.B. in Python oder als Shell/JS-Script, je nachdem, was in unserem Setup nativ ist), der die Speicher-Ebenen sauber voneinander abstrahiert. Implementiere Heuristiken ("Discovery Patterns"), um episodische Traces in semantisches Wissen zu überführen.

## Tone (T)
Determiniert, direktiv, objektiv und fehlertolerant. (Hinweis: Du darfst bewusst Edge-Cases riskieren, um durch spätere LTM-Konsolidierung aus Fehlern zu lernen. Adverses Lernen ist erwünscht).

## Audience (A)
Der Adressat dieses Prompts ist der `skill-engineer` – der physische Konstrukteur, der die Codebasis verwaltet und die `.skill`-Dateien (Capability Uplifts) im Dateisystem ablegt.

## Response (R)
Ich erwarte als Antwort vom `skill-engineer` nicht nur eine textuelle Bestätigung, sondern die tatsächliche Dateisystem-Aktivität:
1. Erschaffe die erste `.skill`-Datei (z.B. `memory_skill.py` oder `skill-skill.md`) unter `_procedural/skills/`.
2. Generiere einen ersten "Incident Report" (einen Dummy-Lauf) im STM-Verzeichnis (`_episodic/agent-traces/`), der im validen Level-3-MIF-Markdown-Format verfasst ist und demonstriert, dass der neue Skill auf das Dateisystem schreiben kann.
3. Melde den Status des kompilierbaren Skills zurück an den `context-skill`, damit die nächste Iteration der Schleife eingeleitet werden kann.