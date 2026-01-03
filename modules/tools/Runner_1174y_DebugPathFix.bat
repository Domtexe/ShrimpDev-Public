@echo off
setlocal
title [1174y] DebugPathFix

set ROOT=D:\ShrimpDev
set MAIN=%ROOT%\main_gui.py
set ARCH=%ROOT%\_Archiv
set PY=py -3 -u

echo [1174y] DebugPathFix: starte Patch...
if not exist "%MAIN%" (
  echo [1174y] FEHLER: %MAIN% nicht gefunden.
  exit /b 2
)

for /f "tokens=1-3 delims=/:. " %%a in ("%date% %time%") do set TS=%%c%%b%%a_%%d%%e%%f
copy /y "%MAIN%" "%ARCH%\main_gui.py.%TS%.bak" >nul

%PY% "%~dp0Runner_1174y_DebugPathFix.py" --file "%MAIN%"
if errorlevel 1 (
  echo [1174y] FEHLER. Siehe Konsole.
  exit /b 10
)

echo [1174y] Smoke (optional)...
%PY% "%ROOT%\main_gui.py"
echo [1174y] Ende.
endlocal
