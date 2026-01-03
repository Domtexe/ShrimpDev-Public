@echo off
setlocal
title [1174z] DebugPathFix (robust)

set ROOT=D:\ShrimpDev
set MAIN=%ROOT%\main_gui.py
set ARCH=%ROOT%\_Archiv
set PY=py -3 -u

echo [1174z] DebugPathFix: starte Patch...
if not exist "%MAIN%" (
  echo [1174z] FEHLER: %MAIN% nicht gefunden.
  exit /b 2
)

for /f "tokens=1-3 delims=/:. " %%a in ("%date% %time%") do set TS=%%c%%b%%a_%%d%%e%%f
set TS=%TS: =0%
copy /y "%MAIN%" "%ARCH%\main_gui.py.%TS%.bak" >nul

%PY% "%~dp0Runner_1174z_DebugPathFix.py" --file "%MAIN%"
if errorlevel 1 (
  echo [1174z] FEHLER. Siehe Konsole.
  exit /b 10
)

echo [1174z] Smoke-Test...
%PY% "%ROOT%\main_gui.py"
echo [1174z] Ende.
endlocal
