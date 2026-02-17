# Changelog
## 2025-12-18 – R2373
- Neues Modul: modules/ini_writer.py (merge + atomic)
- Pipeline: Defactoring obsoleter Dateien nach erfolgreicher Umstellung einsortiert


## Docking Persistence Fix
_added 2026-01-08 12:26 via R3147_

- Fixed docking restore issue caused by legacy INI state.
- Normalized docking persistence semantics.
- No functional code changes; documentation + state reset only.

## [2026-01-13]
- DOCS: Docking Verify finalized (core verified)
- DOCS: Log-Tab Button-Row detection als Non-Blocking-Subtask ergänzt

<!-- R3431 -->
- DOCS: Docking Verify final (R3413 exit 0, referenziert)
- DOCS: Verify-Referenz aufgenommen: Reports/Report_R3413_20260113_160946.md

<!-- R3432 -->
- DOCS: P1 Docking (Parent) final auf DONE gesetzt
- DOCS: Referenz auf finalen Verify-Report: Reports/Report_R3413_20260113_160946.md

## 2026-02-09 – R8429
- DOCS: Neue kanonische SOP eingeführt: `docs/NACHSORGE_PLUS_SOP.md`
- Zweck: standardisierte Nachsorge (Read-Only Diagnose → Bewertung → optional Apply)

## 2026-02-16 — P6P Buttons
- Fix: P6P Push/Purge starten Runner wieder über einheitlichen Pfad.
- Cleanup: PP_DIAG-Dateien entfernt.
- Nachsorge: `Report_R8651_20260216_233513.md`
---

## 2026-02-17
- Lane B: Runner-SSOT stabilisiert (Popup delegiert an `runner_executor.execute_runner`), DIAG-Kette R8652–R8659; Output-Capture in `logic_actions.py` bewusst beibehalten (rc/out/err), TechDebt tasks in Pipeline ergänzt.
