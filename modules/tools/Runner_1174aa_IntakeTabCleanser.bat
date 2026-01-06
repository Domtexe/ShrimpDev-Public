@echo off
setlocal ENABLEEXTENSIONS
title [1174aa] IntakeTabCleanser

set ROOT=D:\ShrimpDev
set MAIN=%ROOT%\main_gui.py
set ARCH=%ROOT%\_Archiv
set PY=py -3 -u

if not exist "%ARCH%" mkdir "%ARCH%"
for /f "tokens=1-3 delims=/:. " %%a in ("%date% %time%") do set TS=%%c%%b%%a_%%d%%e%%f
copy /y "%MAIN%" "%ARCH%\main_gui.py.%TS%.bak" >nul
echo [1174aa] Backup erstellt.

%PY% "%~dp0Runner_1174aa_IntakeTabCleanser.py" || (
  echo [1174aa] FEHLER im Python-Runner. Stelle Backup wieder her...
  copy /y "%ARCH%\main_gui.py.%TS%.bak" "%MAIN%" >nul
  exit /b 1
)

py -3 - <<PY
import py_compile; py_compile.compile(r"%MAIN%", doraise=True)
print("Syntax OK")
PY
if errorlevel 1 (
  echo [1174aa] Syntaxfehler -> Rollback
  copy /y "%ARCH%\main_gui.py.%TS%.bak" "%MAIN%" >nul
  exit /b 2
)

echo [1174aa] Erfolgreich. Teste jetzt mit:
echo py -3 main_gui.py
exit /b 0
