@echo off
setlocal ENABLEDELAYEDEXPANSION
title [1174g] IntakePostBuildFix

set ROOT=D:\ShrimpDev
set MOD=%ROOT%\modules\module_code_intake.py
set ARCH=%ROOT%\_Archiv
set PY=%ROOT%\tools\Runner_1174g_IntakePostBuildFix.py

echo [1174g] IntakePostBuildFix: starte Patch...

if not exist "%ARCH%" mkdir "%ARCH%"
for /f "tokens=1-3 delims=.:/ " %%a in ("%date% %time%") do set TS=%%c%%b%%a_%%d%%e%%f
set BAK=%ARCH%\module_code_intake.py.%TS%.bak
copy /Y "%MOD%" "%BAK%" >nul
echo [1174g] Backup erstellt: %BAK%

py -3 -u "%PY%"
if errorlevel 1 (
    echo [1174g] Fehler -> Rollback...
    copy /Y "%BAK%" "%MOD%" >nul
    echo [1174g] Rollback OK.
    exit /b 1
)

rem Syntaxcheck
py -3 - <<PYCODE
import py_compile, sys
py_compile.compile(r"%MOD%", doraise=True)
print("[1174g] Syntax OK")
PYCODE
if errorlevel 1 (
    echo [1174g] Syntax-Check FEHLER -> Rollback...
    copy /Y "%BAK%" "%MOD%" >nul
    echo [1174g] Rollback OK.
    exit /b 1
)

echo [1174g] Patch uebernommen, Syntax OK.
exit /b 0
