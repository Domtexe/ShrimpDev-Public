# Changelog
## 2026-03-17 – Pipeline-Ideen konsolidiert
- Neue Ideen gegen die bestehende Pipeline dedupliziert und als kanonische Cluster nach Lanes eingeordnet.
- Strategisch wichtige Punkte sauber verankert: `Docs Consistency Check`, `Regression Radar`, `Patch / Runner Compliance Gate`, `Clarivoo Factory`, `Idea Inbox Normalizer`, `Pipeline Quick Add`, `Excel Rescue AI / Makro-Wiederbelebungs-Toolkit`.
- Breite/überlappende Ideen wurden bewusst gebündelt statt mehrfach eingetragen.
- `docs/SHORTCODES.md` schärft jetzt explizit, dass Thread-Ideen vor Pipeline-Übernahme dedupliziert, geclustert und priorisiert werden sollen.

## 2026-03-17 – Intake / Validator / Popup / T666 Nachsorge-Konsolidierung
- Validator/Gate differenziert: `R9417` blockiert Meta-/Maintenance-Runner und normale GUI-Runner nicht mehr stumpf wegen global dirty worktree; `tmp/`, `.git/`, `__pycache__/` zaehlen nicht als harte Zusatz-Zonen.
- Intake/Tree stabilisiert: Sort-State persistent, Rebuild/Refresh deterministischer, Reentry-/Inflight-Probleme entschaerft, Rechtsklick-Kontextmenue fuer den aktiven Runner-/Intake-Tree ergänzt.
- Popup-/Executor-Pfade konsolidiert: Standard-GUI-Runner sowie `Push`/`Purge` laufen ueber den sauberen Executor-/OutputDisplay-Pfad ohne unnötige Standard-Popups.
- Verifiziert im Block: `R9425`, `R9341`, `R2693`, `R2224`, `R9419`.
- `T666` wiederhergestellt, purge-geschützt und zur kleinen Universal Runner Engine mit `diag`, `smoke`, `filecheck <path>`, `echo <text>` ausgebaut.
- Protected-Runner-Audit bewusst konservativ abgeschlossen: keine unüberlegte Entschützung und keine GUI-Button-Entfernung ohne klar belegte Redundanz.

## 2026-03-15 – Protected Runners / Special Buttons
- Protected runner SSOT erweitert: `R9418`, `R9419`, `R9420`, `R9421`, `R9999`, `R1802`.
- GUI: neue Sonderrunner-Buttons `Ideas Feed`, `Ideas Scan`, `Ideas Decision`, `RunnerGuard`.
- Schutz: normale Delete-/Trash-Logik blockiert geschuetzte Runner; Purge-Schutzlisten erweitert.

## 2026-03-15 – R9418
- Ideas import path clarified: canonical source remains `docs/IDEA_INBOX.md`.
- `R9418` corrected to feed `NEW` `## ENTRY` blocks into the existing inbox flow.
- `docs/ideas/ideas_inbox_*.md` retained only as optional archive evidence, not as an import path.

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

---

## Lane C Nachsorge (2026-02-17 10:56)

Status:
- Preflight-Modul vorhanden (modules/preflight_checks.py)
- Zentraler Hook NICHT gesetzt (bewusste Entscheidung nach DIAG)
- Keine Blind-Patches gemäß MasterRules

DIAG-Kette:
R8661–R8666

Entscheidung:
- Kein Risiko-Patch ohne eindeutigen Gatekeeper
- Zentraler Hook bleibt Tech-Debt Task

Tech-Debt:
- Global Runner Entry Mapping fehlt
- Preflight noch nicht SSOT-gekoppelt

Lane-C-Bewertung:
➡️ bearbeitet  
➡️ stabil  
➡️ nicht vollständig abgeschlossen

<!-- BEGIN:R8598 -->
## 2026-02-22 — UI OutputDisplay + Recovery

- Display/Output zentralisiert (OutputDisplay in main_gui, Tree entkoppelt)
- UI-Polish OutputDisplay (Header/Copy/Clear/Scrollbars)
- Recovery nach `IndentationError`: Restore auf kompilierbare Backup-Version
- Governance: Compile-Gate + Restore-Regel (siehe MR Block R8598)
<!-- END:R8598 -->

## 20260223_000540
- Governance + Shortcodes stabilized
## 2026-02-25 — Nachsorge R9062

- Nachsorge automatisiert: Backups + Report + marker-basierte Docs-Updates.
- Problem-Kontext: Intake Build brach durch fehlende optionale Hooks (`enable_lasso`) ab; UI blieb leer.
- Nächste Schritte: Intake-Build stabilisieren, rechte Seite (Tree/Toolbar/Output) wieder einhängen, danach RUN verifizieren.


## Nachsorge
- 2026-02-28 00:21 Nachsorge R9107: Stabilisierung/Backups + SyntaxGate. Drift-Risiko bestätigt; nächster Schritt: Call-Site-DIAG für Intake-Builder (kein Raten nach _build_intake).

## 2026-03-08 — Intake/Runner/Inbox Stabilisierung
- Intake stabilization: `_build_intake()` Guard gegen Mehrfachaufbau, Right-Stack stabil (`Output -> Toolbar -> Tree`), R9207-DIAG zeitlich korrigiert.
- Run wiring fix: R9256-Methoden als echte `ShrimpDevApp`-Methoden eingehängt; Run E2E verifiziert.
- Runner output capture: `stdout/stderr` live in OutputDisplay + Log gespiegelt.
- Tree search restored: Suche + Runner-Counter/Trefferanzeige wieder aktiv.
- Right toolbar actions implemented: `_cmd_trash`, `_cmd_rename`, `action_autopush_both`, `action_purge_one`, `action_guard_futurefix_safe`, `action_r9998`, `action_r9999`.
- Idea inbox/orchestrator introduced: `docs/IDEA_INBOX.md`, `docs/IDEA_INBOX_SPEC.md`, `modules/idea_inbox_status.py`, Import-Flow `GUI -> R9341`.
## Version 2.0 - 2026-03-16

### Added

- stabile Dispo-Planungslogik
- Nachlasssteuerung
- Mail/DMS Zuteilung
- HTML Mail Preview

### Technical

- Historienbasis vorbereitet (3.0)
- SQLite Datenbank erstellt

### Paused

- Decision History
- Analysefunktionen


---

## R9426 Nachsorge

## 2026-03-16 22:54:26 - R9426 - Nachsorge Clean Run

- Neuer unabhängiger Nachsorge-Runner erstellt
- Doku-Nachsorge für Stabilisierungslauf ergänzt
- Report-Generierung und Backup-Verhalten integriert
- optionale Compile-Prüfung zentraler Dateien durchgeführt

## R9425 Nachsorge (2026-03-17 14:28:31)

- Runner-Startpfad vereinheitlicht und gehärtet.
- Standard-GUI-Runner schreiben Output ins zentrale Display statt in Standard-Popups.
- Output-Marker ergänzt:
  - `RUNNER START: RXXXX`
  - `RUNNER END:   RXXXX (rc=...)`
- Protected Runner sind zentral abgesichert und in der GUI verdrahtet.
- `R9421` RunnerGuard, `R9423` SystemHealth und `R9424` RunnerFailureWatch sind angelegt und lauffähig.
- Purge-Standardpfad wurde auf den passenden Apply-Runner umgebogen; Schutzlogik bleibt aktiv.
- Offene Punkte:
  - Tk-`after`-Callbacks beim GUI-Destroy sauber aufräumen
  - R9424 Failure-Signal-Noise reduzieren
  - Intake Auto-Refresh gezielt gegenprüfen
