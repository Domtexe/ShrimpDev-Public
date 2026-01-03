@echo off
setlocal
pushd "%~dp0\.." || ( echo [R1132] CD-Fehler & exit /b 2 )

echo [R1132] FixGuardParent

rem Python-Launcher bevorzugen, sonst python.exe
set "PYCMD="
where py >NUL 2>&1 && set "PYCMD=py -3"
if not defined PYCMD (
  where python >NUL 2>&1 && set "PYCMD=python"
)
if not defined PYCMD (
  echo [R1132] Fehler: Weder "py" noch "python" gefunden.
  popd & exit /b 9009
)

%PYCMD% -u "tools\Runner_1132_FixGuardParent.py"
set "RC=%ERRORLEVEL%"

popd
echo [R1132] Ende (RC=%RC%)
exit /b %RC%
