@echo off
rem ShrimpDev – Post-Patch Guard Hook
rem Ruft den Sanity-Guard auf (CRLF, Tabs->Spaces, __future__ nach oben,
rem IntakeFrame-Reindent, try/except-Fixes, Delete-Dialog-Härtung, AST-Check).

setlocal EnableExtensions DisableDelayedExpansion
pushd "%~dp0"
cd ..
set "PYEXE="
where py >nul 2>nul && set "PYEXE=py -3"
if not defined PYEXE ( where python >nul 2>nul && set "PYEXE=python" )
if not defined PYEXE (
  echo [GUARD] Python nicht gefunden. Uebersprungen.
  popd & exit /b 0
)

echo [GUARD] Sanity-Check: tools\Runner_1063_Intake_SanityGuard.py
%PYEXE% tools\Runner_1063_Intake_SanityGuard.py
set "RC=%ERRORLEVEL%"
if not "%RC%"=="0" (
  echo [GUARD] Fehlercode %RC% — siehe debug_output.txt (Dump + Kontext).
  popd & exit /b %RC%
)
echo [GUARD] OK.
popd & exit /b 0
