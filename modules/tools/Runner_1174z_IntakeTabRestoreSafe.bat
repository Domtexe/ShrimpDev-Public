@echo off
setlocal ENABLEEXTENSIONS
REM [1174z] IntakeTabRestoreSafe: starte Patch...

pushd "%~dp0\.."
set ROOT=%CD%
set TARGET=%ROOT%\main_gui.py
set ARCH=%ROOT%\_Archiv

if not exist "%ARCH%" mkdir "%ARCH%"

for /f "tokens=1-3 delims=/:. " %%a in ("%date% %time%") do (
  set TS=%%c%%b%%a_%%d%%e%%f
)
set BAK=%ARCH%\main_gui.py.%TS%.bak

copy /y "%TARGET%" "%BAK%" >nul
echo [1174z] Backup erstellt: %BAK%

py -3 -u "%~dp0Runner_1174z_IntakeTabRestoreSafe.py" || (
  echo [1174z] FEHLER: Python-Runner. Stelle aus Backup wieder her...
  copy /y "%BAK%" "%TARGET%" >nul
  exit /b 1
)

REM Syntax-Check
py -3 - <<PY
import py_compile, sys
py_compile.compile(r"%TARGET%", doraise=True)
print("OK")
PY
if errorlevel 1 (
  echo [1174z] Syntax-Check FEHLER -> Rollback.
  copy /y "%BAK%" "%TARGET%" >nul
  exit /b 1
)

echo [1174z] Patch erfolgreich, Syntax OK.
popd
exit /b 0
