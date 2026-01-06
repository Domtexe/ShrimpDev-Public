@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0\.."
set "PY=py"
set "PYFLAGS=-3 -u"

echo [R1181d] Fixing broken try-block in main_gui.py...
"%PY%" %PYFLAGS% "tools\Runner_1181d_MainGuiTryFix.py"
set RC=%ERRORLEVEL%
if %RC% NEQ 0 (
  echo [R1181d] FAILED (rc=%RC%). See debug_output.txt
  exit /b %RC%
)

echo [R1181d] OK. Launching Main GUI...
if exist "tools\Start_MainGui.bat" (
  call "tools\Start_MainGui.bat"
) else (
  "%PY%" %PYFLAGS% "main_gui.py"
)
exit /b 0
