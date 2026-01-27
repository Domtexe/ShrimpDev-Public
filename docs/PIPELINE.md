<!-- PIPELINE_V1_START -->
# PIPELINE v1 — Lanes & Turnus (Source of Truth)


- [x] (DONE) Agent-Tab Empfehlungen stabilisiert: R2086 baseline/delta + R1802 Stamp (Agent_LastDiag.json) + robust anchors (R3837–R3844).
## Tech Debt / Hygiene

<!-- ACTIVE_TASK:START -->
- [ ] (LOW) Runner-WARN `venv python not found` / Template-Policy: WARN ist kosmetisch; Templates greifen nur bei Neugenerierung; optional später `REQUIRE_VENV`-Flag (WARN nur wenn explizit verlangt).
## ACTIVE_TASK
- id: P1-R2086-baseline-and-pipeline-active-flag
- since: 2026-01-26 08:41
- owner: Dom
- status: ACTIVE
- note: Baseline/Delta for R2086 + ACTIVE flag mechanism in pipeline
<!-- ACTIVE_TASK:END -->

<!-- LANE_OVERVIEW:CANONICAL -->
## 🧭 Pipeline-Lanes – Überblick (kanonisch)

| Lane | Zweck | Typische Tasks | Standard-Priorität |
|------|------|---------------|--------------------|
| **A** | Stabilität, Startfähigkeit, Crash/Import-Risiken, Safety | DIAG → APPLY, Guarding, Smoke-Tests | **P0/P1** |
| **B** | Core-Funktionalität ShrimpDev/ShrimpHub (UI/Features) | APPLY (modular), kleine Verbesserungen | **P1/P2** |
| **C** | Tooling & Automationen (Build/Patch/Push/Scans) | DIAG/APPLY, Hygiene, Automatisierung | **P1/P2** |
| **D** | Regeln, Doku, Governance, Konsistenz | DOCS-only, Pipeline-Schärfung | **P1/P2** |
| **E** | Websites/SEO/Monetarisierung (Shirimpi) | Ideen → Plan → Umsetzung | **P2/P3** |

**Turnus (Rotation):** A → B → C → D → E → repeat  
**Hard-Override:** Wenn in **Lane A** ein **P0** existiert, hat das Vorrang vor Rotation.  
**Arbeitsmodus:** *Diagnose zuerst*, dann **minimal-invasiver Fix**, immer mit Backup + Report.

---

## Lane A — Stabilität & Core
<!-- R3512_LANE_A_P0_START -->
**R3512 NOTE – Lane A P0 Clarification (post-phantom cleanup):**
- Only items that **block app start** or **cause crashes in default flows** remain P0.
- Historical/architectural items or feature hardening belong to P1/P2.
- Each remaining P0 must state a *crash/start symptom* and a *clear DoD*.

**Action:** Review the following Lane-A items and downgrade any that do not meet P0 criteria.

<!-- R3512_LANE_A_P0_END -->

<!-- R3511_NOTE_START -->

**R3511 NOTE (verified by R3510 recursive scan):**
- `R2374 / R2375 / R2377 / R2378` are **referenced historically** (docs/pipeline), but **no active runner files** were found in the repo scan.
- `R2379` exists as tools runner files, but other references are largely docs/reports.
- Treat these as **ARCH/HISTORICAL** unless we explicitly *materialize* missing runners.
- Rule: *Pipeline items with missing runner artifacts must be tagged as Phantom/Archived until materialized.*

<!-- R3511_NOTE_END -->

- [x] (P0) [CORE] (HIGHEST / BLOCKER) **R2372 – Architektur: INI Single Writer (Design + API)** (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2370.py:L122)

  - [x] (DONE) APPLY: module_docking cfg.write(f) -> ini_writer.write() (R3354)
    - report: Report_R3354_20260112_145514.md | pipeline mark: R3355 | 2026-01-12 15:02


  - [x] (DONE) APPLY: Fix: Runner-ID mismatch (py = cmd-1) (R3351)
    - report: Report_R3351_*.md | pipeline mark: R3352 | 2026-01-12 14:39


  - [x] (DONE) APPLY: config_loader INI writes -> ini_writer.write() (R3349)
    - report: Report_R3349_*.md | pipeline mark: R3350 | 2026-01-12 14:26

  - [x] (DONE) DIAG: INI write offenders scan (R3347) → Report_R3347_20260112_125757.md
  - [x] (DONE) Docs: Runner Architecture – Lessons Learned (R3346)
    - Pipeline-Markierung via R3348
    - gesetzt am 2026-01-12 14:14

- [x] (P0) [CORE] (HIGHEST / BLOCKER) **R2376 – Docking über Single Writer** (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2370.py:L141) — DONE (verified 2026-01-12 via R3378/R3379)
- [x] (P0) [CORE] **main_gui.py Stabilität: Silent-Exceptions sichtbar gemacht** (R3333; DIAG: R3331/R3332)
- [x] (P1) [CORE] **INI Redirect Logging Noise gedrosselt (Callsite-Gating)** (R3334)

<!-- R3316_PIPELINE_DOCKING_TASKS_INSERT -->
- [x] (P1) [CORE] Docking: **Konsolidierung der Undock-Overrides** (R3302–R3315) in eine kanonische Implementierung — DONE (verified) (Report_R3397_20260112_224300.md) (Report_R3398_20260112_225641.md)
- [x] (P1) [CORE] Docking: **Verify-Runner** für Undock/Restore/UI-Integration (inkl. Log-Tab Button-Row)
<!-- /R3316_PIPELINE_DOCKING_TASKS_INSERT -->


**Ziel:** Alle Themen (ShrimpDev/ShrimpHub/Website/Doku/Tooling) gleichmäßig voranbringen — ohne Chaos.  
**Regel:** Start-/Crash-Stabilität schlägt alles.

## Lanes (Themenbahnen)
- **Lane A — Stabilität / Crash / Startfähigkeit (P0/P1)**
- **Lane B — Core Features (P1/P2)**
- **Lane C — Tooling / Automationen (P1/P2)**
- **Lane D — Doku / Regeln / Konsistenz (P1/P2)**

<!-- R3569_LANE_D_GOV_TASKS_BEGIN -->
### Lane D — Governance-Schärfung (Docs-only)

<!-- PIPELINE_LANE_D_BEGIN -->
- [ ] (P1) **Report-Agent: Reports-Auswertung → Todos ableiten → priorisieren → Pipeline-Einsortierung (MVP DIAG, optional APPLY)**  <!-- TASK_REPORT_AGENT__R3755_NACHSORGE_RUNNER_PROTECT -->  - **Quelle/Referenz:** R3755 (Agent-Report), R3753 (Output-Guard), Nachsorge-Regeln (MR-NG*)  - **MVP (DIAG / read-only):**
    - [ ] `Reports/` scannen (z. B. letzte 30)
    - [ ] FAIL/WARN/ExitCodes + Keywords clustern (Dedup)
    - [ ] Priorität P0–P2 vergeben
    - [ ] Empfehlung: Lane/Phase + nächster Runner-Typ (DIAG/APPLY)
    - [ ] Ergebnis als Agent-Report schreiben (kein Auto-Schreiben in PIPELINE)
  - **Optional (kontrolliert, APPLY):**
    - [ ] „Übernimm Todo #X“ schreibt **genau einen** Pipeline-Eintrag (dedupe-sicher, Token Pflicht)
  - **Nachsorge-Plus: Runner-Schutz und modulare Ablösung**
    - [ ] Runner, die künftig wieder genutzt werden, müssen **protected/whitelisted** werden
    - [ ] Wenn Funktion ersetzt wird: **modularer Ersatz**, Alt-Runner erst nach Stabilitätsnachweis aus der kritischen Nutzung nehmen

