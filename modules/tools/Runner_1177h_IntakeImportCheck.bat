@echo off
setlocal
cd /d "%~dp0\.."
echo [R1177h] Running Intake import diagnostics...
py -3 -u "tools\Runner_1177h_IntakeImportCheck.py"
set rc=%ERRORLEVEL%
if %rc% NEQ 0 (
  echo [R1177h] FAILED with exit code %rc%
  exit /b %rc%
)
echo [R1177h] DONE. Check debug_output.txt for details.
pause
exit /b 0
