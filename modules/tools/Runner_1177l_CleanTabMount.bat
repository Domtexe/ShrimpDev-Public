@echo off
setlocal
cd /d "%~dp0\.."
echo [R1177l] Applying Clean Tab-Mount for ShrimpDev...
py -3 -u "tools\Runner_1177l_CleanTabMount.py"
set rc=%ERRORLEVEL%
if %rc% NEQ 0 (
  echo [R1177l] FAILED with exit code %rc%
  exit /b %rc%
)
echo [R1177l] OK. Launching Main GUI...
if exist "tools\Start_MainGui.bat" call "tools\Start_MainGui.bat"
exit /b 0
