@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM ===========================================================================
REM [R2374H] FINAL: Replace ShrimpDevConfigManager.save() completely
REM Root: D:\ShrimpDev
REM ===========================================================================

set "ROOT=%~dp0.."
set "ROOT=%ROOT:\tools\..=%"
pushd "%ROOT%" >nul

set "RID=R2374H"
echo ===========================================================================
echo [%RID%] Final safe replacement of save()
echo Root: %CD%
echo ===========================================================================

py -3 "tools\%RID%.py"
set "RC=%ERRORLEVEL%"

echo.
echo [%RID%] Beendet mit Code %RC%
popd >nul
exit /b %RC%
