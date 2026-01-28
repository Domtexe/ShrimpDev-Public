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
- Nicht jeder Shortcode enthält automatisch Alignment (siehe Definitionen).

---

## Alignment (neu)

**Zweck**  
Reiner Orientierungs- und Regelhinweis.  
Keine Analyse, kein Status, kein zusätzlicher Inhalt.

**Ausgabe enthält ausschließlich:**
- Hinweis auf **Master Rules (MR)**
- Hinweis auf **Templates** (`docs/templates/`)
- Hinweis auf **Pipeline** (`docs/PIPELINE.md`)
- Hinweis auf weiteres relevantes Regelwerk
- Hinweis auf das **Public GitHub Repository**

**No-Gos**
- Kein Status
- Keine Analyse
- Keine Entscheidungen
- Kein zusätzlicher Text

---

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
- **MUSS Alignment enthalten**

---

## Status

**Zweck**  
Kompakte Übersicht über Fortschritt und Zustand.

**Inhalt**
- Fortschritt nach Bereichen / Lanes (oft in %)
- Stabilität / Risiko
- ggf. Ausblick

**Wichtig**
- **Enthält bewusst KEIN Alignment**

---

## Halt, Stop!

**Zweck**  
Sofortiger Kollaborations-Reset.

**Inhalt**
- Arbeitsstopp
- Klärung von Ziel, Modus und nächstem Schritt

**Hinweis**
- Sonderfall
- Kein Alignment erforderlich

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
- Kein Alignment erforderlich

---

## Pflege & Governance

- Diese Datei ist **verbindlich**.
- Neue Shortcodes werden **hier ergänzt**, nicht implizit benutzt.
- Änderungen erfolgen über **Docs-only Runner**.
- Nach Änderungen ist ein **Push ins Public GitHub** erforderlich.

---

*Stand: 2026-01-28 07:04*