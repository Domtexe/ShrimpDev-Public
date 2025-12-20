@echo off
setlocal
rem Gehe zuverlässig ins Projekt-Root (Ordner über "tools")
pushd "%~dp0\.." || (
  echo [RUN] Fehler: Konnte nicht ins Projekt-Root wechseln.
  exit /b 2
)

echo [RUN] Runner_1127_IntakeDetox

rem 1) py-Launcher bevorzugen
where py >NUL 2>&1
if %ERRORLEVEL% EQU 0 (
  py -3 "tools\Runner_1127_IntakeDetox.py"
) else (
  rem 2) Fallback: python.exe
  where python >NUL 2>&1
  if %ERRORLEVEL% EQU 0 (
    python "tools\Runner_1127_IntakeDetox.py"
  ) else (
    echo [RUN] Fehler: Weder "py" noch "python" im PATH gefunden.
    popd
    exit /b 9009
  )
)

set "RC=%ERRORLEVEL%"
popd
echo [RUN] Ende (RC=%RC%)
exit /b %RC%
