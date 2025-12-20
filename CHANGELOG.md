# CHANGELOG

## v9.8.2 (2025-10-18)
- Intake: Kopierfunktion aus History (Button + Ctrl+C)
- Intake: Dateien aus History endgültig löschen (Button + Entf), mit Bestätigung und Trash-Fallback
- Intake: „Intake leeren“-Button (Pfad & Status zurücksetzen, LED neutral)

## v9.8.3 (2025-10-18)
- FIX: Modulimporte stabil (echte Packages durch __init__.py, sys.path-Safeguard)
- FEATURE: Always-on-Top (Togglebar + Ctrl+T), Setting persistiert in intake.ini

## v9.8.4 (2025-10-18)
- FIX: Snippets automatisch wiederhergestellt (logger_snippet, file_detect_snippet)
- GUI: Fallback-Logger in main_gui (startet auch ohne Snippet), Versionsbump

## v9.8.6 (2025-10-18)
- FIX: Pfad/Import-Stabilität für ShrimpDev (keine importlib-Checks ohne sys.path)
- FIX: Snippets + __init__.py werden sicher angelegt
- FIX: Fallback-Logger korrekt und eingerückt injiziert

## v9.8.7 (2025-10-18)
- FIX: main_gui.py vollständig neu aufgebaut (gültiger try/except, Fallback-Logger)
- FEATURE: Always-on-Top bleibt erhalten; sys.path-Safeguard konsolidiert

## v9.8.8 (2025-10-18)
- FIX: config_mgr.py vollständig restauriert; gültige ConfigMgr-Klasse inkl. always_on_top & History-APIs
- Stabilität: threadsichere INI-Lese/Schreiblogik, Logger-Fallback

## v9.8.9 (2025-10-18)
- FIX: module_agent_ui.py (AgentFrame) und module_project_ui.py (ProjectFrame) sauber wiederhergestellt
- GUI: Versionstitel aktualisiert

## v9.9.0 (2025-10-18)
- Intake-UI: Kopfzeile (Workspace/Datei/Endung/Zielordner), Editor links, Treeview rechts (name/ext/subfolder)
- Aktionen: Speichern (Ctrl+S), Erkennen (Ctrl+I), Kopieren (Ctrl+C), Löschen (Entf), Explorer im Kontextmenü
- LED „Erkennung OK“ oben rechts; Checkbox „Nicht wieder anzeigen (Speicher-OK)“ (suppress_save_ok)
- Menüleiste: File / Tools / Help / Info

## v9.9.1 (2025-10-18)
- UI: Ordnung & Responsive-Layout (Grid-Gewichte, PanedWindow, Scrollbars)
- Fix: Menübefehle + Shortcuts funktionieren zuverlässig
- Optik: ttk-Styles (clam), klare Abstände/Toolbar

## v9.9.2 (2025-10-18)
- Intake: Toolbar-Buttons (Erkennen, Speichern, Löschen), Name-Feld separat (kopierbar)
- LEDs: Target-Existenz, Erkennung, Speichern
- Tooltips & Kontextmenüs flächendeckend
- Menü aufgeräumt (keine Action-Duplikate)

## v9.9.3 (2025-10-18)
- FIX: Unerwartete Einrückung im Menü (m_file.add_separator) behoben.

## v9.9.4 (2025-10-18)
- Safe-Boot: Import-/Init-Fehler stoppen die GUI nicht (Platzhalter-Tabs mit Details)
- Diagnose: Fehler in Konsole + debug_output.txt, SHRIMPDEV_DEBUG=1 aktiviert
- Exit-Code 0 bei abgefangenen Startfehlern

## v9.9.5 (2025-10-18)
- FIX: SyntaxError durch unescaped Zeilenumbruch in SafeImport-String (Fehler: IntakeFrame...)

## v9.9.6 (2025-10-18)
- FIX: main_gui.py vollständig neu geschrieben; alle Safe-Boot Strings korrekt escaped
- Beibehaltener Funktionsumfang: Safe-Boot, schlankes Menü, globale Shortcuts

