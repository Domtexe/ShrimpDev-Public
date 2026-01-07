# R2497 – Patch: Left Artefakte menu add Datei kopieren (Explorer-Paste)

- Time: 20251222_114551
- Target: `modules/ui_runner_products_tab.py`

## Changes
- Added Windows CF_HDROP clipboard helpers (module-level)
- Added _on_copy_file_paste() action near _tree_context_menu
- Added menu entry after 'Pfad kopieren'

## Backup
- `C:\Users\rasta\OneDrive\ShrimpDev\_Archiv\ui_runner_products_tab.py.R2497_20251222_114551.bak`

## Compile
- py_compile: OK

