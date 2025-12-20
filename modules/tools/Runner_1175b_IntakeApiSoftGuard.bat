@echo off
setlocal
echo [1175b] IntakeApiSoftGuard: starte Patch...
where py >nul 2>&1 && (set PY=py -3) || (set PY=python)
%PY% "D:\ShrimpDev\tools\Runner_1175b_IntakeApiSoftGuard.py"
if errorlevel 1 (
  echo [1175b] FEHLER. Siehe Konsole/debug_output.txt
) else (
  echo [1175b] Patch erfolgreich, Syntax OK.
)
endlocal
