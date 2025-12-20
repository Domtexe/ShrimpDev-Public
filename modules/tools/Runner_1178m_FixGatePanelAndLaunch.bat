@echo off
setlocal EnableExtensions EnableDelayedExpansion

rem --- Wurzelverzeichnis sauber setzen ---
cd /d "%~dp0.."
set "ROOT=%CD%"
set "LOG=%ROOT%\debug_output.txt"

rem --- Python-Aufruf korrekt trennen (kein zusammengequoteter Befehl!) ---
set "PY=py"
set "PYFLAGS=-3 -u"

echo [R1178m] Starting FixGatePanelAndLaunch.bat
echo [R1178m] Backing up module_gate_panel.py...

if exist "%ROOT%\modules\module_gate_panel.py" (
  if not exist "%ROOT%\_Archiv" mkdir "%ROOT%\_Archiv"
  for /f "tokens=1-3 delims=.:/ " %%a in ("%date% %time%") do set "STAMP=%%c%%b%%a_%%d%%e%%f"
  copy /Y "%ROOT%\modules\module_gate_panel.py" "%ROOT%\_Archiv\modules_module_gate_panel.py.%STAMP%.bak" >nul 2>&1
)

echo [R1178m] Applying GatePanel fix...
"%PY%" %PYFLAGS% "%ROOT%\tools\Runner_1178m_FixGatePanelAndLaunch.py"
if errorlevel 1 (
  echo [R1178m] FAILED. See "%LOG%"
  exit /b 1
)

echo [R1178m] OK. Launching Main GUI...
if exist "%ROOT%\tools\Start_MainGui.bat" (
  call "%ROOT%\tools\Start_MainGui.bat"
) else (
  "%PY%" %PYFLAGS% "%ROOT%\main_gui.py"
)
exit /b 0
