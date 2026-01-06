@echo off
setlocal ENABLEDELAYEDEXPANSION
pushd %~dp0
cd ..
echo [1171m] IntakeToolbarReflowFix: starte sicheren Patch...
py -3 tools\Runner_1171m_IntakeToolbarReflowFix.py
set _rc=%ERRORLEVEL%
if not "%_rc%"=="0" (
  echo [1171m] FEHLER (%_rc%). Abbruch.
  exit /b %_rc%
)
echo [1171m] OK. Syntax-Check bestanden.
popd
exit /b 0
