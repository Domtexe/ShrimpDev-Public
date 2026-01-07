# R2499 – Patch: Clipboard typing fix (GlobalLock invalid handle)

- Time: 20251222_125817
- Target: `modules/ui_runner_products_tab.py`

## Backup
- `C:\Users\rasta\OneDrive\ShrimpDev\_Archiv\ui_runner_products_tab.py.R2499_20251222_125817.bak`

## Compile
- py_compile: OK


## Expected result
- Fixes GetLastError=6 by enforcing correct WinAPI argtypes/restype on 64-bit.
