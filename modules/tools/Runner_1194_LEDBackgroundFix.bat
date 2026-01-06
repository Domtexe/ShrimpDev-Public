@echo off
setlocal
cd /d "%~dp0\.."
echo [R1194] Starting LEDBackgroundFix...

REM Python ermitteln
where py >nul 2>nul && (set PY=py) || (set PY=python)

%PY% -3 -u "tools\Runner_1194_LEDBackgroundFix.py"
set RC=%ERRORLEVEL%
if %RC% NEQ 0 (
  echo [R1194] FAILED (rc=%RC%). See debug_output.txt.
  exit /b %RC%
)

echo [R1194] OK. Launching Main GUI...
call tools\Start_MainGui.bat
endlocal
