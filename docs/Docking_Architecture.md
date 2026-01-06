# Docking – Architektur & Persistenz

Dieses Dokument beschreibt das Docking/Undocking der Read-Only Viewer (Pipeline, Log, Artefakte).

## Begriffe
- **Docked**: Tab im Notebook (kein Extra-Fenster).
- **Undocked**: eigenes Toplevel-Fenster, verwaltet durch `module_docking.py`.

## Ownership
- Window-Lifecycle (erzeugen, schließen, persistieren, restoren) liegt ausschließlich in:
  - `modules/module_docking.py`
- Tab-Builder erzeugen Inhalte im Parent-Widget, aber keine Fenster.

## Persistenz in ShrimpDev.ini
Section: `[Docking]`

Pro Key (z. B. `pipeline`, `log`, `runner_products`, `main`):
- `<key>.open`   : `1` wenn undocked Fenster beim letzten Persist offen war
- `<key>.docked` : `1` wenn docked (Tab), `0` wenn undocked
- `<key>.geometry`: `WxH+X+Y`
- `<key>.ts`     : Timestamp der letzten Persist

## Restore-Regeln (verbindlich)
1) Restore nur wenn `open=1` und `docked=0`
2) Geometry bevorzugen: `<key>.geometry`
3) Fallback: legacy `w/h/x/y`, falls `geometry` fehlt
4) Offscreen-Guard: Offscreen Geometry wird verworfen; dann erst center/fallback

## Anti-Pattern (nicht zulässig)
- Nach Restore pauschal zentrieren (führt zu ständigem Zentrieren trotz gespeicherter Geo).
- Tab-Builder bauen eigene `tk.Toplevel`-Fenster (führt zu doppeltem Window-Management).
- Restore ignoriert `<key>.open` (öffnet geschlossene Fenster wieder).

## Purge UX – Anzeigeprinzip (verbindlich)
- Purge-Runner (z. B. R2218/R2224) arbeiten headless und erzeugen Reports.
- Die UI-Bridge ist ausschließlich Anzeige und Navigation.
- Das Popup zeigt:
  - eine Kurz-Summary (Status, moved_files, missing_parts)
  - einen Button „Report öffnen“ zum echten Report.
- Leere Popups sind verboten (siehe MR-UX-PURGE-001).
