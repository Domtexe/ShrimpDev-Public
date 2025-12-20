@echo off
setlocal ENABLEDELAYEDEXPANSION
cd /d "%~dp0"
echo [1173p] MainGuiIntakeWireForce: starte Patch...
py -3 "%~dp0Runner_1173p_MainGuiIntakeWireForce.py"
set rc=%ERRORLEVEL%
if %rc% NEQ 0 (
  echo [1173p] FEHLER (%rc%). Siehe debug_output.txt
) else (
  echo [1173p] Patch erfolgreich, Syntax OK.
)
endlocal
