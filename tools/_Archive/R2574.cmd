@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM ============================================================
REM R2574 - CI: exclude legacy ui_toolbar.py from Ruff + add TechDebt to Pipeline
REM Root: repo root (this .cmd lives in tools\)
REM ============================================================

set "ROOT=%~dp0.."
set "PY=%ROOT%\tools\R2574.py"

echo [R2574] START
python "%PY%"
set "ERR=%ERRORLEVEL%"

if not "%ERR%"=="0" (
  echo [R2574] FAILED with code %ERR%
  exit /b %ERR%
)

echo [R2574] OK
exit /b 0
