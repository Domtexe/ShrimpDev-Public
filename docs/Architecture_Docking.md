
# Docking Persist/Restore (R2339)

- Persistiert Undocked-Fenster in ShrimpDev.ini unter [Docking] (w/h/x/y, keys).
- Restore beim Start: DockManager.restore_from_ini() wird einmalig nach DockManager-Erzeugung aufgerufen.
- Center nur beim ersten Öffnen; beim Restore wird keine Center-Logik ausgeführt.
- Offscreen-Schutz: wenn gespeicherte Position außerhalb Screen, wird Default (Center) verwendet.
- Main-Window wird nicht angefasst.

## R2340 Robustness Fix
- Persist nutzt wm_geometry() und parst WxH+X+Y (robuster als winfo_*).
- Restore wendet geometry per after_idle einmalig an (kein Auto-Refresh), um WM-Overrides zu verhindern.
- Offscreen-Check via sichtbare Fläche statt harter Grenzen.

## R2343 Hard-INI Geometry Persist
- INI-Pfad ist hart auf Projektroot/ShrimpDev.ini gesetzt (keine config_manager-Ableitung).
- Persist schreibt <key>.geometry = WxH+X+Y zusätzlich zu w/h/x/y.
- keys wird erweitert (z.B. log,runner_products,pipeline).

## R2352 (Restore Fix)
- Bugfix: Entfernt kaputten Aufruf mit undefinierten cfg/sec in undock_readonly().
- Restore-Fallback: liest x/y/w/h aus ShrimpDev.ini und baut restore_geometry, auch wenn Screen-Size beim Boot noch 0 ist.
- Center nur, wenn wirklich keine Restore-Daten vorhanden sind.

## Docking State Persistence
_added 2026-01-08 12:26 via R3147_

## Persist & Restore Semantics
- Docking persistence stores **runtime state only**.
- All undocked windows at shutdown are persisted with `.open = 1`.
- Restore recreates exactly these windows.

### Defaults
- Defaults (e.g. only `main`) are applied **only** via explicit reset or first-run.
- Persistence must never enforce defaults.
