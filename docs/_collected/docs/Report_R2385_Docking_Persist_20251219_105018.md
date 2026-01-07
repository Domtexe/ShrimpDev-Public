# Report R2385 – Docking Persist before Restart/Close

- Timestamp: 2025-12-19 10:50:18
- Changed files: 2
  - C:\Users\rasta\OneDrive\ShrimpDev\main_gui.py
  - C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_toolbar.py

## Backups
- C:\Users\rasta\OneDrive\ShrimpDev\_Archiv\main_gui.py.R2385_20251219_105018.bak
- C:\Users\rasta\OneDrive\ShrimpDev\_Archiv\ui_toolbar.py.R2385_20251219_105018.bak

## Notes
- main_gui: dm.persist_all() before destroy() (best-effort)
- ui_toolbar: in effective restart override, dm.persist_all() after save_state
