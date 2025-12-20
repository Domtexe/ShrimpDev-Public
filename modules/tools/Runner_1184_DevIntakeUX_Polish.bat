@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0\.."
set "PY=py"
set "PYFLAGS=-3 -u"

echo [R1184] Installing Dev-Intake UX Polish...
"%PY%" %PYFLAGS% "tools\Runner_1184_DevIntakeUX_Polish.py"
set RC=%ERRORLEVEL%
if %RC% NEQ 0 (
  echo [R1184] FAILED (rc=%RC%). Siehe debug_output.txt
  exit /b %RC%
)

echo [R1184] OK. Launching Main GUI...
if exist "tools\Start_MainGui.bat" (
  call "tools\Start_MainGui.bat"
) else (
  "%PY%" %PYFLAGS% "main_gui.py"
)
exit /b 0
