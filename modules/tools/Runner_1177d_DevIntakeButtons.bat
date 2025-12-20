@echo off
setlocal
cd /d "%~dp0\.."
echo [R1177d] Restoring Dev-Intake toolbar & actions...
py -3 -u "tools\Runner_1177d_DevIntakeButtons.py"
set rc=%ERRORLEVEL%
if %rc% NEQ 0 (
  echo [R1177d] FAILED with exit code %rc%
  exit /b %rc%
)
echo [R1177d] OK. Launching Main GUI...
if exist "tools\Start_MainGui.bat" call "tools\Start_MainGui.bat"
exit /b 0
