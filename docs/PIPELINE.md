# ShrimpDev – PIPELINE

## Daueraufgabe – Systempflege (GLOBAL / IMMER AKTIV)

- [ ] (HIGH) Refactoring: Architektur vereinfachen, Altpfade abbauen, Redundanzen entfernen
- [ ] (HIGH) Troubleshooting: Fehlerursachen systematisch analysieren (nicht symptomatisch flicken)
- [ ] (HIGH) Bugfixes: Erkannte Bugs sofort beheben; wenn riskant/umfangreich -> Pipeline-Eintrag mit Prio + Risiko/Sideeffects

### EPIC: INI SINGLE WRITER (BLOCKER / HIGHEST)

> Ziel: Alle Quellen schreiben ausschließlich über **EINE interne Instanz** in **EINE** `ShrimpDev.ini`.
> Keine Neben-Schreiber mehr. Keine Overwrites. Keine Race-/Merge-Probleme.

- [ ] (HIGHEST / BLOCKER) **R2371 – INI-WriteMap (READ-ONLY Diagnose)**
  - Wer schreibt wann wie in `ShrimpDev.ini`? (Callsites + Pfade + Write-Strategie)
  - Output: `docs/INI_WriteMap.md` + Report (Runner-Output)
  - Guard: **READ-ONLY**, keine Codeänderungen

- [ ] (HIGHEST / BLOCKER) **R2372 – Architektur: INI Single Writer (Design + API)**
  - Definiere zentrale Instanz (z. B. `modules/ini_store.py` oder `config_manager`-Singleton)
  - API: `get() / set() / update_many() / save_merge_atomic()`
  - Output: `docs/Architecture_INI_SingleWriter.md`

- [ ] (HIGHEST / BLOCKER) **R2373 – Implementierung: zentraler INI-Writer (Merge + atomic)**
  - Harte Ziel-Datei: Projektroot `ShrimpDev.ini`
  - Merge-Write: bestehende INI bleibt erhalten, neue Keys werden überlagert
  - Atomic write: tmp + replace (Crash-sicher)
  - Logging: jede Save-Aktion mit Source-Tag (z. B. `source="docking"`)

- [ ] (HIGHEST / BLOCKER) **R2374 – config_manager Save konsolidieren**
  - `config_manager.save()` darf niemals full-overwrite machen
  - Alle Saves delegieren an zentralen INI-Writer (keine zweite Wahrheit)

- [ ] (HIGHEST / BLOCKER) **R2375 – Shims: config_loader.py / config_mgr.py**
  - Nur noch **lesen** oder **delegieren**
  - Keine direkten Writes mehr (sonst wieder Overwrite)

- [ ] (HIGHEST / BLOCKER) **R2376 – Docking über Single Writer**
  - 1 Datensatz pro Fenster:
    - `main`, `log`, `pipeline`, `artefakte`
  - Keys pro Fenster:
    - `open`, `docked`, `geometry`, `ts`
  - Offscreen-Regel: offscreen -> Default/Center (nur dann)

- [ ] (HIGHEST / BLOCKER) **R2377 – Monkeypatch/Altlogik Quarantäne**
  - Genau **eine** aktive Docking-Logik
  - Alte Patch-Blöcke markieren/deaktivieren (ohne Voll-Rewrite)

- [ ] (HIGHEST / BLOCKER) **R2378 – Restore Reihenfolge finalisieren**
  - Restore erst nach WM-Init (kein späteres Center/geometry override)
  - Regression: Main + Artefakte + Pipeline + Log Position stabil

- [ ] (HIGHEST / BLOCKER) **R2379 – Regression-Testplan**
  - Dokumentiere reproduzierbaren Testablauf in `docs/Testplan_INI_Docking.md`
  - Muss vor Feature-Arbeit grün sein


