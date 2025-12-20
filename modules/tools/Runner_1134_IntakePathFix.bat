@echo off
setlocal
pushd "%~dp0\.." || (echo [R1134] CD-Fehler & exit /b 2)
echo [R1134] IntakePathFix

set "PYCMD="
where py >NUL 2>&1 && set "PYCMD=py -3"
if not defined PYCMD (where python >NUL 2>&1 && set "PYCMD=python")
if not defined PYCMD (
  echo [R1134] Fehler: Kein Python gefunden.
  popd & exit /b 9009
)

%PYCMD% -u "tools\Runner_1134_IntakePathFix.py"
set "RC=%ERRORLEVEL%"
popd
echo [R1134] Ende (RC=%RC%)
exit /b %RC%
