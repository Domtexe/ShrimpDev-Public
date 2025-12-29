@echo off
setlocal ENABLEDELAYEDEXPANSION

set "SCRIPT_DIR=%~dp0"
for %%I in ("%SCRIPT_DIR%..") do set "ROOT=%%~fI"

echo ======================================================================
echo [R2857] READ-ONLY: Smoke Test (syntax + structure)
echo Root: "%ROOT%"
echo ======================================================================

if not exist "%ROOT%\tools\R2857.py" (
  echo [R2857] ERROR: tools\R2857.py not found
  exit /b 11
)

python "%ROOT%\tools\R2857.py" "%ROOT%"
set "EC=%ERRORLEVEL%"

if not "%EC%"=="0" (
  echo [R2857] FAIL (code %EC%)
  exit /b %EC%
)

echo [R2857] OK
exit /b 0
