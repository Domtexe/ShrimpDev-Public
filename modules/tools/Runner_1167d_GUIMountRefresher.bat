@echo off
setlocal ENABLEDELAYEDEXPANSION
pushd "%~dp0\.."
echo [1167d] GUIMountRefresher: Patch main_gui.py (safe)...
py -3 -u "tools\Runner_1167d_GUIMountRefresher.py"
set rc=%ERRORLEVEL%
if %rc% NEQ 0 (
  echo [1167d] FEHLER (rc=%rc%). Siehe debug_output.txt
) else (
  echo [1167d] OK. Siehe debug_output.txt
)
popd
exit /B %rc%
