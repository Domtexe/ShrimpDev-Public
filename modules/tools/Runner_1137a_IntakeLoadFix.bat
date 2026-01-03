@echo on
setlocal ENABLEDELAYEDEXPANSION

pushd "%~dp0\.." || ( echo [R1137a] CD-Fehler & exit /b 2 )
echo [R1137a] CWD=%CD%

set "PYCMD="
where py 1>nul 2>nul && set "PYCMD=py -3 -X utf8 -u"
if not defined PYCMD (
  where python 1>nul 2>nul && set "PYCMD=python -X utf8 -u"
)
if not defined PYCMD (
  echo [R1137a] Fehler: Weder 'py' noch 'python' im PATH.
  popd & exit /b 9009
)

echo [R1137a] PYCMD: %PYCMD%
%PYCMD% "tools\Runner_1137a_IntakeLoadFix.py"
set "RC=%ERRORLEVEL%"

popd
echo [R1137a] Ende (RC=%RC%)
exit /b %RC%
