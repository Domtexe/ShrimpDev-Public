@echo off
setlocal ENABLEDELAYEDEXPANSION
title [1175n] FixPyCallAndCleanMain

set ROOT=D:\ShrimpDev
set TOOLS=%ROOT%\tools
set MODS=%ROOT%\modules
set ARCH=%ROOT%\_Archiv

rem WICHTIG: KEINE GESAMT-QUOTES UM BEFEHL+ARGUMENTE!
rem Wir halten den Python-Aufruf minimal und hängen Argumente separat an:
set PY=py -3

echo [1175n] Backups anlegen...
for /f "tokens=1-4 delims=/:. " %%a in ("%date% %time%") do set TS=%%d%%c%%b%%a_%%e%%f%%g
if not exist "%ARCH%" mkdir "%ARCH%"
copy "%ROOT%\main_gui.py" "%ARCH%\main_gui.py.%TS%.bak" >nul

echo [1175n] Starte Python-Patcher...
%PY% -u "%TOOLS%\Runner_1175n_FixPyCallAndCleanMain.py"
set RC=%ERRORLEVEL%
if %RC% NEQ 0 (
  echo [1175n] FEHLER RC=%RC%. Siehe debug_output.txt
  goto :eof
)

echo [1175n] Syntax-Smoketest...
%PY% - <<PYCODE
import py_compile
py_compile.compile(r"D:\ShrimpDev\main_gui.py", doraise=True)
print("[1175n] Smoke OK (main_gui.py).")
PYCODE

echo [1175n] FERTIG.
exit /b 0
