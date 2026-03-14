# Architecture Index

This file is the navigation index for architecture documentation in `ShrimpDev_REPO`.

See also:
- [ARCHITECTURE.md](ARCHITECTURE.md) for the canonical high-level overview
- [FILE_MAP.md](FILE_MAP.md) for repository-level navigation and ownership
- [FILE_MAP_TECH.md](FILE_MAP_TECH.md) for technical entrypoints and relationships

## High-level overview

- [ARCHITECTURE.md](ARCHITECTURE.md) — canonical high-level repository architecture overview

## Subsystem architecture docs

- [Architecture_RunnerExecution.md](Architecture_RunnerExecution.md) — canonical runner execution path and allowed exceptions
- [ARCHITECTURE_PERSISTENCE.md](ARCHITECTURE_PERSISTENCE.md) — high-level persistence and INI architecture
- [Architecture_Docking.md](Architecture_Docking.md) — docking persist/restore behavior
- [Architecture_ContextMenus.md](Architecture_ContextMenus.md) — context menu architecture and interaction rules
- [Architecture_ProjectTab.md](Architecture_ProjectTab.md) — project tab GUI architecture
- [Architecture_Tools.md](Architecture_Tools.md) — tools, cleanup, and tool-surface policy
- [Architecture_Purge_Actions.md](Architecture_Purge_Actions.md) — purge action to runner mapping
- [Architecture_Actions_and_Gating.md](Architecture_Actions_and_Gating.md) — action surfaces and gating rules
- [Architecture_Workspaces.md](Architecture_Workspaces.md) — workspace and registry behavior
- [Architecture_Config.md](Architecture_Config.md) — config-related notes; purpose is partly historical
- [Architecture_Guard.md](Architecture_Guard.md) — guard and single-writer policy
- [Architecture_StabilityPolicy.md](Architecture_StabilityPolicy.md) — repository stability policy
- [Architecture_DnD_FileOut.md](Architecture_DnD_FileOut.md) — drag-and-drop file-out behavior
- [Architecture_ShrimpDev.md](Architecture_ShrimpDev.md) — older ShrimpDev architecture overview with runtime-specific detail
- [Architecture_ShrimpDev_ContextState.md](Architecture_ShrimpDev_ContextState.md) — context-state bugfix and behavior notes
- [ARCHITEKTUR_ShrimpDev_vs_ShrimpHub.md](ARCHITEKTUR_ShrimpDev_vs_ShrimpHub.md) — comparison architecture between ShrimpDev and ShrimpHub

## Architecture folder docs

- [Docking_Persist_Contract.md](Architecture/Docking_Persist_Contract.md) — docking persistence contract
- [Current/Docking_Persist_Current.md](Architecture/Current/Docking_Persist_Current.md) — current docking state and reference behavior
- [runner_execution.md](Architecture/runner_execution.md) — canonical path and gateway pattern for runner execution
- [Runner_Reference_Policy.md](Architecture/Runner_Reference_Policy.md) — policy for active vs. historical runner references
- [agent_guard.md](Architecture/agent_guard.md) — mini-architecture for agent and guard behavior
- [INI_SingleWriter.md](Architecture/INI_SingleWriter.md) — INI single-writer architecture
- [INI_SingleWriter_API.md](Architecture/INI_SingleWriter_API.md) — API-level single-writer detail
- [INI_SingleWriter_Migration.md](Architecture/INI_SingleWriter_Migration.md) — migration notes for the single-writer model
- [INI_Canonical_Path_and_SingleWriter.md](Architecture/INI_Canonical_Path_and_SingleWriter.md) — canonical INI path and write ownership
- [INI_Content_Map.md](Architecture/INI_Content_Map.md) — content map of INI sections and usage
- [WEBSITE_SYSTEM.md](Architecture/WEBSITE_SYSTEM.md) — website-system architecture lane
- [Hardening_Plan_LaneB_Executor_UI_Toolbar.md](Architecture/Hardening_Plan_LaneB_Executor_UI_Toolbar.md) — hardening/action-plan doc for executor and toolbar

## Historical, map, and analysis docs

- [ARCHITECTURE_MAP.md](ARCHITECTURE_MAP.md) — generated architecture map; useful as supporting inventory, not the canonical overview
- [Architecture_Lessons_Learned.md](Architecture_Lessons_Learned.md) — lessons learned and governance insights
- [Archive/ShrimpDev_Architecture.md](Architecture/Archive/ShrimpDev_Architecture.md) — archived older architecture overview

## Role Notes

- `ARCHITECTURE.md` is the canonical high-level overview.
- Subsystem docs remain authoritative for their own topic.
- Generated maps, archived docs, and lessons-learned notes should support orientation, not replace topic docs.
- Some older documents overlap in naming; they are kept because they still contain topic-specific or historical value.

## Maintenance

Refresh this file when:
- architecture changes
- entrypoints change
- new subprojects are added
- runner workflows change
- Excel/VBA project structure changes
- major UI structure changes
