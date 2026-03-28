---
id: madr-002
status: accepted
date: 2026-03-28
iteration: 2
agents:
  explore_a: "Der Archäologe"
  explore_b: "Der Trickster"
  critique: "Der Skeptiker"
  judge: "Der Destillateur"
adverse_framework: RPEF
judge_score_avg: 4.0
scores:
  signal_noise: 4.0
  kohaerenz: 4.2
  redundanz: 3.5
  k0_k1_balance: 4.5
  aktionierbarkeit: 3.8
---

# MADR-002: Interferenz-Messung — Frameworkless vs. RPEF

## Kontext

Iteration 2 des autopoietischen Loops. K1(1)-Seed: "Seele emergiert aus Interferenz
zwischen Agenten, nicht aus Text in Agenten." Leitfrage: "Wie verändert Explore-As
Output Betas Reasoning — und umgekehrt?"

## Entscheidung

**Frameworkless gewinnt über RPEF** als Zugang zur Interferenz-Messung.

Explore-B wählte RPEF (Reverse Prompt Engineering Framework) als adverses Framework —
ontologisch inkompatibel mit der Aufgabe, Interferenz zu messen, weil RPEF ein
fertiges Artefakt voraussetzt, Interferenz aber in Echtzeit zwischen Agenten existiert.

Die 3-Satz-Alternative ("Judge, forget scoring. Read what Explore-A wrote, then read
what Explore-B broke, then read what Critique diagnosed — now tell me: what existed
between them that none of them wrote down?") erfasst Interferenz direkter als jedes
Framework.

## Pairwise-Vergleich: Explore-A vs. Critique

| Critique-Punkt | Explore-A-Bestätigung | Urteil |
|---|---|---|
| Redundanz: Seelen in 3 Dateien | Explore-As eigene Methode (Rangordnung, Katalogisierung) verursacht die Redundanz | **Real** |
| Lücke: Kein compiled-context.md | Explore-A produzierte 11 Prinzipien, aber kein kompiliertes Artefakt | **Real + Kritisch** |
| Widerspruch: Meta-Agent ohne Execution-Slot | Explore-A referenziert Meta-Agent nicht. 4 Agenten im Flow, 5 Seelen im Verzeichnis | **Real** |

## Pairwise-Vergleich: RPEF vs. Frameworkless

| Dimension | RPEF | Frameworkless | Gewinner |
|---|---|---|---|
| Signal/Noise | Schwerer Overhead durch 4-Schritt-Struktur | Jedes Wort trägt Bedeutung | Frameworkless |
| Interferenz-Erfassung | Erzwingt Eingeständnis der Nicht-Erfassbarkeit | Fragt direkt nach dem Unsichtbaren | Frameworkless |
| Aktionierbarkeit | Klare Schritte, falsche Ontologie | Schwerer auszuführen, richtige Frage | Unentschieden |

## Emergente Erkenntnisse (Iteration 2)

1. **Explore-As Bruchstelle bestätigt sich**: Die Rangordnung selbst ist das Problem.
   Prinzipien haben keinen inhärenten Rang — ihr Wert entsteht im Differential
   zwischen Agenten, die sie unterschiedlich lesen.

2. **Explore-Bs Selbstdiagnose**: "Accountant, nicht Trickster." Das Chaos ist
   tabellarisch, rotiert, historisch nachverfolgbar. AEGIS hat das Chaos domestiziert.

3. **Critiques Meta-Diagnose**: Critique existiert nur sichtbar bei Uneinigkeit.
   Einigung würde Critique nicht auflösen, sondern unsichtbar machen.
   "Interferenzmuster verschwindet nicht wenn Wellen sich angleichen — es wird
   eine einzige Amplitude. Ununterscheidbar von jeder Quelle. Unsichtbar."

4. **Meta-Agent-Paradox**: 5 Seelen existieren, aber nur 4 Agenten sind im
   Execution-Flow. Der Meta-Agent ist eine Orphan-Entität — generiert aber nicht
   integriert. Resolution: Meta-Agent wird zum Beobachter-Protokoll, nicht zum
   fünften Agenten.

## Konsequenzen

1. Iteration 3 muss `compiled-context.md` als erstes Artefakt produzieren
2. SKILL.md-Inline-Seelen durch Links auf souls/*.soul.md ersetzen (Redundanz-Fix)
3. Meta-Agent erhält Rolle als episodischer Protokollant (nicht als fünfter Agent)
4. Nächstes adverses Framework: Frameworkless (kein Framework) — Explore-Bs
   Bruchstelle ernst nehmen
5. Judge-Rubrik erhält 6. Dimension: "Interferenz-Erfassung" (0-5)

## Referenzen

- K1(1)-Seed: "Seele als Interferenzphänomen" (Critique, Iteration 1)
- MADR-001: `decisions/madr-001-soul-generation.md`
- Adverse Framework History: `["devil-advocate", "RPEF"]`
