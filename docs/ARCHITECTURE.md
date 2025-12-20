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
