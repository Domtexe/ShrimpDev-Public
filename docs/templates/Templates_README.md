# Templates (Single Source of Truth)

Diese Templates sind verbindlich für neue Runner.

## Pflicht-Output (CMD)
- START-Block mit Trennern
- Root-Ausgabe
- ExitCode-Block
- Report-Hinweis

## Pflicht-Output (PY)
- schreibt Report in Reports/
- gibt Report-Pfad per print() aus

## Anti-Regression
- Neue Runner sollen aus diesen Templates erstellt werden.
- Wenn Output wieder 'hohl' wird: Output-Guard laufen lassen.

## Batch-Sonderzeichen (wichtig)
In .cmd-Dateien müssen Sonderzeichen in `echo` escaped werden:
- `&` als `^&`
- `|` als `^|`
- `>` als `^>` und `<` als `^<`
Sonst interpretiert CMD das als Befehlsverkettung/Redirect.

<!-- R9241_TEMPLATES_README -->
## Runner_CMD_Template.cmd Requirements
- Must start with `@echo off`.
- Must set `RC` via `set "RC=%ERRORLEVEL%"` and exit `exit /b %RC%`.
- Must call `python tools\%RUNNER_ID%.py` (never `py -3`).
- Must be saved as ASCII+CRLF (guarded).

