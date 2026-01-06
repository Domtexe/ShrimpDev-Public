@echo off
setlocal enabledelayedexpansion
title [1174n] IntakeHotFix_UIInit

REM === Pfade ===
set ROOT=D:\ShrimpDev
set MOD=%ROOT%\modules\module_code_intake.py
set PY=%ROOT%\tools\Runner_1174n_IntakeHotFix_UIInit.py

echo [1174n] IntakeHotFix_UIInit: starte Patch...
if not exist "%MOD%" (
  echo [1174n] FEHLER: %MOD% nicht gefunden.
  exit /b 2
)

REM Backup
for /f "tokens=1-3 delims=/:. " %%a in ("%date% %time%") do set TS=%%c%%b%%a_%%d%%e%%f
set BAK=%ROOT%\_Archiv\module_code_intake.py.%TS%.bak
if not exist "%ROOT%\_Archiv" mkdir "%ROOT%\_Archiv"
copy /y "%MOD%" "%BAK%" >nul
echo [1174n] Backup erstellt: %BAK%

REM Patch
py -3 -u "%PY%"
if errorlevel 1 (
  echo [1174n] Python-Runner meldet Fehler – Rollback...
  copy /y "%BAK%" "%MOD%" >nul
  echo [1174n] Rollback OK.
  exit /b 10
)

REM Syntax-Check
py -3 - <<PYEND
import py_compile, sys
try:
    py_compile.compile(r"%MOD%", doraise=True)
    print("[1174n] Syntax OK.")
    sys.exit(0)
except Exception as e:
    print("[1174n] SyntaxCheck FEHLER:", e)
    sys.exit(1)
PYEND
if errorlevel 1 (
  echo [1174n] Syntax-Check fehlgeschlagen – Rollback...
  copy /y "%BAK%" "%MOD%" >nul
  echo [1174n] Rollback OK.
  exit /b 11
)

echo [1174n] Patch uebernommen, Syntax OK.
echo [1174n] Ende.
exit /b 0
