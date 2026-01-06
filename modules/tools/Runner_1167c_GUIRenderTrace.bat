@echo off
setlocal ENABLEDELAYEDEXPANSION
pushd "%~dp0\.."
echo [1167c] Starte GUI-Render-Trace (headless)...
py -3 -u "tools\Runner_1167c_GUIRenderTrace.py"
set rc=%ERRORLEVEL%
if %rc% NEQ 0 (
  echo [1167c] FEHLER (rc=%rc%). Siehe debug_output.txt
) else (
  echo [1167c] OK. Siehe debug_output.txt
)
popd
exit /B %rc%
