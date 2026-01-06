@echo off
setlocal
echo [1175g] ModulesPackageFix: starte Patch...
where py >nul 2>&1 && (set PY=py -3) || (set PY=python)
%PY% "D:\ShrimpDev\tools\Runner_1175g_ModulesPackageFix.py"
if errorlevel 1 (
  echo [1175g] FEHLER. Siehe Konsole / debug_output.txt
) else (
  echo [1175g] Patch erfolgreich, Syntax OK.
)
endlocal
