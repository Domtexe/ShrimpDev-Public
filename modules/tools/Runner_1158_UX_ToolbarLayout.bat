@echo off
setlocal EnableExtensions DisableDelayedExpansion
title ShrimpDev - R1158 UX ToolbarLayout (RUN)

pushd "%~dp0"
cd ..

echo [CWD] %CD%

if not exist "tools\Runner_1158_UX_ToolbarLayout.py" (
  echo [ERR] tools\Runner_1158_UX_ToolbarLayout.py not found
  goto :END
)

rem --- Interpreter-Priorität: py -3, sonst python ---
set "PYEXE="
where py >nul 2>&1 && set "PYEXE=py -3"
if not defined PYEXE (
  where python >nul 2>&1 && set "PYEXE=python"
)
if not defined PYEXE (
  echo [ERR] No python interpreter found.
  goto :END
)

echo [RUN ] %PYEXE% -u tools\Runner_1158_UX_ToolbarLayout.py
%PYEXE% -u tools\Runner_1158_UX_ToolbarLayout.py
set "RC=%ERRORLEVEL%"
echo [END ] RC=%RC%

:END
popd
exit /b %RC%
