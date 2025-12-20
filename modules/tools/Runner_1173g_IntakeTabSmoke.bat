@echo off
cd /d "%~dp0\.."
echo [1173g] Smoke: starte...
python tools\Runner_1173g_IntakeTabSmoke.py || (
  echo [1173g] Smoke FEHLER.
  exit /b 1
)
echo [1173g] Smoke OK.
exit /b 0
