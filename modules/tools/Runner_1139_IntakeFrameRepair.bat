@echo off
setlocal ENABLEDELAYEDEXPANSION
echo [R1139] IntakeFrameRepair
pushd "%~dp0\.." || (echo [R1139] CD-Fehler & exit /b 2)

set "PYCMD="
where py >nul 2>nul && set "PYCMD=py -3 -X utf8 -u"
if not defined PYCMD (where python >nul 2>nul && set "PYCMD=python -X utf8 -u")
if not defined PYCMD (
  echo [R1139] Fehler: Kein Python gefunden.
  popd & exit /b 9009
)

%PYCMD% "tools\Runner_1139_IntakeFrameRepair.py"
set "RC=%ERRORLEVEL%"
popd
echo [R1139] Ende (RC=%RC%)
exit /b %RC%
