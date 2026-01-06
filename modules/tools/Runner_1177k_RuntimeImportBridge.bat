@echo off
setlocal
cd /d "%~dp0\.."
echo [R1177k] Applying RuntimeImportBridge (module_shim_intake.py)...
py -3 -u "tools\Runner_1177k_RuntimeImportBridge.py"
set rc=%ERRORLEVEL%
if %rc% NEQ 0 (
  echo [R1177k] FAILED with exit code %rc%
  exit /b %rc%
)
echo [R1177k] OK. Launching Main GUI...
if exist "tools\Start_MainGui.bat" call "tools\Start_MainGui.bat"
exit /b 0
