@echo off
setlocal EnableExtensions EnableDelayedExpansion

set "ROOT=%~dp0.."
set "PY=%ROOT%\tools\R2809.py"

echo.
echo ======================================================================
echo [R2809] HOTFIX: Fix empty try blocks in ui_toolbar.py + neutralize popup calls safely
echo Root: "%ROOT%"
echo ======================================================================
echo.

if not exist "%PY%" (
  echo [R2809] ERROR: Missing "%PY%"
  exit /b 11
)

python "%PY%" "%ROOT%"
set "RC=%ERRORLEVEL%"

echo.
if not "%RC%"=="0" (
  echo [R2809] FAIL (code %RC%)
) else (
  echo [R2809] OK
)
echo.
exit /b %RC%
