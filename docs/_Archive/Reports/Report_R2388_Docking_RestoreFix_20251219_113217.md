# Report R2388 – Docking Restore Fix

- Timestamp: 2025-12-19 11:32:17
- Root: `C:\Users\rasta\OneDrive\ShrimpDev`

## Backups
- `C:\Users\rasta\OneDrive\ShrimpDev\modules\module_docking.py` -> `module_docking.py.R2388_20251219_113217.bak`
- `C:\Users\rasta\OneDrive\ShrimpDev\main_gui.py` -> `main_gui.py.R2388_20251219_113217.bak`

## module_docking.py
- Before SHA256: `70441fef48b358de39a8d5a030fa1951305673b5e976c3b9bee82470e35d758a`
- FIX: ersetze `win.geometry(` -> `w.geometry(`
- FIX: `restore_geometry` bleibt Geometry-String (kein False), wenn `Docking.<key>.geometry` existiert
- Changed: **True**

## main_gui.py
- Before SHA256: `f8ee03af3b3cd496c1f16362bf93cc7ad9eb3cfb0a1b89bcf780652a90580ae8`
- FIX: main restore liest jetzt fallback aus `[Docking] main.geometry`
- Changed: **True**

## Syntax-Check
- OK: py_compile für beide Dateien

## After (file hashes)
- module_docking.py SHA256: `cb475649b3f92db71b77ce766c12dfa94fae52d7d663396aa04e84a4976528c5`
- main_gui.py SHA256: `9786a40e0b12dcd2b60c807707e414c9531d5419181cb9177241cb08384a543e`