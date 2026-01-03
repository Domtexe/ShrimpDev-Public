@echo off
setlocal
cd /d "%~dp0\.."
echo [1174d] MainGuiIntakeCleanup: starte Patch...
python tools\Runner_1174d_MainGuiIntakeCleanup.py
set rc=%ERRORLEVEL%
if %rc% NEQ 0 (
  echo [1174d] FEHLER (%rc%). Siehe debug_output.txt
) else (
  echo [1174d] Patch erfolgreich, Syntax OK.
)
endlocal
exit /b %rc%
