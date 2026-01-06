@echo off
setlocal
echo [1175f] IntakeShimFix: starte Patch...
where py >nul 2>&1 && (set PY=py -3) || (set PY=python)
%PY% "D:\ShrimpDev\tools\Runner_1175f_IntakeShimFix.py"
if errorlevel 1 (
  echo [1175f] FEHLER. Siehe Konsole / debug_output.txt
) else (
  echo [1175f] Patch erfolgreich, Syntax OK.
)
endlocal
