@echo off
setlocal
pushd "%~dp0\.."
echo [1171k] IntakeToolbarReflowExternalize: starte sicheren Patch...
py -3 -u "tools\Runner_1171k_IntakeToolbarReflowExternalize.py"
set rc=%ERRORLEVEL%
if %rc% neq 0 (
  echo [1171k] FEHLER (rc=%rc%). Siehe debug_output.txt
) else (
  echo [1171k] OK. Siehe debug_output.txt
)
popd
exit /b %rc%
