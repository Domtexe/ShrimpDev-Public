@echo off
setlocal
pushd "%~dp0\.." || ( echo [R1135] CD-Fehler & exit /b 2 )

echo [R1135] ModulesInitAndDiagnose

set "PYCMD="
where py >NUL 2>&1 && set "PYCMD=py -3"
if not defined PYCMD ( where python >NUL 2>&1 && set "PYCMD=python" )
if not defined PYCMD (
  echo [R1135] Fehler: Weder "py" noch "python" im PATH.
  popd & exit /b 9009
)

%PYCMD% -u "tools\Runner_1135_ModulesInitAndDiagnose.py"
set "RC=%ERRORLEVEL%"

popd
echo [R1135] Ende (RC=%RC%)
exit /b %RC%
