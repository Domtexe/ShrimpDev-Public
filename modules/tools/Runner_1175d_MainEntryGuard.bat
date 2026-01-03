@echo off
setlocal
echo [1175d] MainEntryGuard: starte Patch...
where py >nul 2>&1 && (set PY=py -3) || (set PY=python)
%PY% "D:\ShrimpDev\tools\Runner_1175d_MainEntryGuard.py"
if errorlevel 1 (
  echo [1175d] FEHLER. Siehe Konsole / debug_output.txt
) else (
  echo [1175d] Patch erfolgreich, Syntax OK.
)
endlocal
