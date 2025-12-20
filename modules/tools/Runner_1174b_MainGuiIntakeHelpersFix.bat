@echo off
setlocal ENABLEDELAYEDEXPANSION
cd /d "%~dp0\.."
echo [1174b] MainGuiIntakeHelpersFix: starte Patch...
python tools\Runner_1174b_MainGuiIntakeHelpersFix.py
set rc=%ERRORLEVEL%
if %rc% NEQ 0 (
  echo [1174b] FEHLER (%rc%). Siehe debug_output.txt
) else (
  echo [1174b] Patch erfolgreich, Syntax OK.
)
echo [1174b] Ende.
endlocal
exit /b %rc%
