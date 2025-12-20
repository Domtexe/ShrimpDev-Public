@echo off
setlocal EnableExtensions DisableDelayedExpansion
title ShrimpDev - R1166c Intake MinimalScopeFix (RUN)

pushd "%~dp0"
cd ..

if not exist "tools\Runner_1166c_Intake_MinimalScopeFix.py" (
  echo [ERR] tools\Runner_1166c_Intake_MinimalScopeFix.py not found
  goto :END
)

set "PYEXE="
where py >nul 2>&1 && set "PYEXE=py -3"
if not defined PYEXE ( where python >nul 2>&1 && set "PYEXE=python" )
if not defined PYEXE ( echo [ERR] No Python interpreter found. & goto :END )

echo [RUN ] %PYEXE% -u tools\Runner_1166c_Intake_MinimalScopeFix.py
%PYEXE% -u tools\Runner_1166c_Intake_MinimalScopeFix.py
echo [END ] RC=%ERRORLEVEL%

:END
popd
exit /b %ERRORLEVEL%