## v9.9.7 (2025-10-18)
- FIX: Intake-Context „Öffnen im Explorer“ – fehlende Methode _open_selected() ergänzt
- Robustheit: _path_of_item() abgesichert

## v9.9.8 (2025-10-18)
- Intake: 'Kop.'-Button entfernt, stattdessen Button 'Einfügen' (Clipboard -> Name)
- Tabelle: Kontextmenü 'Name kopieren' (nur Spalte name)

## v9.9.9 (2025-10-18)
- Intake: Endung editierbar (Override), Detect überschreibt manuelle Eingabe nicht
- Save: setzt/ersetzt Endung konsistent; Delete ohne Auswahl bleibt folgenlos
- QA: Statische Checks für Verkabelung

## v9.9.10 (2025-10-18)
- FIX: _detect() überschreibt manuelle Endung nicht mehr (var_ext_manual-Guard)

## v9.9.11 (2025-10-18)
- FIX: SafeBoot NameError _ex→ex behoben
- logger_snippet: Retry bei PermissionError

## v9.9.12 (2025-10-18)
- FIX: SafeBoot-Fehler `ex not defined` behoben
- logger_snippet: Retry+Lock-Fix (sichere Logschleife)

## v9.9.13 (2025-10-18)
- main_gui: Safe-Import-Block vollständig repariert (gültige except-Blöcke, korrekte Fallback-Frames)

## v9.9.14 (2025-10-18)
- main_gui: Fallback-Frames komplett neu geschrieben (keine 'ex not defined'-Fehler mehr)

## v9.9.15 (2025-10-18)
- logger_snippet: atomarer Write, Retry + Temp-Fallback (kein PermissionError mehr)

## v9.9.16 (2025-10-18)
- main_gui: Safe-Fallbacks erfassen Tracebacks im except-Block (kein 'NoneType: None' mehr)

## v9.9.17 (2025-10-18)
- module_code_intake: IndentationError in _save() behoben

## v9.9.18 (2025-10-18)
- Intake: _save() neu geschrieben (korrekte Einrückung, Endungs-Override konsistent)
- Helper _apply_ext_to_name() in der Klasse sichergestellt

## v9.9.18 (2025-10-18)
- Intake: _save() neu geschrieben (korrekte Einrückung, Endungs-Override konsistent)
- Helper _apply_ext_to_name() in der Klasse sichergestellt

## v9.9.19 (2025-10-18)
- Intake-Modul komplett erneuert (konsistente 4-Spaces, CRLF)
- Kontextmenüs, Einfügen-Button, manuelle Endung (Override), robuste Aktionen

## v9.9.20 (2025-10-18)
- Intake: Buttons repariert (grid-Toolbar, saubere Commands, Tooltips)
- Shortcuts gefixt (unbind+bind_all), kein Überlappen beim Resizing

## v9.9.20 (2025-10-18)
- Intake: Buttons repariert (grid-Toolbar, saubere Commands, Tooltips)
- Shortcuts gefixt (unbind+bind_all), kein Überlappen beim Resizing

## v9.9.21 (2025-10-18)
- Intake: Buttons hart verdrahtet über Wrapper (mit Logging & Fehlermeldung)
- Toolbar fix (grid), Shortcuts auf Wrapper; QA prüft Verkabelung

## v9.9.22 (2025-10-18)
- Intake: Buttons hart verdrahtet (command + MouseUp), Ping-Label, Wrapper mit Log+bell

## v9.9.22 (2025-10-18)
- Intake: Buttons hart verdrahtet (command + MouseUp), Ping-Label, Wrapper mit Log+bell

## v9.9.23 (2025-10-18)
- Fix: 'body = ttk.Panedwindow(self, orient="horizontal")' wieder korrekt in einer Zeile
- Body-Adds geprüft (left/right)

## v9.9.23 (2025-10-18)
- Fix: 'body = ttk.Panedwindow(self, orient="horizontal")' wieder korrekt in einer Zeile
- Body-Adds geprüft (left/right)

