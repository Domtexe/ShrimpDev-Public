@echo off
setlocal ENABLEDELAYEDEXPANSION
echo [R1143b] IntakeToolbarGuardFix_Safe
pushd "%~dp0" || (echo CD-Fehler & exit /b 2)

set "PYCMD="
where py >nul 2>nul && set "PYCMD=py -3 -X utf8 -u"
if not defined PYCMD (where python >nul 2>nul && set "PYCMD=python -X utf8 -u")
if not defined PYCMD (echo Kein Python gefunden & popd & exit /b 9009)

%PYCMD% "Runner_1143b_IntakeToolbarGuardFix_Safe.py"
set "RC=%ERRORLEVEL%"
popd
echo [R1143b] Ende (RC=%RC%)
exit /b %RC%
