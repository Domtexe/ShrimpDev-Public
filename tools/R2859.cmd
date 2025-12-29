@echo off
setlocal ENABLEDELAYEDEXPANSION

set "SCRIPT_DIR=%~dp0"
for %%I in ("%SCRIPT_DIR%..") do set "ROOT=%%~fI"

echo ======================================================================
echo [R2859] SAFE PATCH: Replace tools\R2857.py (exclude tools\Archiv)
echo Root: "%ROOT%"
echo ======================================================================

if not exist "%ROOT%\tools\R2859.py" (
  echo [R2859] ERROR: tools\R2859.py not found
  exit /b 11
)

python "%ROOT%\tools\R2859.py" "%ROOT%"
exit /b %ERRORLEVEL%
