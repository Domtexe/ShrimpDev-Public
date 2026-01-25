# Runner Execution – Canonical Path & Gateway Pattern

## Ziel
Runner-Ausführung muss **zentral, nachvollziehbar und governance-sicher** sein.
UI/Logic dürfen **niemals** Prozesse direkt starten. Stattdessen existiert
ein einziger kanonischer Ausführungspfad.

## Kanonischer Datenfluss (SSOT)
~~~
UI / Logic
    ↓
modules/module_runner_gateway.py
    ↓
modules/toolbar_runner_exec.py   (canonical executor)
    ↓
tools/R####.cmd  +  tools/R####.py
    ↓
Reports/Report_R####_*.md
~~~

## Motivation
- Verhindert verstreute subprocess-Aufrufe in UI/Logic
- Erzwingt einen Single Entry Point für Runner-Starts
- Erhöht Auditierbarkeit und Stabilität

## Erlaubt
- UI/Logic:
  - Nutzung von `module_runner_gateway.run_cmd_path(...)`
  - Öffnen von Dateien/Ordnern ausschließlich über `module_shell_open.open_path(...)`
- Executor/Core:
  - `toolbar_runner_exec.py`
  - `module_runner_exec.py`
  - `module_runner_popup.py`
  dürfen intern subprocess verwenden

## Verboten (No-Gos)
- `subprocess.Popen(...)` oder `subprocess.run(...)` in UI/Logic
- `os.system(...)` in UI/Logic
- `cmd /c tools\R####.cmd` außerhalb Gateway/Executor
- Direkte Calls wie `module_runner_exec.run(...)` aus UI/Logic

## Governance
- **DIAG-first**: Befund per Report
- **APPLY nur minimal** und gezielt
- **VERIFY Pflicht** nach APPLY (z. B. R3769)

## Referenzen
- Lane B Fixes: R3770, R3772, R3773
- Verify: R3769 (final)
