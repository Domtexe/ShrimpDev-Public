@echo off
setlocal ENABLEDELAYEDEXECUTION
title [1174p] IntakeCtorFix

rem --- Pfade / Settings ---
set "ROOT=D:\ShrimpDev"
set "MOD=%ROOT%\modules\module_code_intake.py"
set "ARCH=%ROOT%\_Archiv"
set "PY=py -3"

if not exist "%ARCH%" mkdir "%ARCH%"

echo [1174p] IntakeCtorFix: starte Patch...

for /f "tokens=1-6 delims=/:. " %%a in ("%date% %time%") do (
    set "TS=%%c%%b%%a_%%d%%e%%f"
)
set "BAK=%ARCH%\module_code_intake.py.%TS%.bak"

copy /y "%MOD%" "%BAK%" >nul
if errorlevel 1 (
  echo [1174p] FEHLER: Backup fehlgeschlagen.
  exit /b 2
)

rem --- Python-Patcher ausfuehren ---
%PY% -u "%ROOT%\tools\Runner_1174p_IntakeCtorFix.py" --mod "%MOD%" --bak "%BAK%" --root "%ROOT%"
set "RC=%ERRORLEVEL%"
if not "%RC%"=="0" (
  echo [1174p] Python-Runner RC=%RC%. Stelle aus Backup wieder her...
  copy /y "%BAK%" "%MOD%" >nul
  exit /b %RC%
)

rem --- Syntax-Check ohne Here-Doc: temporäre Datei ---
set "TMPPY=%ROOT%\tools\_tmp_1174p_syntax.py"
> "%TMPPY%" echo import py_compile, sys
>>"%TMPPY%" echo try:
>>"%TMPPY%" echo ^    py_compile.compile(r"%MOD%", doraise=True)
>>"%TMPPY%" echo ^    sys.exit(0)
>>"%TMPPY%" echo except Exception as e:
>>"%TMPPY%" echo ^    print("Syntax-Check FEHLER:", e)
>>"%TMPPY%" echo ^    sys.exit(1)

%PY% -u "%TMPPY%"
set "RC=%ERRORLEVEL%"
del "%TMPPY%" >nul 2>&1

if not "%RC%"=="0" (
  echo [1174p] Rollback: Syntax-Check fehlgeschlagen.
  copy /y "%BAK%" "%MOD%" >nul
  exit /b 3
)

echo [1174p] Patch uebernommen, Syntax OK.
exit /b 0
