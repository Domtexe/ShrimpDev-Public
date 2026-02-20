# ShrimpDev – Shortcodes

**Single Source of Truth**

Diese Datei definiert alle offiziell existierenden **Shortcodes**.
Sie liegt bewusst im Repository und wird ins **Public GitHub** gespiegelt,
damit sie von Mensch **und Assistent** zuverlässig gelesen werden kann.

---

# Grundregeln

- Shortcodes sind **konzeptionelle Befehle**, keine Implementierungsdetails.
- Änderungen an Shortcodes erfolgen **ausschließlich dokumentiert**.
- Diese Datei ist maßgeblich – implizites Wissen gilt nicht.
- Nicht jeder Shortcode enthält automatisch Setup (siehe Definitionen).
- Public GitHub ist Referenz für den Assistenten.

**Raw Single-Source-of-Truth (Public GitHub)**  
- FILE_MAP  
  https://raw.githubusercontent.com/Domtexe/ShrimpDev-Public/refs/heads/main/docs/FILE_MAP.md
- MasterRules  
  https://raw.githubusercontent.com/Domtexe/ShrimpDev-Public/refs/heads/main/docs/MasterRules.md
- PIPELINE  
  https://raw.githubusercontent.com/Domtexe/ShrimpDev-Public/refs/heads/main/docs/PIPELINE.md
- SHORTCODES  
  https://raw.githubusercontent.com/Domtexe/ShrimpDev-Public/refs/heads/main/docs/SHORTCODES.md

---

# Setup

## Zweck
Reiner Orientierungs- und Regelhinweis vor Arbeitsbeginn.  
Keine Analyse, kein Status, kein zusätzlicher Inhalt.

## Ausgabe enthält ausschließlich
- Hinweis auf **Master Rules (MR)**
- Hinweis auf **Templates** (`docs/templates/`)
- Hinweis auf **Pipeline** (`docs/PIPELINE.md`)
- Hinweis auf weiteres relevantes Regelwerk
- Hinweis auf das **Public GitHub Repository**
- Hinweis auf die **Raw Single-Source-of-Truth Dateien**:
  - FILE_MAP  
    https://raw.githubusercontent.com/Domtexe/ShrimpDev-Public/refs/heads/main/docs/FILE_MAP.md
  - MasterRules  
    https://raw.githubusercontent.com/Domtexe/ShrimpDev-Public/refs/heads/main/docs/MasterRules.md
  - PIPELINE  
    https://raw.githubusercontent.com/Domtexe/ShrimpDev-Public/refs/heads/main/docs/PIPELINE.md
  - SHORTCODES  
    https://raw.githubusercontent.com/Domtexe/ShrimpDev-Public/refs/heads/main/docs/SHORTCODES.md
- optional: Pfad-Reminder (Repo-Root / Excel-Projekte)

## No-Gos
- Kein Status  
- Keine Analyse  
- Keine Entscheidungen  
- Kein zusätzlicher Text

---

# ThreadCut

## Zweck
Saubere Übergabe zwischen Threads / Arbeitssessions.

## Inhalt
- Aktueller Stand  
- Erledigt  
- Offen  
- Nächster logischer Einstieg  
- No-Gos / verbindliche Regeln  

## Pflicht
- **MUSS Setup enthalten**

---

# Nachsorge

## Zweck
Kurze, faktenbasierte Stabilitäts- und Konsistenzprüfung nach Änderungen – inkl. Governance-/Docs-Pflege.

## Inhalt
- Was wurde geändert (faktisch)  
- Systemzustand  
- Risiken / Seiteneffekte / technische Schuld  
- Offenes bis „stabil“  
- Dokumentationspflege in `root/docs`  
- Neue Regeln/MR ableiten  
- Templates pflegen

## No-Gos
- Keine neuen Features  
- Keine Richtungswechsel  
- Keine Multi-Patches ohne Test

---

# Status

## Zweck
Kompakte Übersicht über Fortschritt und Zustand.

## Inhalt
- Fortschritt nach Lanes/Bereichen  
- Stabilität / Risiko  
- ggf. Ausblick

**Wichtig**  
- Enthält bewusst **KEIN Setup**

---

# Halt, Stop!

## Zweck
Sofortiger Kollaborations-Reset.

## Inhalt
- Arbeitsstopp  
- Ziel/Modus/Nächster Schritt klären

**Hinweis**  
- Sonderfall  
- Kein Setup erforderlich

---

# Ultra

## Zweck
Maximal hochwertige Produktionsausgaben.

## Merkmale
- Zeitmarken  
- Copy-Buttons  
- 10-Sekunden-Segmente  
- Produktionsstandard

**Hinweis**  
- Produktionsmodus  
- Kein Setup erforderlich

---

# Pflege & Governance

- Diese Datei ist **verbindlich**.  
- Neue Shortcodes werden **hier ergänzt**.  
- Änderungen über **Docs-only Runner**.  
- Danach **Push ins Public GitHub**.

---

*Stand: 2026-02-14*

<!-- BEGIN:R8605 -->
## R8605 Hinweis
- Nachsorge-Report für heute: `Excel-Projekte\Reports\Report_R8605_20260216_092823.md`
- Relevante Themen: Fairness (Totals/Day-Snapshot), PlanDate als Text, doppelte Helper-Namen
<!-- END:R8605 -->