## v9.9.25 (2025-10-18)
- Detect final: Name-Änderung hebt manuellen Override auf; LED gelb.
- Erkennung: Name -> Endung, sonst Text-Heuristiken; manuelle Endung bleibt unberührt.

## v9.9.25 (2025-10-18)
- Detect final: Name-Änderung hebt manuellen Override auf; LED gelb.
- Erkennung: Name -> Endung, sonst Text-Heuristiken; manuelle Endung bleibt unberührt.

## v9.9.26 (2025-10-18)
- Detect: Dateiname wird aus Code-Text erkannt (Runner_XXXX_*.ext, tools\Runner_*.ext, py/call-Aufrufe, Kommentar/SET name)
- Name wird nur gesetzt, wenn nicht manuell editiert; Ext-Override bleibt respektiert

## v9.9.27 (2025-10-18)
- _detect() vollständig neu aufgebaut (sicherer content-Read, Name- und Ext-Erkennung, korrekte try/except).
- Tabs im Bereich entfernt; Helpers sichergestellt.

## v9.9.28 (2025-10-18)
- Intake: Einrückungen normalisiert; 'except/finally' auf 'try' ausgerichtet (IndentationError behoben).

## v9.9.30 (2025-10-18)
- module_code_intake.py komplett neu aufgebaut: stabile Buttons/Shortcuts, Name-/Ext-Erkennung,
  Override-Respekt, Kontextmenüs, Ping/LEDs, Resizing-fest. 4 Spaces + CRLF.

## v9.9.31 (2025-10-18)
- Intake: Auto-Erkennung bei Paste/Tippen (<<Paste>>, <Ctrl+V>, <<Modified>>), debounced.
- Initiale Auto-Erkennung nach Start, wenn Editor nicht leer ist.

## v9.9.32 (2025-10-18)
- Auto-Detect hart verdrahtet (Paste/Key/Start, debounced).
- Buttons zusätzlich via MouseUp gebunden.
- Rechte Liste: Fallback-Scan des Zielordners, wenn keine History da ist.

## v9.9.33 (2025-10-18)
- Intake: Alle akustischen Signale entfernt (keine bell()).
- Type-Hints aus Funktionssignaturen entfernt (Kompatibilitäts-/Syntax-Fix).

## v9.9.34 (2025-10-18)
- module_code_intake.py sauber neu installiert (ohne Type-Hints & Sounds).
- Auto-Erkennung (Paste/Key/Start), Buttons fest verdrahtet, Listenscan-Fallback.

## v9.9.35 (2025-10-18)
- Auto-Detect erzwingt _detect() nach Paste/Key/Start; Name wird gesetzt, solange nicht manuell editiert.
- Rechte Liste: zusätzliche Spalten 'date' und 'time' (Datei-Änderungszeit).

## v9.9.36 (2025-10-18)
- Name-Detect: erkennt jetzt auch 'Runner_XXXX_*' ohne Endung (z.B. in Docstrings).
- Fallback: generiert snippet_YYYYMMDD_HHMMSS, wenn kein Name gefunden und nicht manuell.
- Tabelle: neue Spalten 'date' und 'time', gefüllt aus Datei-mtime.

## v9.9.37 (2025-10-18)
- Intake-Modul vollständig neu geschrieben (stabile Einrückungen, Auto-Detect, Runner-Erkennung, Fallback-Name).
- Treeview: date/time Spalten.
- Keine Sounds, keine Type-Hints.

## v9.9.39 (2025-10-18)
- Intake Header-Layout: Name-Spalte vergrößert (weight=3), Ext-Spalte verkleinert (width=6, kein Stretch).

## v9.9.39 (2025-10-18)
- Intake Header-Layout: Name-Spalte vergrößert (weight=3), Ext-Spalte verkleinert (width=6, kein Stretch).

## v9.9.42 (2025-10-18)
- Fix: SyntaxError durch doppelte Klammer in ent_ext.grid() korrigiert.

## v9.9.43 (2025-10-18)
- Intake: [Löschen] leert Editor + Name + Endung.
- Intake: Paste setzt Name/Endung zurück und triggert Auto-Erkennung neu.

