# Changelog
## 2025-12-18 – R2373
- Neues Modul: modules/ini_writer.py (merge + atomic)
- Pipeline: Defactoring obsoleter Dateien nach erfolgreicher Umstellung einsortiert


## Docking Persistence Fix
_added 2026-01-08 12:26 via R3147_

- Fixed docking restore issue caused by legacy INI state.
- Normalized docking persistence semantics.
- No functional code changes; documentation + state reset only.
