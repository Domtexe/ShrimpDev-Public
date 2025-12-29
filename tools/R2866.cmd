@echo off
setlocal EnableExtensions EnableDelayedExpansion

rem Root = parent of tools\
set "ROOT=%~dp0.."
for %%I in ("%ROOT%") do set "ROOT=%%~fI"

echo ======================================================================
echo [R2866] PATCH: MasterRules - Debug-Logging darf keine neuen Variablen einfuehren
echo Root: "%ROOT%"
echo ======================================================================

py -3 "%~dp0R2866.py" "%ROOT%"
set "EC=%ERRORLEVEL%"

echo.
echo [R2866] Runner beendet mit Code %EC%
exit /b %EC%