## v9.9.44 (2025-10-18)
- Fix: falsches Escaping in self._ping("Gelöscht.") entfernt.
- UX: [Löschen] leert Editor/Name/Endung; Paste setzt Name/Endung zurück und triggert Auto-Erkennung.

## v9.9.45 (2025-10-18)
- Intake: _on_editor_modified() korrigiert (Indentation + zuverlässiger Body).

## v9.9.46 (2025-10-18)
- Intake: _on_editor_modified() strikt neu gesetzt (Indent fix + stabiler Body); Tabs→Spaces im Klassenblock.

## v9.9.47 (2025-10-18)
- Intake: Indentation-Audit + robuste Ersetzung von _on_editor_modified(); Tabs→Spaces im Klassenblock.

## v9.9.47 (2025-10-18)
- Intake: Indentation-Audit + robuste Ersetzung von _on_editor_modified(); Tabs→Spaces im Klassenblock.

## v9.9.48 (2025-10-18)
- Intake: Block _on_editor_key/_on_editor_modified vollständig neu geschrieben (saubere 4-Space-Indent).

## v9.9.49 (2025-10-18)
- Intake: Delete-Handler vollständig neu gesetzt (saubere Einrückung, Bestätigung, UI-Reset).

## v9.9.50 (2025-10-18)
- Intake: Delete-Handler auf String-Konkatenation umgestellt (keine f-Strings), CRLF + 4 Spaces.

## v9.9.52 (2025-10-18)
- Intake: Alle `from __future__ import ...` automatisch an den Dateianfang verschoben.

## v9.9.54
- Intake: Guard-Button + Handler integriert (Prüfen & ✅-Markierung)


## R1987 Intake Health & Autofix
- 2025-12-08: Intake-Health-Scan und Legacy-Archivierung (R1987).
- Intake-Module geprueft; Legacy-Intake kopiert nach _Archiv/Legacy_Intake.
- Pipeline-Eintraege fuer offene Punkte erzeugt.

## 2025-12-14 – R2143
- Added: Notebook-Tab "MasterRules" (Viewer fuer docs/Master).
- Added: modules/ui_masterrules_tab.py
- Changed: main_gui.py (Tab-Hook + Import)
- Docs: ARCHITECTURE.md, Pipeline_Notes.md

## 2025-12-14 – R2143
- Added: Notebook-Tab "MasterRules" (Viewer fuer docs/Master).
- Added: modules/ui_masterrules_tab.py
- Changed: main_gui.py (Tab-Hook + Import)
- Docs: ARCHITECTURE.md, Pipeline_Notes.md

## 2025-12-14 – R2144
- Fixed: Crash beim Start (SyntaxError in modules/ui_masterrules_tab.py).

## 2025-12-14 – R2148
- Added: Log-Tab Auto-Refresh/Tail (neue Eintraege automatisch).

## 2025-12-14 – R2153
- Fixed: ui_pipeline_tab.py (Indentation/Syntax) + Added: Done/Offen Anzeige.

## 2025-12-14 – R2154
- Added: Pipeline-Tab Checkbox click-to-toggle + persist to PIPELINE.md.

## 2025-12-14 – R2155
- Improved: Pipeline-Tab Lesbarkeit/Bedienbarkeit (Task-Liste statt Text).

## 2025-12-14 – R2156
- Fixed: Pipeline-Tab zeigt jetzt Datei-Pfad/Status und erkennt Tasks robuster.

## 2025-12-14 – R2158
- Fixed: R2157 IndentationError by rollback + safe patch.

## 2025-12-14 – R2162
- Fixed: R2159 main() detection (main() -> None) + install exception_logger.install(ROOT).

## 2025-12-14 – R2165
- Added: Runner guard infrastructure (central exception handling).

## 2025-12-14 – R2166
- Improved: Pipeline tab UX (Search, Sort, Zebra, emphasis for done/HIGH).

## 2025-12-14 – R2166
- Improved: Pipeline tab UX (Search, Sort, Zebra, emphasis for done/HIGH).

## 2025-12-14 – R2167a
- Docs: Agent contract clarified; legacy Agent UI module marked as unused.

