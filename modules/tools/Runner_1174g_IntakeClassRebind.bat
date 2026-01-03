@echo off
setlocal enabledelayedexpansion
set ROOT=D:\ShrimpDev
set MOD=%ROOT%\modules\module_code_intake.py
set ARCH=%ROOT%\_Archiv
for /f "tokens=1-3 delims=/ " %%a in ('date /t') do set D=%%c%%b%%a
for /f "tokens=1 delims=:" %%a in ("%time%") do set H=%%a
set TS=%D%_%H%%time:~3,2%%time:~6,2%
if not exist "%ARCH%" mkdir "%ARCH%"

echo [1174g] IntakeClassRebind: starte Patch...
copy /y "%MOD%" "%ARCH%\module_code_intake.py.%TS%.bak" >nul
if errorlevel 1 (
  echo [1174g] Konnte Backup nicht schreiben. Abbruch.
  exit /b 1
)

py -3 -u "%ROOT%\tools\Runner_1174g_IntakeClassRebind.py"
set RC=%ERRORLEVEL%
if %RC% NEQ 0 (
  echo [1174g] FEHLER (%RC%). Siehe debug_output.txt
  exit /b %RC%
)
echo [1174g] Patch erfolgreich, Syntax OK.
exit /b 0
