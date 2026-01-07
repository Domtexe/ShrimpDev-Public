# R2485 – Extend right-list context menu (enable_context_menu)

- Time: 20251222_102819
- Target: `modules/ui_project_tree.py`

## Change
- Added menu items: Datei(en) kopieren (Paste) + Backup wiederherstellen…
- Uses Windows CF_HDROP + Preferred DropEffect COPY

## Backup
- `C:\Users\rasta\OneDrive\ShrimpDev\_Archiv\ui_project_tree.py.R2485_20251222_102819.bak`

## Compile
- py_compile: FAIL
- Error: `Sorry: IndentationError: unexpected indent (ui_project_tree.py, line 1037)`
