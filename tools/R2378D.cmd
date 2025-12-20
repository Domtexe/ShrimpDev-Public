@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM ===========================================================================
REM [R2378D] READ-ONLY INI + Docking Diagnose (no writes)
REM Root: D:\ShrimpDev
REM ===========================================================================

set "ROOT=%~dp0.."
pushd "%ROOT%" >nul

echo ===========================================================================
echo [R2378D] READ-ONLY INI + Docking Diagnose (no writes)
echo Root: %CD%
echo ===========================================================================

py -3 "tools\R2378D.py"
set "RC=%ERRORLEVEL%"

echo.
echo [R2378D] Beendet mit Code %RC%
echo.
popd >nul
exit /b %RC%
