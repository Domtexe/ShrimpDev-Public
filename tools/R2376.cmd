@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM ===========================================================================
REM [R2376] Docking Restore DIAG (READ-ONLY)
REM Root: D:\ShrimpDev
REM ===========================================================================

set "ROOT=%~dp0.."
set "ROOT=%ROOT:\tools\..=%"
pushd "%ROOT%" >nul

set "RID=R2376"
echo ===========================================================================
echo [%RID%] Docking Restore DIAG (READ-ONLY)
echo Root: %CD%
echo ===========================================================================

py -3 "tools\%RID%.py"
set "RC=%ERRORLEVEL%"

echo.
echo [%RID%] Beendet mit Code %RC%
popd >nul
exit /b %RC%
