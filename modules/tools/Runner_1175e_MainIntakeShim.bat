@echo off
setlocal
echo [1175e] MainIntakeShim: starte Patch...
where py >nul 2>&1 && (set PY=py -3) || (set PY=python)
%PY% "D:\ShrimpDev\tools\Runner_1175e_MainIntakeShim.py"
if errorlevel 1 (
  echo [1175e] FEHLER. Siehe Konsole / debug_output.txt
) else (
  echo [1175e] Patch erfolgreich, Syntax OK.
)
endlocal
