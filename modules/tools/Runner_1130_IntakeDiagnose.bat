@echo off
setlocal
pushd "%~dp0\.." || ( echo [R1130] CD-Fehler & exit /b 2 )
echo [R1130] IntakeDiagnose

REM Python auflösen
where py >NUL 2>&1
if %ERRORLEVEL% EQU 0 (
  py -3 "tools\Runner_1130_IntakeDiagnose.py"
) else (
  where python >NUL 2>&1 || ( echo [R1130] Python nicht gefunden & popd & exit /b 9009 )
  python "tools\Runner_1130_IntakeDiagnose.py"
)

set RC=%ERRORLEVEL%
popd
echo [R1130] Ende (RC=%RC%)
exit /b %RC%
