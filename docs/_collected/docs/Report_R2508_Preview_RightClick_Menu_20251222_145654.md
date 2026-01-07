# R2508 – Patch Preview right-click menu (WRITE)

- Time: 20251222_145654
- Root: `C:\Users\rasta\OneDrive\ShrimpDev`
- Target: `modules/ui_runner_products_tab.py`

## Backup
- `C:\Users\rasta\OneDrive\ShrimpDev\_Archiv\ui_runner_products_tab.py.R2508_20251222_145654.bak`

## Added
- Right-click context menu on Preview (tk.Text)
- Inhalt kopieren (selected/all), Pfad kopieren, Datei kopieren (Explorer-Paste)

## Compile
- py_compile: FAIL
- Error: `  File "C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_runner_products_tab.py", line 770
    def _preview_copy_selection_or_all():
    ^^^
SyntaxError: expected 'except' or 'finally' block
`