## 2025-12-14 – R2171
- Pipeline: Added HIGH item for Intake autosave-on-paste (guarded by syntax check).

## 2025-12-14 – R2173
- Added: Clickable recommendations in Agent tab (run/copy/pipeline).

## 2025-12-14 – R2174
- UI: Agent popups are now centered over main window.

## 2025-12-14 – R2180
- Docs: Generated docs/Runner_Status.md (read-only runner status report).

## 2025-12-14 – R2181
- Docs: Generated docs/Runner_Archive_Plan.md (archive proposal, no changes).

## 2025-12-14 – R2183
- Pipeline: Added item to remove obsolete GUI buttons across all tabs.
- Docs: Generated docs/GUI_Obsolete_Buttons.md (read-only analysis report).

## 2025-12-14 – R2184
- Docs: Generated docs/GUI_Tab_Inventory.md (tabs/buttons inventory, read-only).
## 20251215_232948 – R2243
- Intake Run Button nutzt jetzt zentralen Runner-Exec (vollständig geloggt)
## 2025-12-16 08:22 – R2249
- Runner-Logging zentralisiert (START/END/exit in debug_output.txt)
- Keine Marker-Inserts mehr in logic_actions.action_run (Try/Except-Falle)


## 2025-12-18 - R2339
- Docking: Persist/Restore für Undocked-Fenster (w/h/x/y) via INI, Offscreen-Default, Center nur beim Erst-Undock.
- Docs: docs/Architecture_Docking.md ergänzt/aktualisiert.

## 2025-12-18 - R2340
- Docking: Persist/Restore robuster (wm_geometry + after_idle apply + Offscreen-Check verbessert).

## 2025-12-18 - R2343
- Docking: Persist schreibt jetzt garantiert in ShrimpDev.ini und speichert .geometry (WxH+X+Y).

## 2025-12-18 - R2344
- Obsolete Config-Module archiviert (Dubletten entfernt): config_mgr/config_loader/root-config_manager.
- Report: docs/Obsolete_Configs_R2344.md

## 2025-12-18 - R2345
- Fix: ImportError behoben durch Compat-Aliase modules/config_loader.py + modules/config_mgr.py -> config_manager.
\n## 2025-12-18 - R2346\n- Fix: ui_filters Import/Usage von config_loader.load() wieder kompatibel gemacht (Compat-API in config_loader/config_mgr).\n
## 2025-12-18 - R2348
- Fix: Merge-Save robust gepatcht (save() Signatur mit Type-Hints).

## 2025-12-18 - R2350
- Fix: INI Merge-save verhindert das Zurücksetzen von [Docking] (keys/runner_products bleiben erhalten).

## 2025-12-18 - R2352
- Fix: Undocked Fenster kommen wieder an gespeicherter Position (INI restore robust gegen frühes Boot-Timing).

## 2025-12-18 - R2353
- Prozess: Diagnose-First Standard in Pipeline verankert (ab 2. Versuch kein Try&Error mehr ohne Messung).
- MasterRules: Diagnose-First-Regel ergänzt.
- Docs: Diagnosis_Playbook_GUI.md hinzugefügt.

## R2361
- Docking: geometry (WxH+X+Y) wird immer persistiert
- Restore nutzt geometry exklusiv, Center nur als Fallback

## R2363
- Docking Refactor: Geometry exklusiv im DockManager

## R2364
- INI: config_manager.save() schreibt jetzt MERGE (bewahrt [Docking])
- Restart: persist_all() vor quit()

## R2367
- Docking: Hard-Fix persist_one/persist_all (MERGE-write, geometry Pflicht)

## R2368
- Docking: Restore-Hardfix nutzt <key>.geometry + Offscreen-Fallback
- Main: late-apply UI.geometry nach update_idletasks

## R2368
- Docking: Restore-Hardfix nutzt <key>.geometry + Offscreen-Fallback
- Main: late-apply UI.geometry nach update_idletasks

## R2369
- Docking: pro Fenster Datensatz (open/docked/geometry/ts)
- Docking: Diagnose-Logs persist/restore
