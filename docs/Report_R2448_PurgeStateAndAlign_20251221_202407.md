# R2448 UI: Purge state + top-right alignment

- Time: 2025-12-21 20:24:07
- Root: `C:\Users\rasta\OneDrive\ShrimpDev`
- File: `C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_toolbar.py`

## Actions

- OK: added _purge_plan_ok() helper
- OK: injected purge state logic into _update_push_states()
- OK: btn_apply right-edge padding set to padx=(6,0)
- OK: btn_scan padding set to padx=(6,0)

- Backup: `C:\Users\rasta\OneDrive\ShrimpDev\_Archiv\ui_toolbar.py.R2448_20251221_202407.bak`

## Compile

- ERROR: compile failed after patch: `PyCompileError('Sorry: IndentationError: expected an indented block after function definition on line 820 (ui_toolbar.py, line 821)', 'IndentationError', IndentationError('expected an indented block after function definition on line 820', ('C:\\Users\\rasta\\OneDrive\\ShrimpDev\\modules\\ui_toolbar.py', 821, 9, '        try:\n', 821, 12)), 'C:\\Users\\rasta\\OneDrive\\ShrimpDev\\modules\\ui_toolbar.py')`
- Rolled back to original.
- Compile after rollback: OK ``
