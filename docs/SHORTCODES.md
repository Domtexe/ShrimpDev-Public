# ShrimpDev – Shortcodes (SSOT)

**Single Source of Truth**

Diese Datei definiert alle offiziell existierenden **Shortcodes**.
Sie liegt bewusst im Repository und wird ins **Public GitHub** gespiegelt,
damit Mensch **und Assistent** zuverlässig dieselben Regeln verwenden.

---

# Grundprinzip: Ausführungsvertrag (verbindlich)

Jeder Shortcode hat zwei Ebenen:

1) **Inhaltsebene** (was der Shortcode bedeutet)  
2) **Ausführungsebene** (was der Assistent bei Aufruf *tatsächlich* liefern/machen muss)

## A. Assistenten-Pflichten bei JEDEM Shortcode-Aufruf
- **Keine Theorie ohne Aktion**: Wenn der Shortcode eine Aufgabe impliziert, muss der Assistent konkrete Schritte liefern.
- **Änderungen nur mit Runner**: Jede Code-/Doku-/Governance-Änderung wird als Runner (`tools\R####.cmd` + `tools\R####.py`) geliefert – inkl. Backup + Report.
- **Safety Gate**: Bei UI/Core-Python-Änderungen ist ein Compile-Gate verpflichtend (z. B. `python -m py_compile ...`) im Runner.
- **Keine Heuristik-Patches** ohne Diagnose: Wenn ein Fix nicht beim ersten Versuch verifiziert funktioniert → Diagnose-Runner.

## B. Docs-/Governance-Sicherung (Pflicht, wenn Änderungen passiert sind)
Wenn im Thread/auf Anfrage Änderungen erzeugt wurden, muss als Abschluss ein **Nachsorge-Runner** kommen, der mindestens aktualisiert:
- `docs/MasterRules.md`
- `docs/PIPELINE.md`
- `docs/FILE_MAP.md`
- `docs/SHORTCODES.md` (nur wenn betroffen)
- `docs/CHANGELOG.md` (falls vorhanden)

---

# Raw Single-Source-of-Truth (Public GitHub)
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

## Ausführung (Assistent MUSS)
- Ausgabe enthält **ausschließlich**:
  - Hinweis auf **Master Rules (MR)**
  - Hinweis auf **Templates** (`docs/templates/`)
  - Hinweis auf **Pipeline** (`docs/PIPELINE.md`)
  - Hinweis auf weiteres relevantes Regelwerk
  - Hinweis auf das **Public GitHub Repository**
  - Hinweis auf die **Raw SSOT Dateien** (FILE_MAP/MR/PIPELINE/SHORTCODES)
- Optional: Pfad-Reminder (Repo-Root / Excel-Projekte)
- **No-Gos**: kein Status, keine Analyse, keine Entscheidungen

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

## Ausführung (Assistent MUSS)
- **MUSS Setup enthalten** (als eigener Abschnitt)
- Muss außerdem liefern:
  - klare „Next Step“-Anweisung (1–3 Schritte)
  - falls im Thread Änderungen entstanden: Hinweis „Nachsorge folgt/ist Pflicht“

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
- File Map pflegen / anlegen
- System Map pflegen / anlegen
- Changelog
- Versionsnummer

## Ausführung (Assistent MUSS)
- **Immer** einen **Nachsorge-Runner** liefern, der:
  - Backups macht
  - Report schreibt
  - Docs/MR/Pipeline/Maps aktualisiert (minimal-invasiv, marker-basiert)
- **No-Gos**: keine neuen Features, keine Richtungswechsel, keine Multi-Patches ohne Test

---

# Status

## Zweck
Kompakte Übersicht über Fortschritt und Zustand.

## Inhalt
- Fortschritt nach Lanes/Bereichen
- Stabilität / Risiko
- ggf. Ausblick

## Ausführung (Assistent MUSS)
- Nur Status (bewusst **kein Setup**)
- Keine neuen Entscheidungen/Features

---

# Status+

## Zweck
Vollständiger Overall-Status über das gesamte ShrimpDev-Ökosystem (alle Projekte, Teilprojekte, Produkte).

## Inhalt
- Gesamtbewertung (Reife/Stabilität/Produktionsfähigkeit/Monetarisierungsnähe)
- Status je Bereich/Projekt inkl. Teilprojekte (in %; kurz begründet)
- Top-Engpässe / Risiken (max. 3)
- Nächster Fokus / nächster GO-Anker (konkret)
- Optional: Money-Lane Kurzstand (wenn relevant)

## Ausführung (Assistent MUSS)
- Reiner Lagebericht + nächster Schritt (bewusst **kein Setup**)
- Keine neuen Entscheidungen/Features

## Standard
- Am Ende jeder Session standardmäßig: **Status+** (sofern nicht ausdrücklich abgewählt)

---

# Halt, Stop!

## Zweck
Sofortiger Kollaborations-Reset.

## Inhalt
- Arbeitsstopp
- Ziel/Modus/Nächster Schritt klären

## Ausführung (Assistent MUSS)
- Sofort stoppen + neu ausrichten
- Kein Setup erforderlich

---

# Feierabend

## Zweck
Soll verhindern, dass wichtige Änderungen verlorengehen oder Abschlussarbeiten vergessen werden.

## Inhalt (Reihenfolge ist fix)
1) Nachsorge (inkl. Runner!)
2) Status
3) Status+

## Ausführung (Assistent MUSS)
- Wenn Änderungen im Thread passiert sind:
  - **Nachsorge-Runner ist Pflicht** (Docs/MR/Pipeline/Maps sichern)
- Kein Setup. Feierabend.

---

# Ultra

## Zweck
Maximal hochwertige Produktionsausgaben.

## Merkmale
- Zeitmarken
- Copy-Buttons
- 10-Sekunden-Segmente
- Produktionsstandard

## Ausführung (Assistent MUSS)
- Ausgabe exakt im Ultra-Standard
- Kein Setup erforderlich

---

# STATUS_ALL (Overall Status – kommt am Schluss)

**Befehl:** `StatusAll` / `STATUS_ALL`

## Zweck
Am Ende jedes Threads/Sessions: vollständiger Gesamtstatus über alle Projekte/Teilprojekte/Produkte.

## Ausführung (Assistent MUSS)
- **Regel:** STATUS_ALL kommt **nach Nachsorge**, nicht davor.

---

# Pflege & Governance

- Diese Datei ist **verbindlich**.
- Neue Shortcodes werden **hier ergänzt**.
- Änderungen über **Docs-only Runner**.
- Danach **Push ins Public GitHub**.

*Stand: 2026-02-22*
