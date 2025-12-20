@echo off
setlocal
pushd "%~dp0\.."
echo [1171i] IntakeToolbarReflowSafe: starte sicheren Patch...
py -3 -u "tools\Runner_1171i_IntakeToolbarReflowSafe.py"
set rc=%ERRORLEVEL%
if %rc% neq 0 (
  echo [1171i] FEHLER (rc=%rc%). Siehe debug_output.txt
) else (
  echo [1171i] OK. Siehe debug_output.txt
)
popd
exit /b %rc%
