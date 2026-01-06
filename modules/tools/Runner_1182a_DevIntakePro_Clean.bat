@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0\.."
set "PY=py"
set "PYFLAGS=-3 -u"

echo [R1182a] Installing Dev-Intake Pro (clean ASCII)...
"%PY%" %PYFLAGS% "tools\Runner_1182a_DevIntakePro_Clean.py"
set RC=%ERRORLEVEL%
if %RC% NEQ 0 (
  echo [R1182a] FAILED (rc=%RC%). See debug_output.txt
  exit /b %RC%
)

echo [R1182a] OK. Launching Main GUI...
if exist "tools\Start_MainGui.bat" (
  call "tools\Start_MainGui.bat"
) else (
  "%PY%" %PYFLAGS% "main_gui.py"
)
exit /b 0
