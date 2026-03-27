# Extraction Log

Tracks which source files from `Markdown-docs/` have been processed through the ETL pipeline.

**Progress: 3 / 94 files processed**

---

## Processed Files

| # | File | Date | Entities Found | Notes |
|---|------|------|---------------|-------|
| 1 | `KoharenzProtokoll39KapitelMatrix.md` | 2026-03-26 | 15 | Initial extraction |
| 2 | `KaelsDissociativeArchitectureAnalysis.md` | 2026-03-27 | 114 | Kael alter system, TSDP/IFS/ANP, Juna, AEGIS |
| 3 | `DualKernelAiAndNarrativeCollapse.md` | 2026-03-27 | 90 | DKT physics, NCP, Landauer, Dramatica, Throughline |

---

## Remaining Files (91)

```
40ChapterPlotModule.md
AegisAnalyseUndPromptOptimierung.md
AegisEmergenzAusDerLeere.md
AegisGenesisKrise20prosaAuftrag20formulieren.md
AegisPhilosophieUndManifestEntwicklung.md
AegisPhilosophieUndSystemtheorie.md
AegisPhilosophischeUndSystemtheoretischeAnalyse.md
AegisProtokolleKritischeEvaluationNeukonzeption.md
AnIntroductionToTheConceptsOfCoherenceProtocol.md
AngereichertesPlotkonzeptKapitelthemenKoharenzProtokoll.md
Blueprint.md
BridgingNarrativeTheoryAndAiAuthorship.md
CharakterarchitekturFurNarrativesRomanprojekt.md
DialetheismusImKoharenzProtokoll.md
DramaticaTheoryOverviewAndResources.md
DramaturgicalPrecisionDeconstructingTheIrreversibleConflictInKoharenzProtokoll.md
EinleitungGenesisDerExistenz.md
EmergenzAutonomerSystemeAegisForschung.md
ErkenntnistheorieFurNarrativeProjektgestaltung.md
ExistenzKosmosSeinUndBewusstsein.md
ForschungsprojektKoharenzProtokollAnalyse.md
GrenzenDerExistenzEineUmfassendeAnalyse.md
GuardiansUndKernWeltenKonzept.md
HolographischesPrinzipFurKoharenzProtokoll.md
IdentitatGrenzenUndWandel.md
InterdisziplinareRechercheFurKoharenzProtokoll.md
KernweltenFurKoharenzProtokoll.md
KoharenzProtokollKapitelstrukturMitKonzepten39Kapitel.md
KoharenzProtokollKonzept.md
KoharenzProtokollKonzeptionelleAusarbeitung.md
KoharenzProtokollKonzeptionelleThemenStruktur.md
KoharenzProtokollMetaForeshadowingBeobachterLogik.md
KoharenzProtokollPlotBlueprintErstellung.md
KoharenzProtokollPlotEntwicklungUndWahrheitsdualitat.md
KopieVonNarrativeLosungenFurRomanprojekt.md
LogiksystemAegisEntwicklungsszenarien.md
MonstergruppeAlsDenkmodellDerKomplexitat.md
MonstergruppeBabymonstergruppeFragmentierungErzahlung.md
MonstergruppeNarrativeClusterUndMetaphern.md
NarrativExistenziellerKoharenzNztProtokoll.md
NarrativePlotExplorationExistenzielleKoharenz.md
NarrativeRekombinationPotenzialExplorationPlotSynopsen.md
NarrativeVertiefungKoharenzProtokoll.md
OrteKonzeptFurKoharenzProtokoll.md
PVsNpUndKoharenz.md
ParadoxienDerKoharenzProtokollEntwicklung.md
ParakonsistenteLogikFurKoharenzProtokoll.md
ParakonsistenzAegisUndNichtExistenz.md
PhilosophieGrenzenUndZukunft.md
PhysikGrenzenUndRatselDesUniversums.md
PlotBlueprintMethodikKoharenzProtokoll.md
PlotExplorationKoharenzProtokollkonzepte.md
PlotKonzepteKoharenzProtokollGenerierung.md
PlotkonzeptKoharenzProtokollHeldinnenreiseStruktur.md
ProjektKoharenzProtokollTiefenanalyse.md
RomanBlueprintSeelenKoharenzProtokoll.md
RomanEntwicklungKoharenzUndLeitfragen.md
RomanFundamentTheoretischeRecherche.md
RomanKapitelAusformulierungKoharenzProtokoll.md
RomanKoharenzProtokoll.md
RomanKoharenzProtokoll2.md
RomanKonzeptDualitatKoharenzSpannung.md
RomanKonzeptentwicklungKoharenzProtokoll.md
RomanLokalitatenKonzeptUndAusarbeitung.md
RomanRefactoringKoharenzUndCharakterentwicklung.md
RomanSyntheseMitDualKernelTheorie.md
RomanUrvertrauenLiebeTranszendenz.md
RomanWorldbuildingFragmentierteIdentitatMetaRealitat.md
RomanentwurfKoharenzProtokollTeil1.md
Romanstruktur3Teile39Kapitel1Anfang.md
RomanstrukturUndPhilosophischeEinleitung.md
SpannungsfelderUndAegisMetaFrameworkAnalyse.md
StorytellingCommandmentsExplained.md
SymmetrieParadoxieExistenzJenseitsSimulation.md
SymmetrienClusterungUberWissensgebieteHinweg.md
TheCoherenceProtocolADefinitiveGuideToTheNarrativeArchitecture.md
TheCoherenceProtocolANarrativeDesignWorldArchitectureDocument.md
TheFoundationProtocolAMetaphysicalThesisOnTheReAnchoringOfReality.md
TheKoharenzProtokollADefinitiveGuideToNarrativeArchitecture.md
TheThematicArchitectureOfKoharenzProtokollAConceptualLexiconOfCoreDualities.md
TheTrueCoherenceProtocolArchitectingKaelsJourneyFromTsdpFragmentationToFunctionalMultiplicity.md
Top13ForschungsfragenZurRealitat.md
TranszendenzLogischerSystemeEntropie.md
TranszendenzUndParadoxienVerbindungslinien.md
TsdpAnalyseKaelsInnereWelt.md
UmfassendesLokalitatenKonzeptFurRoman.md
VTheFoundationAndKaelsIntegrationArc.md
WahrheitstheorienKoharenzVsKorrespondenz.md
ZeitGrenzenWahrnehmungUndTheorien.md
test-kael-konflikt.md
```

---

## Notes

- `Markdown-docs/README.md` is excluded (navigation index, not a research document).
- Scanner limitation: spaCy NER produces false-positive entities from markdown table fragments (e.g., `|---|---|`). These are deleted after generation and reported as wikilink warnings. Known issue, not a blocker.
- The scanner processes one file at a time and overwrites `source-inventory.json`. For batch runs across many files, use `python tools/parallel_ingestion.py` (merges results).
- When adding a row to this table, also run `python tools/entity_stats.py` to regenerate `knowledge-graph/_index/extraction-report.md`.
