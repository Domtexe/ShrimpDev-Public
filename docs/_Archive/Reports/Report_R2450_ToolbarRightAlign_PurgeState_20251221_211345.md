# R2450 UI Toolbar Fix: right-top alignment + Purge state

- Time: 2025-12-21 21:13:45
- Root: `C:\Users\rasta\OneDrive\ShrimpDev`
- File: `C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_toolbar.py`

## Backup
- `C:\Users\rasta\OneDrive\ShrimpDev\_Archiv\ui_toolbar.py.R2450_20251221_211345.bak`

## Actions
- WARN: header_right.pack(fill="x"... ) not found (no change)
- WARN: _set_btn_state not found (no guard injected)
- OK: injected purge enable/disable logic into _update_push_states()
- OK: wired btn_scan into purge_btns["scan"]
- OK: wired btn_apply into purge_btns["apply"]

## Compile
- OK: py_compile passed
