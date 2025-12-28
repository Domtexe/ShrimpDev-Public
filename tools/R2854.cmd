@echo off
setlocal ENABLEDELAYEDEXPANSION

set "SCRIPT_DIR=%~dp0"
for %%I in ("%SCRIPT_DIR%..") do set "ROOT=%%~fI"

echo ======================================================================
echo [R2854] SAFE PATCH: Pipeline P3 Cleanup
echo Root: "%ROOT%"
echo ======================================================================

if not exist "%ROOT%\tools\R2854.py" (
  echo [R2854] ERROR: tools\R2854.py not found
  exit /b 11
)

python "%ROOT%\tools\R2854.py" "%ROOT%"
exit /b %ERRORLEVEL%
