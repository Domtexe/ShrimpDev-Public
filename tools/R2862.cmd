@echo off
setlocal ENABLEDELAYEDEXPANSION

set "SCRIPT_DIR=%~dp0"
for %%I in ("%SCRIPT_DIR%..") do set "ROOT=%%~fI"

echo ======================================================================
echo [R2862] SYNC: Private -> Public Export (and optionally push)
echo Root: "%ROOT%"
echo ======================================================================

if not exist "%ROOT%\tools\R2862.py" (
  echo [R2862] ERROR: tools\R2862.py not found
  exit /b 11
)

python "%ROOT%\tools\R2862.py" "%ROOT%"
exit /b %ERRORLEVEL%
