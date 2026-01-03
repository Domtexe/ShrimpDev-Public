@echo off
setlocal
cd /d "%~dp0\.."
echo [R1177a] Starting IntakeMountAdapter Runner...
py -3 -u "tools\Runner_1177a_IntakeMountAdapter.py"
set rc=%ERRORLEVEL%
if %rc% NEQ 0 (
  echo [R1177a] Runner failed with exit code %rc%.
  exit /b %rc%
)
echo [R1177a] Runner finished successfully.
exit /b 0
