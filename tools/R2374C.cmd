@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM ===========================================================================
REM [R2374C] Robust: save() -> _save_delegate() -> ini_writer
REM Root: D:\ShrimpDev
REM ===========================================================================

set "ROOT=%~dp0.."
set "ROOT=%ROOT:\tools\..=%"
pushd "%ROOT%" >nul

set "RID=R2374C"
echo ===========================================================================
echo [%RID%] Robust save delegation (delegate method)
echo Root: %CD%
echo ===========================================================================

py -3 "tools\%RID%.py"
set "RC=%ERRORLEVEL%"

echo.
echo [%RID%] Beendet mit Code %RC%
popd >nul
exit /b %RC%
