@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0\.."
set "PY=py"
set "PYFLAGS=-3 -u"

echo [R1183] Installing Dev-Intake UX...
"%PY%" %PYFLAGS% "tools\Runner_1183_DevIntakeUX.py"
set RC=%ERRORLEVEL%
if %RC% NEQ 0 (
  echo [R1183] FAILED (rc=%RC%). See debug_output.txt
  exit /b %RC%
)

echo [R1183] OK. Launching Main GUI...
if exist "tools\Start_MainGui.bat" (
  call "tools\Start_MainGui.bat"
) else (
  "%PY%" %PYFLAGS% "main_gui.py"
)
exit /b 0