- [ ] (P1) **Governance-Schärfung (R3568/R3569):** Pipeline-SSOT, Diagnose-first (Enforcement), Runner Scope-Lock, Definition of Done, Stop-Kriterien
  - **DoD**
    - [ ] MR-Block vorhanden (R3568) ✅
    - [ ] Pipeline-Tasks vorhanden (R3569)
    - [ ] Architektur-Prinzipien ergänzt (R3569)
    - [ ] Report vorhanden (R3568 + R3569)

- [ ] (P2) **Public/Private Repo Audit-Rhythmus** definieren (z. B. alle 10 Runner oder wöchentlich): „was darf public / was nie“
- [ ] (P2) **Decision-/Rejected-Ideas-Log** minimal pflegen (1 Satz „warum nicht“ statt Vergessen)
<!-- R3569_LANE_D_GOV_TASKS_END -->

- **Lane E — Website / SEO-Netzwerk (P2/P3)**

## Turnus
1. **Hard Override:** Wenn es **P0 in Lane A** gibt → **immer zuerst**.
2. Sonst rotieren wir: **A → B → C → D → E → (repeat)**.
3. Pro Session: **1 Anchor-Task** aus der aktuellen Lane (optional Kleinkram max. 20%).

## Arbeitskonvention (kurz)
- Tasks sind pro Lane gruppiert.
- Jede Änderung an Pipeline: **Backup + Report**.
<!-- PIPELINE_V1_END -->

---

## P0 – ui_toolbar.py entschärfen (Modularisierung + Stabilitäts-Guards)

**Priorität:** P0 / superurgent  
**Problem:** `modules/ui_toolbar.py` ist import-kritisch und fragil (Indent/Scope/NameError). Kleine Änderungen können den App-Start crashen.  
**Ziel:** Startstabilität absichern + Risiko modular reduzieren, ohne Vollrewrite.

**Definition of Done**
- `ui_toolbar.py` wird deutlich dünner (Orchestrator)
- Repo/Registry/Action-Routing in eigene Module ausgelagert (testbar)
- Push/Purge bleiben funktional (keine Verluste)
- Smoke-Test/Import-Check Runner vorhanden

**Umsetzungsplan (MR: mehrere kleine Runner)**
<!-- R3382_UI_TOOLBAR_SUBTASKS_BEGIN -->

**Unterpunkte (geordnet, verifizierbar – kein Chaos)**
- **P0.A Runner-Execution isolieren**: Threading/Subprocess aus `ui_toolbar.py` hinter eine klare API; UI ruft nur noch Orchestrator auf. — DONE (verified) (Report_R3402_20260112_233849.md) (Report_R3403_20260112_234334.md)
  - DoD: keine Runner-Startlogik direkt im UI; 1 definierte `run_runner(...)`-Entry; UI bleibt responsiv.
- **P0.B Smoke/Crash-Schutz**: Read-only Smoke-Runner vor APPLY-Stufen (Import + minimaler Toolbar-Aufbau wenn möglich). — DONE (verified via R3390 on 2026-01-12) (Verification: Report_R3390_20260112_210110.md)
- **P0.C Central Dispatch Entry-Point**: toolbar actions laufen über `_dispatch_action(...)` (minimaler Router-Einstieg, keine Behavior-Änderung). (Verification: Report_R3409_20260113_095743.md) — DONE (verified 2026-01-13)
  - DoD: Smoke grün nach jedem APPLY; Report + Exitcodes.
- **P1.A Popup/Report-Handling konsolidieren**: ein kanonischer Pfad für Report-Anzeige (Push/Purge gemäß Standard). — DONE (verified) (Report_R3393_20260112_221547.md) (Report_R3394_20260112_222242.md)
  - DoD: keine doppelten Popup-Overlays; konsistentes Verhalten.
- **P1.B Import-Hygiene/Verantwortlichkeiten**: redundante/verteile Imports reduzieren (nur minimal, ohne Semantikänderung).
  - DoD: Top-level Imports sauber; keine überraschenden Side-Effects.
- **P2 Nested-def Reduktion (nur wo nötig)**: kritische nested Worker/Callbacks testbarer machen (ohne Vollrewrite).
  - DoD: weniger Tiefe im Runner-Cluster; Verhalten unverändert.

<!-- R3382_UI_TOOLBAR_SUBTASKS_END -->

1. **READ-ONLY Toolbar Map Report**
   - listet Funktionen, nested helper, after()-ticks, referenced actions, risk lines
2. **Extract repo/registry helpers** → `modules/toolbar_helpers_repo.py`
   - `read_registry_path()`, `is_git_repo()`, `repo_pushable()`
3. **Extract action router** → `modules/toolbar_action_router.py`
   - `call_action(app, name)` robust + logging
4. **Extract Push/Purge section** → `modules/toolbar_sections/section_push_purge.py`
   - Builder-Funktion, reduziert nested closures im Hauptfile
5. **ui_toolbar.py cleanup**
   - nur Orchestrator-Aufrufe, keine Logikvermischung
6. **Smoke-Test Runner**
   - `python -c "import modules.ui_toolbar"` (und optional GUI-smoke, wenn vorhanden)

**Risiko/Schutz**
- Jede Stufe: Backup + Report
- Keine Voll-Rewrites, keine radikalen Strukturänderungen
- Wenn Fix nicht direkt verifiziert: Diagnose zuerst (MR)

<!-- SHRIMPDEV_POLICY_REPO_LAYERS -->

### UI / Runner-Popup – Report-Link + Copy-to-Clipboard (NEW)

- **Goal:** Wenn Runner einen Report erzeugen, soll der Report im Runner-Popup direkt nutzbar sein.
- **Why:** Spart Zeit, verhindert „Report suchen“ und erleichtert Debug/Sharing.

**Acceptance Criteria**
- Parser erkennt Report-Pfade in Runner-Output, z. B. `Report:` / `OK: Report:` (absolute Pfade).
- Runner-Popup zeigt:
  - **Open Report** (klickbarer Link, öffnet Datei via Default-App)
  - **Copy Report** (kopiert den vollständigen Report-Text in die Zwischenablage)
- Wenn kein Report gefunden: UI-Elemente deaktiviert/ausgeblendet.
- Robust: keine Crashes bei leerem Output, Sonderzeichen, CRLF/LF.

**Implementation Notes**
- In `modules/module_runner_popup.py`:
  - stdout/stderr nach bekannten Mustern scannen (Regex).
  - Pfad normalisieren (Windows).
  - Open: `os.startfile(path)` (Windows) / fallback.
  - Copy: Tk clipboard (`root.clipboard_clear(); root.clipboard_append(path)`).

**Priority**
- P2 (UX/Workflow), nach Stabilität/CI-Blockern.

## Policy: Repo-Layers (Production vs Archive) & CI Scope

**New insight (R2652/R2653):** Dieses Repo enthält bewusst mehrere Schichten.

