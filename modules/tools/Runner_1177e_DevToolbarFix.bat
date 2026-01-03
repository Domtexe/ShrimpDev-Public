@echo off
setlocal
cd /d "%~dp0\.."
echo [R1177e] Applying Dev-Toolbar Fix...
py -3 -u "tools\Runner_1177e_DevToolbarFix.py"
set rc=%ERRORLEVEL%
if %rc% NEQ 0 (
  echo [R1177e] FAILED with exit code %rc%
  exit /b %rc%
)
echo [R1177e] OK. Launching Main GUI...
if exist "tools\Start_MainGui.bat" call "tools\Start_MainGui.bat"
exit /b 0
