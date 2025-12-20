@echo off
setlocal ENABLEDELAYEDEXPANSION
pushd "%~dp0\.."
echo [1167e] RunnerExec SafeImport patchen...
py -3 -u "tools\Runner_1167e_RunnerExecSafeImport.py"
set rc=%ERRORLEVEL%
if %rc% NEQ 0 (
  echo [1167e] FEHLER (rc=%rc%). Siehe debug_output.txt
) else (
  echo [1167e] OK. Siehe debug_output.txt
)
popd
exit /B %rc%
