@echo off
setlocal EnableExtensions EnableDelayedExpansion

set "ROOT=%~dp0.."
set "PY=%ROOT%\tools\R2814.py"

echo.
echo ======================================================================
echo [R2814] HOTFIX: Restore logic_tools.py + safe patch purge functions (compile-gated)
echo Root: "%ROOT%"
echo ======================================================================
echo.

if not exist "%PY%" (
  echo [R2814] ERROR: Missing "%PY%"
  exit /b 11
)

python "%PY%" "%ROOT%"
set "RC=%ERRORLEVEL%"

echo.
if not "%RC%"=="0" (
  echo [R2814] FAIL (code %RC%)
) else (
  echo [R2814] OK
)
echo.
exit /b %RC%