- [ ] (LOW) **Nach erfolgreicher Umstellung: De-factoring/Archivierung obsoleter Dateien**
  - Nur nach gruenem Regression-Test und stabiler neuer Struktur
  - Ziel: alte/obsolet gewordene Dateien in _Archiv oder _Obsolete verschieben (nach Plan, nicht ad-hoc)
## INI SingleWriter – Konsolidierung (TOP-PRIO)

**Status:** SAVE-Seite stabil (keine Overwrites). Offenes Thema: **Restore-Orchestrierung** (Fensterpositionen/Geometry pro Key korrekt wiederherstellen).

- [ ] (TOP/HIGH) Phase 2: Restore-Orchestrierung (pro Fenster-Key)
  - Ziel: Main, Log, Pipeline, Artefakte (runner_products) öffnen **exakt** dort, wo sie geschlossen wurden.
  - Regeln:
    - Restore nur **einmalig** beim Start (kein Auto-Refresh).
    - Apply-Timing: `after_idle` / WM-ready, damit WM nicht “drüberbügelt”.
    - Offscreen-Schutz: wenn Geometry außerhalb Screen -> Default/Center.
    - Pro Fenster **eigener Datensatz**: `<key>.open/.docked/.geometry/.ts`
  - Subtasks (zerlegt, damit es nicht eskaliert):
    - R2376 (DIAG, READ-ONLY): Logge Restore-Input (INI) + Apply + Effective Geometry (Main + Undocked)
    - R2377 (FIX): Per-Key Restore anwenden (Timing + Offscreen Clamp) **ohne** Save-Anpassungen
    - R2378 (HOOKS): Restore in App-Start + Restart-Button Pfad sicherstellen (immer gleicher Writer/INI)
    - R2379 (VERIFY): Testplan + Report + Doku-Update (Architektur/Changelog)

- [ ] (HIGH) Migration: Remaining Writers -> SingleWriter
  - Ziel: **Alle** INI-Schreibpfade (config_loader/config_mgr/docking/sonstige) konsolidieren, sodass nur `modules/ini_writer` schreibt.
  - Vorgehen: Diagnose-Report -> gezielte Delegation -> Verify.

- [ ] (MED) Defactoring / Archivierung (nach erfolgreicher Umstellung)
  - Alte/obsolete Dateien und Altpfade **erst nach** erfolgreicher Migration archivieren (kein Früh-Aufräumen).
  - Ergebnis: weniger Verwechslungen, weniger Import-Crashes, klare Struktur.


## GUI

- [ ] (MED) GUI: Runner-Produkte-Tab UX aufbohren (klickbar, kopierbar, öffnen, Pfad kopieren, Kontextmenü)
  - Ziele (typisch & nützlich):
    - Doppelklick: Datei öffnen
    - Rechtsklick-Kontextmenü:
      - Öffnen
      - Ordner öffnen (Explorer)
      - Pfad kopieren
      - Inhalt kopieren (bei Textdateien: .txt/.md/.py/.log/.json)
      - 'Als Ticket in Pipeline übernehmen' (nur Link/Metadaten, kein Auto-Fix)
    - Buttons/Shortcuts: Ctrl+C (Pfad), Ctrl+Shift+C (Inhalt)
    - Preview-Pane (read-only) für Textdateien, ohne Startfile
    - Filter/Sort: Typ (Report/Doc/Backup), Datum, Runner-ID
  - Guards:
    - READ-ONLY: niemals Dateien verändern
    - Große Dateien: Limit + 'gekürzt' Hinweis
    - Binärdateien: nur öffnen/Explorer, kein Inhalt kopieren


- [ ] (MED) GUI: Statusanzeige/Bottom-Puls/Overlap-Schutz (Status-UX)
  - Status-Text "Bereit" aus der unteren Zeile entfernen und **oben unter die LEDs** setzen (links sauber ausgerichtet).
  - Direkt vor dem Status-Text einen **kleinen Status-LED-Punkt** platzieren (Farbe wechselt je nach Status/Action).
  - Ganz unten mittig einen **Puls/Heartbeat-Indikator** anzeigen (farblich harmonisch zum Theme/LEDs).
  - Layout-Schutz: Unterste Zeile darf **nicht überlappt** werden (Grid/Pack/Min-Height/Separator/Sticky-Regeln).

