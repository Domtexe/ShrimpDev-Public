# ShrimpDev – Architektur

Dieses Dokument beschreibt die Architektur von ShrimpDev.

## Docking & Window Lifecycle

### Verantwortung (Ownership)
- `modules/module_docking.py` ist der alleinige Owner für Dock/Undock-Fenster (Read-Only Viewer).
- Tab-Builder (`ui_pipeline_tab`, `ui_runner_products_tab`, `ui_log_tab`) bauen Inhalte in ein Parent-Widget, erzeugen aber keine eigenen Fenster.

### Persistenz-Quelle
- `ShrimpDev.ini` ist die Single Source of Truth für `[Docking]`.
- Relevante Keys pro Fenster: `<key>.open`, `<key>.docked`, `<key>.geometry`, `<key>.ts`.

### Restore-Reihenfolge (verbindlich)
1. INI laden
2. `open/docked` auswerten: restore nur wenn `open=1` und `docked=0`
3. Geometry bevorzugen: `<key>.geometry` (Format `WxH+X+Y`)
4. Fallback nur wenn nötig: legacy `w/h/x/y` verwenden, wenn `geometry` fehlt
5. Offscreen-Schutz: ist die Geometry offscreen, dann erst fallback/center

### Verbotene Muster (Regression-Guards)
- Kein Zentrieren nach erfolgreichem Restore (Center ist nur Offscreen-/No-Geo-Fallback).
- Keine Fenstererzeugung (`tk.Toplevel`) in Tab-Buildern.

