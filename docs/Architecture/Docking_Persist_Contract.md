# Docking Persist Contract (v1)

Stand: 2026-01-11  
Scope: Docking + Undocked Tabs/Windows + AOT + Geometry + Restore-Order  
Owner: `modules/module_docking.py` (alle Persist-Schreibrechte für Docking/Tabs)

## 1. Zielbild

Docking-State ist **deterministisch**:
- Undocked Tabs/Windows werden nach Restart **identisch** wiederhergestellt.
- Geometry & AOT werden pro undocked window/tab persistiert.
- Persist erfolgt über **einen** kanonischen Write-Pfad (Single Writer), niemals via `cfg.write()`.

Dieses Dokument definiert:
- INI Sections/Keys (kanonisch)
- Owner & Trigger
- Encoding/Formatregeln
- Verifikation (Verify-Plan)

## 2. Canonical Storage

Canonical INI:
- `registry/ShrimpDev.ini`

Backup:
- `registry/ShrimpDev.ini.bak` (durch `ini_writer`/bestehende Backup-Regel)

## 3. Single Writer (verbindlich)

### 3.1 Schreib-Owner
- **Einziger** Owner für Docking Persist: `modules/module_docking.py`

### 3.2 Verbotene Schreiber
Folgende sind für Docking-Persist **verboten**:
- `main_gui.py` (darf Docking nicht schreiben)
- UI-Module (z. B. `ui_toolbar.py`, `ui_filters.py`) für Docking/Tabs
- Jede direkte Datei-Schreiboperation: **`cfg.write(f)` verboten** (umgeht Atomic/Redirect-Regeln)

### 3.3 Erlaubte API
Docking darf INI nur schreiben über:
- `config_loader.save(cfg)` **oder**
- `ini_writer.write_configparser_atomic(...)` (falls das die kanonische Implementierung ist)

=> Entscheidung im APPLY: **eine** Methode wird verbindlich genutzt, die andere nicht parallel.

## 4. INI Schema (kanonisch)

### 4.1 Section: [Docking]
Diese Section repräsentiert ausschließlich den Zustand der *undocked windows/tabs*.

Pflicht-Keys:
- `undocked.count` = int (0..N)
- `undocked.ids` = CSV von IDs (stabil, keine Spaces), z. B. `log,pipeline,project`

Optional/Erweiterbar:
- `restore.enabled` = 0/1 (Default: 1)
- `restore.version` = int (Default: 1)

### 4.2 Subkeys pro Undocked-ID
Für jede ID in `undocked.ids` gelten Pflicht-Keys:

- `undocked.<id>.tab_key` = str (interner Tab-Key / Identifier)
- `undocked.<id>.geometry` = `WxH+X+Y` (Tk-Standard)
- `undocked.<id>.aot` = 0/1
- `undocked.<id>.state` = `normal|maximized` (optional, falls vorhanden)

Optional:
- `undocked.<id>.monitor_hint` = int/str (nur falls Multi-Monitor robust nötig)

### 4.3 Section: [Tabs] (neu, v1 minimal)
Diese Section ist **nicht** Docking, sondern Tab-Semantik (Main Window).

Pflicht-Keys:
- `open` = CSV tab_keys (sichtbar/aktiv im Main)
- `active` = tab_key (oder leer)

Hinweis:
- `UI.last_tab` bleibt bestehen, wird aber **nicht** als Ersatz für Tabs-Persist akzeptiert.
- Tabs-Persist ist Owner `module_docking.py` (weil Docking-Engine Tabs orchestriert).

## 5. Trigger (wann wird geschrieben)

### 5.1 Persist-Trigger (Docking Owner)
`module_docking.py` muss persistieren bei:

1) **on_undock(tab_key / window_id)**  
   - nach erfolgreichem Undock + Geometry/AOT gesetzt
2) **on_redock(tab_key / window_id)**  
   - nach erfolgreichem Redock (undocked entry entfernen)
3) **on_floating_config_change(window_id)**  
   - Geometry-Change (Configure) *debounced* (z. B. 250–500ms)  
   - AOT-Change (Toggle)
