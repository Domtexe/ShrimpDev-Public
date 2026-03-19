# FILE MAP

This file is a curated navigation map for `ShrimpDev_REPO`.

It is intentionally selective:
- focus on entrypoints, governance, major subsystems, and stable directories
- summarize archives, caches, and backups instead of dumping them
- help humans and Codex stay inside the right scope before patching

See also:
- [ARCHITECTURE.md](ARCHITECTURE.md) for the high-level architecture overview
- [ARCH_INDEX.md](ARCH_INDEX.md) for architecture document navigation
- [FILE_MAP_TECH.md](FILE_MAP_TECH.md) for technical entrypoints and relationships

## 1. Core documentation (SSOT)

These files act as the project governance layer. They define rules, workflows, and the expected operating model.

- `docs/MasterRules.md`
  Primary project rules and operating constraints.
- `docs/PIPELINE.md`
  Main pipeline / work orchestration reference.
- `docs/FILE_MAP.md`
  Curated repository navigation map.
- `docs/SHORTCODES.md`
  Project shorthand and command reference.
- `AGENTS.md`
  Agent workflow rules for repo work, especially DIAG -> FIX -> VERIFY and scope discipline.

Useful companion docs in the same area:
- `docs/ARCHITECTURE.md`
- `docs/ARCHITECTURE_MAP.md`
- `docs/UI_MAP.md`
- `docs/Runner_Index.md`
- `docs/IDEA_INBOX.md`
  Kanonische Quelle fuer das bestehende Ideen-System; `NEW`/`IMPORTED` werden hier gelesen.
- `docs/IDEA_INBOX_SPEC.md`
  Format- und Feeder-Regeln fuer Inbox-Eintraege; `docs/ideas/` ist nicht-kanonisch.

## 2. Main application entrypoints

- `main_gui.py`
  Main Tkinter application entrypoint and app bootstrap.
  Aktiver SSOT fuer den rechten Stack `Output -> Toolbar -> Tree`, den Intake-Runner-Tree, dessen Sort-/Refresh-State, das OutputDisplay-Binding und das Rechtsklick-Kontextmenue des aktiven Runner-/Intake-Trees.
- `RUNBABYRUN.CMD`
  Windows launcher shortcut for the local app workflow.
- `learning_engine.py`
  Top-level learning/analysis entrypoint; related to the self-learning subsystem.

## 3. Core Python modules

The `modules/` directory is the main application layer. It contains many files, but only a smaller set acts as stable architectural anchors.

### UI / layout

- `modules/ui_toolbar.py`
  Main right-side toolbar implementation.
- `modules/ui_output_display.py`
  Output/log display widget used by the GUI.
- `modules/ui_project_tree.py`
  Project tree / file tree UI and selection behavior.
- `modules/ui_left_panel.py`
  Left-side panel construction.
- `modules/ui_pipeline_tab.py`
  Pipeline tab UI.
- `modules/ui_runner_products_tab.py`
  Runner products / output tab UI.
- `modules/ui_settings_tab.py`
  Settings tab UI.
- `modules/ui_menus.py`
  Main menu construction.
- `modules/module_docking.py`
  Docking / pane layout behavior.

### Runner execution and actions

- `modules/module_runner_exec.py`
  CMD-first runner execution, capture, and UI output streaming.
- `modules/runner_executor.py`
  Additional runner execution support; likely legacy/adjacent to the main executor.
- `modules/toolbar_runner_exec.py`
  Central toolbar runner gateway; `run_by_id(...)` is the canonical launch path for GUI-triggered runners.
  Beherbergt Inflight-Guard, `app=None`-Fallback, defensive Guards fuer `runner_id`, sowie die Popup-vs-OutputDisplay-Entscheidung auf Basis der INI-Policy.
- `modules/runner_ids.py`
  Canonical runner-id constants plus protected-runner SSOT used by GUI quick-launch, delete guards und T666-/Special-Runner-Schutz.
  Toolbar-triggered runner execution helpers.
- `modules/logic_actions.py`
  Toolbar / action routing for delete, rename, push, purge, and related commands.
- `modules/toolbar_action_router.py`
  Action dispatch / routing around toolbar commands.

### Intake / tree / editor support

- `modules/logic_intake.py`
  Intake logic for incoming files/content.
- `modules/module_code_intake.py`
  Main code intake subsystem.
- `modules/module_code_intake_v1.py`
  Older intake implementation kept alongside the current flow.
- `modules/module_intake_workers.py`
  Intake background tasks / worker logic.
- `modules/module_shim_intake.py`
  Compatibility / bridge layer for intake behavior.

### Config, state, registry

- `modules/config_loader.py`
  Config loading helpers.
- `modules/config_manager.py`
  Config manager implementation.
- `modules/context_state.py`
  Shared app context/state handling.
- `modules/module_registry.py`
  Registry-related logic.
- `modules/workspace_registry.py`
  Workspace-level registry handling.

### Reports, logging, safety

- `modules/exception_logger.py`
  Error and runner logging.
