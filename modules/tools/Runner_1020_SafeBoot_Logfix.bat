@echo off
setlocal EnableExtensions DisableDelayedExpansion
title ShrimpDev - Runner_1020_SafeBoot_Logfix

pushd "%~dp0"
cd ..
echo [CWD] %CD%
where py >nul 2>nul && set "PYEXE=py -3"
if not defined PYEXE (where python >nul 2>nul && set "PYEXE=python")
if not defined PYEXE (echo [ERR] Kein Python gefunden & pause & exit /b 1)

echo [RUN ] %PYEXE% tools\Runner_1020_SafeBoot_Logfix.py
%PYEXE% tools\Runner_1020_SafeBoot_Logfix.py
if errorlevel 1 (echo [ERR] Patch fehlgeschlagen & pause & exit /b 1)

echo [RUN ] %PYEXE% main_gui.py
%PYEXE% main_gui.py
set RC=%ERRORLEVEL%
echo [END ] RC=%RC%
pause
exit /b %RC%
