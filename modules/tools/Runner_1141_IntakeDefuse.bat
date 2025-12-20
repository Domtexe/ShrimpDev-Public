@echo off
setlocal ENABLEDELAYEDEXPANSION
echo [R1141] IntakeDefuse
set "PYCMD="
where py  >nul 2>nul && set "PYCMD=py -3 -X utf8 -u"
if not defined PYCMD (where python >nul 2>nul && set "PYCMD=python -X utf8 -u")
if not defined PYCMD (
  echo [R1141] Fehler: Weder 'py' noch 'python' im PATH.
  exit /b 9009
)

pushd "%~dp0\.."
%PYCMD% "tools\Runner_1141_IntakeDefuse.py"
set "RC=%ERRORLEVEL%"
popd
echo [R1141] Ende (RC=%RC%)
exit /b %RC%
