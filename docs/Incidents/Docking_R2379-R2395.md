# Incident: Docking Restore Regression (R2379–R2395)

- Date: 2025-12-19
- Scope: Read-Only Viewer Docking (Pipeline/Log/Artefakte) + Main window geometry

## Symptome
- Nach Restart kamen Pipeline/Log/Artefakte wieder hoch, auch wenn vorher geschlossen.
- Fenster wurden zentriert (statt gespeicherter Position).
- Main-Fenster driftete leicht bei jedem Restart.

## Root Cause
- Restore-Pfad berücksichtigte `Docking.<key>.open` nicht strikt.
- Restore verwendete bevorzugt legacy `w/h/x/y` oder erzeugte `restore_geo=None` → Center-Fallback.

## Fix (R2395)
- `restore_from_ini()` respektiert `open=1` und `docked=0`.
- `<key>.geometry` (`WxH+X+Y`) wird priorisiert.
- Fallback auf `w/h/x/y` nur wenn `geometry` fehlt.
- Offscreen-Guard verhindert Restore außerhalb des sichtbaren Bereichs.

## Verifikation
- Geschlossene Fenster bleiben geschlossen nach Restart.
- Offene Fenster kommen mit gespeicherter Geometry zurück (kein erzwungenes Centering).

