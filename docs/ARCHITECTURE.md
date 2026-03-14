# Architecture Overview

This file is the canonical high-level architecture overview for `ShrimpDev_REPO`.

Use it to understand repository layers, key entrypoints, and patch boundaries.
Detailed subsystem documents remain authoritative for their own topic.
For navigation across architecture documents, see [ARCH_INDEX.md](ARCH_INDEX.md).
For repository navigation and ownership orientation, see [FILE_MAP.md](FILE_MAP.md).
For technical entrypoints and relationships, see [FILE_MAP_TECH.md](FILE_MAP_TECH.md).

## Scope and Role

This overview is intentionally curated.
It does not replace subsystem documents such as docking, runner execution, persistence, tools, or workspace architecture.

## Repository Layers

### Governance and docs layer
- `docs/MasterRules.md` defines repo-wide governance and working rules.
- `docs/PIPELINE.md` is the planning and prioritization SSOT.
- `docs/SHORTCODES.md` captures recurring workflow patterns.
- `AGENTS.md` defines Codex operating rules for this repository.

### Main GUI layer
- `main_gui.py` is the primary application entrypoint and top-level UI orchestrator.
- The GUI composes tabs, shared panels, and runtime wiring across the module layer.

### Module layer
- `modules/` contains the runtime Python modules.
- Major responsibilities include UI composition, runner execution, persistence, tree handling, and domain-specific actions.

### Runner and tooling layer
- `tools/` contains numbered runners in the `R####.cmd` + `R####.py` pattern.
- Runners are used for diagnosis, minimal patches, verification, repo tooling, exports, and automation support.

### Reports, backups, and archive layer
- `Reports/` stores runner and task reports.
- `Backups/`, `_Archiv/`, and similar areas hold historical or recovery artifacts.
- These areas are operationally important, but they are not primary architecture entrypoints.

### Excel/VBA layer
- `Excel-Projekte/` contains Excel-based subprojects with workbook and VBA logic.
- `Excel-Projekte/Dispo-Tool` is a major domain area with workbook-driven logic and modules such as `modDispoAssign`, `modMail`, and related planning/status code.

### Subproject layer
- The repository also contains subprojects, experiments, and product-specific document areas.
- These should be treated as bounded contexts rather than folded into the main GUI/runtime architecture.

## Major Architectural Areas

- GUI shell and runtime orchestration: `main_gui.py`, `modules/ui_*`, selected `modules/module_*`
- Runner execution and gating: `tools/`, `modules/toolbar_runner_exec.py`, runner governance docs
- Persistence and registry/INI behavior: documented in persistence and INI architecture docs
- Docking and window lifecycle: documented in docking architecture docs
- Tools, purge, and cleanup policy: documented in tools and purge architecture docs
- Workspaces, context state, and project surfaces: documented in workspace/project/context docs
- Excel/VBA workflows: workbook-specific and intentionally separate from the Python runtime

## Key Debugging Entrypoints

- `main_gui.py` for application startup issues
- `modules/ui_toolbar.py` for runner launch wiring
- `modules/ui_project_tree.py` for tool tree behavior
- `modules/toolbar_runner_exec.py` for canonical runner execution flow
- `tools/R####*.cmd` and `tools/R####*.py` for runner-specific diagnosis/fix flows
- `Excel-Projekte/Dispo-Tool` for workbook/VBA-specific troubleshooting

## High-Risk Areas

- `main_gui.py`
  - central runtime entrypoint; changes can affect broad UI behavior
- `modules/ui_toolbar.py`
  - sensitive because toolbar layout and runner wiring are tightly governed
- `modules/toolbar_runner_exec.py`
  - canonical execution path for runners
- persistence and docking code
  - small regressions can break restore state, window behavior, or configuration writes
- `Excel-Projekte/Dispo-Tool`
  - workbook logic is stateful and patch-sensitive; keep Python and VBA scopes clearly separated

## Detailed Architecture Documents

Use [ARCH_INDEX.md](ARCH_INDEX.md) as the document map.
Important detail documents include:

- `Architecture_RunnerExecution.md`
- `ARCHITECTURE_PERSISTENCE.md`
- `Architecture_Docking.md`
- `Architecture_ContextMenus.md`
- `Architecture_ProjectTab.md`
- `Architecture_Tools.md`
- `Architecture_Workspaces.md`
- `Architecture_Actions_and_Gating.md`

## Maintenance

Refresh this file when:
- architecture layers change
- entrypoints change
- new major subsystems are added
- runner workflows change materially
- Excel/VBA project structure changes
- major UI structure changes
