# MasterRules_Runners – Runner-Standards

_Automatisch generiert oder aktualisiert durch R2037 am 2025-12-09 09:39:55_

## 1. Struktur

- Jeder Runner besteht aus einer `.cmd`-Datei (Starter) und einer `.py`-Datei
  (Logik), z. B. `tools/R2037.cmd` -> `tools/R2037.py`.
- Die .cmd-Datei setzt das Projekt-Root und startet Python mit der Runner-Logik.

## 2. Backups & Reports

- Vor Änderungen an wichtigen Dateien werden Backups mit ID und Timestamp
  angelegt (z. B. unter `_Archiv`).
- Jeder Runner, der Änderungen vornimmt, erzeugt einen Report unter `_Reports/`.

## 3. Exit-Codes

- Erfolgreiche Läufe beenden sich mit Exit-Code 0.
- Bei Fehlern wird ein Code ungleich 0 gesetzt und im Report dokumentiert.

## 4. Geltungsbereich

- Neue Runner bearbeiten nur den aktiven Codekern (z. B. `modules`, `tools`,
  `main_gui.py`) und lassen Archive (`_Trash`, `_OldStuff` etc.) unverändert.

## R2165 – Pflicht: Runner Guard
- Jeder neue Runner MUSS über runner_guard.run_guarded() laufen.
- Keine eigenen try/except-Blöcke in Runnern.
- Exceptions werden zentral nach debug_output.txt geschrieben.

## Runner Output Policy (Popup-first)
- (Neu, 2025-12-15 10:11:31) Runner werden standardmaessig im zentralen Runner-Popup ausgefuehrt (Exit-Code + Live-Output).
- Ausnahme nur, wenn die Ausfuehrung sichtbar/transparent ist (z.B. bewusstes externes Tool mit eindeutiger Rueckmeldung).

## Intake Detect Policy (Header-first)
- (Neu, 2025-12-15 10:11:31) Intake-Detect muss FILE/Path-Header (z.B. `# file: tools/R####.py`) priorisieren.
- Niemals nur die erste gefundene `R####`-ID im Text als Dateiname verwenden, wenn ein Header vorhanden ist.
- Empfehlung: jeder Runner beginnt mit `# file: tools/R####.py` als erste Zeile.

## Dokumentationspflicht (immer mitpflegen)
- (Neu, 2025-12-15 10:11:31) Bei jeder Aenderung muessen **Doku, Architektur, Pipeline, Changelog, CURRENT_VERSION** (und verwandte Uebersichten) mitgepflegt werden.
- Keine Implementierung ohne passende Aktualisierung der zugehoerigen Dokumentation.

## Zentraler Runner-Log (Pflicht)

- Runner-Logging ist zentral und einheitlich.
- Alle Runner-Starts (auch Tools-Buttons/Popup-Pfad) MUESSEN ueber `exception_logger` loggen:
  - START (rid, label)
  - STDOUT/STDERR
  - END (exit_code)
- Popup ist reine Anzeige und ersetzt kein Logging.
- Umgesetzt durch R2230 am 2025-12-15 18:17:36.

## Runner-Logging Pfad (Pflicht)
- Wenn logger im Package liegt, muss import relativ erfolgen (modules.exception_logger / from . import ...).

## Logging-Pflicht
- Runner-Logs MUESSEN in debug_output.txt landen (kein stilles Verschlucken).
- exception_logger implementiert log_runner_start/log_runner_output/log_runner_end robust.

## Runner-Bootstrap Pflicht

- Jeder Runner MUSS den Projekt-Root in `sys.path` setzen (keine Annahmen, kein Raten).
  Beispiel (am Anfang des .py):
  - `ROOT = Path(__file__).resolve().parents[1]`
  - `sys.path.insert(0, str(ROOT))`
- Danach erst `from modules import ...`.

- Runner-Logs MUESSEN in **`debug_output.txt`** landen (START/STDOUT/ERR/END, Exit-Code).
- Keine stillen Swallows: wenn Schreiben fehlschlägt, muss es im Runner-Output sichtbar sein.
- Einheitliche API: `modules.exception_logger.log_runner_start/log_runner_output/log_runner_end`.
### Zentralisiertes Runner-Logging (verbindlich)
- Runner-Start/Ende/Exit wird nur zentral geloggt (module_runner_exec/exception_logger).
- GUI/logic_actions darf kein eigenes Runner-Logging implementieren.
- logic_actions.action_run ist wegen verschachtelten try/except Bloecken keine Patch-Zielzone fuer Marker-Inserts.

