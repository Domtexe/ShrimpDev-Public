@echo off
setlocal ENABLEDELAYEDEXPANSION
pushd "%~dp0\.."
echo [1167f] RunnerExec SafeImport (zweiter Versuch)...
py -3 -u "tools\Runner_1167f_RunnerExecSafeImport2.py"
set rc=%ERRORLEVEL%
if %rc% NEQ 0 (
  echo [1167f] FEHLER (rc=%rc%). Siehe debug_output.txt
) else (
  echo [1167f] OK. Siehe debug_output.txt
)
popd
exit /B %rc%
