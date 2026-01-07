# R2502 – Fix SyntaxError (glued newline)

- Time: 20251222_133621
- Target: `modules/ui_runner_products_tab.py`

## Change
- Repaired 'pass if hfx and fmt:' into two lines

## Backup
- `C:\Users\rasta\OneDrive\ShrimpDev\_Archiv\ui_runner_products_tab.py.R2502_20251222_133621.bak`

## Compile
- py_compile: FAIL
- Error: `Sorry: IndentationError: expected an indented block after 'if' statement on line 168 (ui_runner_products_tab.py, line 169)`
