@echo off
setlocal
cd /d "%~dp0\.."
echo [R1177b] Restoring Intake features...
py -3 -u "tools\Runner_1177b_IntakeRestore.py"
set rc=%ERRORLEVEL%
if %rc% NEQ 0 (
  echo [R1177b] FAILED with exit code %rc%
  exit /b %rc%
)
echo [R1177b] OK. Start Main GUI...
if exist "tools\Start_MainGui.bat" call "tools\Start_MainGui.bat"
exit /b 0
