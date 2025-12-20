@echo off
setlocal
cd /d "%~dp0\.."
echo [R1177j] Applying Intake Shim HardFix...
py -3 -u "tools\Runner_1177j_IntakeShimHardFix.py"
set rc=%ERRORLEVEL%
if %rc% NEQ 0 (
  echo [R1177j] FAILED with exit code %rc%
  exit /b %rc%
)
echo [R1177j] OK. Launching Main GUI...
if exist "tools\Start_MainGui.bat" call "tools\Start_MainGui.bat"
exit /b 0
