# ShrimpDev – Shortcodes

**Single Source of Truth**

Diese Datei definiert alle offiziell existierenden **Shortcodes**.
Sie liegt bewusst im Repository und wird ins **Public GitHub** gespiegelt,
damit sie von Mensch **und Assistent** zuverlässig gelesen werden kann.

---

## Grundregeln

- Shortcodes sind **konzeptionelle Befehle**, keine Implementierungsdetails.
- Änderungen an Shortcodes erfolgen **ausschließlich dokumentiert**.
- Diese Datei ist maßgeblich – implizites Wissen gilt nicht.
- Nicht jeder Shortcode enthält automatisch Setup (siehe Definitionen).

---

## Setup

**Zweck**  
Reiner Orientierungs- und Regelhinweis vor Arbeitsbeginn.  
Keine Analyse, kein Status, kein zusätzlicher Inhalt.

**Ausgabe enthält ausschließlich:**
- Hinweis auf **Master Rules (MR)**
- Hinweis auf **Templates** (`docs/templates/`)
- Hinweis auf **Pipeline** (`docs/PIPELINE.md`)
- Hinweis auf weiteres relevantes Regelwerk
- Hinweis auf das **Public GitHub Repository**
- optional: Pfad-Reminder (Repo-Root / Excel-Projekte)

**No-Gos**
- Kein Status
- Keine Analyse
- Keine Entscheidungen
- Kein zusätzlicher Text


## ThreadCut

**Zweck**  
Saubere Übergabe zwischen Threads / Arbeitssessions.

**Inhalt**
- Aktueller Stand
- Erledigt
- Offen
- Nächster logischer Einstieg
- No-Gos / verbindliche Regeln

**Pflicht**
- **MUSS Setup enthalten**

---



## Nachsorge

**Zweck**  
Kurze, faktenbasierte Stabilitäts- und Konsistenzprüfung nach Änderungen – inkl. Governance-/Docs-Pflege.

**Inhalt**
- Was wurde geändert (faktisch)
- Systemzustand (läuft es stabil, Daten ok)
- Risiken / Seiteneffekte / technische Schuld (kurz)
- Offenes (was fehlt bis „stabil“)
- **Dokumentation & Pflege**: notwendige Updates unter `root/docs` (Pipeline, Architektur, Regeln, Guides etc.)
- **Neue Regeln / MR**: falls entstanden → ableiten & niederschreiben (kurz, präzise)
- **Templates**: falls betroffen → definieren oder updaten

**No-Gos**
- Keine neuen Features
- Keine Richtungswechsel
- Keine Multi-Patches ohne Test


## Status

**Zweck**  
Kompakte Übersicht über Fortschritt und Zustand.

**Inhalt**
- Fortschritt nach Bereichen / Lanes (oft in %)
- Stabilität / Risiko
- ggf. Ausblick

**Wichtig**
- **Enthält bewusst KEIN Setup**

---

## Halt, Stop!

**Zweck**  
Sofortiger Kollaborations-Reset.

**Inhalt**
- Arbeitsstopp
- Klärung von Ziel, Modus und nächstem Schritt

**Hinweis**
- Sonderfall
- Kein Setup erforderlich

---

## Ultra

**Zweck**  
Maximal hochwertige Produktionsausgaben (z. B. Sora / Storyboards).

**Merkmale**
- Zeitmarken
- Copy-Buttons
- 10-Sekunden-kompatible Segmente
- Produktionsstandard

**Hinweis**
- Produktionsmodus
- Kein Setup erforderlich

---

## Pflege & Governance

- Diese Datei ist **verbindlich**.
- Neue Shortcodes werden **hier ergänzt**, nicht implizit benutzt.
- Änderungen erfolgen über **Docs-only Runner**.
- Nach Änderungen ist ein **Push ins Public GitHub** erforderlich.

---

*Stand: 2026-01-28 07:04*