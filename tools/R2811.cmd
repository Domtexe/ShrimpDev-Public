@echo off
setlocal EnableExtensions EnableDelayedExpansion

set "ROOT=%~dp0.."
set "PY=%ROOT%\tools\R2811.py"

echo.
echo ======================================================================
echo [R2811] FINAL FIX: Purge popup single-source + remove duplicate triggers + remove bridge content
echo Root: "%ROOT%"
echo ======================================================================
echo.

if not exist "%PY%" (
  echo [R2811] ERROR: Missing "%PY%"
  exit /b 11
)

python "%PY%" "%ROOT%"
set "RC=%ERRORLEVEL%"

echo.
if not "%RC%"=="0" (
  echo [R2811] FAIL (code %RC%)
) else (
  echo [R2811] OK
)
echo.
exit /b %RC%
