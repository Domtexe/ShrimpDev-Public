# Report R2390 – Crash-Recovery (Rollback)

- Timestamp: 2025-12-19 11:49:51
- Root: `C:\Users\rasta\OneDrive\ShrimpDev`

## Backups (current state)
- `C:\Users\rasta\OneDrive\ShrimpDev\modules\module_docking.py` -> `module_docking.py.R2390_20251219_114951.bak`
- `C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_runner_products_tab.py` -> `ui_runner_products_tab.py.R2390_20251219_114951.bak`

## Restores (from _Archiv)
- `module_docking.py` <= `module_docking.py.R2389_20251219_113442.bak`
- `ui_runner_products_tab.py` <= `ui_runner_products_tab.py.R2390_20251219_114951.bak`

## Syntax-Check (py_compile)
- OK: module_docking.py
- FAIL: PyCompileError('  File "D:\\ShrimpDev\\modules\\ui_runner_products_tab.py", line 94\n    if not getattr(win, \'_restored_from_docking\', False):\n    ^^\nSyntaxError: expected \'except\' or \'finally\' block\n', 'SyntaxError', SyntaxError("expected 'except' or 'finally' block", ('D:\\ShrimpDev\\modules\\ui_runner_products_tab.py', 94, 9, "        if not getattr(win, '_restored_from_docking', False):\n", 94, 11)), 'D:\\ShrimpDev\\modules\\ui_runner_products_tab.py')