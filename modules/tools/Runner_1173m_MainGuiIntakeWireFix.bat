@echo off
setlocal ENABLEDELAYEDEXPANSION
cd /d "%~dp0"
echo [1173m] MainGuiIntakeWireFix: starte Patch...
py -3 "%~dp0Runner_1173m_MainGuiIntakeWireFix.py"
set rc=%ERRORLEVEL%
if %rc% NEQ 0 (
  echo [1173m] FEHLER (%rc%).
) else (
  echo [1173m] Patch erfolgreich, Syntax OK.
)
endlocal
