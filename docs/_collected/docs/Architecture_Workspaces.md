# Workspaces (Registry)

Kanonische Quelle: `registry/workspaces.json`

API: `modules/workspace_registry.py`

- `get_active_workspace_root()` liefert den Root-Pfad für alle Workspace-abhängigen Aktionen.
- UI/Tools dürfen keine alten Hardcodes auf OneDrive/D:/ etc. behalten; stattdessen immer den Workspace-Root verwenden.

Erst-Setup via Runner: R2436

