@echo off
setlocal ENABLEEXTENSIONS ENABLEDELAYEDEXPANSION

REM ============================================================
REM R2570 - Docs: CI scope/runtime-only + cross-reference rules
REM ============================================================

set "ROOT=%~dp0.."
set "PY=%ROOT%\tools\R2570.py"
set "REPORTS=%ROOT%\Reports"

if not exist "%REPORTS%" mkdir "%REPORTS%"

echo [R2570] START
python "%PY%"
set "ERR=%ERRORLEVEL%"

if not "%ERR%"=="0" (
  echo [R2570] FAILED with code %ERR%
  exit /b %ERR%
)

echo [R2570] OK
exit /b 0