- `modules/module_preflight.py`
  Preflight checks before operations.
- `modules/preflight_checks.py`
  Additional validation helpers.
- `modules/module_patch_release.py`
  Patch/release oriented helper logic.

### Ideas / inbox

- `modules/idea_inbox_gui.py`
  GUI integration for the idea inbox.
- `modules/idea_inbox_status.py`
  Idea inbox status computation against `docs/IDEA_INBOX.md`.
- `modules/idea_import_button.py`
  Import-Ideas action entry; triggers the existing `GUI -> R9341` import flow.
- `modules/idea_editor_gui.py`
  GUI/editor for adding `## ENTRY` blocks into the canonical inbox.

If a module is not listed here, it is usually either:
- a smaller helper
- a more local subsystem file
- a legacy/backup artifact
- or a specialized module better understood from the surrounding feature docs

## 4. `tools/` directory

`tools/` is the runner system. This is central to the repo.

Typical structure:
- `tools/R####.cmd`
  Windows runner entrypoint.
- `tools/R####.py`
  Runner logic paired with the `.cmd`.

Runner purpose usually falls into one of these categories:
- DIAG
- FIX
- VERIFY
- repo tooling
- patch execution
- automation / migration

Important supporting files:
- `tools/patch_engine.py`
  Patch-oriented helper tooling.
- `tools/compile_gate.py`
  Compile / validation gate support.

Important current runners from the stabilization block:
- `tools/R9417.py`
  AI Patch Validator / Gate. Bewertet den angeforderten Runner inzwischen differenzierter statt globalen Worktree-Schmutz stumpf zu blockieren.
- `tools/R9447.py`
  Hook Inventory DIAG fuer erkannte GUI-/Toolbar-Actions; beruecksichtigt den gueltigen `delete`-Alias/Fallback jetzt korrekt und meldet dadurch keine False-Negatives mehr fuer diesen Hook.
- `tools/R9425.py`
  Nachsorge-Runner fuer den Stabilisierungs-/Konsolidierungsblock.
- `tools/T666.py`
  Kleine Universal Runner Engine fuer `diag`, `smoke`, `filecheck <path>`, `echo <text>`.
- `tools/T666.cmd`
  Launcher fuer `T666.py`; reicht `%*` an die Python-Logik durch.

Runner workflow in practice:
1. Diagnose the current state.
2. Apply a minimal patch or scripted change.
3. Verify the result and write outputs to `Reports/`.

`tools/Archiv/` exists, but it is historical storage and should not be treated as the active source of truth.

## 5. Reports / Backups / Archives

These directories are operational history, not core architecture.

- `Reports/`
  Current task reports, captures, trace logs, and generated evidence.
- `Backups/`
  Active backup storage for reversible changes.
- `Backups_ALT/`
  Alternate backup area.
- `_Archiv/`, `_Archive/`, `_Backups/`, `_Backup/`
  Historical material, old runs, preserved backups, and archived artifacts.

Important rule:
- use these folders for traceability and rollback context
- do not recursively enumerate them in this file map

Low-value directories intentionally summarized only:
- `__pycache__/`
- `.ruff_cache/`
- scratch/temp/trash style folders such as `_Temp/`, `_Scratch/`, `_Trash/`
- `docs/ideas/`
  Optional archive snapshots for idea batches; not a canonical import source.

## 6. Excel-Projekte

The repo contains Excel/VBA-based subprojects alongside the Python application.

- `Excel-Projekte/Dispo-Tool`
  Main Excel scheduling / dispatch tool with VBA modules and workbook copies.
- `Excel-Projekte/Dispo-Tool - Kopie`
  Copy-based working area for safer workbook patching.
- `Excel-Projekte/ASM-Tool`
  Separate Excel subproject.
- `Excel-Projekte/Reports`
  Reports related to Excel/VBA patch tasks.

### `Excel-Projekte/Dispo-Tool`

General purpose:
- workbook-based planning / dispatch tool
- VBA-heavy logic for assignment, status generation, and mail/HTML preview rendering

Major VBA modules known from recent work:
- `modDispoAssign`
  Assignment / slot allocation logic.
- `modMail`
  Mail and HTML preview generation, including Nachlass status rendering.
- `modPlanStore`
  Plan date / plan store helpers.
- `modPlanDateUI`
  Plan-date UI and workday/holiday helpers.

The exact full VBA module inventory can vary per workbook export. Use workbook export or recent DIAG folders when a patch needs precise module scope.

## 7. Other subprojects

- `clarivoo_site/`
  Hugo-based website/content subproject with `content/`, `layouts/`, `static/`, and `public/`.
- `config/`
  Shared configuration data.
- `registry/`
  Registry and lookup artifacts.
- `debug/`
  Debug-oriented outputs or support files.
- `docs/websites/`, `docs/pipelines/`, `docs/templates/`
  Documentation areas for additional pipelines and site/content systems.

Some root-level files and folders have unclear or legacy-specific purpose, for example:
- `R1252.py`
- `Pipeline`
- `run`
- `writes`
- `right_stack`

