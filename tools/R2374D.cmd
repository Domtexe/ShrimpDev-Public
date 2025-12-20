@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM ===========================================================================
REM [R2374D] READ-ONLY Diagnose: reale Write-Entry-Points in config_manager.py
REM Root: D:\ShrimpDev
REM ===========================================================================

set "ROOT=%~dp0.."
set "ROOT=%ROOT:\tools\..=%"
pushd "%ROOT%" >nul

set "RID=R2374D"
echo ===========================================================================
echo [%RID%] Diagnose: config_manager Write-Entry-Points (READ-ONLY)
echo Root: %CD%
echo ===========================================================================

py -3 "tools\%RID%.py"
set "RC=%ERRORLEVEL%"

echo.
echo [%RID%] Beendet mit Code %RC%
popd >nul
exit /b %RC%
