@echo off
setlocal
cd /d "%~dp0\.."
echo [1174g] MainGuiReorderFix: starte Patch...
for %%P in (python.exe py.exe) do (
    where %%P >nul 2>nul && set "PYTHON=%%P" && goto :found
)
echo [1174g] FEHLER: Kein Python-Interpreter gefunden!
exit /b 2
:found
"%PYTHON%" -u "tools\Runner_1174g_MainGuiReorderFix.py"
set rc=%ERRORLEVEL%
if %rc% NEQ 0 (
  echo [1174g] FEHLER (%rc%). Siehe debug_output.txt
) else (
  echo [1174g] Patch erfolgreich, Syntax OK.
)
endlocal
exit /b %rc%
