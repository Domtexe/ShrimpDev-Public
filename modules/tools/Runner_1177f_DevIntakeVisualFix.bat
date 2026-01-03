@echo off
setlocal
cd /d "%~dp0\.."
echo [R1177f] Applying DevIntake Visual Fix (Imports + Toolbar mount)...
py -3 -u "tools\Runner_1177f_DevIntakeVisualFix.py"
set rc=%ERRORLEVEL%
if %rc% NEQ 0 (
  echo [R1177f] FAILED with exit code %rc%
  exit /b %rc%
)
echo [R1177f] OK. Launching Main GUI...
if exist "tools\Start_MainGui.bat" call "tools\Start_MainGui.bat"
exit /b 0
