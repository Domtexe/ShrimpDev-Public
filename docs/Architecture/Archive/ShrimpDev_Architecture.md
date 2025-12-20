# ShrimpDev – Architekturübersicht (v0.1)

Stand: 2025-12-03  
Status: Config-Konsolidierung (ShrimpDev.ini), SyntaxLED-Hardening, Toolbar-Recovery

---

## 1. Ziel & Gesamtbild

**ShrimpDev** ist die Entwicklungs-IDE für ShrimpHub:

- GUI-zentrierte Umgebung für:
  - Intake-Analysen (Code, Logs, Runner-Ausgaben, etc.)
  - Runner-Steuerung (tools/R####.cmd/.py)
  - LearningJournal-Verwaltung
  - AutoSanity-/Guard-Mechanismen
- Verantwortlich für Patches, Reparaturen und Automatisierungen in ShrimpDev & ShrimpHub.

High-Level-Datenfluss:

User (GUI)
→ main_gui.ShrimpDevApp
→ modules.logic_actions (zentrale Aktions-Schicht)
→ UI-Module (ui_*.py, module_*.py) & Runners (tools/R####)
→ Dateien / Config / Logs / Backups

Persistente Kernartefakte:

- **ShrimpDev.ini** – zentrale Konfiguration
- **debug_output.txt** – globales Log
- **learning_journal.json** – Wissensbasis
- **_Archiv** – Backups
- **_Snapshots** – Projekt-Snapshots
- **_Reports** – Reports von Runnern

---

## 2. Hauptkomponenten

### 2.1 main_gui.py – App-Container & Einstieg

Verantwortung:

- Einstiegspunkt (`main()` + `ShrimpDevApp`)
- Erzeugt Tkinter-Hauptfenster
- Lädt Config (über config_manager, sofern aktiv)
- Baut die Tabs (Notebook):
  - Intake
  - LearningJournal
  - Settings
  - weitere projektspezifische Tabs

Wichtige Aufgaben:

- Initialisiert:
  - Toolbar (via ui_toolbar.build_toolbar_left/right oder build_toolbar)
  - Intake-Editor (ui_left_panel)
  - LED-Bar (ui_leds)
  - rechte Tree-/Listenansicht (ui_project_tree/ui_filters)
- Hält Referenzen (z. B. app.editor, app.led_bar, app.right_list).

**Stabilitätsregel:**  
main_gui.py ist „hoch-sensibel“ – Änderungen hier nur gezielt und mit expliziter Freigabe.


### 2.2 modules/logic_actions.py – Aktions-Fassade

Verantwortung:

- Bietet die öffentlichen Aktionen, die von UI aufgerufen werden, z. B.:
  - Intake:
    - action_new(app)
    - action_detect(app)
    - action_save(app)
    - action_undo(app)
  - Runner:
    - action_run(app)
    - action_delete(app)
    - action_tree_rename(app)
    - action_tree_delete(app)
    - action_tree_undo(app)
  - LearningJournal:
    - action_learning_journal(app)
  - Guards / Sonderfunktionen:
    - action_guard_futurefix(app)
    - action_guard_futurefix_safe(app)
    - action_r9998(app)
    - action_r9999(app)
- Schreibt Logeinträge (u. a. über log_debug) nach debug_output.txt.

**Stabilitätsregel:**  
Die Signaturen von action_* bilden eine interne API für UI-Module. Runner dürfen einzelne Blöcke gezielt patchen, aber keine anonymen Voll-Rewrites.


### 2.3 modules/ui_toolbar.py – Toolbar (Intake, Runner, Log)

Verantwortung:

- Baut die obere Toolbar der ShrimpDev-GUI:

  Linke Seite:
  - Intake-Steuerung (z. B. Neu, Erkennen, Speichern, Undo)
  - LED-Bar (ui_leds.build_led_bar)

  Rechte Seite:
  - LearningJournal-Button
  - Guards / Sonder-Buttons
  - Runner-Aktionen (Run, Delete, Rename, Undo, TreeDel)
  - Log-Button (öffnet Log-Viewer)

Öffentliche Funktionen:

- build_toolbar(app, parent)  
  → Baut komplette Toolbar in einem Frame.
- build_toolbar_left(parent, app) / build_toolbar_right(parent, app)  
  → Kompatibilitäts-Wrapper für main_gui-Versionen, die linke/rechte Seite separat aufbauen.

Log-Viewer:

- _action_show_log(app)
  - Öffnet ein Toplevel mit dem Inhalt von debug_output.txt.
  - Position & Größe werden in ShrimpDev.ini unter [LogWindow] gespeichert (geometry=…).

**Patch-Zone:**  
_ui_toolbar._action_show_log(app)_ ist eine explizite Stelle für Verbesserungen:
- Tail-Log (nur letzte N Zeilen / KBytes laden)
- Button „Ältere laden“
- Live-Update (Timer)
- AOT-freundliches Placement (Fenster über der GUI, Geometrie-Persistenz)

Wichtig: Signatur und Fehler-Handling müssen stabil bleiben (Log-Popup darf ShrimpDev niemals crashen).


### 2.4 modules/ui_left_panel.py – Intake-Panel

Verantwortung:

- Stellt den Intake-Editor + UI-Elemente bereit.
- Bindet Editor-Events an logic_actions (New, Detect, Save, Undo).
- Arbeitet eng mit ui_leds.evaluate(app) zusammen (Status der LEDs basiert auf Intake-Inhalt).


### 2.5 modules/ui_project_tree.py & modules/ui_filters.py – Rechte Seite

Verantwortung:

- ui_project_tree.py: Tree-/Listen-Ansicht (Runner / Dateien / Projektstruktur).
- ui_filters.py: Filter- / Refresh-Logik für die rechte Seite.

Special-Helper (in ui_toolbar):

- _r1838_refresh_right_list(app):
  - bevorzugt ui_filters.refresh(app)
  - fällt zurück auf app.right_list.refresh(), falls vorhanden.

**Stabilitätsregel:**  
Refresh-Logik für die rechte Seite soll über _r1838_refresh_right_list(app) laufen, damit UI-Änderungen zentral verkabelt bleiben.


### 2.6 modules/ui_leds.py – LED-Bar & SyntaxLED

Verantwortung:

- build_led_bar(parent):
  - erzeugt LED-Bar-Widget (z. B. Syntax, Pfade, Runner-Status).
- evaluate(app):
  - analysiert Intake-Inhalt
  - setzt LED-Zustände
  - schreibt bei Problemen Logs (z. B. SyntaxLED-Parsefehler) nach debug_output.txt.

R1908 – SyntaxLED-Hardening:

- Evaluate-Block ist jetzt gegen Ausrutscher abgesichert.
- _sanitize_code_for_syntax_check(...) ist erweitert (Invisible Characters, BOM, etc.).
- Fehler werden sinnvoll geloggt, ohne Log-Spam.

**Patch-Zone:**  
ui_leds.py ist ein klar definierter Ort für weitere Sicherheits-/Analyse-Verbesserungen.


### 2.7 modules/ui_theme_classic.py – Styles & Farben

Verantwortung:

- Enthält Farben, Fonts und Stil-Definitionen für Buttons und Flächen.
- Wird in allen GUI-Modulen verwendet (Toolbar, Panels, Tabs).

**Lernpunkt:**  
Toolbar-Implementierungen müssen zur tatsächlich vorhandenen API in ui_theme_classic passen (keine Annahmen über nicht existierende Konstanten).


### 2.8 Settings & Config – config_manager.py, ui_settings_tab.py, module_settings_ui.py

Verantwortung:

- config_manager.py:
  - Laden/Schreiben von ShrimpDev.ini.
  - Zentrale Settings wie:
    - workspace_root
    - quiet_mode
    - weitere Flags / Pfade.
- ui_settings_tab.py:
  - Stellt einen „Settings“-Tab bereit (UI-Seite).
  - Bietet Controls für die in config_manager verwaltete Config.
- module_settings_ui.py (falls vorhanden):
  - Ergänzende UI-Bausteine / Dialoge.

**Zielrichtung:**  
Konsolidierte und nachvollziehbare Nutzung von ShrimpDev.ini in allen betroffenen Modulen.


### 2.9 module_runner_popup.py

Verantwortung:

- Popups rund um Runner-Ausführung:
  - Statusmeldungen
  - Fehlermeldungen
  - ggf. Details aus debug_output.txt / Reports

**Schnittstelle:**  
Aufgerufen über logic_actions / Runner-UI, darf selbst keine core-Logik enthalten, sondern darstellen.


### 2.10 LearningJournal-Module

Verantwortung:

- Laden & Anzeigen von learning_journal.json.
- Tabs / Views für Einträge und Historie.
- Logging wie z. B.:
  - [module_learningjournal] … LearningJournal geladen: X Einträge
  - [module_learningjournal] … LearningJournal-Tab (Phase C) gebaut …

**Regel:**  
LearningJournal ist persistenter Wissensspeicher – Änderungen nur nachvollziehbar (Runner mit Reports, Backups).


---

## 3. Runner-System (tools/R####.cmd + .py)

### 3.1 Grundstruktur

- tools/R####.cmd
  - setzt PROJECT_ROOT
  - startet R####.py (python/py)
  - hält Konsole offen (Pause am Ende)

- tools/R####.py
  - bestimmt Projektroot (eine Ebene über tools)
  - findet Ziel-Dateien
  - legt Backups im _Archiv-Verzeichnis an
  - führt minimal-invasive Änderungen aus
  - loggt in Konsole und ggf. debug_output.txt
  - beendet sich mit Code 0 (Erfolg) oder 1 (Fehler)

### 3.2 Speicherorte

- _Archiv
  - Backups, z. B.:
    - ui_toolbar.py.R1909_YYYYMMDD_HHMMSS.bak
- _Snapshots
  - ZIP-Snapshots, z. B.:
    - ShrimpDev_YYYYMMDD_HHMMSS_R1668.zip
- _Reports
  - Reports, z. B.:
    - R1715_LearningJournal_Report.json

### 3.3 Regeln für Runner (Mastermodus)

- Ein Runner = ein klarer Zweck (ein Fehler, ein Feature, eine Zone).
- Niemals Voll-Rewrite eines Moduls ohne ausdrückliche Freigabe.
- Immer:
  - Backup vor Änderung
  - kleinster möglicher Diff
  - logging der vorgenommenen Schritte
- Patch-Zonen vorher definieren (z. B. nur _action_show_log in ui_toolbar).


---

## 4. Config & Persistenz

### 4.1 ShrimpDev.ini

Zentrale INI-Datei im Projektroot. Beispiele:

- [Core]
  - workspace_root = D:\ShrimpDev
  - quiet_mode = false
- [LogWindow]
  - geometry = 900x600+100+100
- weitere Sektionen:
  - MainWindow (Geometrie, AOT)
  - Tabs / zuletzt benutzte Pfade

Genutzt von:

- config_manager.py
- ui_toolbar._action_show_log (Log-Fenster-Geometrie)
- zukünftigen Features (Profile, Workspaces, etc.).


### 4.2 debug_output.txt

- Zentrales Logfile.
- Formattypisch:
  - [module_name] YYYY-MM-DD HH:MM:SS Nachricht
- Dient als Grundlage für:
  - Log-Fenster (Log-Button in Toolbar)
  - Debug / Fehleranalyse
  - Sanity-/Runner-Ausgaben.

Geplante Erweiterungen:

- Tail-Log beim Öffnen (nicht mehr Full-Load).
- Button „Ältere laden“.
- Live-Update via Timer.
- Bessere Nutzbarkeit in Verbindung mit AOT.


### 4.3 learning_journal.json

- JSON-Struktur mit Einträgen (Snippets, Learnings, Entscheidungen).
- Wird in LearningJournal-Tab angezeigt.
- Kann von Runnern (z. B. R1715) „aufgeräumt“ werden (Dedup, Normalisierung, Reports).


---

## 5. Startup-Sequenz (vereinfacht)

1. Start:
   - D:\ShrimpDev\main_gui.py

2. main_gui.main():
   - erstellt ShrimpDevApp()

3. ShrimpDevApp.__init__():
   - (optional) Config laden (config_manager)
   - Notebook & Tabs erstellen
   - Intake-Struktur aufbauen (Toolbar, Editor, LED-Bar)
   - LearningJournal-Tab und Settings-Tab bauen

4. Tkinter mainloop:
   - Button-Klicks, Menüaufrufe, Tree-Events
   - → logic_actions
   - → Module / Runner
   - → Dateien, Logs, LED-Update


---

## 6. Stabilitäts- & Patch-Zonen

**Stabile Zonen (möglichst unverändert halten):**

- main_gui.py – App & Tab-Struktur
- Signaturen in logic_actions.py (action_*-API)
- Öffentliche UI-Einstiegspunkte:
  - ui_toolbar.build_toolbar / build_toolbar_left/right
  - ui_leds.build_led_bar / ui_leds.evaluate

**Patch-Zonen (für Runner geeignet):**

- ui_toolbar._action_show_log(app)
  - Log-Viewer-Verhalten (Tail, Buttons, Position, Live-Update)
- ui_leds.py
  - weitere Hardening-/Analyse-Verbesserungen
- config_manager.py / ui_settings_tab.py
  - neue Settings, Konsolidierung der INI-Nutzung
- spezieller Logik-Code in logic_actions (gezielt, nicht flächendeckend)


---

## 7. Disziplin: Wie wir sicherstellen, dass wir uns daran halten

1. Vor jedem neuen Runner:
   - Prüfen: Welche Module werden angefasst?
   - Gegencheck in dieser Architektur: Ist das eine erlaubte Patch-Zone?
   - Wenn nicht: Design anpassen oder explizit freigeben.

2. Nach jedem Patch-Runner:
   - Kurzen Eintrag ins LearningJournal:
     - Welche Module?
     - Welcher Zweck?
     - Welche Patch-Zone?
   - Ggf. Version/Status dieser Datei auf v0.2, v0.3 etc. hochziehen.

3. Harte Regeln:
   - Keine fremden „Standardmodule“ über eigene Dateien bügeln.
   - Keine neuen Abhängigkeiten ohne Eintrag hier.
   - Kein cross-modularer Wildwuchs (alles über logic_actions / definierte UI-Funktionen).

Damit wird diese Datei zur Referenz für alle zukünftigen Entscheidungen rund um ShrimpDev.


<!-- AUTO:MODULES_START -->
### Module (automatisch generiert)

**UI Module:**
- ui_buttons.py
- ui_filters.py
- ui_learningpanel.py
- ui_leds.py
- ui_left_panel.py
- ui_lists.py
- ui_menus.py
- ui_project_tree.py
- ui_settings_tab.py
- ui_statusbar.py
- ui_theme_classic.py
- ui_themes.py
- ui_toolbar.py
- ui_toolbar_dev.py
- ui_tooltips.py

**Logic Module:**
- logic_actions.py
- logic_intake.py
- logic_tools.py

**Other Module:**
- __init__.py
- common_tabs.py
- config_loader.py
- config_manager.py
- config_mgr.py
- learning_engine.py
- main_shortcuts_patch.py
- module_agent.py
- module_agent_ui.py
- module_code_intake.py
- module_code_intake_v1.py
- module_gate_panel.py
- module_gate_smoke.py
- module_intake_workers.py
- module_learningjournal.py
- module_learningjournal_ui_ext.py
- module_patch_release.py
- module_preflight.py
- module_project_scan.py
- module_project_ui.py
- module_registry.py
- module_runner_board.py
- module_runner_exec.py
- module_runner_popup.py
- module_runnerbar.py
- module_settings_ui.py
- module_shim_intake.py



<!-- AUTO:MODULES_END -->


<!-- AUTO:RUNNERS_START -->
### Runner (automatisch generiert – kompakte Version)

- Anzahl Runner (PY): 824
- Anzahl Runner (CMD): 382
- Nummernbereich: R1266 – R9999

**Lücken:**
- Zwischen R1299 und R1301
- Zwischen R1305 und R1307
- Zwischen R1308 und R1351
- Zwischen R1351 und R1401
- Zwischen R1438 und R1440
- Zwischen R1455 und R1457
- Zwischen R1458 und R1461
- Zwischen R1488 und R1491
- Zwischen R1514 und R1516
- Zwischen R1521 und R1523
- Zwischen R1533 und R1601
- Zwischen R1608 und R1610
- Zwischen R1615 und R1617
- Zwischen R1628 und R1630
- Zwischen R1648 und R1650
- Zwischen R1664 und R1666
- Zwischen R1682 und R1684
- Zwischen R1690 und R1692
- Zwischen R1716 und R1800
- Zwischen R1819 und R1821
- Zwischen R1824 und R1826
- Zwischen R1849 und R1851
- Zwischen R1853 und R1901
- Zwischen R1912 und R1920
- Zwischen R1935 und R9900
- Zwischen R9900 und R9997

**Wichtige System-Runner:**
- R1668 – Snapshot System
- R1715 – LearningJournal Stabilisierung
- R1908 – SyntaxLED-Hardening
- R1922 – MasterRulesGuard v3
- R1931 – Architecture Snapshot
- R1932 – Architecture Delta
- R1933 – Integrity Check
- R1934 – Architecture Auto-Update
- R1935 – Auto-Sektion-Installer



<!-- AUTO:RUNNERS_END -->


<!-- AUTO:STATS_START -->
### Projektstatistik (automatisch generiert)

- Anzahl Module: 45
- Anzahl Runner (PY): 824



<!-- AUTO:STATS_END -->


<!-- AUTO:INTEGRITY_LAST_START -->
### Letzter Integrity Check (automatisch importiert)

```
ShrimpDev Architecture Integrity Check
Generated: 2025-12-03 20:27:03
Project root: D:\ShrimpDev
=====================================

ERRORS:
  - Modul ist leer (0 Bytes): __init__.py
  - Modul ist leer (0 Bytes): module_gate_panel.py
  - Verbotenes Pattern 'subprocess.Popen(' in Modul: logic_actions.py
  - Verbotenes Pattern 'subprocess.Popen(' in Modul: logic_tools.py
  - Verbotenes Pattern 'subprocess.Popen(' in Modul: module_code_intake.py
  - Verbotenes Pattern 'subprocess.Popen(' in Modul: module_runner_board.py
  - Verbotenes Pattern 'subprocess.Popen(' in Modul: module_runner_exec.py
  - Verbotenes Pattern 'subprocess.Popen(' in Modul: module_runner_popup.py
  - Verbotenes Pattern 'subprocess.Popen(' in Modul: module_runnerbar.py
  - Verbotenes Pattern 'subprocess.Popen(' in Modul: ui_buttons.py
  - Verbotenes Pattern 'eval(' in Modul: ui_left_panel.py

WARNINGS:
  - Runner-Nummernlücke: R1299 -> R1301
  - Runner-Nummernlücke: R1305 -> R1307
  - Runner-Nummernlücke: R1308 -> R1351
  - Runner-Nummernlücke: R1351 -> R1401
  - Runner-Nummernlücke: R1438 -> R1440
  - Runner-Nummernlücke: R1455 -> R1457
  - Runner-Nummernlücke: R1458 -> R1461
  - Runner-Nummernlücke: R1488 -> R1491
  - Runner-Nummernlücke: R1514 -> R1516
  - Runner-Nummernlücke: R1521 -> R1523
  - Runner-Nummernlücke: R1533 -> R1601
  - Runner-Nummernlücke: R1608 -> R1610
  - Runner-Nummernlücke: R1615 -> R1617
  - Runner-Nummernlücke: R1628 -> R1630
  - Runner-Nummernlücke: R1648 -> R1650
  - Runner-Nummernlücke: R1664 -> R1666
  - Runner-Nummernlücke: R1682 -> R1684
  - Runner-Nummernlücke: R1690 -> R1692
  - Runner-Nummernlücke: R1716 -> R1800
  - Runner-Nummernlücke: R1819 -> R1821
  - Runner-Nummernlücke: R1824 -> R1826
  - Runner-Nummernlücke: R1849 -> R1851
  - Runner-Nummernlücke: R1853 -> R1901
  - Runner-Nummernlücke: R1912 -> R1920
  - Runner-Nummernlücke: R1933 -> R9900
  - Runner-Nummernlücke: R9900 -> R9997
  - Fehlende PY-Datei für Runner 1288: R1288.py
  - Fehlende PY-Datei für Runner 1297: R1297.py
  - Fehlende PY-Datei für Runner 1301: R1301.py
  - Fehlende PY-Datei für Runner 1305: R1305.py
  - Fehlende PY-Datei für Runner 1402: R1402.py
  - Fehlende PY-Datei für Runner 1404: R1404.py
  - Fehlende PY-Datei für Runner 1405: R1405.py
  - Fehlende PY-Datei für Runner 1406: R1406.py
  - Fehlende PY-Datei für Runner 1418: R1418.py
  - Fehlende PY-Datei für Runner 1420: R1420.py
  - Fehlende PY-Datei für Runner 1421: R1421.py
  - Fehlende PY-Datei für Runner 1423: R1423.py
  - Fehlende PY-Datei für Runner 1428: R1428.py
  - Fehlende PY-Datei für Runner 1429: R1429.py
  - Fehlende PY-Datei für Runner 1430: R1430.py
  - Fehlende PY-Datei für Runner 1431: R1431.py
  - Fehlende PY-Datei für Runner 1432: R1432.py
  - Fehlende PY-Datei für Runner 1433: R1433.py
  - Fehlende PY-Datei für Runner 1436: R1436.py
  - Fehlende CMD-Datei für Runner 1471: R1471.cmd
  - Fehlende CMD-Datei für Runner 1472: R1472.cmd
  - Fehlende PY-Datei für Runner 1532: R1532.py
  - Fehlende CMD-Datei für Runner 1638: R1638.cmd
  - Fehlende PY-Datei für Runner 1639: R1639.py
  - Fehlende PY-Datei für Runner 1841: R1841.py

Modules analyzed:
  * __init__.py
  * common_tabs.py
  * config_loader.py
  * config_manager.py
  * config_mgr.py
  * learning_engine.py
  * logic_actions.py
  * logic_intake.py
  * logic_tools.py
  * main_shortcuts_patch.py
  * module_agent.py
  * module_agent_ui.py
  * module_code_intake.py
  * module_code_intake_v1.py
  * module_gate_panel.py
  * module_gate_smoke.py
  * module_intake_workers.py
  * module_learningjournal.py
  * module_learningjournal_ui_ext.py
  * module_patch_release.py
  * module_preflight.py
  * module_project_scan.py
  * module_project_ui.py
  * module_registry.py
  * module_runner_board.py
  * module_runner_exec.py
  * module_runner_popup.py
  * module_runnerbar.py
  * module_settings_ui.py
  * module_shim_intake.py
  * ui_buttons.py
  * ui_filters.py
  * ui_learningpanel.py
  * ui_leds.py
  * ui_left_panel.py
  * ui_lists.py
  * ui_menus.py
  * ui_project_tree.py
  * ui_settings_tab.py
  * ui_statusbar.py
  * ui_theme_classic.py
  * ui_themes.py
  * ui_toolbar.py
  * ui_toolbar_dev.py
  * ui_tooltips.py

Tools analyzed:
  * R1252_LearningJournal.py
  * R1266.py
  * R1267.py
  * R1268.py
  * R1269.py
  * R1270.py
  * R1271.py
  * R1272.py
  * R1273.py
  * R1274.py
  * R1275.py
  * R1276.py
  * R1277.py
  * R1278.py
  * R1279.py
  * R1280.py
  * R1281.py
  * R1282.py
  * R1283.py
  * R1284.py
  * R1285.py
  * R1286.py
  * R1287.py
  * R1288_RestoreOriginalIntake.py
  * R1289.py
  * R1290.py
  * R1291.py
  * R1292.py
  * R1293.py
  * R1294.py
  * R1295.py
  * R1296.py
  * R1298.py
  * R1299.py
  * R1300_IntakeV1_Install.py
  * R1301_IntakeV1_Install.py
  * R1302.py
  * R1303.py
  * R1304.py
  * R1305_IntakeHardFix.py
  * R1306_FixIntakeV1.py
  * R1307.py
  * R1308.py
  * R1310_IntakeV1_Fix.py
  * R1311_RestoreTrueIntake.py
  * R1312_FixMainGUI_IntakeMount.py
  * R1313_MainGUI_TrueFix.py
  * R1350_LearningJournalTab.py
  * R1351.py
  * R1351_MainGUI_FixFutureImport.py
  * R1401.py
  * R1402_PatchTopmostAndLabels.py
  * R1403.py
  * R1404_RemoveRootMenuPatch.py
  * R1405_FixRootMenuBlock.py
  * R1405_PatchIntakeNaming.py
  * R1406_UI_NamesAndVersion.py
  * R1407.py
  * R1407_Fastfix.py
  * R1408.py
  * R1409.py
  * R1410.py
  * R1411.py
  * R1412.py
  * R1413.py
  * R1413_FixIntakeIndent.py
  * R1414.py
  * R1415.py
  * R1416.py
  * R1417.py
  * R1418_FixMainGuiClass.py
  * R1419.py
  * R1420_FixMainEntry.py
  * R1421_UIThemeAndTabs.py
  * R1422.py
  * R1422_DefaultPath.py
  * R1423_MenuAndPolish.py
  * R1424.py
  * R1425.py
  * R1426.py
  * R1427.py
  * R1428_IntakeHeal.py
  * R1429_SyntaxRepair.py
  * R1430_IntakeAndMenuGuards.py
  * R1431_FixMenuAndStarter.py
  * R1432_AddIntakeHelpers.py
  * R1433_ShrimpAppRestore.py
  * R1434.py
  * R1434_FixTryBlocks.py
  * R1435.py
  * R1436_FutureOrderFix.py
  * R1437.py
  * R1438.py
  * R1440.py
  * R1441.py
  * R1442.py
  * R1443.py
  * R1444.py
  * R1445.py
  * R1446.py
  * R1447.py
  * R1448.py
  * R1449.py
  * R1450.py
  * R1451.py
  * R1452.py
  * R1453.py
  * R1454.py
  * R1455.py
  * R1457.py
  * R1458.py
  * R1461.py
  * R1462.py
  * R1463.py
  * R1464.py
  * R1465.py
  * R1466.py
  * R1467.py
  * R1468.py
  * R1469.py
  * R1470.py
  * R1471.py
  * R1472.py
  * R1473.py
  * R1474.py
  * R1475.py
  * R1476.py
  * R1477.py
  * R1478.py
  * R1479.py
  * R1480.py
  * R1481.py
  * R1482.py
  * R1483.py
  * R1484.py
  * R1485.py
  * R1486.py
  * R1487.py
  * R1488.py
  * R1491.py
  * R1492.py
  * R1493.py
  * R1494.py
  * R1495.py
  * R1496.py
  * R1497.py
  * R1498.py
  * R1499.py
  * R1500.py
  * R1501.py
  * R1502.py
  * R1503.py
  * R1504.py
  * R1504b.py
  * R1505.py
  * R1506.py
  * R1507.py
  * R1508.py
  * R1509.py
  * R1510.py
  * R1511.py
  * R1512.py
  * R1513.py
  * R1514.py
  * R1516.py
  * R1517.py
  * R1518.py
  * R1519.py
  * R1520.py
  * R1521.py
  * R1523.py
  * R1524.py
  * R1525.py
  * R1526.py
  * R1527.py
  * R1528.py
  * R1529.py
  * R1530.py
  * R1531.py
  * R1533.py
  * R1601.py
  * R1602.py
  * R1603.py
  * R1604.py
  * R1605.py
  * R1606.py
  * R1607.py
  * R1608.py
  * R1610.py
  * R1611.py
  * R1612.py
  * R1613.py
  * R1614.py
  * R1615.py
  * R1617.py
  * R1618.py
  * R1619.py
  * R1620.py
  * R1621.py
  * R1622.py
  * R1623.py
  * R1623b.py
  * R1624.py
  * R1625.py
  * R1626.py
  * R1627.py
  * R1628.py
  * R1630.py
  * R1631.py
  * R1632.py
  * R1633.py
  * R1634.py
  * R1635.py
  * R1636.py
  * R1637.py
  * R1638.py
  * R1640.py
  * R1641.py
  * R1642.py
  * R1643.py
  * R1644.py
  * R1645.py
  * R1646.py
  * R1647.py
  * R1648.py
  * R1648b.py
  * R1650.py
  * R1651.py
  * R1652.py
  * R1653.py
  * R1654.py
  * R1655.py
  * R1656.py
  * R1657.py
  * R1658.py
  * R1659.py
  * R1660.py
  * R1661.py
  * R1662.py
  * R1663.py
  * R1664.py
  * R1666.py
  * R1667.py
  * R1668.py
  * R1669.py
  * R1670.py
  * R1670b.py
  * R1671.py
  * R1672.py
  * R1673.py
  * R1674.py
  * R1675.py
  * R1676.py
  * R1677.py
  * R1678.py
  * R1679.py
  * R1680.py
  * R1681.py
  * R1682.py
  * R1684.py
  * R1685.py
  * R1686.py
  * R1687.py
  * R1688.py
  * R1689.py
  * R1690.py
  * R1690b.py
  * R1692.py
  * R1693.py
  * R1693b.py
  * R1694.py
  * R1694b.py
  * R1695.py
  * R1696.py
  * R1697.py
  * R1698.py
  * R1699.py
  * R1700.py
  * R1701.py
  * R1702.py
  * R1703.py
  * R1704.py
  * R1705.py
  * R1706.py
  * R1707.py
  * R1708.py
  * R1709.py
  * R1710.py
  * R1711.py
  * R1712.py
  * R1713.py
  * R1714.py
  * R1715.py
  * R1716.py
  * R1800.py
  * R1801.py
  * R1802.py
  * R1803.py
  * R1804.py
  * R1805.py
  * R1806.py
  * R1807.py
  * R1808.py
  * R1809.py
  * R1810.py
  * R1811.py
  * R1812.py
  * R1813.py
  * R1814.py
  * R1815.py
  * R1816.py
  * R1817.py
  * R1818.py
  * R1819.py
  * R1821.py
  * R1822.py
  * R1823.py
  * R1824.py
  * R1826.py
  * R1827.py
  * R1828.py
  * R1829.py
  * R1830.py
  * R1831.py
  * R1832.py
  * R1833.py
  * R1834.py
  * R1835.py
  * R1836.py
  * R1837.py
  * R1838.py
  * R1839.py
  * R1840.py
  * R1841b.py
  * R1842.py
  * R1843.py
  * R1844.py
  * R1845.py
  * R1846.py
  * R1847.py
  * R1848.py
  * R1849.py
  * R1851.py
  * R1852.py
  * R1853.py
  * R1901.py
  * R1902.py
  * R1903.py
  * R1904.py
  * R1905.py
  * R1906.py
  * R1907.py
  * R1908.py
  * R1909.py
  * R1910.py
  * R1911.py
  * R1912.py
  * R1920.py
  * R1921.py
  * R1922.py
  * R1923.py
  * R1924.py
  * R1925.py
  * R1926.py
  * R1927.py
  * R1928.py
  * R1929.py
  * R1930.py
  * R1931.py
  * R1931b.py
  * R1932.py
  * R1933.py
  * R9900.py
  * R9997.py
  * R9998.py
  * R9999.py
  * Runner_1000_IntakeActions.py
  * Runner_1001_AlwaysOnTopFixImports.py
  * Runner_1002_SnippetsRestore.py
  * Runner_1003_FixIndentFallbackLogger.py
  * Runner_1004_ShrimpDev_PathFix.py
  * Runner_1005_MainGUI_Rewrite.py
  * Runner_1006_ConfigMgr_Restore.py
  * Runner_1007_UIFrames_Restore.py
  * Runner_1008_IntakeUX_Revamp.py
  * Runner_1010_IntakeUX_Refine.py
  * Runner_1011_IntakeUX_ActionsBar.py
  * Runner_1012_FixMenuIndent.py
  * Runner_1013_SafeBoot_Debug.py
  * Runner_1014_SafeBoot_StringFix.py
  * Runner_1015_SafeBoot_StringHardFix.py
  * Runner_1016_IntakeFix_ContextActions.py
  * Runner_1017_IntakeUX_CopyPasteName.py
  * Runner_1018_ExtOverride_AndQA.py
  * Runner_1019_ExtOverride_DetectFix.py
  * Runner_1020_SafeBoot_Logfix.py
  * Runner_1021_SafeBoot_FinalFix.py
  * Runner_1022_MainGUI_SafeImportsRepair.py
  * Runner_1023_SafeFallbackRepair.py
  * Runner_1024_LoggerAtomicFix.py
  * Runner_1025_SafeFallbackCapture.py
  * Runner_1026_IntakeIndentFix.py
  * Runner_1027_IntakeSaveRewrite.py
  * Runner_1028_IntakeModule_Reset.py
  * Runner_1030_IntakeButtons_Fix.py
  * Runner_1031_ButtonsForceWire_Debug.py
  * Runner_1032_ButtonsHardBind_Ping.py
  * Runner_1033_FixBrokenPanedwindow.py
  * Runner_1034_IntakeDetect_SmartFix.py
  * Runner_1035_DetectWire_All.py
  * Runner_1036_NameDetect_FromCode.py
  * Runner_1037_FixDetectSyntax.py
  * Runner_1038_DetectBlock_Rewrite.py
  * Runner_1039_IndentFix_TryExcept.py
  * Runner_1040_Intake_FullReset.py
  * Runner_1041_AutoDetect_OnPaste.py
  * Runner_1042_AutoDetect_Hardwire_Scan.py
  * Runner_1043_NoBell_StripTypeHints.py
  * Runner_1044_Intake_Reinstall_Clean.py
  * Runner_1045_NameForceAndDateCols.py
  * Runner_1046_NameDocstring_Fallback_DateCols.py
  * Runner_1047_Intake_CleanHardReset.py
  * Runner_1048_Intake_DeleteAndRecent50.py
  * Runner_1049_Intake_ResizeNameExt.py
  * Runner_1050_ExtDetectStrong.py
  * Runner_1051_ExtDetectStrong_FixSub.py
  * Runner_1052_FixEntExtGrid.py
  * Runner_1053_Intake_ClearOnDelete_RefreshOnPaste.py
  * Runner_1054_Intake_QuoteFix_ClearDelete_PasteReset.py
  * Runner_1055_FixIndent_OnEditorModified.py
  * Runner_1056_FixIndent_OnEditorModified_Strict.py
  * Runner_1057_IndentAudit_IntakeFrame.py
  * Runner_1058_FixKeyAndModified_Block.py
  * Runner_1059_FixDeleteIndent.py
  * Runner_1060_FixAskYesNo_StringConcat.py
  * Runner_1061_FixAskYesNo_StringEscape.py
  * Runner_1062_FutureAtTop.py
  * Runner_1063_Intake_SanityGuard.py
  * Runner_1064_IntegrateGuard_UI.py
  * Runner_1065_IntakeRescueAndRollback.py
  * Runner_1066_FixGuard_MissingHelpers.py
  * Runner_1067_WriteGuard_Safe.py
  * Runner_1068_FixLonelyTry.py
  * Runner_1069_FixIntake_GuardToolbar.py
  * Runner_1070_FixSemicolonLines.py
  * Runner_1071_AddRunButton_PyExec.py
  * Runner_1072_InsertRunButton_AnyAnchor.py
  * Runner_1073_FixToolbarAndRunButton.py
  * Runner_1074_DeleteButtons_WithRecycleBin.py
  * Runner_1074b_DeleteButtons_WithRecycleBin_Fix.py
  * Runner_1077_FixIndent_UIBlock.py
  * Runner_1078_WriteGuard_Clean.py
  * Runner_1082_Guard_VerboseOK.py
  * Runner_1084_FixGuard_ArgParse.py
  * Runner_1089_ApplyNameDetect_GuardRun_Delete.py
  * Runner_1090_FixIntake_Indent.py
  * Runner_1092_FixRecycleBinIndent.py
  * Runner_1093_FixIntake_IndentGlobal.py
  * Runner_1094_FixRecycleBinIndentFinal.py
  * Runner_1095_ClassSafeguard_Intake.py
  * Runner_1096_Reindent_IntakeMethods.py
  * Runner_1097_FixIntake_Reindent.py
  * Runner_1097b_FixIntake_Reindent2.py
  * Runner_1097c_FixIntake_ReindentHard.py
  * Runner_1097d_Reindent_Intake_Strict.py
  * Runner_1098_FixIntake_ReindentClassBlocks.py
  * Runner_1099_FixIntake_RepairIndentPass2.py
  * Runner_1100_FixIntake_ReindentAll.py
  * Runner_1100_Reindent_IntakeFrame_Harden.py
  * Runner_1101_FixIntake_ReindentAll.py
  * Runner_1101a_FixReplace_RecycleBin.py
  * Runner_1102_FixIntake_ReindentAndScope.py
  * Runner_1103_FixIntake_ReindentAndScope.py
  * Runner_1104_ReplaceIntake_Clean.py
  * Runner_1105_FixDeleteSignature_Compile.py
  * Runner_1106_ShrimpGuard_Integriert.py
  * Runner_1106b_IntegrateGuard_UI.py
  * Runner_1106c_IntegrateGuard_UI_FixedFuture.py
  * Runner_1107_AutoRepair_IndentBlocks.py
  * Runner_1107_AutoRepair_Intake_BindsAndTry.py
  * Runner_1107b_AutoRepair_IndentBlocks_ReturnFix.py
  * Runner_1108_DisableButtonReleaseBinds.py
  * Runner_1109_EnableTkCallbackTrace.py
  * Runner_1110_FixIntake_ToolbarTryAndHelpers.py
  * Runner_1112_DeepRepair_IntakeAndGUI.py
  * Runner_1113_DeepRepair_FixReturnScope.py
  * Runner_1114_DeepSanityAndRepair.py
  * Runner_1114b_FixUnexpectedIndent_MainGUI.py
  * Runner_1115_IntegrateRepairUI.py
  * Runner_1116_ReentrantBindGuard.py
  * Runner_1116a_FixMainGUITabs.py
  * Runner_1116b_ReentrantBindGuard_AST.py
  * Runner_1116c_DeepFix_IntakeUI.py
  * Runner_1116d_FixRecycleBinHelper_Only.py
  * Runner_1116e_DeepFix_IntakeUI_Safe.py
  * Runner_1116f_DumpSyntaxContext.py
  * Runner_1116g_FixToolbarBlock.py
  * Runner_1117.py
  * Runner_1118_SafeTkHandler.py
  * Runner_1118b_GlobalTkPatch.py
  * Runner_1119_TkGuardTopLevel.py
  * Runner_1120_FixFutureAndGuard.py
  * Runner_1121_CentralGuard.py
  * Runner_1122_RepairMainGUI_SafeLogging.py
  * Runner_1123_EditorGuardPatch.py
  * Runner_1124_AllFixes_IntakeStable.py
  * Runner_1125_IntakeRescue.py
  * Runner_1126_IntakeRescue2.py
  * Runner_1127_IntakeDetox.py
  * Runner_1127_IntakeFix_All.py
  * Runner_1128_FixToolbarAndBindings.py
  * Runner_1129_IntakeLoadGuard.py
  * Runner_1130_IntakeDiagnose.py
  * Runner_1131_FixIntakeToolbar.py
  * Runner_1132_FixGuardParent.py
  * Runner_1132_FixIntakeActions.py
  * Runner_1133_IntakeAutoHeal.py
  * Runner_1134_IntakePathFix.py
  * Runner_1135_ModulesInitAndDiagnose.py
  * Runner_1136_FixMissingRepairButton.py
  * Runner_1137_IntakeLoadFix.py
  * Runner_1137a_IntakeLoadFix.py
  * Runner_1138_IntakeLoadFix2.py
  * Runner_1139_IntakeFrameRepair.py
  * Runner_1140_IntakeFinalFix.py
  * Runner_1141_IntakeDefuse.py
  * Runner_1142_DefuseSafe.py
  * Runner_1143_IntakeToolbarGuardFix.py
  * Runner_1143b_IntakeToolbarGuardFix_Safe.py
  * Runner_1144_ReplaceIntakeSafe.py
  * Runner_1145_IntakeAudit.py
  * Runner_1146_FeatureGapAudit.py
  * Runner_1148_ImproveDetection.py
  * Runner_1148b_ForceDetectionFix.py
  * Runner_1149_TablePopulate.py
  * Runner_1150_DetectionFinalFix.py
  * Runner_1151_AddPackSaveButton.py
  * Runner_1152_TableUX_Interactions.py
  * Runner_1153_SmartDetect_AutoSave.py
  * Runner_1153d_RegexHyphenFix.py
  * Runner_1153e_PathInitFix.py
  * Runner_1153f_SafeDetectRegex.py
  * Runner_1153g_SafeRegexAllIntake.py
  * Runner_1153h_FixDetectAndRegex.py
  * Runner_1153k_DetectGuard.py
  * Runner_1154_AddDeleteButtons.py
  * Runner_1154b_AddDeleteButtons.py
  * Runner_1154c_AddDeleteButtons.py
  * Runner_1154d_FixIntakeToolbarAndGuard.py
  * Runner_1154e_IntakeSyntaxHeal.py
  * Runner_1154f_IntakeSyntaxHeal.py
  * Runner_1154g_FixIntakeButtonsAndGuard.py
  * Runner_1154h_FixMissingBuildUiDef.py
  * Runner_1155_IntakeBootDiag.py
  * Runner_1156_AddInitAndBuildUI.py
  * Runner_1156c_FixTtkAndInitUI.py
  * Runner_1156d_TtkGlobalizeLocals.py
  * Runner_1156e_CombineInitAndTtk.py
  * Runner_1157_FixDetectPatterns.py
  * Runner_1158_UX_ToolbarLayout.py
  * Runner_1158c_UX_ToolbarLayoutFix.py
  * Runner_1161_DetectRegex_Hotfix.py
  * Runner_1162_DetectRegexScanner.py
  * Runner_1163_DetectGuardFix.py
  * Runner_1163b_DetectGuardFixSafe.py
  * Runner_1163d_DetectGuardFixSafePlain.py
  * Runner_1163e_DetectGuardFix_AST.py
  * Runner_1163f_FixPyHeadRegex.py
  * Runner_1163h2_FixPythonHeadRegex_SafePlain.py
  * Runner_1163h3_FixPythonHeadRegex_DirectReplace.py
  * Runner_1163h4_FixPythonHeadRegex_LineSwap.py
  * Runner_1163h_FixPythonHeadRegex_Safe.py
  * Runner_1164_ClearAlsoClearsExt.py
  * Runner_1164b_OptionalConfirmOnClear.py
  * Runner_1164c_ClearExt_And_OptionalConfirm.py
  * Runner_1164d_ClearExt_OptionalConfirm_Traversal.py
  * Runner_1165_IntakeInitFix.py
  * Runner_1166_IntakeTTK_ScopeFix_and_Rules.py
  * Runner_1166b_IntakeScopeFix_SafeIndent.py
  * Runner_1166c_Intake_MinimalScopeFix.py
  * Runner_1166d_Intake_IndentAndTTKFix.py
  * Runner_1166e_Intake_FinalFix.py
  * Runner_1166f_Intake_DeepRepair.py
  * Runner_1166g_Intake_SafeDedent.py
  * Runner_1166h_Intake_SafeDedent2.py
  * Runner_1167a_Intake_SanityCheck.py
  * Runner_1167b_GUIIntakePresenceCheck.py
  * Runner_1167c_GUIRenderTrace.py
  * Runner_1167d_GUIMountRefresher.py
  * Runner_1167e_RunnerExecSafeImport.py
  * Runner_1167f_RunnerExecSafeImport2.py
  * Runner_1167g_RunnerExecLogAppendSafe.py
  * Runner_1167h_IntakeErrDump.py
  * Runner_1167i_IntakeFix_CallModuleFunc.py
  * Runner_1167j_IniDetectHelperPatch.py
  * Runner_1170a_IntakeRegression.py
  * Runner_1170b_IntakeBindRepair.py
  * Runner_1170c_IntakeShortcutWire.py
  * Runner_1170d_UXLayoutPolish.py
  * Runner_1170e_IntakeLifecycleWire.py
  * Runner_1171a_IntakeUXAndDetect.py
  * Runner_1171b_IntakeUXAndDetect.py
  * Runner_1171c_IntakeDetectClean.py
  * Runner_1171d_IntakeHelperIndentFix.py
  * Runner_1171e_IntakeToolbarFix.py
  * Runner_1171f_IntakeToolbarFix2.py
  * Runner_1171g_IntakeToolbarReflow.py
  * Runner_1171h_IntakeHelperIndentSweep.py
  * Runner_1171j_IntakeToolbarReflowTopLevel.py
  * Runner_1171k_IntakeToolbarReflowExternalize.py
  * Runner_1171m_IntakeToolbarReflowFix.py
  * Runner_1171n_IntakeSyntaxRebuilder.py
  * Runner_1171p_IntakeIndentHeal.py
  * Runner_1171q_IntakeCleanAndExternalize.py
  * Runner_1171q_IntakeToolbarReflowSafe.py
  * Runner_1171r_IntakeUILayoutTidy.py
  * Runner_1172_IntakeTabGuard.py
  * Runner_1173_IntakeUILayoutFix.py
  * Runner_1173b_IntakeUILayoutFix.py
  * Runner_1173c_IntakeTTKImportFix.py
  * Runner_1173d_IntakeFallbackReturnFix.py
  * Runner_1173e_MainGuiTabHelper.py
  * Runner_1173f_IntakeTabSafeAdd.py
  * Runner_1173g_IntakeTabSmoke.py
  * Runner_1173h_MainGuiHelpersOrderFix.py
  * Runner_1173i_MainGuiHeadDedent.py
  * Runner_1173k_MainGuiCallRelocate.py
  * Runner_1173m_MainGuiIntakeWireFix.py
  * Runner_1173p_MainGuiIntakeWireForce.py
  * Runner_1173z_IntakeSmoke.py
  * Runner_1174a_MainGuiIntakeHelpersFix.py
  * Runner_1174aa_IntakeTabCleanser.py
  * Runner_1174b_MainGuiIntakeHelpersFix.py
  * Runner_1174c_MainGuiIntakeHelpersFix.py
  * Runner_1174d_MainGuiIntakeCleanup.py
  * Runner_1174e_MainGuiIntakeCleanup.py
  * Runner_1174f_MainGuiIntakeCleanup.py
  * Runner_1174g_IntakeClassRebind.py
  * Runner_1174g_IntakePostBuildFix.py
  * Runner_1174g_MainGuiReorderFix.py
  * Runner_1174h_IntakeHardReset.py
  * Runner_1174i_IntakeRestoreSmart.py
  * Runner_1174j_IntakeRestoreSmartFix.py
  * Runner_1174k_IntakeFeatureRestore.py
  * Runner_1174m_IntakeFrameRebuild.py
  * Runner_1174n_IntakeHotFix_UIInit.py
  * Runner_1174p_IntakeCtorFix.py
  * Runner_1174r_IntakeTabRebind.py
  * Runner_1174s_MainGuiSmoke.py
  * Runner_1174t_IntakeTabRebindFix.py
  * Runner_1174u_MainGuiRestoreLast.py
  * Runner_1174v_IntakeTabHarden.py
  * Runner_1174w_MainSyntaxSmoke.py
  * Runner_1174x_IntakeRevive.py
  * Runner_1174y_DebugPathFix.py
  * Runner_1174z_DebugPathFix.py
  * Runner_1174z_IntakeTabRestoreSafe.py
  * Runner_1175a_MainGuiIntakeHelperFix.py
  * Runner_1175b_IntakeApiSoftGuard.py
  * Runner_1175d_MainEntryGuard.py
  * Runner_1175e_MainIntakeShim.py
  * Runner_1175f_IntakeShimFix.py
  * Runner_1175g_ModulesPackageFix.py
  * Runner_1175h_IntakeCleanRestore.py
  * Runner_1175i_RemoveFakeNbAdd.py
  * Runner_1175m_IntakeResurrect.py
  * Runner_1175n_FixPyCallAndCleanMain.py
  * Runner_1175q_IntakeHardRestore.py
  * Runner_1176a_IntakeShimUpgrade.py
  * Runner_1176b_FixIntakeMount.py
  * Runner_1176c_GatePanelIntegration.py
  * Runner_1176d_FixShimName.py
  * Runner_1176d_IntakeShimHotfix.py
  * Runner_1177a_IntakeMountAdapter.py
  * Runner_1177a_IntakeMountAdapter_Hotfix.py
  * Runner_1177b_DevIntakeRestore.py
  * Runner_1177b_IntakeRestore.py
  * Runner_1177c_IntakeRecover.py
  * Runner_1177d_DevIntakeButtons.py
  * Runner_1177e_DevToolbarFix.py
  * Runner_1177f_DevIntakeVisualFix.py
  * Runner_1177g_DevIntakeCoreRebuild.py
  * Runner_1177h_IntakeImportCheck.py
  * Runner_1177i_ImportPathFix.py
  * Runner_1177j_IntakeShimHardFix.py
  * Runner_1177k_RuntimeImportBridge.py
  * Runner_1177l_CleanTabMount.py
  * Runner_1177m_FixMainAndGate.py
  * Runner_1177m_MainGuiFix.py
  * Runner_1177n_GatePanelUpdate.py
  * Runner_1178i_ImportPathFix.py
  * Runner_1178j_FixDevIntake.py
  * Runner_1178m_FixGatePanelAndLaunch.py
  * Runner_1178o_FixGatePanelAndLaunch.py
  * Runner_1180_StartFix.py
  * Runner_1181_IntakeDeDuplicate.py
  * Runner_1181b_MainGuiIndentFix.py
  * Runner_1181c_MainGuiIndentFix2.py
  * Runner_1181d_MainGuiTryFix.py
  * Runner_1182_DevIntakePro.py
  * Runner_1182a_DevIntakePro_Clean.py
  * Runner_1183_DevIntakeUX.py
  * Runner_1183c_DevIntakeUX_DetectFix.py
  * Runner_1184_DevIntakeUX_Polish.py
  * Runner_1185_DevIntakeLEDs_Detect2.py
  * Runner_1185b_DevIntakeLEDs_Detect2Fix.py
  * Runner_1186_IntakeUX_FixDetectAndUX.py
  * Runner_1187_IntakeLEDs_Add.py
  * Runner_1188_IntakeLEDs_DetectHardening.py
  * Runner_1189_IntakeRepairAndLEDsFix.py
  * Runner_1190_DevIntake_Install.py
  * Runner_1191_DevIntake_CleanInstall.py
  * Runner_1192_DevIntake_UIRefine.py
  * Runner_1193_DevIntake_FixDetectAndInstall.py
  * Runner_1193_IntakeDetectUpgrade.py
  * Runner_1194_DevIntake_UIArrange.py
  * Runner_1194_LEDBackgroundFix.py
  * Runner_1195_DevIntake_UISortPolish.py
  * Runner_1196_DevIntake_Apply.py
  * Runner_1198_IntakeLedFix.py
  * Runner_1199_FixSaveAndLEDs.py
  * Runner_1199_IntakeHotfix.py
  * Runner_1200_DevIntake_AutoDetectAndPolish.py
  * Runner_1201_DevIntake_Stabilize.py
  * Runner_1202_FixIndentationPath.py
  * Runner_1203_DevIntake_Recovery.py
  * Runner_1204_FixIndent_AutoDetect_SaveAs.py
  * Runner_1205_FixIntakeIndentAndLEDs.py
  * Runner_1206_FixIntakeCore.py
  * Runner_1207_FixIntakeCoreSafe.py
  * Runner_1208_FixRegexEscape.py
  * Runner_1209_IntakePathFinalFix.py
  * Runner_1210_DevIntake_FixCoreAndUX.py
  * Runner_1211_FixIntakeCoreStable.py
  * Runner_1212_FixIntakeCoreStable.py
  * Runner_1213_FixIntakeCoreStable.py
  * Runner_1214_FixIntake_Final.py
  * Runner_1215_FixIntakeCoreFinal.py
  * Runner_1216_FixIntakeCore_Final.py
  * Runner_1217_FixIntakeCoreSuperSafe.py
  * Runner_1218_FixIntake_NewlineSafe.py
  * Runner_1218_FixIntakeCoreSuperSafe.py
  * Runner_1220_SyntaxGate_AllModules.py
  * Runner_1221_IntakeCore_Addons.py
  * Runner_1225_IntakeCore_RepairAndIntegrate.py
  * Runner_1230_RestoreIntakeFromBackup.py
  * Runner_1231_Intake_MinimalFixes.py
  * Runner_1234_IntakeCore_RepairIntegrate.py
  * Runner_1241_Intake_AllInOne.py
  * Runner_1242_Intake_RepairAndIntegrate.py
  * Runner_1244_SyntaxRecovery_Final.py
  * Runner_1244b_SyntaxRecovery_Final.py
  * Runner_1245_IntakeSyntaxResurrection.py
  * Runner_1246_IntakeCodePurge.py
  * Runner_1247_WriteTextFixer.py
  * Runner_1248_IntakeSyntaxRescue.py
  * Runner_1249_IntakeHardRestore.py
  * Runner_1250_MasterRulesPersist.py
  * Runner_1251_SanityGateDaemon.py
  * Runner_1257_AddCmdSupport.py
  * Runner_1258_IntakeRebuildFinal.py
  * Runner_1259_IntakeRegexRebuild.py
  * Runner_1260_IntakeRegexFinalFix.py
  * Runner_1262_IntakeRestoreFromBackups.py
  * Runner_1263_IntakeBackupDeepScan.py
  * Runner_1264.py
  * Runner_1265.py
  * Runner_1293_UpdateIntakeMount.py
  * Runner_900_Setup.py
  * Runner_901_Verify.py
  * Runner_902_LogTail.py
  * Runner_902_Starter.py
  * Runner_903_Fix.py
  * Runner_904_WarnSilence.py
  * Runner_905_FixToggle.py
  * Runner_910_Install.py
  * Runner_911_Scan.py
  * Runner_912_Watch.py
  * Runner_913_Silence.py
  * Runner_914_NoPopup.py
  * Runner_915_QuietToggle.py
  * Runner_916_ScanUX.py
  * Runner_917_FixIndent.py
  * Runner_918_FixIndentMain.py
  * Runner_930_AllInOne.py
  * Runner_935_FixMainGUI.py
  * Runner_940_CoreKit.py
  * Runner_941_Preflight.py
  * Runner_942_NewModule.py
  * Runner_943_NewRunner.py
  * Runner_944_AllGUIIntegrate.py
  * Runner_946_IntakeSmart.py
  * Runner_947_IntakeSelfTest.py
  * Runner_948_IntakeUX.py
  * Runner_949_TryFix.py
  * Runner_950.py
  * Runner_951_FixAgentStart.py
  * Runner_952_FixTryEverywhere.py
  * Runner_953_FixLoneTry.py
  * Runner_954_MainCleanup.py
  * Runner_956_Unswallow.py
  * Runner_957_FixMainBlock.py
  * Runner_960_BootFix.py
  * Runner_960_Menus.py
  * Runner_961_MenuFix.py
  * Runner_962_FixMainGUI.py
  * Runner_970_AllInOneInstall.py
  * Runner_971_UnifyTabs.py
  * Runner_972_SafePatch.py
  * Runner_980_DevConsolidate.py
  * Runner_981_IntakeUX.py
  * Runner_982_IntakeUIEnhance.py
  * Runner_983_IntakeFix.py
  * Runner_984_IntakeGeometryFix.py
  * Runner_990_FixGUI.py
  * Runner_991_AllTabsIntegrate.py
  * Runner_995_IntakeDetectorFix.py
  * Runner_996_IntakeFix_And_Default.py
  * Runner_997_Intake_BatAndDefault.py
  * Runner_998_DefaultIntake.py
  * Runner_998_IntakeBatDetector.py
  * Runner_999_Test.py
  * R1252_LearningJournal.cmd
  * R1266.cmd
  * R1267.cmd
  * R1268.cmd
  * R1269.cmd
  * R1270.cmd
  * R1271.cmd
  * R1272.cmd
  * R1273.cmd
  * R1274.cmd
  * R1275.cmd
  * R1276.cmd
  * R1277.cmd
  * R1278.cmd
  * R1279.cmd
  * R1280.cmd
  * R1281.cmd
  * R1282.cmd
  * R1283.cmd
  * R1284.cmd
  * R1285.cmd
  * R1286.cmd
  * R1287.cmd
  * R1288.cmd
  * R1289.cmd
  * R1290.cmd
  * R1291.cmd
  * R1292.cmd
  * R1293.cmd
  * R1294.cmd
  * R1295.cmd
  * R1296.cmd
  * R1297.cmd
  * R1298.cmd
  * R1299.cmd
  * R1300_IntakeV1_Install.cmd
  * R1301.cmd
  * R1302.cmd
  * R1303.cmd
  * R1304.cmd
  * R1305.cmd
  * R1306_FixIntakeV1.cmd
  * R1307.cmd
  * R1308.cmd
  * R1310_IntakeV1_Fix.cmd
  * R1311_RestoreTrueIntake.cmd
  * R1312_FixMainGUI_IntakeMount.cmd
  * R1313_MainGUI_TrueFix.cmd
  * R1350_LearningJournalTab.cmd
  * R1351.cmd
  * R1351_MainGUI_FixFutureImport.cmd
  * R1401.cmd
  * R1402.cmd
  * R1403.cmd
  * R1404.cmd
  * R1405.cmd
  * R1406.cmd
  * R1407.cmd
  * R1408.cmd
  * R1409.cmd
  * R1410.cmd
  * R1411.cmd
  * R1412.cmd
  * R1413.cmd
  * R1414.cmd
  * R1415.cmd
  * R1416.cmd
  * R1417.cmd
  * R1418.cmd
  * R1419.cmd
  * R1420.cmd
  * R1421.cmd
  * R1422.cmd
  * R1423.cmd
  * R1424.cmd
  * R1425.cmd
  * R1426.cmd
  * R1427.cmd
  * R1428.cmd
  * R1429.cmd
  * R1430.cmd
  * R1431.cmd
  * R1432.cmd
  * R1433.cmd
  * R1434.cmd
  * R1435.cmd
  * R1436.cmd
  * R1437.cmd
  * R1438.cmd
  * R1440.cmd
  * R1441.cmd
  * R1442.cmd
  * R1443.cmd
  * R1444.cmd
  * R1445.cmd
  * R1446.cmd
  * R1447.cmd
  * R1448.cmd
  * R1449.cmd
  * R1450.cmd
  * R1451.cmd
  * R1452.cmd
  * R1453.cmd
  * R1454.cmd
  * R1455.cmd
  * R1457.cmd
  * R1458.cmd
  * R1461.cmd
  * R1462.cmd
  * R1463.cmd
  * R1464.cmd
  * R1465.cmd
  * R1466.cmd
  * R1467.cmd
  * R1468.cmd
  * R1469.cmd
  * R1470.cmd
  * R1473.cmd
  * R1474.cmd
  * R1475.cmd
  * R1476.cmd
  * R1477.cmd
  * R1478.cmd
  * R1479.cmd
  * R1480.cmd
  * R1481.cmd
  * R1482.cmd
  * R1483.cmd
  * R1484.cmd
  * R1485.cmd
  * R1486.cmd
  * R1487.cmd
  * R1488.cmd
  * R1491.cmd
  * R1492.cmd
  * R1493.cmd
  * R1494.cmd
  * R1495.cmd
  * R1496.cmd
  * R1497.cmd
  * R1498.cmd
  * R1499.cmd
  * R1500.cmd
  * R1501.cmd
  * R1502.cmd
  * R1503.cmd
  * R1504.cmd
  * R1504b.cmd
  * R1505.cmd
  * R1506.cmd
  * R1507.cmd
  * R1508.cmd
  * R1509.cmd
  * R1510.cmd
  * R1511.cmd
  * R1512.cmd
  * R1513.cmd
  * R1514.cmd
  * R1516.cmd
  * R1517.cmd
  * R1518.cmd
  * R1519.cmd
  * R1520.cmd
  * R1521.cmd
  * R1523.cmd
  * R1524.cmd
  * R1525.cmd
  * R1526.cmd
  * R1527.cmd
  * R1528.cmd
  * R1529.cmd
  * R1530.cmd
  * R1531.cmd
  * R1532.cmd
  * R1533.cmd
  * R1601.cmd
  * R1602.cmd
  * R1603.cmd
  * R1604.cmd
  * R1605.cmd
  * R1606.cmd
  * R1607.cmd
  * R1608.cmd
  * R1610.cmd
  * R1611.cmd
  * R1612.cmd
  * R1613.cmd
  * R1614.cmd
  * R1615.cmd
  * R1617.cmd
  * R1618.cmd
  * R1619.cmd
  * R1620.cmd
  * R1621.cmd
  * R1622.cmd
  * R1623.cmd
  * R1623b.cmd
  * R1624.cmd
  * R1625.cmd
  * R1626.cmd
  * R1627.cmd
  * R1628.cmd
  * R1630.cmd
  * R1631.cmd
  * R1632.cmd
  * R1633.cmd
  * R1634.cmd
  * R1635.cmd
  * R1636.cmd
  * R1637.cmd
  * R1639.cmd
  * R1640.cmd
  * R1641.cmd
  * R1642.cmd
  * R1643.cmd
  * R1644.cmd
  * R1645.cmd
  * R1646.cmd
  * R1647.cmd
  * R1648.cmd
  * R1648b.cmd
  * R1650.cmd
  * R1651.cmd
  * R1652.cmd
  * R1653.cmd
  * R1654.cmd
  * R1655.cmd
  * R1656.cmd
  * R1657.cmd
  * R1658.cmd
  * R1659.cmd
  * R1660.cmd
  * R1661.cmd
  * R1662.cmd
  * R1663.cmd
  * R1664.cmd
  * R1666.cmd
  * R1667.cmd
  * R1668.cmd
  * R1669.cmd
  * R1670.cmd
  * R1670b.cmd
  * R1671.cmd
  * R1672.cmd
  * R1673.cmd
  * R1674.cmd
  * R1675.cmd
  * R1676.cmd
  * R1677.cmd
  * R1678.cmd
  * R1679.cmd
  * R1680.cmd
  * R1681.cmd
  * R1682.cmd
  * R1684.cmd
  * R1685.cmd
  * R1686.cmd
  * R1687.cmd
  * R1688.cmd
  * R1689.cmd
  * R1690.cmd
  * R1690b.cmd
  * R1692.cmd
  * R1693.cmd
  * R1693b.cmd
  * R1694.cmd
  * R1694b.cmd
  * R1695.cmd
  * R1696.cmd
  * R1697.cmd
  * R1698.cmd
  * R1699.cmd
  * R1700.cmd
  * R1701.cmd
  * R1702.cmd
  * R1703.cmd
  * R1704.cmd
  * R1705.cmd
  * R1706.cmd
  * R1707.cmd
  * R1708.cmd
  * R1709.cmd
  * R1710.cmd
  * R1711.cmd
  * R1712.cmd
  * R1713.cmd
  * R1714.cmd
  * R1715.cmd
  * R1716.cmd
  * R1800.cmd
  * R1801.cmd
  * R1802.cmd
  * R1803.cmd
  * R1804.cmd
  * R1805.cmd
  * R1806.cmd
  * R1807.cmd
  * R1808.cmd
  * R1809.cmd
  * R1810.cmd
  * R1811.cmd
  * R1812.cmd
  * R1813.cmd
  * R1814.cmd
  * R1815.cmd
  * R1816.cmd
  * R1817.cmd
  * R1818.cmd
  * R1819.cmd
  * R1821.cmd
  * R1822.cmd
  * R1823.cmd
  * R1824.cmd
  * R1826.cmd
  * R1827.cmd
  * R1828.cmd
  * R1829.cmd
  * R1830.cmd
  * R1831.cmd
  * R1832.cmd
  * R1833.cmd
  * R1834.cmd
  * R1835.cmd
  * R1836.cmd
  * R1837.cmd
  * R1838.cmd
  * R1839.cmd
  * R1840.cmd
  * R1841.cmd
  * R1841b.cmd
  * R1842.cmd
  * R1843.cmd
  * R1844.cmd
  * R1845.cmd
  * R1846.cmd
  * R1847.cmd
  * R1848.cmd
  * R1849.cmd
  * R1851.cmd
  * R1852.cmd
  * R1853.cmd
  * R1901.cmd
  * R1902.cmd
  * R1903.cmd
  * R1904.cmd
  * R1905.cmd
  * R1906.cmd
  * R1907.cmd
  * R1908.cmd
  * R1909.cmd
  * R1910.cmd
  * R1911.cmd
  * R1912.cmd
  * R1920.cmd
  * R1921.cmd
  * R1922.cmd
  * R1923.cmd
  * R1924.cmd
  * R1925.cmd
  * R1926.cmd
  * R1927.cmd
  * R1928.cmd
  * R1929.cmd
  * R1930.cmd
  * R1931.cmd
  * R1931b.cmd
  * R1932.cmd
  * R1933.cmd
  * R9900.cmd
  * R9997.cmd
  * R9998.cmd
  * R9999.cmd
  * Runner_1247_WriteTextFixer.cmd
  * Runner_1250_MasterRulesPersist.cmd
  * Runner_1251_SanityGateDaemon.cmd
  * Runner_1262_IntakeRestoreFromBackups.cmd
  * Runner_1263_IntakeBackupDeepScan.cmd
  * Runner_1264.cmd
  * Runner_1265.cmd
  * Runner_1293_UpdateIntakeMount.cmd
```

<!-- AUTO:INTEGRITY_LAST_END -->
