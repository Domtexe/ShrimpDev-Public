@echo off
setlocal
cd /d "%~dp0\.."
echo [1174e] MainGuiIntakeCleanup: starte Patch...
python -3 -u tools\Runner_1174e_MainGuiIntakeCleanup.py
set rc=%ERRORLEVEL%
if %rc% NEQ 0 (
  echo [1174e] FEHLER (%rc%). Siehe debug_output.txt
) else (
  echo [1174e] Patch erfolgreich, Syntax OK.
)
endlocal
exit /b %rc%
