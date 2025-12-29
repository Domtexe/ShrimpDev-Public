@echo off
setlocal EnableExtensions EnableDelayedExpansion

set "ROOT=%~dp0.."
set "PY=%ROOT%\tools\R2815.py"

echo.
echo ======================================================================
echo [R2815] HOTFIX: Purge call _r1851_run_tools_runner without unsupported title kwarg
echo Root: "%ROOT%"
echo ======================================================================
echo.

if not exist "%PY%" (
  echo [R2815] ERROR: Missing "%PY%"
  exit /b 11
)

python "%PY%" "%ROOT%"
set "RC=%ERRORLEVEL%"

echo.
if not "%RC%"=="0" (
  echo [R2815] FAIL (code %RC%)
) else (
  echo [R2815] OK
)
echo.
exit /b %RC%
