@echo off
setlocal ENABLEDELAYEDEXPANSION

set "SCRIPT_DIR=%~dp0"
for %%I in ("%SCRIPT_DIR%..") do set "ROOT=%%~fI"

echo ======================================================================
echo [R2858] SAFE PATCH: Refine Smoke Test (exclude tools/Archiv)
echo Root: "%ROOT%"
echo ======================================================================

if not exist "%ROOT%\tools\R2858.py" (
  echo [R2858] ERROR: tools\R2858.py not found
  exit /b 11
)

python "%ROOT%\tools\R2858.py" "%ROOT%"
exit /b %ERRORLEVEL%
