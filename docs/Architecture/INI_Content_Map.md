# INI Content Map

- Generated: `20260111_075157`
- Root: `C:\Users\rasta\OneDrive\ShrimpDev_REPO`
- Files scanned: `89` (main_gui + modules)

## Purpose
This document is the **contract map** for INI persistence: sections, keys, likely owners, and write callsites.

## Sections & Keys
### [Intake]
- Owner (guess): `modules/ui_left_panel.py`
- Keys:
  - `last_target_dir` (writes observed: 1)
    - examples:
      - `modules\ui_left_panel.py:123`

### [LogWindow]
- Owner (guess): `modules/ui_toolbar.py`
- Keys:
  - `geometry` (writes observed: 1)
    - examples:
      - `modules\ui_toolbar.py:546`

### [UI]
- Owner (guess): `main_gui.py`
- Keys:
  - `always_on_top` (writes observed: 2)
    - examples:
      - `main_gui.py:194`
      - `main_gui.py:461`
  - `geometry` (writes observed: 4)
    - examples:
      - `main_gui.py:452`
      - `modules\module_docking.py:1295`
      - `modules\module_docking_FIXED_v2.py:1164`
      - `modules\module_docking_manuell_20260108_224600.py:1191`
  - `last_tab` (writes observed: 1)
    - examples:
      - `main_gui.py:468`
  - `maximized` (writes observed: 2)
    - examples:
      - `main_gui.py:447`
      - `main_gui.py:449`

## INI Write Callsites (high signal)
- `main_gui.py:473`  `config_loader.save(cfg)`
- `modules\config_loader manuell 20260111_011600.py:9`  `- config_loader.save(cfg)`
- `modules\config_loader manuell 20260111_011600.py:183`  `ini_writer.write_configparser_atomic(path, cfg)`
- `modules\config_loader.py:10`  `- config_loader.save(cfg)`
- `modules\config_loader.py:186`  `ini_writer.write_configparser_atomic(str(p), cfg)  # type: ignore[attr-defined]`
- `modules\config_loader.py:194`  `cfg.write(f)`
- `modules\config_loader.py:198`  `cfg.write(f)`
- `modules\config_mgr.py:9`  `- config_loader.save(cfg)`
- `modules\ini_writer.py:206`  `def write_configparser_atomic(path, cfg) -> None:`
- `modules\ini_writer.py:215`  `cfg.write(f)`
- `modules\logic_actions.py:1275`  `"""ShrimpDev.ini ueber modules.config_loader.save() speichern."""`
- `modules\logic_actions.py:1558`  `"""ShrimpDev.ini ueber modules.config_loader.save() speichern."""`
- `modules\module_docking.py:100`  `config_loader.save(cfg)`
- `modules\module_docking.py:196`  `cfg.write(f)`
- `modules\module_docking.py:201`  `cfg.write(f)`
- `modules\module_docking.py:401`  `config_loader.save(cfg)`
- `modules\module_docking_FIXED_v2.py:92`  `cfg.write(f)`
- `modules\module_docking_FIXED_v2.py:97`  `cfg.write(f)`
- `modules\module_docking_FIXED_v2.py:271`  `config_loader.save(cfg)`
- `modules\module_docking_manuell_20260108_224600.py:271`  `_iw.write_configparser_atomic(path, cfg)`
- `modules\module_docking_manuell_20260108_224600.py:297`  `_iw.write_configparser_atomic(path, cfg)`
- `modules\ui_filters.py:48`  `config_loader.save(cfg)`
- `modules\ui_filters.py:64`  `config_loader.save(cfg)`

## [Docking]
Owner: modules/module_docking.py
Write-API: DockingManager.persist_all()  (intern: Merge->SingleWriter via config_loader.save)
Read-API:  DockingManager.restore_all()  (intern: config_loader.load / redirected canonical INI)

Write-Trigger (verbindlich):
- Main Close (WM_DELETE_WINDOW / tatsächlicher Close-Handler)
- Undock eines Tabs (wenn Tab final undocked ist)
- Optional: Geometry/AOT Change (nur wenn wir später “live persist” wollen)

Key-Schema (canonical):
- keys: CSV Liste der Docking-Keys (z.B. log,main,pipeline,runner_products)
- <key>.open: 0|1
- <key>.docked: 0|1
- <key>.geometry: Tk geometry string (z.B. 1263x726+0+10)
- <key>.ts: timestamp (YYYY-MM-DD HH:MM:SS) – debug/forensics
- <key>.aot: 0|1 (optional, nur für undocked windows relevant)
- last_active: <key> (zuletzt aktiver Tab)

Notes:
- Root-INI ist verboten. Canonical ist registry/ShrimpDev.ini.
- module_docking darf NIE direkt cfg.write() benutzen (Contract: Single Writer).
