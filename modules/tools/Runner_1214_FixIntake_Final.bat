@echo off
setlocal
cd /d "%~dp0"
echo [R1214] FixIntake_Final starting...

REM Python 3 launcher ermitteln (py -3 bevorzugt)
set PY=py -3
%PY% -V >nul 2>&1 || set PY=py
%PY% -V >nul 2>&1 || set PY=python

%PY% -u "%~dp0Runner_1214_FixIntake_Final.py"
set rc=%ERRORLEVEL%
if not %rc%==0 (
  echo [R1214] FAILED. Siehe debug_output.txt
  exit /b %rc%
)

echo [R1214] Done. Launching GUI...
cd /d "D:\ShrimpDev"
%PY% -3 -u main_gui.py
endlocal
