@echo off
setlocal
cd /d "%~dp0..\"
echo [1176c] GatePanelIntegration: starte Patch...

where py >nul 2>&1 && (set _PY=py -3) || (set _PY=python)

%_PY% -u "tools\Runner_1176c_GatePanelIntegration.py"
if errorlevel 1 (
  echo [1176c] FEHLER. Siehe Konsole / debug_output.txt
  exit /b 1
)

echo [1176c] Patch erfolgreich, Syntax OK.
endlocal
