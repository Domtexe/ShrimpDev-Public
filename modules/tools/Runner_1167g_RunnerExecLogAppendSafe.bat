@echo off
setlocal ENABLEDELAYEDEXPANSION
pushd "%~dp0\.."
echo [1167g] RunnerExec: sichere _log()-Wrapper-Definition anhängen...
py -3 -u "tools\Runner_1167g_RunnerExecLogAppendSafe.py"
set rc=%ERRORLEVEL%
if %rc% NEQ 0 (
  echo [1167g] FEHLER (rc=%rc%). Siehe debug_output.txt
) else (
  echo [1167g] OK. Siehe debug_output.txt
)
popd
exit /B %rc%
