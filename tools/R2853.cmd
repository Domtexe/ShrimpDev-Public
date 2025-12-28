@echo off
setlocal ENABLEDELAYEDEXPANSION

REM ==========================================================
REM R2853 - READ-ONLY: Pipeline P3 Audit
REM Root auto-detected from this script location (tools\)
REM ==========================================================

set "SCRIPT_DIR=%~dp0"
for %%I in ("%SCRIPT_DIR%..") do set "ROOT=%%~fI"

echo ======================================================================
echo [R2853] READ-ONLY: Pipeline P3 Audit
echo Root: "%ROOT%"
echo ======================================================================

if not exist "%ROOT%\tools\R2853.py" (
  echo [R2853] ERROR: tools\R2853.py not found under "%ROOT%"
  exit /b 11
)

python "%ROOT%\tools\R2853.py" "%ROOT%"
set "EC=%ERRORLEVEL%"

if not "%EC%"=="0" (
  echo [R2853] FAIL (code %EC%)
  exit /b %EC%
)

echo [R2853] OK
exit /b 0
