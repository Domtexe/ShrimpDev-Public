@echo off
setlocal
cd /d "%~dp0..\"
echo [1176d] FixShimName: starte Patch...
where py >nul 2>&1 && (set _PY=py -3) || (set _PY=python)
%_PY% -u "tools\Runner_1176d_FixShimName.py"
if errorlevel 1 (
  echo [1176d] FEHLER. Siehe Konsole / debug_output.txt
  exit /b 1
)
echo [1176d] Patch erfolgreich, Syntax OK.
endlocal
