@echo off
setlocal ENABLEDELAYEDEXPANSION
REM ===========================================
REM Runner_1167a_Intake_SanityCheck.bat
REM Startet den Sanity-Check für das Intake-Modul
REM ===========================================
pushd "%~dp0\.."
echo [1167a] Starte Intake Sanity-Check...
py -3 -u "tools\Runner_1167a_Intake_SanityCheck.py"
set rc=%ERRORLEVEL%
if %rc% NEQ 0 (
  echo [1167a] FEHLER (rc=%rc%). Siehe debug_output.txt
) else (
  echo [1167a] OK. Siehe debug_output.txt
)
popd
exit /B %rc%
