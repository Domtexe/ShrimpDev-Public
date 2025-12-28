@echo off
setlocal ENABLEDELAYEDEXPANSION

set "SCRIPT_DIR=%~dp0"
for %%I in ("%SCRIPT_DIR%..") do set "ROOT=%%~fI"

echo ======================================================================
echo [R2860] SAFE PATCH: CI add Smoke-Test step (R2857.py)
echo Root: "%ROOT%"
echo ======================================================================

if not exist "%ROOT%\tools\R2860.py" (
  echo [R2860] ERROR: tools\R2860.py not found
  exit /b 11
)

python "%ROOT%\tools\R2860.py" "%ROOT%"
exit /b %ERRORLEVEL%
