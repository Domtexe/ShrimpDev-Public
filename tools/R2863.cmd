@echo off
setlocal ENABLEDELAYEDEXPANSION

set "SCRIPT_DIR=%~dp0"
for %%I in ("%SCRIPT_DIR%..") do set "ROOT=%%~fI"

echo ======================================================================
echo [R2863] SAFE PATCH: Add Export Public button + action (R2862)
echo Root: "%ROOT%"
echo ======================================================================

if not exist "%ROOT%\tools\R2863.py" (
  echo [R2863] ERROR: tools\R2863.py not found
  exit /b 11
)

python "%ROOT%\tools\R2863.py" "%ROOT%"
exit /b %ERRORLEVEL%
