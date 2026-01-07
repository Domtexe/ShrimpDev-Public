# Runner Registry – ShrimpDev

Diese Datei dokumentiert alle bekannten Runner in ShrimpDev.
Ziel ist Transparenz, Wartbarkeit und die Vermeidung von implizitem Wissen.

---

## Core Infrastructure

### runner_guard.py
**Typ:** Core-Komponente (kein R-Runner)
**Status:** Aktiv – kritisch

**Zweck**
- Sichere Ausführung aller Runner
- Fängt Exceptions, Tracebacks und Exit-Codes ab
- Zentrale Logging-Instanz
- Verhindert System-Crashes durch fehlerhafte Runner

---

## Active / Maintenance Runner

### R1802 – LearningJournal Konsolidierung
**Status:** Aktiv
**Kategorie:** Data Maintenance / Learning Engine

- Bereinigung und Konsolidierung von learning_journal.json
- Deduplikation und Normalisierung
- Erstellung eines Reports unter _Reports

### R1922 – Snapshot / Systemzustand
**Status:** Aktiv
**Kategorie:** Backup & Recovery

- Erstellt Projekt-Snapshots
- Grundlage für Rollback und Archivierung

### R2086 – Konfigurations- & Strukturkonsolidierung
**Status:** Aktiv
**Kategorie:** System Maintenance

- Konsolidiert Konfigurationsstände
- Stabilisiert Übergänge zwischen Entwicklungsphasen

---

## Diagnostics / Testing

### R9999 – Intentional Crash
**Status:** Aktiv (Test)
**Kategorie:** Diagnostics / Testing

- Erzwingt einen absichtlichen Crash
- Testet runner_guard, Logging und Fehlerpfade

### R9998 – Legacy Logging / Error Test
**Status:** Beobachten
**Kategorie:** Diagnostics (Legacy)

- Frühere Tests für Logging und Fehlerbehandlung
- Teilweise durch R9999 ersetzt

### R9997 – Sonder-/Debug-Runner
**Status:** Beobachten
**Kategorie:** Legacy / Undefined

- Historischer Debug-Runner ohne klaren aktuellen Zweck

---

## Legacy / Referenz

### R1987 – Syntax- & Strukturprüfung
**Status:** Legacy (Referenz)
**Kategorie:** Diagnostics / Safety

- Früher Syntax- und Strukturprüfung für Python-Code
- Vorläufer von Intake + runner_guard

### R1352 – Früher Migrations-/Repair-Runner
**Status:** Legacy
**Kategorie:** Early Infrastructure

### R1252 – Früher Basis-Runner
**Status:** Legacy
**Kategorie:** Early Infrastructure

---

## Zusammenfassung

**Aktiv & Behalten**
- runner_guard
- R1802
- R1922
- R2086
- R9999

**Beobachten / Konsolidieren**
- R9998
- R9997

**Archiv / Referenz**
- R1987
- R1352
- R1252

_Generiert am 2025-12-14 21:39:29 durch R2178_
