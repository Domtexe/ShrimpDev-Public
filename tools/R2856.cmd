@echo off
setlocal ENABLEDELAYEDEXPANSION

set "SCRIPT_DIR=%~dp0"
for %%I in ("%SCRIPT_DIR%..") do set "ROOT=%%~fI"

echo ======================================================================
echo [R2856] PATCH: Learnings + Rules + CI Guide
echo Root: "%ROOT%"
echo ======================================================================

if not exist "%ROOT%\tools\R2856.py" (
  echo [R2856] ERROR: tools\R2856.py not found
  exit /b 11
)

python "%ROOT%\tools\R2856.py" "%ROOT%"
exit /b %ERRORLEVEL%
