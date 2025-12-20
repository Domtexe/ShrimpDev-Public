@echo off
setlocal EnableExtensions EnableDelayedExpansion
title [1174k] IntakeFeatureRestore

rem Verlässlicher Startpunkt
pushd "%~dp0"
cd ..
set "ROOT=%CD%"
set "PY=py -3 -u"

if not exist "%ROOT%\_Archiv" mkdir "%ROOT%\_Archiv"

echo [1174k] IntakeFeatureRestore: starte Patch...
echo [1174k] Root   : %ROOT%
echo.

rem Starte Python-Runner (gleicher Basisname .py)
%PY% "tools\Runner_1174k_IntakeFeatureRestore.py"
set RC=%ERRORLEVEL%
if not "%RC%"=="0" (
  echo [1174k] FEHLER: Python-Runner RC=%RC%.
  echo "." kann syntaktisch an dieser Stelle nicht verarbeitet werden.
  exit /b %RC%
)

echo [1174k] OK. Ende.
endlocal
