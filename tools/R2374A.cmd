@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM ===========================================================================
REM [R2374A] Diagnose: Write-Pfade in config_manager (READ-ONLY)
REM Root: D:\ShrimpDev
REM ===========================================================================

set "ROOT=%~dp0.."
set "ROOT=%ROOT:\tools\..=%"
pushd "%ROOT%" >nul

set "RID=R2374A"
echo ===========================================================================
echo [%RID%] Diagnose: Write-Pfade in config_manager (READ-ONLY)
echo Root: %CD%
echo ===========================================================================

py -3 "tools\%RID%.py"
set "RC=%ERRORLEVEL%"

echo.
echo [%RID%] Beendet mit Code %RC%
popd >nul
exit /b %RC%
