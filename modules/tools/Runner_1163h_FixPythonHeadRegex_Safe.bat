@echo off
setlocal EnableExtensions DisableDelayedExpansion
title ShrimpDev - R1163h FixPythonHeadRegex_Safe (RUN)

pushd "%~dp0"
cd ..

if not exist "tools\Runner_1163h_FixPythonHeadRegex_Safe.py" (
  echo [ERR] tools\Runner_1163h_FixPythonHeadRegex_Safe.py not found
  goto :END
)

set "PYEXE="
where py >nul 2>&1 && set "PYEXE=py -3"
if not defined PYEXE ( where python >nul 2>&1 && set "PYEXE=python" )
if not defined PYEXE ( echo [ERR] No Python interpreter found. & goto :END )

echo [RUN ] %PYEXE% -u tools\Runner_1163h_FixPythonHeadRegex_Safe.py
%PYEXE% -u tools\Runner_1163h_FixPythonHeadRegex_Safe.py
echo [END ] RC=%ERRORLEVEL%

:END
popd
exit /b %ERRORLEVEL%
