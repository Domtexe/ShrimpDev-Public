@echo off
setlocal ENABLEDELAYEDEXPANSION
echo [R1155] IntakeBootDiag (Debug)

rem Projekt-Root bestimmen
set "SELF=%~dp0"
pushd "%SELF%\.." || (
  echo [R1155] Fehler: konnte Projekt-Root nicht finden.
  pause
  exit /b 2
)

echo [R1155] CWD: %CD%

rem Python finden
set "PYCMD="
where py >nul 2>nul && set "PYCMD=py -3 -X utf8 -u"
if not defined PYCMD (
  where python >nul 2>nul && set "PYCMD=python -X utf8 -u"
)
if not defined PYCMD (
  echo [R1155] Fehler: Weder 'py' noch 'python' im PATH.
  pause
  exit /b 9009
)

if not exist "tools\Runner_1155_IntakeBootDiag.py" (
  echo [R1155] Script fehlt: %CD%\tools\Runner_1155_IntakeBootDiag.py
  pause
  exit /b 3
)

echo [R1155] PYTHON: %PYCMD%
echo [R1155] Starte: %PYCMD% "tools\Runner_1155_IntakeBootDiag.py"
echo ------------------------------------------------------------
%PYCMD% "tools\Runner_1155_IntakeBootDiag.py"
echo ------------------------------------------------------------
set "RC=%ERRORLEVEL%"
echo [R1155] Rückgabecode: %RC%

pause
exit /b %RC%