- **Production layer (must be syntactically clean):** `modules/**`, `main_gui.py` (und nur ausdrücklich freigegebene Prod-Tools)
- **Archive/Legacy layer (may be broken):** `_OldStuff/**`, `_Trash/**`, `tools/Archiv/**`, historische Runner/Friedhof

**Rule:** CI-/Syntax-Gates (compileall, Ruff E9) dürfen **nur** auf dem Production-Layer laufen.

**Reason:** Archive/Legacy enthält absichtlich kaputte/inkompatible Dateien (Syntax/Encoding/Indent), die nicht als Blocker gelten.

**Implementation standard:**

```text
python -m compileall -q main_gui.py modules
ruff check modules main_gui.py --select E9
```

**Exclude standard (lint/ci):** `_OldStuff/**`, `_Trash/**`, `tools/Archiv/**`, `modules/snippets/**`, Outputs (`Reports/**`, `_Archiv/**`, `_Exports/**`).



<!-- SHRIMPDEV_POLICY_CI_WORKFLOW_YAML -->
## Policy: CI-Workflow zuerst auf YAML-Validität prüfen

**Rule:** Wenn GitHub Actions **„Invalid workflow file“** oder **„You have an error in your yaml syntax“** meldet, wird **immer zuerst** die YAML-Struktur geprüft (Indentation/Mapping), bevor Tooling (ruff/compileall/etc.) debuggt wird.

**Reason:** Bei YAML-Parsefehlern werden **keine Steps** ausgeführt – Tool-Logs sind dann irrelevant.

**Quick checklist:**
- `jobs:` → darunter müssen Job-IDs **eingerückt** sein (z. B. `  lint:`)
- `runs-on:` / `steps:` sind **unter dem Job** eingerückt
- Step-Listenpunkte beginnen mit `-` und sind korrekt eingerückt

<!-- SHRIMPDEV_PIPELINE_TASKS_BLOCK -->
## Pipeline Tasks


<!-- SHRIMPDEV_PIPELINE_IMPORTED_TASKS_START -->
### Imported Tasks (auto)

> Auto-importiert (Extended Scan: inkl. Markdown TODOs + Legacy). Bitte später konsolidieren.

