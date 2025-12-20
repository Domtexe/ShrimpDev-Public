@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0\.."
set "PY=py"
set "PYFLAGS=-3 -u"

echo [R1186] Patch: UX-Fix + Detect-Guard...
"%PY%" %PYFLAGS% "tools\Runner_1186_IntakeUX_FixDetectAndUX.py"
set RC=%ERRORLEVEL%
if %RC% NEQ 0 (
  echo [R1186] FAILED (rc=%RC%). Siehe debug_output.txt
  exit /b %RC%
)

echo [R1186] OK. Starte Main GUI...
if exist "tools\Start_MainGui.bat" (
  call "tools\Start_MainGui.bat"
) else (
  "%PY%" %PYFLAGS% "main_gui.py"
)
exit /b 0
