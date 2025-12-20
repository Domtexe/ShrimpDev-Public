@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM ===========================================================================
REM [R2375] PIPELINE + MasterRules: SingleWriter Phase 2 + Diagnose-first + Defactoring
REM Root: D:\ShrimpDev
REM ===========================================================================

set "ROOT=%~dp0.."
set "ROOT=%ROOT:\tools\..=%"
pushd "%ROOT%" >nul

set "RID=R2375"
echo ===========================================================================
echo [%RID%] Pipeline + MasterRules Update (INI SingleWriter Phase 2)
echo Root: %CD%
echo ===========================================================================

py -3 "tools\%RID%.py"
set "RC=%ERRORLEVEL%"

echo.
echo [%RID%] Beendet mit Code %RC%
popd >nul
exit /b %RC%
