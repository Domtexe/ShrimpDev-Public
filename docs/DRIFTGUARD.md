# DriftGuard v1

## Ziel
Verhindert Systemdrift durch sichere Runner-Ausführung.

## Regeln

### Preflight
- py_compile MUSS erfolgreich sein
- Anchor MUSS existieren

### Apply
- Nur in Memory
- Kein direktes Schreiben

### Postflight
- py_compile
- Import-Test

### Atomic Write
- Erst nach Erfolg ersetzen

### Backup
- Nur 'good' Backups gelten als valide

## Verboten
- Regex ohne Anchor
- Multi-Patches
- Blindes Injecten
