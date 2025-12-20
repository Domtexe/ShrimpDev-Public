@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM ===========================================================================
REM [R2377B] Minimal Restore Fix (.geometry + flags + main)
REM Root: D:\ShrimpDev
REM ===========================================================================

set "ROOT=%~dp0.."
set "ROOT=%ROOT:\tools\..=%"
pushd "%ROOT%" >nul

set "RID=R2377B"
echo ===========================================================================
echo [%RID%] Minimal Restore Fix
echo Root: %CD%
echo ===========================================================================

py -3 "tools\%RID%.py"
set "RC=%ERRORLEVEL%"

echo.
echo [%RID%] Beendet mit Code %RC%
popd >nul
exit /b %RC%
