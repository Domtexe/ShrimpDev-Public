@echo off
setlocal EnableExtensions DisableDelayedExpansion
title ShrimpDev - R1162 DetectRegexScanner (RUN)

pushd "%~dp0"
cd ..

echo [CWD] %CD%

if not exist "tools\Runner_1162_DetectRegexScanner.py" (
  echo [ERR] tools\Runner_1162_DetectRegexScanner.py not found
  goto :END
)

rem --- Interpreter: bevorzugt py -3, sonst python ---
set "PYEXE="
where py >nul 2>&1 && set "PYEXE=py -3"
if not defined PYEXE (
  where python >nul 2>&1 && set "PYEXE=python"
)
if not defined PYEXE (
  echo [ERR] No Python interpreter found.
  goto :END
)

echo [RUN ] %PYEXE% -u tools\Runner_1162_DetectRegexScanner.py
%PYEXE% -u tools\Runner_1162_DetectRegexScanner.py
set "RC=%ERRORLEVEL%"
echo [END ] RC=%RC%

:END
popd
exit /b %RC%
