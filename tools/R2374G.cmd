@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM ===========================================================================
REM [R2374G] AST-safe save replacement (final)
REM Root: D:\ShrimpDev
REM ===========================================================================

set "ROOT=%~dp0.."
set "ROOT=%ROOT:\tools\..=%"
pushd "%ROOT%" >nul

set "RID=R2374G"
echo ===========================================================================
echo [%RID%] AST-safe save() replacement
echo Root: %CD%
echo ===========================================================================

py -3 "tools\%RID%.py"
set "RC=%ERRORLEVEL%"

echo.
echo [%RID%] Beendet mit Code %RC%
popd >nul
exit /b %RC%
