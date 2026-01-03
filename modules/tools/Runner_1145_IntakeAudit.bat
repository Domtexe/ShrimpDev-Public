@echo off
setlocal ENABLEDELAYEDEXPANSION
echo [R1145] IntakeAudit
pushd "%~dp0\.." 1>nul 2>nul || ( echo [R1145] CD-Fehler & exit /b 2 )

rem Python-Launcher bevorzugen
set "PYCMD="
where py     >nul 2>nul && set "PYCMD=py -3 -X utf8 -u"
if not defined PYCMD ( where python >nul 2>nul && set "PYCMD=python -X utf8 -u" )
if not defined PYCMD (
  echo [R1145] Fehler: Weder 'py' noch 'python' im PATH.
  popd & exit /b 9009
)

%PYCMD% "tools\Runner_1145_IntakeAudit.py"
set "RC=%ERRORLEVEL%"
popd
echo [R1145] Ende (RC=%RC%)
exit /b %RC%
