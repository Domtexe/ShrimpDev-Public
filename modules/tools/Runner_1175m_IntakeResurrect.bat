@echo off
setlocal ENABLEDELAYEDEXPANSION
title [1175m] IntakeResurrect

set ROOT=D:\ShrimpDev
set TOOLS=%ROOT%\tools
set MODS=%ROOT%\modules
set ARCH=%ROOT%\_Archiv
set PY=py -3 -u

echo [1175m] IntakeResurrect: starte Patch...
if not exist "%ARCH%" mkdir "%ARCH%"

rem --- Backup anlegen ---
for /f "tokens=1-4 delims=/:. " %%a in ("%date% %time%") do set TS=%%d%%c%%b%%a_%%e%%f%%g
copy "%ROOT%\main_gui.py" "%ARCH%\main_gui.py.%TS%.bak" >nul
copy "%MODS%\module_code_intake.py" "%ARCH%\module_code_intake.py.%TS%.bak" >nul 2>nul

rem --- Python-Runner ausführen ---
"%PY%" "%TOOLS%\Runner_1175m_IntakeResurrect.py"
set RC=%ERRORLEVEL%
if %RC% NEQ 0 (
  echo [1175m] FEHLER RC=%RC%. Siehe Konsole / debug_output.txt
  goto :eof
)

rem --- Smoke-Check nur Main (startet nicht, nur compile) ---
"%PY%" - <<PYCODE
import py_compile, sys
py_compile.compile(r"D:\ShrimpDev\main_gui.py", doraise=True)
py_compile.compile(r"D:\ShrimpDev\modules\module_code_intake.py", doraise=True)
print("[1175m] Smoke OK.")
PYCODE

set RC=%ERRORLEVEL%
if %RC% NEQ 0 (
  echo [1175m] Smoke FEHLER RC=%RC%.
  goto :eof
)

echo [1175m] Patch erfolgreich, Syntax OK.
echo [1175m] Ende.
exit /b 0
