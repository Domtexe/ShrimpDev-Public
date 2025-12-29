@echo off
setlocal EnableExtensions EnableDelayedExpansion

set "ROOT=%~dp0.."
for %%I in ("%ROOT%") do set "ROOT=%%~fI"

echo ======================================================================
echo [R2868] PATCH: MasterRules + Pipeline (f-string safety + guard policy)
echo Root: "%ROOT%"
echo ======================================================================

py -3 "%~dp0R2868.py" "%ROOT%"
set "EC=%ERRORLEVEL%"

echo.
echo [R2868] Runner beendet mit Code %EC%
exit /b %EC%
