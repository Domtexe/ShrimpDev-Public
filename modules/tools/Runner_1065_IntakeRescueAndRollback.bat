@echo off
setlocal EnableExtensions DisableDelayedExpansion
title ShrimpDev - Runner_1065_IntakeRescueAndRollback

pushd "%~dp0"
cd ..
echo [CWD] %CD%

set "PYEXE="
where py >nul 2>nul && set "PYEXE=py -3"
if not defined PYEXE ( where python >nul 2>nul && set "PYEXE=python" )
if not defined PYEXE ( echo [ERR] Python nicht gefunden & pause & exit /b 1 )

echo [RUN ] %PYEXE% tools\Runner_1065_IntakeRescueAndRollback.py
%PYEXE% tools\Runner_1065_IntakeRescueAndRollback.py || (echo [ERR] Rescue fehlgeschlagen & pause & exit /b 1)

echo [RUN ] %PYEXE% main_gui.py
%PYEXE% main_gui.py
set RC=%ERRORLEVEL%
echo [END ] RC=%RC%
pause
exit /b %RC%
