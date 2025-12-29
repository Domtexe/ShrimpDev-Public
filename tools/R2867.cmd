@echo off
setlocal EnableExtensions EnableDelayedExpansion

set "ROOT=%~dp0.."
for %%I in ("%ROOT%") do set "ROOT=%%~fI"

echo ======================================================================
echo [R2867] READ-ONLY: Lint-Guard (f-string unknown identifiers)
echo Root: "%ROOT%"
echo ======================================================================

py -3 "%~dp0R2867.py" "%ROOT%"
set "EC=%ERRORLEVEL%"

echo.
echo [R2867] Runner beendet mit Code %EC%
exit /b %EC%
