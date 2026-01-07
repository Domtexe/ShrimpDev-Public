# R2463 – Patch: remove purge gating from nested _update_push_states

- Time: 20251222_004434
- Root: `C:\Users\rasta\OneDrive\ShrimpDev`
- Target: `modules/ui_toolbar.py`
- Range: L833–L908

## Änderung
- Entfernt purge-gating Zeilen innerhalb `_update_push_states()` (dropped=5).
- Purge Enable/Disable bleibt in `_update_purge_states()`.

## Backup
- `C:\Users\rasta\OneDrive\ShrimpDev\_Archiv\ui_toolbar.py.R2463_20251222_004434.bak`

## Compile
- py_compile: FAIL
- Error: `Sorry: IndentationError: expected an indented block after 'try' statement on line 858 (ui_toolbar.py, line 859)`
