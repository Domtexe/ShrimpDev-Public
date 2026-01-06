@echo off
setlocal ENABLEDELAYEDEXPANSION
echo [R1153d] RegexHyphenFix

rem immer ins Projekt-Root (Ordner ueber "tools")
pushd "%~dp0..\"  || ( echo [R1153d] CD-Fehler & exit /b 2 )

rem Python-Launcher bevorzugen
set "PYCMD="
where py  >nul 2>nul && set "PYCMD=py -3 -X utf8 -u"
if not defined PYCMD (where python >nul 2>nul && set "PYCMD=python -X utf8 -u")
if not defined PYCMD (
  echo [R1153d] Fehler: Weder 'py' noch 'python' im PATH.
  popd & exit /b 9009
)

echo [R1153d] %PYCMD%
%PYCMD% "tools\Runner_1153d_RegexHyphenFix.py"
set RC=%ERRORLEVEL%

popd
echo [R1153d] Ende (RC=%RC%)
exit /b %RC%
