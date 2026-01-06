@echo off
setlocal
echo [R1230] Restore Intake from latest backup...

py -3 -u "%~dp0Runner_1230_RestoreIntakeFromBackup.py"
if errorlevel 1 (
  echo [R1230] FAILED. Siehe debug_output.txt
  exit /b 1
) else (
  echo [R1230] Done. rc=0
)
