@echo off
setlocal EnableExtensions EnableDelayedExpansion

cd /d "%~dp0.."
set "ROOT=%CD%"
set "LOG=%ROOT%\debug_output.txt"
set "PY=py"
set "PYFLAGS=-3 -u"

echo [R1178i] Applying ImportPathFix (main_gui.py)...
if not exist "%ROOT%\_Archiv" mkdir "%ROOT%\_Archiv"
for /f "tokens=1-3 delims=.:/ " %%a in ("%date% %time%") do set "STAMP=%%c%%b%%a_%%d%%e%%f"
copy /Y "%ROOT%\main_gui.py" "%ROOT%\_Archiv\main_gui.py.%STAMP%.bak" >nul 2>&1

"%PY%" %PYFLAGS% "%ROOT%\tools\Runner_1178i_ImportPathFix.py"
if errorlevel 1 (
  echo [R1178i] FAILED. See "%LOG%"
  exit /b 1
)

echo [R1178i] OK. Launching Main GUI...
if exist "%ROOT%\tools\Start_MainGui.bat" (
  call "%ROOT%\tools\Start_MainGui.bat"
) else (
  "%PY%" %PYFLAGS% "%ROOT%\main_gui.py"
)
exit /b 0
