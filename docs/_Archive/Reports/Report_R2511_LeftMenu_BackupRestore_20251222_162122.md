# R2511 – Left menu: Backup wiederherstellen (SAFE)

- Time: 20251222_162122
- Root: `C:\Users\rasta\OneDrive\ShrimpDev`
- Target: `modules/ui_runner_products_tab.py`

## Backup
- `C:\Users\rasta\OneDrive\ShrimpDev\_Archiv\ui_runner_products_tab.py.R2511_20251222_162122.bak`

## Behavior
- Menu entry only appears if selected path is `_Archiv\*.bak`
- Restore searches for exactly one target filename match outside `_Archiv/_Snapshots`
- If ambiguous/missing: no restore, shows candidates and copies list to clipboard
- Before overwrite: creates safety backup of target in `_Archiv`

## Compile
- py_compile: FAIL
- Error: `  File "C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_runner_products_tab.py", line 869
    m.add_separator()
SyntaxError: expected 'except' or 'finally' block
`
