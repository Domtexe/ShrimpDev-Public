@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM ===========================================================================
REM [R2379] INI SingleWriter Enforcement (delegate all writes to ini_writer)
REM Root: D:\ShrimpDev
REM ===========================================================================

set "ROOT=%~dp0.."
pushd "%ROOT%" >nul

echo ===========================================================================
echo [R2379] INI SingleWriter Enforcement (delegate all writes to ini_writer)
echo Root: %CD%
echo ===========================================================================

py -3 "tools\R2379.py"
set "RC=%ERRORLEVEL%"

echo.
echo [R2379] Beendet mit Code %RC%
echo.
popd >nul
exit /b %RC%
