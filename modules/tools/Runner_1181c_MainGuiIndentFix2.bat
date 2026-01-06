@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0\.."
set "PY=py"
set "PYFLAGS=-3 -u"

echo [R1181c] MainGuiIndentFix2...
"%PY%" %PYFLAGS% "tools\Runner_1181c_MainGuiIndentFix2.py"
set RC=%ERRORLEVEL%
if %RC% NEQ 0 (
  echo [R1181c] FAILED (rc=%RC%). Siehe debug_output.txt
  exit /b %RC%
)

echo [R1181c] OK. Launching GUI...
if exist "tools\Start_MainGui.bat" (
  call "tools\Start_MainGui.bat"
) else (
  "%PY%" %PYFLAGS% "main_gui.py"
)
exit /b 0
