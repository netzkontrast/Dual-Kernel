# Entity Relationship Graph

**Generated:** Automatisch generiert aus `knowledge-graph/`

## Statistics

| Metric | Value |
|--------|-------|
| Entities | 15 |
| Relationships | 52 |
| Domains | 7 |
| Conflict Hotspots | 12 |
| Graph Density | 0.495 |

## Hub Entities (Most Connected)

- **Kael** (character): 13 connections ⚠️
- **Riss-Mandat** (mechanic): 11 connections ⚠️
- **Riss** (fundament): 11 connections ⚠️
- **Lex** (character): 11 connections ⚠️
- **K-J Verbindung** (mechanic): 7 connections ⚠️

## Relationship Graph

```mermaid
graph TD
    classDef character fill:#4A90D9,stroke:#333,color:#fff
    classDef alter_system fill:#9B59B6,stroke:#333,color:#fff
    classDef world fill:#27AE60,stroke:#333,color:#fff
    classDef physics fill:#E67E22,stroke:#333,color:#fff
    classDef aegis fill:#E74C3C,stroke:#333,color:#fff
    classDef narrative fill:#F1C40F,stroke:#333,color:#fff
    classDef style fill:#1ABC9C,stroke:#333,color:#fff
    classDef philosophy fill:#8E44AD,stroke:#333,color:#fff
    classDef theme fill:#D35400,stroke:#333,color:#fff
    classDef mechanic fill:#2980B9,stroke:#333,color:#fff
    classDef juna fill:#E91E63,stroke:#333,color:#fff
    classDef fundament fill:#607D8B,stroke:#333,color:#fff
    classDef mathematics fill:#795548,stroke:#333,color:#fff
    classDef conflict stroke:#ff0000,stroke-width:3px,stroke-dasharray: 5 5
    subgraph aegis_group ["AEGIS"]
        AEGIS{{"AEGIS"}}
        Integrity_Guardian{{"Integrity Guardian"}}
        Primal_Directive{{"Primal Directive"}}
        Riss_Mandats{{"Riss-Mandats"}}
    end
    subgraph character_group ["CHARACTER"]
        Juna(["Juna"])
        Kael(["Kael"])
        Komponente_734(["Komponente 734"])
        Lex(["Lex"])
    end
    subgraph fundament_group ["FUNDAMENT"]
        Riss["Riss"]
    end
    subgraph mechanic_group ["MECHANIC"]
        K_J_Verbindung[/"K-J Verbindung"/]
        Riss_Mandat[/"Riss-Mandat"/]
    end
    subgraph narrative_group ["NARRATIVE"]
        Genesis_Krise["Genesis-Krise"]
    end
    subgraph physics_group ["PHYSICS"]
        Koh_renz_Kernel[["Kohärenz-Kernel"]]
    end
    subgraph world_group ["WORLD"]
        Konstrukt_Stadt>"Konstrukt-Stadt"]
        Nexus>"Nexus"]
    end
    Riss_Mandat --- Riss
    Riss_Mandat --- Kael
    Riss_Mandat --- Integrity_Guardian
    Riss_Mandat --- K_J_Verbindung
    Riss_Mandat --- Juna
    Riss_Mandat --- Komponente_734
    Riss_Mandat --- Lex
    K_J_Verbindung --- Riss
    K_J_Verbindung --- Kael
    K_J_Verbindung --- Juna
    K_J_Verbindung --- Komponente_734
    K_J_Verbindung --- Lex
    K_J_Verbindung --- Genesis_Krise
    Nexus --- Riss
    Nexus --- Lex
    Nexus --- Riss_Mandat
    Nexus --- Riss_Mandats
    Konstrukt_Stadt --- Riss_Mandat
    Konstrukt_Stadt --- Riss
    Konstrukt_Stadt --- Kael
    Konstrukt_Stadt --- Riss_Mandats
    Konstrukt_Stadt --- Lex
    Konstrukt_Stadt --- AEGIS
    Genesis_Krise --- Juna
    Genesis_Krise --- Kael
    Genesis_Krise --- Primal_Directive
    Koh_renz_Kernel --- Kael
    Koh_renz_Kernel --- Integrity_Guardian
    Integrity_Guardian --- Riss
    Integrity_Guardian --- Kael
    Integrity_Guardian --- Komponente_734
    Integrity_Guardian --- Lex
    AEGIS --- Riss_Mandat
    AEGIS --- Riss
    AEGIS --- Kael
    AEGIS --- Riss_Mandats
    AEGIS --- Lex
    Riss_Mandats --- Riss_Mandat
    Riss_Mandats --- Riss
    Riss_Mandats --- Kael
    Riss_Mandats --- Lex
    Primal_Directive --- Kael
    Riss --- Kael
    Riss --- Lex
    Juna --- Riss
    Juna --- Kael
    Juna --- Komponente_734
    Juna --- Lex
    Kael --- Komponente_734
    Kael --- Lex
    Komponente_734 --- Riss
    Komponente_734 --- Lex
    class Riss_Mandat,K_J_Verbindung mechanic
    class Nexus,Konstrukt_Stadt world
    class Genesis_Krise narrative
    class Koh_renz_Kernel physics
    class Integrity_Guardian,AEGIS,Riss_Mandats,Primal_Directive aegis
    class Riss fundament
    class Juna,Kael,Komponente_734,Lex character
    class Konstrukt_Stadt,Kael,Komponente_734,K_J_Verbindung,Riss,Riss_Mandats,AEGIS,Juna,Riss_Mandat,Lex,Nexus,Integrity_Guardian conflict
```

## Domain Legend

- **aegis**: 4 entities (#E74C3C)
- **character**: 4 entities (#4A90D9)
- **fundament**: 1 entities (#607D8B)
- **mechanic**: 2 entities (#2980B9)
- **narrative**: 1 entities (#F1C40F)
- **physics**: 1 entities (#E67E22)
- **world**: 2 entities (#27AE60)

_Automatisch generiert von `relationship_graph.py`._
