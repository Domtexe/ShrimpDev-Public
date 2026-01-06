@echo off
setlocal
echo [1175a] MainGuiIntakeHelperFix: starte Patch...

REM Python 3 Launcher robust ermitteln
where py >nul 2>&1 && (set PY=py -3) || (set PY=python)

%PY% "D:\ShrimpDev\tools\Runner_1175a_MainGuiIntakeHelperFix.py"
if errorlevel 1 (
  echo [1175a] FEHLER. Siehe Konsole/debug_output.txt
) else (
  echo [1175a] Patch erfolgreich, Syntax OK.
)
endlocal
