# R2500 – Patch: Clipboard dual-format (CF_HDROP + CF_UNICODETEXT)

- Time: 20251222_131710
- Target: `modules/ui_runner_products_tab.py`

## Backup
- `C:\Users\rasta\OneDrive\ShrimpDev\_Archiv\ui_runner_products_tab.py.R2500_20251222_131710.bak`

## Compile
- py_compile: FAIL
- Error: `  File "C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_runner_products_tab.py", line 167
    pass        if hfx and fmt:
                ^^
SyntaxError: invalid syntax
`

## Result
- Explorer Ctrl+V: file copy via CF_HDROP
- Chat/Editor paste: plaintext path list via CF_UNICODETEXT
