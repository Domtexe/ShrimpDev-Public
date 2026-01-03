@echo off
setlocal
cd /d "%~dp0\.."
echo [R1177c] Recovering original ShrimpDev Intake from _Archiv...
py -3 -u "tools\Runner_1177c_IntakeRecover.py"
set rc=%ERRORLEVEL%
if %rc% NEQ 0 (
  echo [R1177c] FAILED (exit %rc%)
  exit /b %rc%
)
echo [R1177c] DONE. Launching Main GUI...
if exist "tools\Start_MainGui.bat" call "tools\Start_MainGui.bat"
exit /b 0
