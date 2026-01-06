@echo off
setlocal ENABLEDELAYEDEXPANSION
pushd "%~dp0\.."
echo [1167j] Patch: robuste INI-Erkennung (Helper)...
py -3 -u "tools\Runner_1167j_IniDetectHelperPatch.py"
set rc=%ERRORLEVEL%
if %rc% NEQ 0 (
  echo [1167j] FEHLER (rc=%rc%). Siehe debug_output.txt
) else (
  echo [1167j] OK. Siehe debug_output.txt
)
popd
exit /B %rc%
