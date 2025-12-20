@echo off
setlocal
set ROOT=D:\ShrimpDev
set TOOLS=%ROOT%\tools

echo [1174c] MainGuiIntakeHelpersFix: starte Patch...
if not exist "%TOOLS%" (
  echo [1174c] FEHLER: Tools-Verzeichnis nicht gefunden: %TOOLS%
  exit /b 2
)

python -3 -u "%TOOLS%\Runner_1174c_MainGuiIntakeHelpersFix.py"
set ERR=%ERRORLEVEL%
if %ERR% NEQ 0 (
  echo [1174c] Fehlercode %ERR%.
  exit /b %ERR%
) else (
  echo [1174c] Patch OK.
)
exit /b 0
