@echo off
setlocal EnableExtensions EnableDelayedExpansion

set "ROOT=%~dp0.."
set "PY=%ROOT%\tools\R2807.py"

echo.
echo ======================================================================
echo [R2807] FINAL STRUCTURAL FIX: Purge popup single-source + real TXT output
echo Root: "%ROOT%"
echo ======================================================================
echo.

if not exist "%PY%" (
  echo [R2807] ERROR: Missing "%PY%"
  exit /b 11
)

python "%PY%" "%ROOT%"
set "RC=%ERRORLEVEL%"

echo.
if not "%RC%"=="0" (
  echo [R2807] FAIL (code %RC%)
) else (
  echo [R2807] OK
)
echo.
exit /b %RC%
