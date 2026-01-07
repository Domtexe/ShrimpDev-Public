# Architektur – ShrimpDev

## Ziel
Stabiles, nachvollziehbares Entwickeln/Diagnostizieren/Reparieren komplexer Projekte über Runner.

## Hauptbereiche (typisch)
- `main_gui.py` – App-Einstieg, Tab-Aufbau, GUI-Orchestrierung
- `modules/` – UI-Module, Logikmodule, Actions/Utilities
- `tools/` – Runner (R####.cmd + R####.py)
- `docs/` – Architektur, Regeln, Briefings
- `registry/` – Register/Inventar (falls genutzt)
- `_Archiv/` (lokal) – Backups
- `_Reports/` (lokal) – Runner-Reports/Logs
- `_Snapshots/` (lokal) – Tages-Snapshots (Slim)

## Runner-Konzept
- Jeder Runner löst **ein klar umrissenes Problem**.
- Jede Änderung: Backup(s) + Log + (falls relevant) Doku-Update.
- Keine Voll-Rewrites ohne explizite Zustimmung.

## Start/Diagnose
- Start: `python main_gui.py`
- Runner: Doppelklick `tools\R####.cmd`
- Logs: `_Reports/`

## MasterRules Tab (R2143)
- Eigener Notebook-Tab "MasterRules" zeigt Inhalte aus `docs/Master/`.
- Einstieg: `MasterRules.md` (Fallback: `MasterRules_Core.md`, sonst Dateiliste).
- Implementierung: `modules/ui_masterrules_tab.py`, Tab-Hook in `main_gui.py`.

## MasterRules Tab (R2143)
- Eigener Notebook-Tab "MasterRules" zeigt Inhalte aus `docs/Master/`.
- Einstieg: `MasterRules.md` (Fallback: `MasterRules_Core.md`, sonst Dateiliste).
- Implementierung: `modules/ui_masterrules_tab.py`, Tab-Hook in `main_gui.py`.

## Hotfix MasterRules Tab Import (R2144)
- Fix: ui_masterrules_tab.py Fallback-Block korrigiert (unterminated string literal entfernt).
- Ziel: Start/Import-Stabilität von ShrimpDev.

## R2148 – Log Auto-Tail
- Log-Tab laedt neue debug_output.txt Eintraege automatisch nach (append only, sichtbarkeitsbasiert).

## R2153 – Pipeline Tab: Done/Offen sichtbar + Auto-Reload
- build_pipeline_tab Block ersetzt (weil Syntax gebrochen war).
- Summary: Erledigt/Offen + Hervorhebung von Checkbox-Zeilen.

## R2154 – Pipeline Checkbox Toggle
- Pipeline-Tab: Klick auf Task-Zeile toggelt [ ] / [x] und speichert in docs/PIPELINE.md.

## R2155 – Pipeline Tab UX (Treeview)
- Pipeline-Tab nutzt Treeview: Status/Prio/Task/Section, Toggle, Filter, Summary, Auto-Reload.

## R2156 – Pipeline Tab Debug+Parser
- Diagnose (Pfad/exists) + robustes Task-Parsing (+ Explorer-Button).

## R2158 – Pipeline Tab Recovery
- Rollback auf R2157-Backup + sauberer Parser-Replace (Indent stabil) + import re.

## R2162 – Exception Logger Install Fix
- Patched: main_gui.py main() detection robust (supports -> None) + installs exception_logger.

## R2165 – Runner Guard
- Added: tools/runner_guard.py
- All new runners MUST use run_guarded(main, runner_id).

## R2166 – Pipeline Tab UX
- Added: Search field + zebra rows + done/high emphasis + column sorting.
- Scope: modules/ui_pipeline_tab.py only.

## R2166 – Pipeline Tab UX
- Added: Search field + zebra rows + done/high emphasis + column sorting.
- Scope: modules/ui_pipeline_tab.py only.

## R2167a – Agent Vertrag & Legacy bereinigt
- Agent-Tab ist verbindlich: modules/module_agent.py -> build_agent_tab(parent, app)
- modules/module_agent_ui.py als LEGACY/UNUSED markiert (nicht löschen/umbenennen).
- docs/TABS.md als zentrale Tab-Vertragsdatei gepflegt.

## R2167 – Tab-Verträge dokumentiert
- Added/Updated: docs/TABS.md als zentrale Wahrheit für Tab→Builder Mapping.
- Agent-Vertrag festgehalten: modules.module_agent.build_agent_tab(parent, app).

## R2173 – Agent UI klickbar
- Agent-Tab: Empfehlungen als Liste + Aktionen (Ausführen, Pfad kopieren, In Pipeline).
- Pipeline-Pfad fest: docs/PIPELINE.md (mit Nachfrage).

## R2174 – Zentrale Popup-Policy
- Alle Popup-Dialoge im Agent-Tab sind zentriert (parent=app.root).
- Keine direkten messagebox-Aufrufe mehr im Agent-Code.


## Canonical Paths
Zeitpunkt: 2025-12-23 23:26:41

## Kanonische Pfade (verbindlich)
- **Reports/** → alle Reports (einziger Zielort)
- **docs/PIPELINE.md** → ShrimpDev-Pipeline
- **docs/pipelines/** → Produktpipelines (ShrimpHub, ShrimpBridge, …)
- **docs/Architecture/** → Architektur & Systemdesign
- **tools/** → Runner
- **modules/** → Runtime-Code

## Nicht-kanonisch (Legacy / Archiv)
- `_Reports/`
- `docs/Report_*`
- `_Pipeline/`
- `_Archiv/`
- `_Snapshots/`

Nicht-kanonische Pfade dürfen existieren, werden aber **nicht mehr aktiv beschrieben oder ausgewertet**.

## CI & Style

CI ist bewusst **runtime-fokussiert** (Stabilität der App). `tools/` ist **Runner-/Learning-Sandbox** und darf CI nicht blockieren.

**Kanonische Regeln:** siehe `docs/DEVELOPMENT_RULES.md` → Abschnitt **“CI & Ruff – Scope (Runtime-only)”**.

## TechDebt hotspots
- `modules/ui_runner_products_tab.py`: legacy UI handler clustering (deeply nested try/except). Prefer small helper functions and shallow, well-closed error scopes.

---
### CI / Ruff Legacy-Zonen (20251225_174811)
- Marker: `R2638_RUFF_LEGACY_ZONES`
- Policy: UI/Tools/LJ gelten als Legacy-Zonen und blockieren CI nicht mit Stil-/Modernisierungsregeln.
- Umsetzung: `pyproject.toml` per-file-ignores für `modules/ui_*.py`, `modules/tools/*.py`, `modules/module_learningjournal.py`.
- Ziel: CI prüft Stabilität (Syntax/echte Fehler), nicht Legacy-Style.
---



<!-- SHRIMPDEV_POLICY_REPO_LAYERS -->
## Policy: Repo-Layers (Production vs Archive) & CI Scope

**New insight (R2652/R2653):** Dieses Repo enthält bewusst mehrere Schichten.

- **Production layer (must be syntactically clean):** `modules/**`, `main_gui.py` (und nur ausdrücklich freigegebene Prod-Tools)
- **Archive/Legacy layer (may be broken):** `_OldStuff/**`, `_Trash/**`, `tools/Archiv/**`, historische Runner/Friedhof

**Rule:** CI-/Syntax-Gates (compileall, Ruff E9) dürfen **nur** auf dem Production-Layer laufen.

**Reason:** Archive/Legacy enthält absichtlich kaputte/inkompatible Dateien (Syntax/Encoding/Indent), die nicht als Blocker gelten.

**Implementation standard:**

```text
python -m compileall -q main_gui.py modules
ruff check modules main_gui.py --select E9
```

**Exclude standard (lint/ci):** `_OldStuff/**`, `_Trash/**`, `tools/Archiv/**`, `modules/snippets/**`, Outputs (`Reports/**`, `_Archiv/**`, `_Exports/**`).



<!-- SHRIMPDEV_POLICY_CI_WORKFLOW_YAML -->
## Policy: CI-Workflow zuerst auf YAML-Validität prüfen

**Rule:** Wenn GitHub Actions **„Invalid workflow file“** oder **„You have an error in your yaml syntax“** meldet, wird **immer zuerst** die YAML-Struktur geprüft (Indentation/Mapping), bevor Tooling (ruff/compileall/etc.) debuggt wird.

**Reason:** Bei YAML-Parsefehlern werden **keine Steps** ausgeführt – Tool-Logs sind dann irrelevant.

**Quick checklist:**
- `jobs:` → darunter müssen Job-IDs **eingerückt** sein (z. B. `  lint:`)
- `runs-on:` / `steps:` sind **unter dem Job** eingerückt
- Step-Listenpunkte beginnen mit `-` und sind korrekt eingerückt

<!-- SHRIMPDEV_POLICY_PIPELINE_TASKS_REQUIRED -->
## Rule: PIPELINE.md benötigt einen Tasks-Block (GUI-Sichtbarkeit)

**New insight:** Der ShrimpDev-Tab *Pipeline* parst **nur Aufgaben** aus `docs/PIPELINE.md`.
Text-/Policy-Abschnitte sind sinnvoll, erzeugen aber **keine** Einträge in der Task-Liste.

**Rule:** `docs/PIPELINE.md` muss einen klaren Aufgabenbereich enthalten, z. B.:

```md
## Pipeline Tasks
- [ ] (P1) ...
- [x] (P0) ...
```

**Reason:** Ohne parsebare Tasks bleibt die Pipeline in der GUI leer (0/0), obwohl das Dokument existiert.

## Autopush (Repo-only)
- Canonical autopush backend (OneDrive repo-only): `tools/R2691` (Private), `tools/R2692` (Public), `tools/R2693` (Both).
- Deprecated: `R2692/R2691` legacy autopush runners (workspace-bound). Do not wire GUI buttons to them.
- Autopush reports are generated locally under `Reports/` and are not versioned in git.


## UI-Fehlerbehandlung (verbindlich)

- Jeder UI-Flow ist **diagnostizierbar**
- Keine stillen Abbrüche
- Button → Log → Aktion → Report

## Purge Popup Flow (Option A) – R3086

**Ist-Soll:**
- Purge klickt → UI startet `tools\R2224.cmd`
- R2224 schreibt Ergebnis als TXT: `_Reports\R2224_*.txt`
- UI zeigt Ergebnis in einem **dedizierten TXT-Popup** (kein Bridge-Wrapper, keine Abhängigkeit von r1851)

**Begründung:**
R1851 ist für Standard-Reports (typisch Markdown). R2224 liefert TXT → Format-Mismatch → leere Wrapper-Anzeige.  
Option A hält das System stabil, minimal-invasiv und wartbar.
