@echo on
setlocal ENABLEDELAYEDEXPANSION

rem immer ins Projekt-Root wechseln (Ordner über "tools")
pushd "%~dp0\.." || (
  echo [R1137] CD-Fehler: %~dp0
  exit /b 2
)

echo [R1137] IntakeLoadFix :: CWD=%CD%

rem Python-Launcher bevorzugen, sonst python.exe
set "PYCMD="
where py  1>nul 2>nul && set "PYCMD=py -3 -X utf8 -u"
if not defined PYCMD (
  where python 1>nul 2>nul && set "PYCMD=python -X utf8 -u"
)
if not defined PYCMD (
  echo [R1137] Fehler: Weder 'py' noch 'python' im PATH.
  popd & exit /b 9009
)

echo [R1137] PYCMD: %PYCMD%
echo [R1137] Script: tools\Runner_1137_IntakeLoadFix.py

%PYCMD% "tools\Runner_1137_IntakeLoadFix.py"
set "RC=%ERRORLEVEL%"
echo [R1137] Python RC=%RC%

popd
echo [R1137] Ende (RC=%RC%)
exit /b %RC%
