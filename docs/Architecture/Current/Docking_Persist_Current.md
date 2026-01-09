# Docking Persist/Restore (Current)

## Ziel
Undocked Tabs (Toplevel) werden exakt so wiederhergestellt, wie sie beim Schließen von Main offen waren:
- Welche Keys offen waren
- Ob docked/undocked
- Geometry (WxH+X+Y)
- AOT (nur wenn explizit gesetzt)

## Source of Truth
- Datei: `ShrimpDev.ini`
- Section: `[Docking]`

### Schema
- `keys = key1,key2,...`
- `<key>.open = 0/1`
- `<key>.docked = 0/1`
- `<key>.geometry = WxH+X+Y`
- `<key>.aot = 0/1`

## Writer-Policy (Single Writer – verbindlich)
Es darf genau **eine** Schreibstrategie aktiv sein.

**Soll-Standard:**
- Lesen/Schreiben über `modules/config_loader.load()/save()` (ConfigParser-basiert)
- Docking nutzt keinen parallelen Writer (`ini_writer`) für dieselben Keys

## Persist-Trigger (verbindlich)
Persist wird in zwei Situationen ausgeführt:

1) **Main close**
- Trigger: `WM_DELETE_WINDOW` / App shutdown handler
- Aktion: `DockManager.persist_all()`
- Soll: alle aktuell offenen undocked Fenster werden mit `open=1,docked=0,geometry,aot` geschrieben

2) **Undocked window close**
- Trigger: `w.protocol("WM_DELETE_WINDOW", ...)`
- Aktion: `_persist_one(key,w)` und anschließend close/hide
- Soll: Zustand dieses Fensters wird geschrieben (inkl. `open=1,docked=0`)

## Restore (verbindlich)
Beim App-Start:
- lese `[Docking] keys`
- für jedes `key` gilt:
  - wenn `<key>.open==1` und `<key>.docked==0` -> undock + geometry/aot anwenden
  - wenn `<key>.open==1` und `<key>.docked==1` -> docked öffnen (falls unterstützt)
  - andernfalls ignorieren

## No-Gos
- Kein Multi-Writer: Docking darf nicht gleichzeitig `config_loader.save()` UND `ini_writer`-Writes für denselben Zustand nutzen.
- Keine silent try/except-Leichen ohne Diagnosepfad.
- `persist_all()` darf nie `True` zurückgeben, wenn kein Write/Commit stattgefunden hat.

## Minimaler Diagnosepfad (Pflicht)
Für Docking Persist gibt es einen minimalen Diagnosemodus:
- Report/Log unter `Reports/` mit Beleg: Persist wurde aufgerufen + welche Keys geschrieben wurden
