@echo off
setlocal
cd /d "%~dp0\.."
echo [1174f] MainGuiIntakeCleanup: starte Patch...
REM Automatisch passender Python-Interpreter
for %%P in (python.exe py.exe) do (
    where %%P >nul 2>nul && set "PYTHON=%%P" && goto :found
)
echo [1174f] FEHLER: Kein Python-Interpreter gefunden!
exit /b 2
:found
"%PYTHON%" -u "tools\Runner_1174f_MainGuiIntakeCleanup.py"
set rc=%ERRORLEVEL%
if %rc% NEQ 0 (
  echo [1174f] FEHLER (%rc%). Siehe debug_output.txt
) else (
  echo [1174f] Patch erfolgreich, Syntax OK.
)
endlocal
exit /b %rc%
