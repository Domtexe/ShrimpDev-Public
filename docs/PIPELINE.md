<!-- PIPELINE_V1_START -->
# PIPELINE v1 — Lanes & Turnus (Source of Truth)

## Lane A — Stabilität & Core
- [ ] (P0) [CORE] (HIGHEST / BLOCKER) **R2372 – Architektur: INI Single Writer (Design + API)** (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2370.py:L122)
- [ ] (P0) [CORE] (HIGHEST / BLOCKER) **R2376 – Docking über Single Writer** (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2370.py:L141)

**Ziel:** Alle Themen (ShrimpDev/ShrimpHub/Website/Doku/Tooling) gleichmäßig voranbringen — ohne Chaos.  
**Regel:** Start-/Crash-Stabilität schlägt alles.

## Lanes (Themenbahnen)
- **Lane A — Stabilität / Crash / Startfähigkeit (P0/P1)**
- **Lane B — Core Features (P1/P2)**
- **Lane C — Tooling / Automationen (P1/P2)**
- **Lane D — Doku / Regeln / Konsistenz (P1/P2)**
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

- [ ] (P0) [CORE] NOTE: that CI blockers were fixed via R2576. _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2576.py:L103)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L18)- [ ] (P0) (HIGHEST / BLOCKER) **R2373 – Implementierung: zentraler INI-Writer (Merge + atomic)** (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/INI_WriteMap.md:L14478)- [ ] (P0) (HIGHEST / BLOCKER) **R2371 – INI-WriteMap (READ-ONLY Diagnose)** (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2370.py:L117)
- [ ] (P0) [CORE] (HIGHEST / BLOCKER) **R2374 – config_manager Save konsolidieren** (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2370.py:L133)
- [ ] (P0) [CORE] (HIGHEST / BLOCKER) **R2375 – Shims: config_loader.py / config_mgr.py** (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2370.py:L137)
- [ ] (P0) [CORE] (HIGHEST / BLOCKER) **R2377 – Monkeypatch/Altlogik Quarantäne** (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2370.py:L148)
- [ ] (P0) [CORE] (HIGHEST / BLOCKER) **R2378 – Restore Reihenfolge finalisieren** (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2370.py:L152)
- [ ] (P0) [CORE] (HIGHEST / BLOCKER) **R2379 – Regression-Testplan** (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2370.py:L156)
- [ ] (P1) [PROD] TODO: \n- File: `{pipeline}`\n- Backup: `{backup}`\n", _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/_Archiv/Runner_Staging_2025-12-25/R2598.py:L59)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L24)
- [ ] (P1) [CORE] NOTE: Did not match expected 'run: uvx ruff ...' lines. Please verify ci.yml manually.", _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2580.py:L109)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L25)
- [ ] (P1) [PROD] TODO: ][HIGH] Runner-Cleanup – Archivierung unbenutzter Runner _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/_Pipeline/Pipeline_R2016_RunnerCleanup_20251208_154653.txt:L1)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L27)
- [ ] (P1) [CORE] (P1) ... (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/ARCHITECTURE.md:L176)
- [ ] (P1) [CORE] TODO: -Pipeline: eigener GUI-Tab MasterRules (Viewer + Open/Refresh). (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Pipeline_Notes.md:L29)
- [ ] (P1) [CORE] TODO: (Pipeline), sondern bekommen einen eigenen Tab.` (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L19929)
- [ ] (P1) [CORE] TODO: -Pipeline: eigener GUI-Tab MasterRules (Viewer + Open/Refresh).\n"` (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L19950)
- [ ] (P1) [CORE] TODO: ) Pipeline-Eintrag: Tracebacks wieder ins Log (HIGH)` (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L19967)
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

## Lane E — Website / SEO-Netzwerk (P2/P3)

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

