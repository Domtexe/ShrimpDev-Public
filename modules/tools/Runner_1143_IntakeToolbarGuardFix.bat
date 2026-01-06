@echo off
setlocal ENABLEDELAYEDEXPANSION
echo [R1143] IntakeToolbarGuardFix

pushd "D:\ShrimpDev\tools" 1>nul 2>nul || (
  echo [R1143] CD-Fehler
  exit /b 2
)

rem Python-Launcher bevorzugen
set "PYCMD="
where py 1>nul 2>nul && set "PYCMD=py -3 -X utf8 -u"
if not defined PYCMD (where python 1>nul 2>nul && set "PYCMD=python -X utf8 -u")
if not defined PYCMD (
  echo [R1143] FEHLER: Weder 'py' noch 'python' im PATH.
  popd & exit /b 9009
)

echo [R1143] PY: %PYCMD%
%PYCMD% "Runner_1143_IntakeToolbarGuardFix.py"
set "RC=%ERRORLEVEL%"

popd
echo [R1143] Ende (RC=%RC%)
exit /b %RC%
