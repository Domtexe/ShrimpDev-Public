@echo off
setlocal EnableExtensions EnableDelayedExpansion
title ShrimpDev - 1114 SanityRepair

pushd "%~dp0"
cd ..
set "ROOT=%CD%"
echo [CWD] %ROOT%

set "PYEXE=py -3"
for /f "delims=" %%P in ('where py 2^>nul') do (set "PYFOUND=1")
if not defined PYFOUND (
  for /f "delims=" %%P in ('where python 2^>nul') do (set "PYEXE=python")
)

echo [RUN ] %PYEXE% -u tools\Runner_1114_DeepSanityAndRepair.py
%PYEXE% -u tools\Runner_1114_DeepSanityAndRepair.py
set "RC=!ERRORLEVEL!"
echo [END ] RC=!RC!
echo.
pause
endlocal
