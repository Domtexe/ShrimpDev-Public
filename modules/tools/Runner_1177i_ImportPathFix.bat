@echo off
setlocal
cd /d "%~dp0\.."
echo [R1177i] Applying ImportPathFix (main_gui.py)...
py -3 -u "tools\Runner_1177i_ImportPathFix.py"
set rc=%ERRORLEVEL%
if %rc% NEQ 0 (
  echo [R1177i] FAILED with exit code %rc%
  exit /b %rc%
)
echo [R1177i] OK. Launching Main GUI...
if exist "tools\Start_MainGui.bat" call "tools\Start_MainGui.bat"
exit /b 0
