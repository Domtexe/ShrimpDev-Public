@echo off
setlocal
cd /d "%~dp0..\"
echo [1176b] FixIntakeMount: starte Patch...

REM Python 3 bevorzugt mit -3, fallback auf py
where py >nul 2>&1 && (set _PY=py -3) || (set _PY=python)

%_PY% -u "tools\Runner_1176b_FixIntakeMount.py"
if errorlevel 1 (
  echo [1176b] FEHLER. Siehe Konsole / debug_output.txt
  exit /b 1
)

echo [1176b] Patch erfolgreich, Syntax OK.
endlocal
