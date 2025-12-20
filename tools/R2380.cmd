@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM ===========================================================================
REM [R2380] Fix R2379 fallout (restore+safe patch) - INI SingleWriter delegation
REM Root: D:\ShrimpDev
REM ===========================================================================

set "ROOT=%~dp0.."
pushd "%ROOT%" >nul

echo ===========================================================================
echo [R2380] Fix R2379 fallout (restore+safe patch) - INI SingleWriter delegation
echo Root: %CD%
echo ===========================================================================

py -3 "tools\R2380.py"
set "RC=%ERRORLEVEL%"

echo.
echo [R2380] Beendet mit Code %RC%
echo.
popd >nul
exit /b %RC%