Treat these as local/legacy artifacts unless a task explicitly targets them.

## 8. Critical architecture notes

### Docs as SSOT

Before patching, check the governance layer first:
- `docs/MasterRules.md`
- `docs/PIPELINE.md`
- `AGENTS.md`
- this file

### Runner workflow

The repo is runner-first:
- diagnose first
- then patch minimally
- then verify

### GUI structure

The GUI is centered around:
- `main_gui.py`
- `modules/ui_output_display.py`
- `modules/ui_toolbar.py`
- `modules/ui_project_tree.py`

This matters because many tasks are really layout/wiring changes, not broad refactors.

Current active nuance:
- der produktive Runner-/Intake-Tree wird im laufenden GUI-Pfad aktuell aus `main_gui.py` heraus aufgebaut und dort auch fuer Sort-/Refresh-/Kontextmenue-Verhalten stabilisiert
- `modules/ui_project_tree.py` bleibt relevant als Helper-/Altpfad, ist aber derzeit nicht die alleinige SSOT fuer den aktiven rechten Tree

### Right-panel rule

Current repo rules emphasize this stack:
- Output
- Toolbar
- Tree

When patching UI behavior, preserve that order unless a task explicitly changes it.

### Excel work should stay isolated

Excel/VBA changes belong under `Excel-Projekte/` and should not be mixed with Python GUI patches unless the task explicitly spans both.

### Archive awareness

The repository contains a large amount of historical backup material.

Use it for:
- forensic comparison
- rollback context
- prior patch evidence

Do not treat it as the current architecture map.

## 9. Debugging entrypoints

Use these files first when a task is diagnostic, execution-related, or scope-sensitive.

- `main_gui.py`
  Main app bootstrap and the best starting point for UI composition and startup issues.
- `modules/module_runner_exec.py`
  Primary runner launch path, capture flow, and UI sink integration.
- `modules/logic_actions.py`
  Action wiring for delete, rename, push, purge, and related toolbar commands.
- `modules/ui_toolbar.py`
  Toolbar behavior and a frequent hotspot for right-panel regressions.
- `modules/ui_project_tree.py`
  Tree population, selection state, and run-target context.
- `debug_output.txt`
  Runtime output sink used by the app and runner execution flow.
- `Reports/`
  First place to check generated reports, captures, trace logs, and runner evidence.
- `Excel-Projekte/Dispo-Tool`
  Primary debugging surface for Excel/VBA tasks.

## Maintenance

Refresh this file when:
- architecture changes
- entrypoints change
- new subprojects are added
- runner workflows change
- Excel/VBA project structure changes
- major UI structure changes
# Dispo-Tool Release Notes

`Excel-Projekte/Dispo-Tool/Dispo-Tool 2.0.xlsm` ist die stabile Produktionsversion.

`Excel-Projekte/Dispo-Tool/Dispo-Tool 3.0.xlsm` ist der Entwicklungszweig.

`Excel-Projekte/Dispo-Tool/DispoHistory.sqlite` ist die Historien-Datenbank fuer die 3.0-Entwicklung.


---

## R9426 Nachsorge

**2026-03-16 22:54:26 – Nachsorge-Hinweis via R9426**

Relevante Dateien aus dem Stabilisierungslauf:

- `main_gui.py`
- `modules/toolbar_runner_exec.py`
- `modules/module_runner_exec.py`
- `modules/module_runner_popup.py`
- `modules/ui_toolbar.py`
- `modules/logic_actions.py`
- `modules/runner_ids.py`
- `modules/ui_filters.py`
- `registry/ShrimpDev.ini`
- `tools/R9421.py`
- `tools/R9423.py`
- `tools/R9424.py`
- `tools/R9425.py`
- `tools/R9426.py`
- `tools/R9426.cmd`

## R9425 Nachsorge / Diagnostics & Health

Zusätzliche Diagnose-/Health-Entrypoints aus dem jüngsten Stabilisierungslauf:

- `tools/R9421.cmd` / `tools/R9421.py`
  RunnerGuard – prüft aktiven Runner-Bestand, cmd/py-Paare, Compile-Status und Namensschema.
- `tools/R9423.cmd` / `tools/R9423.py`
  SystemHealth – kompakter Gesamtzustandsbericht für Runner, Reports, Protected Runner, GUI-Startschicht und Idea-System.
- `tools/R9424.cmd` / `tools/R9424.py`
  RunnerFailureWatch – konservativer Frühwarn-Runner für Compile-Fails, Failure-Signale und Protected-Runner-Status.

Aktueller GUI-Standardpfad für Runner:
GUI → `modules/toolbar_runner_exec.py` → `run_by_id(...)` → Executor/UI-Sinks → OutputDisplay

OutputDisplay-Standardmarker:
- `RUNNER START: RXXXX`
- `RUNNER END:   RXXXX (rc=...)`

Bekannte offene Punkte:
- Tk-`after`-Cleanup beim GUI-Schließen
- R9424 Signal-Noise reduzieren
