@echo off
setlocal
pushd "%~dp0\.."
echo [1171g] IntakeToolbarReflow: starte sicheren Patch...
py -3 -u "tools\Runner_1171g_IntakeToolbarReflow.py"
set rc=%ERRORLEVEL%
if %rc% neq 0 (
  echo [1171g] FEHLER (rc=%rc%). Siehe debug_output.txt
) else (
  echo [1171g] OK. Siehe debug_output.txt
)
popd
exit /b %rc%
