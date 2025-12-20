@echo off
setlocal
echo [1175i] RemoveFakeNbAdd: starte Fix...
where py >nul 2>&1 && (set PY=py -3) || (set PY=python)
%PY% "D:\ShrimpDev\tools\Runner_1175i_RemoveFakeNbAdd.py"
if errorlevel 1 (
  echo [1175i] FEHLER. Siehe Konsole / debug_output.txt
) else (
  echo [1175i] Fix erfolgreich, Syntax OK.
)
endlocal
