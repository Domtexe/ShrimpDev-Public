@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"
cd ..
set "ROOT=%CD%"
set "LOG=%ROOT%\debug_output.txt"

rem --- Python ermitteln ---
set "PY_EXE="
if exist "%ROOT%\venv\Scripts\python.exe" set "PY_EXE=%ROOT%\venv\Scripts\python.exe"
if not defined PY_EXE set "PY_EXE=py"

rem --- Flags ---
set "PY_FLAGS=-u"
rem Wenn 'py' genutzt wird, nimm explizit 3 + unbuffered
for %%I in ("%PY_EXE%") do (
  if /I "%%~nxI"=="py.exe" set "PY_FLAGS=-3 -u"
  if /I "%%~nxI"=="py"     set "PY_FLAGS=-3 -u"
)

echo [Start] Using: "%PY_EXE%" %PY_FLAGS% main_gui.py
pushd "%ROOT%"
"%PY_EXE%" %PY_FLAGS% "main_gui.py"
set RC=%ERRORLEVEL%
if %RC% NEQ 0 (
  echo [Start] main_gui.py failed (rc=%RC%)
  >nul 2>&1 (
    echo [%%date%% %%time%%] [Start_MainGui] rc=%RC% >> "%LOG%"
  )
)
popd
exit /b %RC%

echo.
pause
