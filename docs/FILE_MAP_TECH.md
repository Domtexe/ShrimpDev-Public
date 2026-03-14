# FILE MAP TECH

This file is the technical companion to `docs/FILE_MAP.md`.

It focuses on execution flow, subsystem boundaries, and practical entrypoints for diagnostics and patches.

See also:
- [FILE_MAP.md](FILE_MAP.md) for repository navigation and ownership orientation
- [ARCHITECTURE.md](ARCHITECTURE.md) for the high-level architecture view
- [ARCH_INDEX.md](ARCH_INDEX.md) for architecture document navigation

## 1. Main entrypoints

### GUI path

- `main_gui.py`
  Bootstraps the Tkinter app and imports the main UI modules.
- Main imported UI anchors visible at the top of `main_gui.py`:
  - `modules.ui_menus`
  - `modules.ui_toolbar`
  - `modules.ui_filters`
  - `modules.ui_project_tree`
  - `modules.ui_left_panel`
  - `modules.ui_leds`
  - `modules.ui_settings_tab`
  - `modules.ui_pipeline_tab`
  - `modules.ui_runner_products_tab`
  - `modules.module_docking`

### Runner path

- UI actions route into:
  - `modules.logic_actions`
  - `modules.toolbar_action_router`
  - `modules.toolbar_runner_exec`
- Actual runner launch is centered on:
  - `modules/module_runner_exec.py`

## 2. Important modules and responsibilities

### Runner and action layer

- `modules/module_runner_exec.py`
  Main CMD-first execution engine for `tools/R####.cmd` and paired Python runners.
- `modules/logic_actions.py`
  Action routing for toolbar operations and service-style commands.
- `modules/toolbar_runner_exec.py`
  Toolbar-side execution bridge into the runner layer.
- `modules/toolbar_action_router.py`
  Action dispatch / routing around toolbar interactions.

### UI composition layer

- `main_gui.py`
  Application composition root and import hub for UI modules.
- `modules/ui_toolbar.py`
  Right-toolbar construction and frequent UI hotspot.
- `modules/ui_output_display.py`
  Output/log display surface used by runner execution feedback.
- `modules/ui_project_tree.py`
  Project tree population, selection, and run context.
- `modules/module_docking.py`
  Pane and docking structure around the main app layout.

### Intake and transformation layer

- `modules/logic_intake.py`
  Intake orchestration for incoming content/files.
- `modules/module_code_intake.py`
  Main intake subsystem.
- `modules/module_code_intake_v1.py`
  Older intake path still kept in the repo.
- `modules/module_intake_workers.py`
  Background work for intake processing.

### State, config, registry

- `modules/config_loader.py`
  Configuration loading.
- `modules/config_manager.py`
  Configuration management and persistence.
- `modules/context_state.py`
  Shared application state layer.
- `modules/module_registry.py`
  Registry logic.
- `modules/workspace_registry.py`
  Workspace-scoped registry support.

### Logging, safety, and patch support

- `modules/exception_logger.py`
  Error and runner logging.
- `modules/module_preflight.py`
  Preflight and readiness checks.
- `modules/preflight_checks.py`
  Additional validation helpers.
- `tools/patch_engine.py`
  Patch-oriented helper tooling.

## 3. Module relationships / imports (high level)

- `main_gui.py` imports and composes the main UI layer.
- `modules/ui_toolbar.py`, `modules/ui_project_tree.py`, and `modules/ui_output_display.py` are the key right-side interaction surfaces.
- UI actions generally route through `modules/logic_actions.py` and related toolbar helpers.
- Runner execution converges on `modules/module_runner_exec.py`.
- Reports and debug traces flow into `Reports/` and `debug_output.txt`.
- Intake-related tasks should trace through `modules/logic_intake.py` into the code-intake modules before changing behavior.

## 4. Runner execution flow

`module_runner_exec.py` describes the intended runner model clearly:

- start runners through `tools/R####.cmd`
- auto-create missing `.cmd` wrappers next to `tools/R####.py`
- execute non-blocking in a thread
- stream stdout to:
  - `debug_output.txt`
  - optional UI sinks
- write captured output to `Reports/`

