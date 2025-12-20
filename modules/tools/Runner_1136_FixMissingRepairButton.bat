@echo off
setlocal
pushd "%~dp0\.." || (echo [R1136] CD-Fehler & exit /b 2)
echo [R1136] FixMissingRepairButton

set "PYCMD="
where py >NUL 2>&1 && set "PYCMD=py -3"
if not defined PYCMD (where python >NUL 2>&1 && set "PYCMD=python")
if not defined PYCMD (
  echo [R1136] Fehler: Kein Python gefunden.
  popd & exit /b 9009
)

%PYCMD% -u "tools\Runner_1136_FixMissingRepairButton.py"
set "RC=%ERRORLEVEL%"
popd
echo [R1136] Ende (RC=%RC%)
exit /b %RC%
