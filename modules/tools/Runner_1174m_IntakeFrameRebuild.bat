@echo off
setlocal ENABLEDELAYEDEXPANSION
REM [1174m] IntakeFrameRebuild: starte Patch...

pushd %~dp0
cd ..

REM Python sauber mit Version-Flag starten (Windows Launcher)
py -3 -u "tools\Runner_1174m_IntakeFrameRebuild.py"
set RC=%ERRORLEVEL%

if %RC% NEQ 0 (
  echo [1174m] FEHLER: Python-Runner RC=%RC%.
) else (
  echo [1174m] OK. Ende.
)

popd
exit /b %RC%
