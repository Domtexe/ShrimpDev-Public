@echo off
setlocal
set "ROOT=%~dp0.."
set "PY=python"

echo ======================================================================
echo [R2872] PATCH (SAFE): Fix ui_toolbar runtime NameErrors (frame_toolbar_right / busy / name in trace)
echo Root: "%ROOT%"
echo ======================================================================

"%PY%" "%~dp0R2872.py" "%ROOT%"
set "EC=%ERRORLEVEL%"

echo.
echo [R2872] Exit Code: %EC%
echo.
exit /b %EC%
