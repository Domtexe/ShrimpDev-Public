@echo off
setlocal EnableExtensions DisableDelayedExpansion
title ShrimpDev - Runner_1040_Intake_FullReset (PATCH+RUN)

pushd "%~dp0"
cd ..
echo [CWD] %CD%

set "PYEXE="
where py >nul 2>nul && set "PYEXE=py -3"
if not defined PYEXE ( where python >nul 2>nul && set "PYEXE=python" )
if not defined PYEXE ( echo [ERR] Kein Python gefunden & pause & exit /b 1 )

echo [RUN ] %PYEXE% tools\Runner_1040_Intake_FullReset.py
%PYEXE% tools\Runner_1040_Intake_FullReset.py || (echo [ERR] Patch fehlgeschlagen & pause & exit /b 1)

echo [RUN ] %PYEXE% main_gui.py
%PYEXE% main_gui.py
set RC=%ERRORLEVEL%
echo [END ] RC=%RC%
pause
exit /b %RC%