- [ ] (MED) GUI: Status-LED Farb-Mapping standardisieren (RUNNING/WARN/ERROR/OK/BUSY/IDLE)
  - Ziel: einheitliche Farben + Semantik in der gesamten GUI (LEDs, Statuspunkt, Puls/Heartbeat, Popup-Status).
  - Definiere zentrale Konstanten/Mapping (z. B. in ui_leds oder ui_theme) und nutze überall dieselben Keys.
  - Vorschlag Keys: IDLE, BUSY, RUNNING, OK, WARN, ERROR
  - Nebenwirkungsschutz: keine Magic-Strings quer im Code; nur Mapping nutzen.

- [ ] (HIGH) GUI: Status-Events zentralisieren (wer setzt BUSY/RUNNING/OK/WARN/ERROR/IDLE wann?)
  - Ziel: Statuspunkt/LEDs/Puls/Popup nutzen **dieselbe** zentrale Statusquelle (kein Wildwuchs).
  - Definiere einen Status-Dispatcher (z. B. module_status.py) mit:
    - set_status(key, detail=None, source=None)
    - get_status()
    - optional: event callbacks (UI refresh)
  - Ereignisse (Beispiele):
    - App-Start -> IDLE
    - Intake Detect/Save -> BUSY -> OK/WARN/ERROR
    - Runner Start -> RUNNING
    - Runner End (rc=0) -> OK (kurz) -> IDLE
    - Runner End (rc!=0) -> ERROR (kurz) -> IDLE
    - Exceptions -> ERROR
  - Sideeffects vermeiden: UI darf nicht blockieren; Statuswechsel threadsicher (after()).




- [ ] (HIGH) GUI: Tab **Runner-Produkte** (Outputs / Artifacts)
  - Zweck: Zentrale Read-Only-Sicht auf alle von Runnern erzeugten Produkte
  - Inhalte:
    - Reports (`_Reports/`)
    - Dokumentation & Architektur (`docs/`)
    - Backups / Snapshots (`_Archiv/`)
  - Funktionen:
    - Filtern nach Runner-ID (z. B. R2254)
    - Filtern nach Typ (Report / Doc / Backup)
    - Sortierung nach Datum (neueste zuerst)
    - Textsuche
  - Aktionen:
    - Öffnen
    - Pfad kopieren
    - Im Explorer anzeigen
    - Optional: Verlinkung zur Pipeline (nur Referenz, kein Verschieben)
  - Regel:
    - Read-Only
    - Dateisystem bleibt Single Source of Truth

- [ ] (MED) GUI: Runner-Ausfuehrung Policy – Runner laufen im Popup (zentraler Output + Exit-Code), ausser die Ausfuehrung ist sichtbar/transparent.

- [ ] (HIGH) GUI: Decision-Doku als Single Source of Truth pflegen: `docs/GUI_Decisions.md` (KEEP/REMOVE/REWORK/MOVE je Tab).

## Intake
- [ ] (HIGH) GUI: Obsolete Buttons entfernen (alle Tabs) – Buttons ohne Funktion/Handler, tote Actions, Altlasten. Erst Analyse-Report, dann Cleanup.

> Quelle der Wahrheit für Status, Phasen und Prioritäten.
- [ ] (HIGH) Intake: Autosave nach Einfügen/Paste in den Intake, aber nur wenn Syntax-Check OK (sonst kein Save + Fehler sichtbar im Intake/Log).
> Änderungen erfolgen **nur über Runner**.

---

## Phase 2.5 – Stabilisierung & Klarheit (AKTIV)

**Ziel:** Ordnung, Transparenz und ruhiger Betrieb nach Agent-/UI-Fixes.

