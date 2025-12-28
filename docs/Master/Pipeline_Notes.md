<!-- LEGACY_NON_CANONICAL -->
**⚠️ Legacy / Nicht-kanonisch** (gesetzt: 2025-12-24 00:04:38)  
Kanonisch: `docs/PIPELINE.md`  
Bitte diese Datei nicht mehr als Quelle verwenden.

---

# Pipeline Notes


_Angelegt durch R2039 am 2025-12-09 10:21:14_


## Offene Themen / Runner-Ideen


- R1987 – Button im Intake rechts pruefen (Sinnvoll? Nutzen? Mehrwert?)

- GUI: Verschiebbare Trennlinie zwischen Intake (links) und TreeView (rechts) einbauen.
- GUI: Log-Ansicht in eigenen Tab verschieben (2. Tab, statt Log-Button).

- GUI: TreeView Mehrfachauswahl ermoeglichen (für Löschen & Rename).

## ✅ Repo-Roots, Push-Buttons & Purge-Stabilisierung – DONE (2025-12-28)

**Diagnose:**
- R2834 (AST Locator)
- R2836 (Runtime Trace)
- R2838 (Whitelist Analyse)

**Fixes:**
- R2837 – Push-Buttons nur bei vorhandenen Wrappern aktiv
- R2839 – Whitelist-Hardening (stem + cmd/py + tools\… Varianten)

**Ergebnis:**
- Push-Buttons konsistent (Repo-root + Wrapper gating)
- Wrapper werden nicht mehr purged (Whitelist robust)
- Purge Scan zeigt KEEP/ARCHIVE korrekt

