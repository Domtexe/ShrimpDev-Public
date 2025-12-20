@echo off
setlocal
cd /d "%~dp0\.."
echo [R1177b_Dev] Installing Dev-Intake...
py -3 -u "tools\Runner_1177b_DevIntakeRestore.py"
set rc=%ERRORLEVEL%
if %rc% NEQ 0 (
  echo [R1177b_Dev] FAILED with exit code %rc%
  exit /b %rc%
)
echo [R1177b_Dev] OK. Launching Main GUI...
if exist "tools\Start_MainGui.bat" call "tools\Start_MainGui.bat"
exit /b 0
