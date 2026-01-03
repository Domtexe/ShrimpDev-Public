@echo off
setlocal ENABLEDELAYEDEXPANSION
pushd "%~dp0\.."
echo [1170e] Patch: Lifecycle-Wire am Ende von _build_ui(self) injizieren...
py -3 -u "tools\Runner_1170e_IntakeLifecycleWire.py"
set rc=%ERRORLEVEL%
if %rc% NEQ 0 (
  echo [1170e] FEHLER. Siehe debug_output.txt
) else (
  echo [1170e] OK. Siehe debug_output.txt
)
popd
exit /B %rc%
