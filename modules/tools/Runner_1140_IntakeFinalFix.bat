@echo off
setlocal ENABLEDELAYEDEXPANSION
echo [R1140] IntakeFinalFix

rem --- ins Projekt-Root wechseln (Ordner ueber "tools")
pushd "%~dp0..\"  || ( echo [R1140] CD-Fehler & exit /b 2 )
set "CWD=%CD%"
echo [R1140] CWD=%CWD%

rem --- Python-Launcher bevorzugen
set "PYCMD="
where py    1>nul 2>nul && set "PYCMD=py -3 -X utf8 -u"
if not defined PYCMD ( where python 1>nul 2>nul && set "PYCMD=python -X utf8 -u" )
if not defined PYCMD (
  echo [R1140] Fehler: Weder 'py' noch 'python' im PATH.
  popd & exit /b 9009
)

echo [R1140] PYCMD: %PYCMD%
set "SCRIPT=tools\Runner_1140_IntakeFinalFix.py"
echo [R1140] Script: %SCRIPT%

%PYCMD% "%SCRIPT%"
set "RC=%ERRORLEVEL%"

popd
echo [R1140] Ende (RC=%RC%)
exit /b %RC%
