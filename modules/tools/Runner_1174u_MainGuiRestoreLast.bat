@echo off
setlocal
cd /d D:\ShrimpDev
echo [1174u] RestoreLast: suche letztes Backup...
py -3 -u "tools\Runner_1174u_MainGuiRestoreLast.py"
set RC=%ERRORLEVEL%
if %RC% NEQ 0 (
  echo [1174u] FEHLER RC=%RC%.
  exit /b %RC%
)
echo [1174u] Restore OK.
exit /b 0