- [ ] (P0) [CORE] (HIGHEST / BLOCKER) **Central Runner-Executor API (App ↔ logic_actions)** — UI-Actions dürfen keine Runner-IDs kennen; 1 kanonischer Executor + Smoke-Test
- [ ] (P0) [CORE] NOTE: that CI blockers were fixed via R2576. _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2576.py:L103)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L18)- [ ] (P0) (HIGHEST / BLOCKER) **R2373 – Implementierung: zentraler INI-Writer (Merge + atomic)** (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/INI_WriteMap.md:L14478)- [ ] (P0) (HIGHEST / BLOCKER) **R2371 – INI-WriteMap (READ-ONLY Diagnose)** (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2370.py:L117)
- [ ] (P0) [CORE] (HIGHEST / BLOCKER) **R2374 – config_manager Save konsolidieren** (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2370.py:L133)
- [ ] (P0) [CORE] (HIGHEST / BLOCKER) **R2375 – Shims: config_loader.py / config_mgr.py** (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2370.py:L137)
- [ ] (P0) [CORE] (HIGHEST / BLOCKER) **R2377 – Monkeypatch/Altlogik Quarantäne** (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2370.py:L148)
- [ ] (P0) [CORE] (HIGHEST / BLOCKER) **R2378 – Restore Reihenfolge finalisieren** (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2370.py:L152)
- [ ] (P0) [CORE] (HIGHEST / BLOCKER) **R2379 – Regression-Testplan** (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2370.py:L156)
- [ ] (P1) [CORE] **Prüfen/Plan: modules/ui_toolbar.py modularisieren** (Import-kritisch) — Ziel: kleine Module (builders/actions/hooks), weniger Seiteneffekte, bessere Testbarkeit
- [ ] (P1) [PROD] TODO: \n- File: `{pipeline}`\n- Backup: `{backup}`\n", _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/_Archiv/Runner_Staging_2025-12-25/R2598.py:L59)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L24)
- [ ] (P1) [CORE] NOTE: Did not match expected 'run: uvx ruff ...' lines. Please verify ci.yml manually.", _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2580.py:L109)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L25)
- [ ] (P1) [PROD] TODO: ][HIGH] Runner-Cleanup – Archivierung unbenutzter Runner _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/_Pipeline/Pipeline_R2016_RunnerCleanup_20251208_154653.txt:L1)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L27)
- [ ] (P1) [CORE] (P1) ... (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/ARCHITECTURE.md:L176)
- [ ] (P1) [CORE] TODO: -Pipeline: eigener GUI-Tab MasterRules (Viewer + Open/Refresh). (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Pipeline_Notes.md:L29)
- [ ] (P1) [CORE] TODO: (Pipeline), sondern bekommen einen eigenen Tab.` (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L19929)
- [x] (P1) [CORE] TODO: -Pipeline: eigener GUI-Tab MasterRules (Viewer + Open/Refresh).\n"` (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L19950)- [ ] (P1) [CORE] TODO: ) Pipeline-Eintrag: Tracebacks wieder ins Log (HIGH)` (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L19967)
- [ ] (P1) [CORE] TODO: in der Pipeline-Datei.` (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L7958)
- [ ] (P1) [CORE] TODO: in docs/Master/Pipeline_Notes.md eintragen:` (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L8944)
- [ ] (P1) [CORE] TODO: (Pipeline), sondern bekommen einen eigenen Tab. (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2143.py:L2)
- [ ] (P1) [CORE] TODO: -Pipeline: eigener GUI-Tab MasterRules (Viewer + Open/Refresh).\n" (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2143.py:L250)
- [ ] (P1) [CORE] TODO: ) Pipeline-Eintrag: Tracebacks wieder ins Log (HIGH) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2144.py:L9)
- [ ] (P1) [CORE] NOTE: for Docking incident and doc links (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2397.py:L2)
- [ ] (P1) [PROD] `docs/Architecture_ProjectTab.md` – **Datenquellen/Contract** (nur lesen: PIPELINE, Reports, SmokeTest) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2521.py:L76)
- [ ] (P2) [PROD] **Incremental Refactor Plan**: Schrittfolge ohne Vollrewrite (1 Modul pro Runner, jeweils compile+smoke) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2519.py:L94)
- [ ] (P3) [PROD] TODO: (reports/ordner konsolidieren) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2596_20251225_111324.md:L4)
- [ ] (P3) [PROD] TODO: `: `False` (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2655_20251225_200722.md:L84)
- [ ] (P3) [PROD] TODO: (reports/ordner konsolidieren)\n" _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/_Archiv/Runner_Staging_2025-12-25/R2596.py:L93)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L28)
- NOTE: (P3) NOTE: readline can block if no output; so we guard by checking rc or waiting small. _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/_Archiv/Runner_Staging_2025-12-25/R2609.py:L70)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L29)
- NOTE: (P3) NOTE: ") _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/modules/ui_lists.py:L7)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L30)
- [x] (P3) [PROD] NOTE: btn_apply pack line not found (maybe already adjusted).") _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2448.py:L138)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L31) (auto-closed R2854: obsolete)
- [x] (P3) [PROD] NOTE: btn_scan pack line not found (maybe already adjusted).") _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2448.py:L148)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L32) (auto-closed R2854: obsolete)
- NOTE: (P3) NOTE: `{pub}` not found.\n", _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2555.py:L26)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L33)
- NOTE: (P3) NOTE: that these were fixed via runner) _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2576.cmd:L9)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L34)
- [x] (P3) [PROD] NOTE: {'patched' if c4 else 'no-op'}") _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2576.py:L184)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L35) (auto-closed R2854: obsolete)
- [x] (P3) [PROD] NOTE: {'patched' if c3 else 'no-op'}") _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2577.py:L174)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L36) (auto-closed R2854: obsolete)
- NOTE: (P3) NOTE: = ( _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2638.py:L203)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L37)
- NOTE: (P3) NOTE: + "\n") _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2638.py:L212)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L38)
- NOTE: (P3) NOTE: (policy visibility) _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2638.py:L231)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L39)
- [ ] (P3) [PROD] TODO: ", _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2655.py:L129)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L40)
- [ ] (P3) [PROD] TODO: /FIXME in code) _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2658.cmd:L5)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L41)
- [ ] (P3) [STRAT] TODO: markers _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2658.py:L107)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L42)
- [ ] (P3) [PROD] TODO: |FIXME|HACK|NOTE)\b[:]?\s*(?P<text>.*)$', re.IGNORECASE) _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2658.py:L26)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L43)
- [ ] (P3) [STRAT] TODO: /FIXME/HACK/NOTE markers in *.py/*.cmd/*.bat/*.ps1/*.yml/*.toml _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2658.py:L8)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L44)
- [ ] (P3) [STRAT] TODO: /FIXME Marker). Bitte bei Bedarf konsolidieren.\n\n") _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2659.py:L108)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L45)
- [ ] (P3) [CORE] TODO: Flag/Policy). (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Architecture_DnD_FileOut.md:L21)
- NOTE: (P3) NOTE: `[Docking]` intentionally excluded from updates (preserved by ini_writer default). (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2382_SingleWriter_Delegation_20251219_101450.md:L7)
- NOTE: (P3) NOTE: ] {n}")` (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L11590)
- [ ] (P3) [CORE] TODO: implement logic here` (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L15280)
- NOTE: (P3) NOTE: ` (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L19697)
- [ ] (P3) [CORE] TODO: list: add a high-priority item about tracebacks in log.` (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L19969)
- NOTE: (P3) NOTE: = "Runner-Logs MUESSEN in debug_output.txt landen"` (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L21653)
- NOTE: (P3) NOTE: Wir ersetzen NUR run_runner_with_popup bis EOF. Helpers bleiben unberührt.` (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L22290)
- [ ] (P3) [CORE] TODO: ` (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L7989)
- [ ] (P3) [CORE] TODO: bereits vorhanden – uebersprungen.\n")` (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L8918)
- [ ] (P3) [CORE] TODO: hinzugefuegt.\n")` (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L8921)
- NOTE: (P3) NOTE: patched restore_from_ini loop (open flag + geometry preferred) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2395_Docking_RestoreOpenGeo_20251219_223827.md:L14)
- [x] (P3) [PROD] NOTE: Root tools_keep.txt exists but is obsolete. Canonical file is registry/tools_keep.txt (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2416_RegistryAndDocsFix_20251221_105138.md:L9) (auto-closed R2854: obsolete)
- NOTE: (P3) NOTE: This runner made **no changes**. It only reports. (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2450_UI_ToolbarState_20251221_215319.md:L208)
- [ ] (P3) [CORE] HACK: für on_sort (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R1301_IntakeV1_Install.py:L353)
- [ ] (P3) [CORE] TODO: actual UI factory if separate exists\n" (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R1305_IntakeHardFix.py:L70)
- NOTE: (P3) NOTE: str) -> None: (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2137.py:L31)
- NOTE: (P3) NOTE: }\n" (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2137.py:L37)
- [ ] (P3) [CORE] TODO: list: add a high-priority item about tracebacks in log. (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2144.py:L118)
- NOTE: (P3) NOTE: later in report (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2183.py:L118)
- NOTE: (P3) NOTE: = "Runner-Logs MUESSEN in debug_output.txt landen" (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2239.py:L124)
- NOTE: (P3) NOTE: not in mr: (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2239.py:L125)
- NOTE: (P3) NOTE: Wir ersetzen NUR run_runner_with_popup bis EOF. Helpers bleiben unberührt. (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2284.py:L52)
- [ ] (P3) [CORE] (TOP/HIGH) Phase 2: Restore-Orchestrierung (pro Fenster-Key) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2375.py:L66)
- [ ] (P3) [CORE] (HIGH) Migration: Remaining Writers -> SingleWriter (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2375.py:L79)
- [ ] (P3) [PROD] (MED) Defactoring / Archivierung (nach erfolgreicher Umstellung) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2375.py:L83)
- NOTE: (P3) NOTE: `[Docking]` intentionally excluded from updates (preserved by ini_writer default).", (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2382.py:L204)
- NOTE: (P3) NOTE: If file has multiple Toplevel creations, we patch the one inside build_runner_products_tab only. (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2393.py:L58)
- NOTE: (P3) NOTE: = _patch_restore_from_ini(src) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2395.py:L165)
- NOTE: (P3) NOTE: {note}") (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2395.py:L169)
- [x] (P3) [CORE] NOTE: Root tools_keep.txt exists but is obsolete. " (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2416.py:L125) (auto-closed R2854: obsolete)
- NOTE: (P3) NOTE: target did not exist before restore", (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2432.py:L67)
- NOTE: (P3) NOTE: This runner made **no changes**. It only reports.\n") (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2450.py:L185)
- NOTE: (P3) NOTE: ", "- Dieser Report ist Grundlage für den minimalen Patch-Runner (R2463)."] (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2462.py:L123)
- NOTE: (P3) NOTE: exists (minimal) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2470.py:L70)
- NOTE: (P3) NOTE: = patch_guard_parent(code1) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/Runner_1132_FixGuardParent.py:L183)
- NOTE: (P3) NOTE: .strip()) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/Runner_1132_FixGuardParent.py:L193)
- NOTE: (P3) NOTE: ] {n}") (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/Runner_1137_IntakeLoadFix.py:L247)
- [ ] (P3) [CORE] TODO: (optional): hier später Reflow/Anordnung implementieren. (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/Runner_1171m_IntakeToolbarReflowFix.py:L47)
- [ ] (P3) [CORE] TODO: implement logic here (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/Runner_943_NewRunner.py:L49)
- [ ] (P3) [CORE] **Define Actions Registry (Docs)**: Liste der erlaubten Actions + Labels (Copy Path/File/Text, Open, Folder, Restore gated) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2519.py:L90)
- [ ] (P3) [CORE] **Define Gating Rules (Docs)**: wann ist Restore sichtbar? wann ist File-Copy erlaubt? (Backup/Archiv-Only, Busy-State) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2519.py:L91)
- [ ] (P3) [CORE] **Central Helpers Plan (Docs)**: gemeinsame Helper-Funktionen (clipboard, file-copy-paste, restore-safe) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2519.py:L92)
- [ ] (P3) [PROD] **Per-Tab Audit**: Artefakte (Tree/Preview), Intake, Runner Products etc. – Abweichungen dokumentieren (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2519.py:L93)
- [ ] (P3) [CORE] **Regression Checklist**: Rechtsklick links/rechts, Selection behavior, busy-state, messageboxes (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2519.py:L95)
- [ ] (P3) [CORE] `docs/Architecture_ProjectTab.md` – **Definition + Non-Goals** (keine Buttons, keine neue Logik) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2521.py:L75)
- [ ] (P3) [CORE] `docs/Architecture_ProjectTab.md` – **Minimaler Anzeige-Contract/Wireframe** (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2521.py:L77)
- [ ] (P3) [STRAT] TODO: markers (now also in .md) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2661.py:L218)
- [ ] (P3) [CORE] TODO: /FIXME/HACK/NOTE lines ALSO in Markdown (.md) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2661.py:L9)

<!-- SHRIMPDEV_PIPELINE_IMPORTED_TASKS_END -->


> **Hinweis:** Der Pipeline-Tab in ShrimpDev zeigt nur **Tasks** (z. B. `- [ ] …`).
> Policies/Regeln bleiben weiter oben im Dokument, aber ohne Tasks bleibt die GUI-Liste leer.

- [ ] (P1) [CORE] CI: Reports wieder als GitHub Actions Artefakte anzeigen (Runner R2656)
- [ ] (P1) [PROD] ShrimpDev: Artefakte-Tab prüfen/reaktivieren, falls Anzeige fehlt
- [ ] (P2) [CORE] LearningJournal Auto-Write: Diagnose + Guard (nach CI stabil)
- [x] (P0) [CORE] CI Syntax-Gate scoped + YAML valid (R2653/R2654)

## Autopush (Repo-only)
- Canonical autopush backend (OneDrive repo-only): `tools/R2691` (Private), `tools/R2692` (Public), `tools/R2693` (Both).
- Deprecated: `R2692/R2691` legacy autopush runners (workspace-bound). Do not wire GUI buttons to them.
- Autopush reports are generated locally under `Reports/` and are not versioned in git.
- [P1] Autopush repo-only finalized: GUI uses R2691/R2692/R2693; legacy R2692/R2691 deprecated; gitignore ignores only Report_R269{1..3}_*.md.

---

## P3-Workspace-Deaktivieren-RepoRoots-Explizit

**Priority:** P3  
**Status:** Planned  
**Scope:** ShrimpDev (Private/Public Root Handling), UI Push Buttons, CI Hygiene

### Goal
Workspace ist ein Alt-Relikt und soll **deaktiviert** bleiben. Stattdessen werden Repo-Roots **explizit** geführt:
- Private Repo Root: per UI „…“-Button auswählbar, in INI gespeichert
- Public Root: automatisch ableitbar (z. B. `ShrimpDev_REPO` → `ShrimpDev_PUBLIC_EXPORT`), optional autocreate des Ordners
- Keine Heuristik über `cwd`, keine „guess roots“

### Tasks
- [ ] Workspace als Root-Quelle deaktivieren (UI/Logic dürfen `workspace_root` nicht mehr als Default verwenden)
- [ ] INI: `[Repo] private_root`, `[Repo] public_root`, `[Repo] public_autocreate`
- [ ] UI: „…“ Button zum Setzen von `private_root`
- [ ] Public Root ableiten; Ordner bei Bedarf anlegen; **kein erzwungenes `git init`**
- [ ] Audit: alle Code-Stellen, die `workspace_*` referenzieren → entfernen/migrieren
- [ ] Dokumentation: Architektur + MasterRules + Pipeline referenzieren

### Rationale
Verhindert Root-Fehlermatches (OneDrive/Startpfad), macht Push-Buttons deterministisch und reduziert CI/Repo-Chaos.

---


## R2854 Summary (auto)
- Date: 2025-12-28 23:08:17
- P3 items scanned: 69
- P3 NOTE converted to non-tasks: 31
- P3 OBSOLETE auto-closed: 6

<!-- SHRIMPDEV_PIPELINE_FSTRING_GUARD -->
(P1) TODO: (CI/Guard) Introduce/keep Lint-Guard for f-string unknown identifiers (Runner R2867) and run it before Push.
(P1) TODO: (UI) Add a toolbar button “Lint Guard (R2867)” near Push/Purge diagnostics; on click run R2867 and show latest report via popup helper.
(P1) TODO: (Docs) Canonical paths reminder: MasterRules live in docs/Master/*.md; pipeline is docs/PIPELINE.md. All doc-updates must target canonical files (no root MasterRules.md).


## Policy Updates



<!-- R3563_FOCUS_POLICY_BEGIN -->
### Fokus-Leitplanke: Basis vor Produkt (Thread-Entscheidung)

- **Priorität:** ShrimpDev-Stabilität + Reproduzierbarkeit + Doku gehen vor Monetarisierung.
- **Regel:** Solange relevante P0/P1 (Lane A/B) offen sind, werden keine neuen Produkte/Repros gestartet.
- **Ideen dürfen existieren**, aber nur als Doku/Parking (keine Umsetzung außerhalb der Pipeline).
- **Verankerung:** siehe `MR-STRAT-FOCUS-01` in `docs/MasterRules.md`.
<!-- R3563_FOCUS_POLICY_END -->

### Public Repo Contract (export policy)

- The public repo is **not a mirror**. It is a curated export.
- Export must be **allowlist-based** (explicit include patterns).
- Forbidden in public: backups, reports, debug captures, registry/state, internal pipeline, internal master rules, internal journals.
- Export must write/update `docs/Public_Contract.md` in the public repo.
- Any policy breach triggers a repair runner that sanitizes the public repo.

### P2 – Log-Tab: Suche im Log
- **Feature:** Suchfeld im Log-Tab, das das Log (Textwidget) live/auf Enter durchsucht.
- **UX:** Treffer markieren + Next/Prev (F3 / Shift+F3), optional Case-Sensitive Toggle.
- **Tech:** keine Blockade im UI-Thread bei sehr großem Log (chunked search / after()).
- **Status:** neu (eingesortiert durch R2988 am 2026-01-03T23:30:09).

### P2 – UI: Searchfield Clear-Button (✕)
- **Feature:** In Suchfeldern rechtsbündig ein ✕ zum **Clear/Stop**.
- **UX:** ✕ nur sichtbar wenn Text ≠ leer; Klick leert Feld + setzt Ergebnis/Filter zurück; Fokus bleibt im Feld.
- **Shortcuts:** `Esc` triggert denselben Clear/Stop; optional Tooltip “Clear”.
- **Scope:** Log-Tab (Suche), Pipeline-Tab, weitere Filterfelder nach Bedarf.
- **Status:** neu (eingesortiert durch R3019 am 2026-01-04T16:52:58).


### P2 – LearningEngine Phase D: Runner-Vorschläge aus LearningJournal (read-only)
- **Ziel:** Aus LJ/Logs/Reports **Vorschläge** ableiten (Cluster/Häufigkeit/Impact), **ohne** Auto-Fix.
- **Output:** Vorschlagsliste als Report/JSON (z. B. `Reports/LearningEngine/Suggestions_*.json`) + kurzer Markdown-Report.
- **Verwandtschaft:** **Agent-Tab** konsumiert diese Vorschläge (anzeigen, filtern, erklären) und führt Runner **nur opt-in** aus.
- **Sicherheit:** Allowlist + Dry-Run/Preview; niemals destructive Runner ohne explizite Bestätigung.
- **Status:** neu (eingesortiert durch R3586 am 2026-01-18T23:50:22).

### P2 – Agent-Tab: empfohlene Runner automatisch ausführen (prüfen)
- **Idee:** Agent-Tab, der auf Basis von Zustand/Logs/Reports Runner **vorschlägt**.
- **Option:** *Auto-Execute* nur **opt-in**.
- **Sicherheit:** Allowlist erlaubter Runner + **Dry-Run/Preview** + Abbruch/Undo.
- **Regeln:** niemals destructive Runner ohne explizite Bestätigung; keine Background-Exec.
- **Status:** neu (eingesortiert durch R2999 am 2026-01-04T00:24:52).



---
### Inbox (auto-added 2026-01-04 17:53)
- **Log-Tab Suche:** Suchfeld im Log-Tab, das das Log (Text) durchsucht.
- **Search-Clear-X:** In Suchfeldern rechtsbündig ein **X** zum Beenden/Leeren der Suche.
- **Agent-Tab:** Empfohlene Runner automatisch vorschlagen und optional (bewusst) ausführen lassen; Sinn/Nutzen prüfen.

## Resolved: Docking Double Tabs
_added 2026-01-08 12:26 via R3147_

- Docking incident resolved (legacy INI state).
- No further action required.
- Area marked as stable.

## P1 – [STRAT] Website / SEO Portfolio

- [ ] (P1) [STRAT] Website-Portfolio: Scope definieren (viele kleine Sites, kein Monolith)
- [ ] (P1) [STRAT] Website-Portfolio: Domain-Strategie festlegen (1 Domain pro Nische)
- [ ] (P1) [STRAT] Website-Portfolio: Erfolgskriterien Phase 1 definieren (Indexierung/Impressions)
- [ ] (P1) [STRAT] Website: Ideenliste mit 20–30 konkreten Produkt-/Problem-Nischen erstellen
- [ ] (P1) [STRAT] Website: Suchlücken-Check (Suchintention + Konkurrenz grob bewerten)
- [ ] (P1) [STRAT] Website: Priorisierungsmatrix definieren (Volumen × Konkurrenz × Monetarisierung)
- [ ] (P1) [STRAT] Website: 1 MVP-Nische final auswählen und begründen

## P2 – [STRAT] Website MVP

- [ ] (P2) [STRAT] Website-MVP: Tech-Setup festlegen (Static/CMS/Hybrid – bewusst simpel)
- [ ] (P2) [STRAT] Website-MVP: Minimale Seitenstruktur definieren (Start + 1–3 Kernseiten)
- [ ] (P2) [STRAT] Website-MVP: SEO-Basics als Checkliste dokumentieren (URLs, H1/H2, interne Links)

## P3 – [STRAT] Website Beobachtung

- [ ] (P3) [STRAT] Website-MVP: Indexierung & Impressions beobachten (Search Console)
- [ ] (P3) [STRAT] Website-MVP: Entscheidung dokumentieren (skalieren oder verwerfen)

<!-- PIPELINE_LANE_D_END -->
## Lane E — Website / SEO-Netzwerk (P2/P3)


**Lane-E Contract (Isolation / Artefakte):**
- **Isolation:** keine Abhängigkeit zu ShrimpDev-Core-State (kein Zugriff auf `ShrimpDev.ini`, Docking/UI-State, Runner-Registry).
- **Erlaubt:** gemeinsame Tooling-Runner (Scanner/Generator/Reports) **ohne** Shared State.
- **Artefakte:** jede Site lebt unter `docs/websites/<site>/...` (Decision, MVP, KPIs, Kill/Scale).
- **Kill/Scale Kriterien:** müssen pro Site schriftlich definiert sein (kein "wird schon").

**Ziel:** Systematisches Portfolio aus Nischenwebsites (SEO-getrieben), monetarisierbar via Affiliate/Ads/Lead.  
**Strategie:** Weg von gesättigten Märkten (z. B. Sneaker) → hin zu klaren Nischen mit echter Suchintention.  
**Prinzip:** Produkte/Probleme statt breite Kategorien; Portfolio-Denken (viele kleine Sites).

### P2 — Setup & Entscheidungsgrundlagen
- [ ] (P2) **WE-01: Marken-/Domain-Strategie festlegen** (eine Marke vs. viele; Namenssystem)
- [ ] (P2) **WE-02: Technik-Stack festlegen** (Static/Hybrid/CMS; Generierungs-Workflow)
- [ ] (P2) **WE-03: Nischen-Funnel definieren** (Idee → Validierung → Content-Cluster → Launch)
- [ ] (P2) **WE-04: “Suchlücken”-Validierungscheckliste** (Suchintention, Konkurrenz, Monetarisierung, Aufwand)

### P2 — Erste Umsetzung (minimal, realistisch)
- [ ] (P2) **WE-10: 10 Nischenideen sammeln** (kurz, messbar)
- [ ] (P2) **WE-11: Top 3 Nischen validieren** (SERP-Check, Konkurrenz grob, Monetarisierungsweg)
- [ ] (P2) **WE-12: Erste Site auswählen + Scope 1** (Start: 1 Thema, 1 Struktur)
- [ ] (P2) **WE-13: Content-Cluster Plan** (Pillar + 10 Supporting Posts)
- [ ] (P2) **WE-14: Produktions-Template für Inhalte** (vergleichbar/entscheidungshilfe-orientiert)

### P3 — Skalierung (später)
- [ ] (P3) **WE-20: Multi-Site-Orchestrierung** (Vorlagen, Deployment, Tracking)
- [ ] (P3) **WE-21: KPI-Tracking** (Impressions/Clicks/CTR/Revenue; wöchentliche Review)

---

## BUG: Docking state not persisted -> undocked tabs not restored

### Symptom
- `ShrimpDev.ini` `[Docking]` bleibt unverändert trotz undocked Tabs / App close.
- Nach Neustart werden undocked Tabs nicht wiederhergestellt.

### Root Cause (IST)
- `modules/module_docking.py`: `DockManager.persist_all()` führt keinen finalen Write/Commit aus (Legacy/Fragment; kein zuverlässiger Save).
- `_persist_one()` enthält try/except-Leichen; Writer-Pfad nicht robust/diagnostizierbar.

### Plan
1) Architektur & Single-Writer verbindlich dokumentieren: `docs/Architecture/Current/Docking_Persist_Current.md`
2) Code fix: `persist_all()` + `_persist_one()` auf Single-Writer konsolidieren, minimalen Diagnosepfad ergänzen
3) Regression-Test: undock->close main->verify INI changed->restart->tabs restored

## Abgeschlossene Themen

### Docking / INI / Persistenz
- **Status:** Done / Parked
- **Abschluss:** 2026-01-11
- **Begründung:**
  - Canonical Docking-Core (_r3321_) aktiv
  - Single Writer etabliert
  - Diagnose (R3327) ergab: kein gefahrlos löschbarer Code
  - Weiterer Abbau = eigenes Refactoring-Projekt
- **Letzte Runner:** R3321–R3327, R3329

<!-- R3416 -->
### P1 · Docking

Status: DONE (core verified)

Der Docking-Core (Undock, Persist, Restore) ist stabilisiert und
durch Verify-Runner abgesichert.

Verifiziert:
- Undock / Redock: OK
- Persist (INI): OK
- Restore (Startup): OK
- Verify-Runner ohne Crash

#### P1.DOCKING.LOGTAB.BUTTON_ROW_DETECTION
Status: OPEN (non-blocking)

Der Finder `_r3315_find_log_button_row(...)` liefert aktuell None.
Dies erzeugt eine WARN-Meldung im Verify, jedoch keinen funktionalen Fehler.

Ursachenannahmen:
- Widget-Hierarchie
- ttk.Button vs. tk.Button
- abweichender Parent-Frame

Vorgehen:
- DIAG (read-only): Widget-Tree-Dump des Log-Tabs
- Danach: minimaler Finder-Fix

<!-- R3431 -->
### P1 · Docking – Verify FINAL

Status: VERIFIED (final)

Nach Abschluss der Fixes (Legacy-Aliases + Compile-Stabilität) läuft der
Docking-Verify Runner stabil und grün.

- Verify: R3413 Exit=0
- Referenz-Report: `Reports/Report_R3413_20260113_160946.md`

Hinweis:
Ältere Reports können noch historische FAILs enthalten (z. B. _r2339_ini_path),
sind aber durch den finalen Verify-Lauf überholt.

<!-- R3432 -->
### P1 · Docking (Parent)

Status: DONE (final, verified)

Alle Subtasks abgeschlossen:
- Verify FINAL dokumentiert (R3431)
- Verify-Lauf grün: R3413 (Exit 0)
- Referenz-Report: `Reports/Report_R3413_20260113_160946.md`

Damit ist der gesamte P1-Docking-Komplex formal abgeschlossen.
### Lane A / Stability
- [ ] INI redirects -> trend to zero (canonical path: `registry/ShrimpDev.ini`, remove hardcoded root INI reads/writes)

<!-- R3518_LANE_B_START -->

## Lane B

- **Lane B – DONE**  (Nachsorge & Hardening: R3770, R3772, R3773, R3774, R3775) — Hardening / Guardrails (post-P&P, post-R3510..R3517)


### P1 — Housekeeping-Konzept (Auto-Purge über Canonical Executor)
<!-- PURGE_ARCH_LINK:CANONICAL -->
- **ARCH:** Purge/Housekeeping Soll-Definition: `docs/ARCH_Purge.md`

- **Ziel**: Automatisches Housekeeping, insbesondere **Purge wieder vollautomatisch** (kein manueller R3106-Run).
- **Prinzip**: UI delegiert ausschließlich an `modules/toolbar_runner_exec.py` (Single Source of Truth).
- **Safety**: Guards/Confirm/Logging/Report-Popup (MR-konform, diagnose-first).
- **Aktion**: B2.1 Purge reaktivieren → Executor → R3106 (oder definierter Nachfolger).
- **Public GitHub Referenz**: https://github.com/Domtexe/ShrimpDev-Public

### B1 — Canonical Runner Executor API (Single Source of Truth)
- [ ] Define one canonical entrypoint (e.g. `runner_exec.run_by_id(app, "R####")` or `app.run_runner_by_id("R####")`)
- [ ] Replace any ad-hoc subprocess/runner wiring in UI code to call the executor only
- [ ] Executor responsibilities:
  - [ ] validate runner id format
  - [ ] resolve cmd path deterministically
  - [ ] run in a robust way (cwd/root consistent)
  - [ ] log report path and exit code (no Tk callback explosions)
- **DoD**
  - [ ] Push uses executor, Purge uses executor
  - [ ] No UI module calls subprocess directly
  - [ ] One place to change behavior (Single Source of Truth)

### B2 — ui_toolbar.py Modularisierung (UI-only)
- [ ] ui_toolbar becomes UI-only:
  - [ ] no INI writes
  - [ ] no runner wiring logic beyond calling logic_actions/executor
  - [ ] no duplicate button builders
- [ ] Extract pure helper pieces if needed (icons/layout/widgets) into small modules
- **DoD**
  - [ ] One Push button + one Purge button in code (no duplicates)
  - [ ] Buttons call logic_actions → executor
  - [ ] py_compile green

### B3 — Redirect/Config Hygiene (Signal stays meaningful)
- [x] Rotate/truncate INI redirect log (R3517) so warnings represent real deltas
- [ ] Add a short “when this warning appears” troubleshooting snippet (docs-only)
- **DoD**
  - [ ] Warning indicates NEW redirects, not historical noise

### B4 — MR Guardrails (anti-kaskade)
- [ ] Explicitly enforce: DIAG → one APPLY → stop; no “runner fixes runner fixes runner”
- [ ] Phantom runner references: must be tagged/archived until materialized (already started)
- **DoD**
  - [ ] Reduced repair cascades; fixes are measured & bounded

<!-- R3518_LANE_B_END -->

<!-- R3541 BEGIN: Housekeeping Follow-ups -->
## Lane B – Hardening: Housekeeping (Follow-ups)

**Done (Housekeeping Baseline):**
- Purge/Housekeeping ist produktiv: räumt real auf (Archiv statt Delete), Relevanz-Policy aktiv (`tools/` zählt nicht als runtime).

**Next Tasks (priorisiert):**
1) **Allowlist standardisieren & aktivieren**  
   Ziel: explizite Pinning-Möglichkeit für kritische Runner (Override unabhängig von Scan/Policy).

2) **Auto-Purge Strategy definieren**  
   Optionen: manuell (Button), zyklisch (z. B. wöchentlich), event-basiert (nach X Runner / vor Push).  
   Entscheidung + Doku + minimaler Implementationspfad.

3) **Noise-Source Hygiene**  
   `debug_output.txt` & ähnliche Artefakte: dauerhaft excluded/abtrennen, damit Diagnosen nicht „Referenzen“ aufblasen.

**Hinweis (Prozessregel):**
- Pipeline-Review ist verpflichtend, aber nicht chaotisch: Prioritäten werden angepasst, wenn Brisanz steigt/fällt.

<!-- R3541 END -->

---

## Lane E — Websites / SEO / Monetarisierung (Ideen-Dump)
**Hinweis:** Konsolidiert nach `## Lane E — Websites / SEO / Monetarisierung (konsolidiert)` durch R3555 (2026-01-17 23:39).
- Dump archiviert/ersetzt, um Dubletten zu vermeiden.

## Lane E — Websites / SEO / Monetarisierung (konsolidiert)

**Quelle:** R3555  
**Zeit:** 2026-01-17 23:39  
**Regel:** Konsolidiert = unique Items, keine Bewertung

### STRAT — Strategie / Grundsatz

- Website-Portfolio-Strategie (viele kleine vs. wenige große)
- Domain-Strategie (1 Domain = 1 Nische?)
- Naming- & Branding-System für Sites
- Vertrauens- & Ethik-Regeln (wann bewusst NICHT monetarisieren)
- Affiliate-Abhängigkeiten & Risiken
- Monetarisierungs-Reihenfolge (Affiliate → Own Product → Bundle)
- Kill-Kriterien für Websites (wann beenden?)
- Erfolgsdefinition Phase 1 (Indexierung, nicht Umsatz)
- Erfolgsdefinition Phase 2 (Conversion, nicht Traffic)
- Internationale Expansion (DE → EN?)
- Multi-Site-Orchestrierung vs. Single-Mega-Site

- Vergleichsseiten (v1, v2, vX)
- Alternativen-Seiten
- Buy-or-Skip-Seiten
- Hub-Seiten
- Übersichtsseiten
- Entscheidungs-PDFs
- Checklisten
- Templates
- Bundles

- Google Search Console Beobachtung
- Indexierungsstatus
- CTR von Titles
- Conversion pro Seitentyp
- Affiliate-Performance
- Update-Frequenz vs. Ranking
- Kill-Entscheidung dokumentieren
- Skalierungs-Trigger definieren
- priorisiert
- gesplittet
- gemerged
- auf `skip` gesetzt
- oder als `obsolet` markiert werden.

- Eigene PDFs (Decision Guides)
- Templates (Matrix, Checklisten)
- Produkt-Bundles
- Preis-Experimente
- Affiliate-Programme (Mapping)
- Risiko-Reduktion (nicht alles verlinken)
- Monetarisierung ohne Cookie-Hölle

- Static-Site-Ansatz evaluieren
- Generator/Exporter aus docs/websites/pages
- Build-Pipeline (Markdown → HTML)
- Frontmatter-Validator
- Broken-Link-Checker
- Sitemap-Generator
- Indexing-Helper
- QA-Runner für Veröffentlichungs-Gates
- Content-Skeleton-Generator
- Hub/Spoke-Autogenerator
- Multi-Domain-Deploy
- Page-Speed-Baseline
- Accessibility-Basics

- Vergleichsseiten-Template
- Alternativen-Seiten-Template
- Buy-or-Skip-Template
- Hub-Seiten-Template
- Content-Guidelines
- SEO-Guidelines
- Page-Metadata-Standard
- Release- & Update-Workflow
- Entscheidungs-Matrix-Vorlagen
- Monetarisierungs-Richtlinien
- Interne-Link-Standards
- Review-Checklisten


### DOC — Definitionen / Standards

- (leer)

### FEAT — Umsetzung / Technik

- (leer)

### CONTENT — Seiten & Assets

- (leer)

### MONETIZATION — Geld & Produkte

- (leer)

### OBS — Beobachtung / Messen

- (leer)

<!-- BAUSTEIN_SNIPPET_STANDARD:START -->
## Baustein-/Snippet-Standard fuer modulare Features (Core)

**Zweck:** Standardisierung neuer Funktionen und GUI-Elemente ueber wiederverwendbare Bausteine/Snippets mit definiertem Contract.  
**Ziel:** Stabilitaet, Skalierbarkeit, produktuebergreifende Wiederverwendung.  
**Regel:** **Neue Features = Baustein** (Bestand bleibt unangetastet, keine Voll-Rewrites).

### P0 – Definition (Docs-only)
- [ ] Baustein-/Snippet-Spec (1 Seite)
- [ ] Definition of Done (Baustein)
- [ ] No-Gos & Escape-Hatches (80/20, Fail-soft, kein Magie-Scanning ohne Whitelist)

### P1 – Referenz (Add-on, risikoarm)
- [ ] `modules/baustein_contract.py` (Result/Contract)
- [ ] `modules/baustein_registry.py` (Registry, fail-soft)
- [ ] 1 Referenz-Action-Baustein (Hello/Diag)
- [ ] Optional: 1 Referenz-GUI-Tab-Baustein (Notebook-Tab)

### P2 – Nutzungspflicht fuer Neues
- [ ] Pipeline-Eintraege fuer neue Features referenzieren eine Baustein-ID
- [ ] Keine Migration als Ziel (nur Standard fuer Neues)

### P3 – Opportunistische Anpassung
- [ ] Nur wenn bestehende Module ohnehin angefasst werden
- [ ] Adapter statt Rewrite (Mastermodus: minimal-invasiv, rueckbaubar)

### P4 – Produkt-Rollout
- [ ] ShrimpHub uebernimmt Baustein-Standard schrittweise per Produkt-Pipeline
- [ ] Weitere Produkte uebernehmen Standard nach Bedarf


<!-- BAUSTEIN_SNIPPET_GOVERNANCE -->
### Governance & Geltung

- **Gilt ab:** Runner **R3561**
- **Regel:** Neue Features und neue GUI-Elemente **muessen** als Baustein/Snippet umgesetzt werden.
- **Nicht-Ziel:** Keine Voll-Rewrites, keine Zwangsmigration bestehender Module.
- **Vorgehen:** Anpassung bestehender Module **nur opportunistisch** (wenn sie ohnehin angefasst werden).
- **Prinzip:** Add-on zuerst, Adapter statt Umbau, immer rueckbaubar.

### Explizite P0-Aufgabe (offen)
- [ ] **Baustein-/Snippet-Spec (1 Seite) inkl. DoD, No-Gos, Escape-Hatches**

<!-- BAUSTEIN_SNIPPET_STANDARD:END -->

<!-- R3566 BEGIN -->
- [x] Lane B: UI Purge Guard enforces canonical `registry/tools_keep.txt` (R3566).
<!-- R3566 END -->


## Lane E — Monetization (ACTIVE)
- **Fokus:** Vergleichsseiten (Affiliate/SEO)
- **MVP:** *Eine* Vergleichsseite
- **KPI:** Erste indexierte Seite (GSC sichtbar)
- **Regel:** Erst Proof, dann Skalierung
- **Nächster Block:** Docs/Strat (kein Code)


- **ThreadCut (Pflicht)**  
  Jeder abgeschlossene Thread endet mit einem ThreadCut zur Verwertung
  von Regeln, Lernen, Dokumentation und Pipeline-Anpassungen.

## Backlog
- [ ] **Intake: Button „Gate: R3677“ (Pipeline)**
  - Zweck: Ein-Klick-Ausführung von `R3677` (Hugo build + interne Deadlink/Target-Prüfung).
  - Scope: **Planung** (keine Implementierung in diesem Schritt).
  - Verhalten (Zielbild):
    - nutzt den kanonischen Runner-Executor
    - zeigt nach Run den neuesten Report (Report-Viewer, kein Log-Popup)
    - klar als **Gate** gekennzeichnet (protected/whitelisted)
  - Acceptance (für spätere Umsetzung):
    - Klick startet R3677 mit korrektem Root
    - Report wird angezeigt
    - R3677 bleibt purge-protected

## Lane G – Monetarisierung (passiv, beobachtend)

### G1 – Artefakt-Extraktion aus bestehender Arbeit
- Priorität: HOCH
- Status: Beobachtung
- Beschreibung:
Identifikation und Sammlung bereits existierender Artefakte (MasterRules, Pipeline-Patterns, ThreadCut-Struktur, Entscheidungslogik), die ohne Systemänderung extern nutzbar wären.
- Kein Bau neuer Produkte
- Nur Markierung & Sammlung
- Rein beobachtend

### G2 – Produktionsmaschine für Affiliate- & Content-Projekte
- Priorität: HOCH
- Status: Beobachtung
- Beschreibung:
Nutzung von ShrimpDev als interne Produktions- und Stabilitätsmaschine für Seiten wie Clarivoo und Folgeprojekte.
- Geld entsteht über Output, nicht über ShrimpDev
- Kein Einfluss auf Kernarchitektur

### G3 – Asynchrones Governance-/Audit-Modell (Marker)
- Priorität: MITTEL
- Status: Beobachtung
- Beschreibung:
Reines Denkmodell: Reports statt Calls, Diagnose statt Beratung.
- Kein Angebot
- Kein Vertrieb
- Nur als potenziell wertvolle Struktur markiert

### G4 – Read-only / Denkmodell-Abkömmlinge
- Priorität: NIEDRIG
- Status: Beobachtung
- Beschreibung:
Abstrakte Ableitungen (Read-only Tools, Denk-Frameworks), nur falls sie sich organisch ergeben.
- Kein Entwicklungsziel
- Kein Zeitdruck
