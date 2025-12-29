@echo off
setlocal ENABLEDELAYEDEXPANSION
REM R2871 runner wrapper
REM Root must be the PRIVATE repo root (where registry/ exists)

set "ROOT=%~dp0.."
pushd "%ROOT%" >nul

if not exist "registry\public_export_root.txt" (
  echo [R2871] FAIL: registry\public_export_root.txt not found
  popd >nul
  exit /b 11
)
if not exist "registry\public_allowlist.txt" (
  echo [R2871] FAIL: registry\public_allowlist.txt not found
  popd >nul
  exit /b 11
)

set "PYEXE=python"
where python >nul 2>nul
if errorlevel 1 (
  where py >nul 2>nul
  if errorlevel 1 (
    echo [R2871] FAIL: python not found in PATH
    popd >nul
    exit /b 11
  ) else (
    set "PYEXE=py -3"
  )
)

%PYEXE% tools\R2871.py
set "EC=%ERRORLEVEL%"

popd >nul
exit /b %EC%
