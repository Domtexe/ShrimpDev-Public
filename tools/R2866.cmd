@echo off
setlocal enabledelayedexpansion

REM ==============================================================
REM [R2866] PATCH (SAFE): Fix NameError frame_toolbar_right in ui_toolbar.build_toolbar_right
REM Root: repo root (parent of tools)
REM ==============================================================

set "ROOT=%~dp0.."
for %%I in ("%ROOT%") do set "ROOT=%%~fI"

python "%ROOT%\tools\R2866.py" "%ROOT%"
set "EC=%ERRORLEVEL%"

echo.
echo [Runner beendet mit Code %EC%]
exit /b %EC%
