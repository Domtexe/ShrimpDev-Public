@echo off
setlocal ENABLEDELAYEDEXPANSION

set "SCRIPT_DIR=%~dp0"
for %%I in ("%SCRIPT_DIR%..") do set "ROOT=%%~fI"

echo ======================================================================
echo [R2864] SAFE PATCH: Fix Export Public button parent (service_frame -> frame_toolbar_right)
echo Root: "%ROOT%"
echo ======================================================================

if not exist "%ROOT%\tools\R2864.py" (
  echo [R2864] ERROR: tools\R2864.py not found
  exit /b 11
)

python "%ROOT%\tools\R2864.py" "%ROOT%"
exit /b %ERRORLEVEL%
