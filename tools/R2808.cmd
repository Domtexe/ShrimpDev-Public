@echo off
setlocal EnableExtensions EnableDelayedExpansion

set "ROOT=%~dp0.."
set "PY=%ROOT%\tools\R2808.py"

echo.
echo ======================================================================
echo [R2808] HOTFIX: Restore ui_toolbar.py from R2807 backup + safe popup neutralization
echo Root: "%ROOT%"
echo ======================================================================
echo.

if not exist "%PY%" (
  echo [R2808] ERROR: Missing "%PY%"
  exit /b 11
)

python "%PY%" "%ROOT%"
set "RC=%ERRORLEVEL%"

echo.
if not "%RC%"=="0" (
  echo [R2808] FAIL (code %RC%)
) else (
  echo [R2808] OK
)
echo.
exit /b %RC%