### Status
- Agent funktionsfähig ✔
- Agent-Tab mit Scrollbar & festen Buttons ✔
- Doppelanzeige im Agent-Tab beseitigt ✔

### To-Do
- ⬜ Pipeline-Tab (Read-Only) einführen
- ⬜ SR optisch & logisch als *Service* trennen
- ⬜ Agent-Empfehlungen erklärbar machen (Warum?)
- ⬜ SR-Liste klassifizieren & bereinigen

---

## Phase 3 – Systemintelligenz (GEPLANT)

**Ziel:** Agent wird Coach, nicht nur Auslöser.

### Geplant
- Agent kann Empfehlungen bündeln (Ketten)
- Agent lernt aus Aktionen (Gewichtung)
- Risiko-Transparenz (sicher vs. patchend)
- Klare UI-Zonen (Arbeit / Analyse / Service)

---

## Notizen
- SR = Service-Runner (ungefährlich, UI-nah)
- R#### = echte Runner (Analyse / Patch / Wirkung)
- Agent empfiehlt **nur R####**, keine SR

---

*Letzte Änderung:* 2025-12-15 10:11:30

## Prio / P0

- [ ] (HIGH) Tracebacks wieder sichtbar machen: Exceptions/Tracebacks in debug_output.txt + Intake-Log + Runner-Log ausgeben (kein 'still fail').
- GUI: Tools Purge Buttons (Scan R2206 / Apply R2207) oben rechts, Apply mit Sicherheitsabfrage, leicht rot.

- [HIGH] LOG: Befüllung global zentralisieren und reparieren (Runner STDOUT/ERR + App-Events -> ein zentraler Pfad + eine API, überall genutzt)

- [ ] (HIGH) LOG: Runner-Logging global zentralisiert (Tools/Popup-Pfad -> exception_logger) [R2230 2025-12-15 18:17:36]

- [ ] (HIGH) Runner-Logging: exception_logger in modules korrekt verdrahtet (R2236)
- [x] (HIGH) Runner-Logging schreibt hart nach debug_output.txt (R2239)
- [ ] (HIGH) MR: Runner-Bootstrap + debug_output Logging-Pflicht als harte Regel verankern (R2240)
- [x] (HIGH) Intake Run delegiert immer an module_runner_exec (R2243)
- [x] (HIGH) Runner-Logging zentral in module_runner_exec/exception_logger (R2249)

## LearningEngine

- [ ] (MED) LearningEngine: Runner-Produkte READ-ONLY scannen (Reports/docs/_Archiv) zur Muster- & Fehlererkennung
  - Zweck: Lernen aus **realen Ergebnissen** (Fehler, Warnungen, No-Ops, Hotspots), keine Code-Autofixes.
  - Scope: `_Reports` primär, `docs` sekundär, `_Archiv` **stark gefiltert**.
  - Modus: **READ-ONLY**, Delta-Scan (nur neue/geänderte Dateien seit letztem Lauf).
  - Taktung: manuell bei Bedarf; optional periodisch **1× täglich oder 1× wöchentlich**.
  - Extraktion (regelbasiert):
    - Error-Signaturen (Traceback, SyntaxError, ModuleNotFoundError, bad escape, FileNotFoundError)
    - No-Op-Marker ("no-op", "already patched")
    - Betroffene Module/Runner (Hotspots)
  - Output:
    - `LearningEngine_Products_Index.json` (Index/Metadaten)
    - `LearningEngine_Products_Findings.md` (Trends, Top-Fehler, Vorschläge)
  - Ergebnis darf **Pipeline-Vorschläge** erzeugen, aber **nichts automatisch ändern**.

## Tools

- [ ] (HIGH) Tools/Purge: Hard-Schutz gegen Self-Purge (KEEP/Whitelist/Anchor niemals verschieben)
  - Regel: Purge darf **niemals** verschieben/löschen:
    - den aktuellsten Anchor (mtime/last-run)
    - KEEP-Liste (registry/tools_keep.txt) und deren Einträge
    - KEEP-Ordner (tools/_keep oder tools_keep)
    - den Purge-Runner selbst (Scan/Apply)
  - Implementierung später: zentraler `is_protected(path)` Guard + Unit-Checks im Scan-Report.