4) **on_main_close()**  
   - finaler Persist-Snapshot

### 5.2 Restore-Trigger
Beim App-Start:
- `module_docking.py` lädt `Docking` + `Tabs` State
- stellt undocked windows her **nach** Tab-Registration, **vor** event-loop idle stabilization
- Offscreen-Fallback & Centering bleibt in Docking-Engine (bestehende Logik)

## 6. Formatregeln / Robustheit

- CSV: ohne Spaces, leer = leer
- IDs: nur `[a-z0-9_-.]` (bei Abweichung: sanitize)
- Geometry: validieren (Regex) und bei ungültig fallback auf Default
- Schreiben ist atomic (über ini_writer/config_loader)
- Keine stillen Swallows: Exceptions müssen im Report/Log sichtbar sein (DIAG zuerst)

## 7. Verify-Plan (Shrimpi-kompatibel)

### 7.1 Verify A: Schema-Check (non-UI)
- Parse `registry/ShrimpDev.ini`
- Wenn `undocked.count > 0`, dann müssen alle Pflicht-Keys pro ID existieren
- Validate geometry format

### 7.2 Verify B: Start-Window (auto)
- Start ShrimpDev kurz (2–3s)
- Prüfe: Logs bleiben leer (INI redirect) + INI bleibt parsebar
- Optional: “no new redirect growth”

### 7.3 Verify C: Determinismus (semi-auto, ohne Runner-Input)
- Dieser Verify ist nur möglich, wenn Docking Engine einen Headless-Trigger bietet.
- Falls nicht vorhanden: Verify bleibt manuell (separater Prozessschritt), aber ohne Runner-Popup-Input.

## 8. No-Gos (explizit)

- Kein `cfg.write(f)` in Docking
- Kein Schreiben von Docking/Tabs aus `main_gui.py`
- Keine parallelen Persist-Implementationen (kein “FIXED_v2” aktiv)
- Keine implizite Erwartung, dass „irgendwo“ Tabs schon gespeichert werden

## 9. Nächste Umsetzungsschritte

P1 (nächster APPLY):
1) Konsolidierung: `module_docking.py` implementiert Persist gemäß Schema (Docking + Tabs)
2) Entfernen/Deaktivieren: direkte `cfg.write` Pfade (nur Docking-relevant)
3) `Rxxxx VERIFY`: Schema-Check + redirect-growth check

Abschlusskriterium:
- Undocked + AOT + Geometry + Active/Open Tabs sind nach Restart reproduzierbar.

## Canonical Docking Persist Contract (RC0)

### Canonical INI
- Canonical Path: `registry/ShrimpDev.ini`
- Root-INI ist verboten (nur Migration/Redirect).

### Single Writer
- **Verboten** in `modules/module_docking.py`: `cfg.write(...)`, direkte File-IO auf ShrimpDev.ini
- **Erlaubt**: Persist ausschließlich über `modules/config_loader.save(cfg)`

### Datenmodell (Docking Section)
- `keys` = CSV Liste aller Docking Keys
- pro Key:
  - `<key>.open` (0|1)
  - `<key>.docked` (0|1)
  - `<key>.geometry` (Tk geometry string)
  - `<key>.ts` (forensics, optional aber empfohlen)
  - `<key>.aot` (optional)
- `last_active` = zuletzt aktiver key

### Trigger (Minimum)
- Persist muss mindestens passieren bei:
  - Main Close (echter Close-Handler)
  - Undock (nach finaler Erstellung des Toplevel/Window)
- Restore muss passieren bei App-Start nach UI-Init, bevor Tabs angezeigt werden.

### Compatibility Rule (Legacy)
- Wenn Legacy-Code alte Pfade nutzt, wird **redirected** und **geloggt** (`Reports/INI_REDIRECT.log`).
- Redirect ist *Warnung*, kein Fehler – aber muss über Zeit gegen 0 laufen.

Status: RC0 (Contract aktiv, ab jetzt verbindlich)
