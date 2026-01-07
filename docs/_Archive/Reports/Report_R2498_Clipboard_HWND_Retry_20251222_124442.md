# R2498 – Patch clipboard: HWND + retry + error diagnostics

- Time: 20251222_124442
- Target: `modules/ui_runner_products_tab.py`

## Backup
- `C:\Users\rasta\OneDrive\ShrimpDev\_Archiv\ui_runner_products_tab.py.R2498_20251222_124442.bak`

## Compile
- py_compile: OK


## Behavior change
- Uses tree.winfo_id() as OpenClipboard owner HWND
- Retries OpenClipboard up to 5 times
- Returns detailed GetLastError on failure