- [ ] (HIGH) Tools/Purge: Runner-KEEP in eigenen Ordner (statt im tools-Root) + klare Regeln
  - Ziel: Wenn Runner bewusst behalten werden sollen, kommen sie in z. B. `tools_keep/` (oder `tools/_keep/`).
  - Purge-Scanner soll standardmäßig **nur** `tools/` (Root) scannen, aber KEEP-Ordner konsequent auslassen.
  - Vorteil: weniger Whitelist-Hacks, klarere Struktur, weniger Risiko.
  - Ergänzung: GUI soll KEEP-Runner optional anzeigen (Filter/Toggle), aber Purge respektiert KEEP immer.



### Runner-Produkte intern öffnen
- Runner-Produkte (Reports/Docs/Logs) im internen Read-Only Viewer öffnen (ähnlich Runner-Popup)
- Buttons: Extern öffnen, Ordner, Pfad kopieren, Inhalt kopieren, Schließen
- Fallback: große / nicht-text Dateien extern öffnen
- Implementierung: R2304

- [ ] (MED) Intake: Refresh-Button oben rechts über der rechten Treeview (wie Screenshot/roter Kasten). Button refresht die Treeview darunter manuell (kein Auto-Refresh). Implementierung erst nach sauberer Anchor-/Diagnose-Analyse in ui_project_tree.py. <!-- R2358_PIPE_INTAKE_REFRESH -->

## Done

### Docking Restore Bug – resolved (R2395)
- Fix: `modules/module_docking.py` restore respects `open/docked` + prefers `<key>.geometry`.
- Docs: `docs/Docking_Architecture.md`
- Incident: `docs/Incidents/Docking_R2379-R2395.md`

## Backlog

### Offene Notizen (nicht dringend, aber merken)
- INI-SingleWriter Konsolidierung ist noch nicht final: `config_loader.save()`/`config_mgr`/vereinzelte `cfg.write()`-Pfade bei Gelegenheit zentralisieren (Ziel: ein Write-Pfad).
- Restart-Pfad ist sensibel (mehrere Persist-Hooks): zukünftige Änderungen nur mit READ-ONLY-Scan + klarer Verifikation, damit kein Regression-Centering/State-Leak entsteht.
- `module_docking.py` ist stabil, aber historisch komplex: Refactoring nur bewusst (Snapshot + Tests/Verifikation), kein „nebenbei“.

- Artefakte: Popup "intern anzeigen" → Button "Quelle kopieren" (kopiert Dateiinhalt, nicht Pfad).

## GUI / Artefakte

- [ ] Artefakte/Popup „intern anzeigen“: Button „Quelle kopieren“ (Datei-INHALT in Zwischenablage, nicht Pfad).

## Config / INI / SingleWriter

- [ ] SingleWriter: Finaler Audit – keine direkten ShrimpDev.ini Overwrites mehr (config_loader/config_mgr/ui_toolbar etc.).
- [ ] SingleWriter: optional Guard-Runner bauen, der direkte INI-Writes in Zukunft als Pipeline-Warnung meldet.

## Docking / Fenster / Geometry

- [ ] Docking/Geometry: Drift & Centering final fix (R2404 auswerten, dann minimaler Patch nur am echten Post-Restore Setter).
- [ ] Docking/Geometry: kurzer Smoke-Test-Runner (Start/Restart, Fensterpositionen vergleichen, Report).

## Docs / Architektur

- [ ] Doku/Architektur: Docking-stabil + SingleWriter-Delegation (R2402/R2403) sauber dokumentieren (Architektur + Troubleshooting).
- [ ] Doku: Report-Index/Changelog-Eintrag für DockingStable Snapshot (R2398) + relevante Reports verlinken.
