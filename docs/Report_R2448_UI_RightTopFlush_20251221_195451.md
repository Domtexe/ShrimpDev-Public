# R2448 UI Fix: Right-top stack flush top-right

- Time: 2025-12-21 19:54:51
- Root: `C:\Users\rasta\OneDrive\ShrimpDev`
- File: `C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_toolbar.py`

## Patch Notes
- OK: header_right.pack -> removed fill='x', keep top-right anchor
- OK: row_push.pack -> removed fill='x', keep top-right anchor
- OK: row0.pack -> removed fill='x', keep top-right anchor

## Compile Check
- py_compile: OK
- output: (no output)

OK: applied + compile-checked.
- Backup: `C:\Users\rasta\OneDrive\ShrimpDev\_Archiv\ui_toolbar.py.R2448_20251221_195451.bak`

