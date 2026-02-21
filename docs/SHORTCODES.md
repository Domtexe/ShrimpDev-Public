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

# Status+

## Zweck
Vollständiger **Overall-Status** über das gesamte ShrimpDev-Ökosystem (alle Projekte, Teilprojekte, Produkte) – als **verbindlicher Abschluss** einer Session.

## Inhalt
- Gesamtbewertung (Reife/Stabilität/Produktionsfähigkeit/Monetarisierungsnähe)
- Status je Bereich/Projekt inkl. Teilprojekte (in %; kurz begründet)
- Top-Engpässe / Risiken (max. 3)
- Nächster Fokus / nächster GO-Anker (konkret)
- Optional: Money-Lane Kurzstand (wenn relevant)

**Wichtig**
- Enthält bewusst **KEIN Setup**
- Keine neuen Entscheidungen/Features – reine Lage + nächster Schritt

## Standard
- Am Ende jeder Session standardmäßig: **Status+** (sofern nicht ausdrücklich abgewählt)

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

<!-- R8524_NACHSORGE_2026-02-21 -->

## STATUS_ALL (Overall Status – kommt am Schluss)
**Befehl:** `StatusAll` / `STATUS_ALL`

**Zweck:** Am Ende jedes Threads/Sessions: vollständiger Gesamtstatus über alle Projekte/Teilprojekte/Produkte.

**Ausgabe umfasst:**
- ShrimpDev Core (GUI/Runner/RUN/DirectRun/Compile-Gate)
- Purge-System (Whitelist-SSOT, R3106 Status)
- DISPO-Tool (Version/Restpunkte)
- Clarivoo (Stand Content/Monetarisierung)
- Governance (MR/Pipeline/Shortcodes/Maps)
- Stabilität (Import-Check, Smoke-Test)
- Nächste 3 Schritte + höchste Risiken

**Regel:** STATUS_ALL kommt **nach Nachsorge**, nicht davor.

<!-- R8524_NACHSORGE_2026-02-21 -->
