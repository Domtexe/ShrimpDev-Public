@echo off
setlocal EnableExtensions EnableDelayedExpansion
title ShrimpDev - Runner_1117 (Deep Sanity Framework)

rem --- Wurzel bestimmen ---
pushd "%~dp0"
cd ..
set "ROOT=%CD%"
echo [CWD] %ROOT%

rem --- Python Resolver: bevorzugt py -3 ---
set "PYEXE=py -3"
for /f "delims=" %%P in ('where py 2^>nul') do (set "PYFOUND=1")
if not defined PYFOUND (
  for /f "delims=" %%P in ('where python 2^>nul') do (set "PYEXE=python")
)

rem --- Reports-Ordner sicherstellen ---
if not exist "%ROOT%\_Reports" mkdir "%ROOT%\_Reports"

rem --- Runner starten ---
echo [RUN ] %PYEXE% -u tools\Runner_1117.py
%PYEXE% -u tools\Runner_1117.py
set "RC=%ERRORLEVEL%"

echo [END ] Runner_1117 RC=%RC%
echo.
echo Bericht: _Reports\Runner_1117_sanity_findings.txt
echo Syntax : _Reports\Runner_1117_syntax_report.txt
echo GUI Out: _Reports\Runner_1117_main_gui_capture.txt
echo Log    : debug_output.txt (Abschnitt [R1117])
echo.
pause
endlocal
