@echo off
setlocal ENABLEDELAYEDEXPANSION
echo [R1138] IntakeLoadFix2

rem Korrekt: nur eine Ebene hoch (vom tools/ in Projekt-Root)
pushd "%~dp0\.."  || ( echo [R1138] CD-Fehler & exit /b 2 )

set "PYCMD="
where py     >nul 2>nul  && set "PYCMD=py -3 -X utf8 -u"
if not defined PYCMD ( where python >nul 2>nul && set "PYCMD=python -X utf8 -u" )
if not defined PYCMD ( echo [R1138] Fehler: Weder 'py' noch 'python' im PATH. & popd & exit /b 9009 )

set "SCRIPT=tools\Runner_1138_IntakeLoadFix2.py"
echo [R1138] CWD=%CD%
echo [R1138] CALL: %PYCMD% "%SCRIPT%"
%PYCMD% "%SCRIPT%"
set "RC=%ERRORLEVEL%"

popd
echo [R1138] Ende (RC=%RC%)
exit /b %RC%
