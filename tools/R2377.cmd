@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM ===========================================================================
REM [R2377] Docking Restore Fix: use .geometry + open/docked + main restore
REM Root: D:\ShrimpDev
REM ===========================================================================

set "ROOT=%~dp0.."
set "ROOT=%ROOT:\tools\..=%"
pushd "%ROOT%" >nul

set "RID=R2377"
echo ===========================================================================
echo [%RID%] Docking Restore Fix (.geometry + flags + main)
echo Root: %CD%
echo ===========================================================================

py -3 "tools\%RID%.py"
set "RC=%ERRORLEVEL%"

echo.
echo [%RID%] Beendet mit Code %RC%
popd >nul
exit /b %RC%
