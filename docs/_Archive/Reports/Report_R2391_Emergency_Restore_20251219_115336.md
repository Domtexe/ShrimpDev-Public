# Report R2391 – Syntax Emergency Restore

- Timestamp: 2025-12-19 11:53:36
- Root: `C:\Users\rasta\OneDrive\ShrimpDev`

## Backups (current state)
- `C:\Users\rasta\OneDrive\ShrimpDev\modules\module_docking.py` -> `module_docking.py.R2391_20251219_115336.bak`
- `C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_runner_products_tab.py` -> `ui_runner_products_tab.py.R2391_20251219_115336.bak`

## Candidate backups (newest first)
- module_docking.py: 41 candidates
- ui_runner_products_tab.py: 22 candidates

## Restore attempts
- Try 01: docking=`module_docking.py.R2389_20251219_113442.bak` artefakte=`ui_runner_products_tab.py.R2390_20251219_114951.bak` -> FAIL PyCompileError('  File "D:\\ShrimpDev\\modules\\ui_runner_products_tab.py", line 94\n    if not getattr(win, \'_restored_from_docking\', False):\n    ^^\nSyntaxError: expected \'except\' or \'finally\' block\n', 'SyntaxError', SyntaxError("expected 'except' or 'finally' block", ('D:\\ShrimpDev\\modules\\ui_runner_products_tab.py', 94, 9, "        if not getattr(win, '_restored_from_docking', False):\n", 94, 11)), 'D:\\ShrimpDev\\modules\\ui_runner_products_tab.py')
- Try 02: docking=`module_docking.py.R2389_20251219_113442.bak` artefakte=`ui_runner_products_tab.py.R2391_20251219_115336.bak` -> FAIL PyCompileError('  File "D:\\ShrimpDev\\modules\\ui_runner_products_tab.py", line 94\n    if not getattr(win, \'_restored_from_docking\', False):\n    ^^\nSyntaxError: expected \'except\' or \'finally\' block\n', 'SyntaxError', SyntaxError("expected 'except' or 'finally' block", ('D:\\ShrimpDev\\modules\\ui_runner_products_tab.py', 94, 9, "        if not getattr(win, '_restored_from_docking', False):\n", 94, 11)), 'D:\\ShrimpDev\\modules\\ui_runner_products_tab.py')
- Try 03: docking=`module_docking.py.R2389_20251219_113442.bak` artefakte=`ui_runner_products_tab.py.R2389_20251219_113442.bak` -> OK 

## RESULT
- RESTORED OK:
  - module_docking.py <= `module_docking.py.R2389_20251219_113442.bak`
  - ui_runner_products_tab.py <= `ui_runner_products_tab.py.R2389_20251219_113442.bak`

## Next
- Jetzt `python main_gui.py` starten und prüfen ob GUI läuft.
- Danach: READ-ONLY Diagnose Runner (GeoTrace) bauen, keine Trial&Error-Patches.