Practical implication:
- the runner pair `.cmd + .py` is the stable unit
- direct ad hoc execution is secondary to the CMD-first workflow

## 5. UI architecture relationships

### Stable high-value UI files

- `main_gui.py`
  App root and composition layer.
- `modules/ui_output_display.py`
  Output/log surface.
- `modules/ui_toolbar.py`
  Toolbar layout and toolbar-triggered behaviors.
- `modules/ui_project_tree.py`
  File/project tree behavior.
- `modules/ui_pipeline_tab.py`
  Pipeline work surface.
- `modules/ui_runner_products_tab.py`
  Runner output / product presentation.

### Related support files

- `modules/common_tabs.py`
  Shared tab helpers.
- `modules/ui_statusbar.py`
  Status bar presentation.
- `modules/ui_theme_classic.py`
- `modules/ui_themes.py`
  Theme handling.

Important relationship note:
- the repo rules emphasize a right-side stack of Output -> Toolbar -> Tree
- UI patches should preserve that structure unless the task explicitly changes it

## 6. Excel/VBA integration notes

Excel work is repo-local but operationally separate from the Python GUI.

Primary area:
- `Excel-Projekte/Dispo-Tool`

Common VBA modules encountered recently:
- `modDispoAssign`
- `modMail`
- `modPlanStore`
- `modPlanDateUI`

Useful technical rule:
- treat workbook exports and workbook copies as the patch surface
- do not assume the Python app and the Excel tools share runtime behavior

Workday / calendar note:
- `modPlanDateUI` contains known helpers such as `NextWorkdayNRW` and `IsHolidayNRW`
- for VBA mail/status tasks mentioning workdays or NRW holidays, check these helpers first

## 7. High-risk / high-change files

- `main_gui.py`
  High-impact composition root; changes here can affect multiple tabs and import paths.
- `modules/ui_toolbar.py`
  High-change UI hotspot tied to action wiring and right-panel layout rules.
- `modules/logic_actions.py`
  High-risk because action dispatch errors affect delete/rename/push/purge flows.
- `modules/module_runner_exec.py`
  High-risk because runner launch/capture issues break the core DIAG/FIX/VERIFY workflow.
- `modules/ui_project_tree.py`
  High-change because tree selection state is central to runner targeting.
- `Excel-Projekte/Dispo-Tool/*.xlsm`
  High-risk because workbook structure and VBA module imports require precise scope control.

## 8. Scope boundaries / patch hotspots

### Safe documentation scope

- `docs/`
  Preferred area for repo maps, architecture notes, and workflow guidance.

### Common Python patch hotspots

- `modules/ui_toolbar.py`
- `modules/ui_project_tree.py`
- `modules/logic_actions.py`
- `modules/module_runner_exec.py`

These are common patch surfaces, but they are also high-regression areas.

### Excel patch boundary

- `Excel-Projekte/`
  Excel/VBA work should stay isolated from Python GUI patches unless the task explicitly spans both.

### Archive boundary

- `_Archiv/`, `_Archive/`, `_Backups/`, `tools/Archiv/`
  Useful for forensics only. Do not treat them as active architecture.

## 9. Idea inbox subsystem

The idea-inbox feature spans both docs and modules:

- Docs:
  - `docs/IDEA_INBOX.md`
  - `docs/IDEA_INBOX_SPEC.md`
- GUI / logic:
  - `modules/idea_inbox_gui.py`
  - `modules/idea_inbox_status.py`
  - `modules/idea_import_button.py`
  - `modules/idea_editor_gui.py`

Use this subsystem when the task mentions:
- imported ideas
- inbox state
- title indicators
- idea editor / import flow

## 10. Low-value areas to summarize only

These areas exist but should usually not be expanded in technical docs:
- `__pycache__/`
- `.ruff_cache/`
- historical runner archives in `tools/Archiv/`
- archive-heavy roots such as `_Archiv/`, `_Archive/`, `_Backups/`

They are useful for forensics, not for day-to-day architecture mapping.

## Maintenance

Refresh this file when:
- architecture changes
- entrypoints change
- new subprojects are added
- runner workflows change
- Excel/VBA project structure changes
- major UI structure changes
