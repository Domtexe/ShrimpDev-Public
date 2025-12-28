

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

- [ ] (P0) NOTE: that CI blockers were fixed via R2576. _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2576.py:L103)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L18)
- [ ] (P0) (HIGHEST / BLOCKER) **R2373 – Implementierung: zentraler INI-Writer (Merge + atomic)** (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/INI_WriteMap.md:L14478)
- [ ] (P0) (HIGHEST / BLOCKER) **R2371 – INI-WriteMap (READ-ONLY Diagnose)** (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2370.py:L117)
- [ ] (P0) (HIGHEST / BLOCKER) **R2372 – Architektur: INI Single Writer (Design + API)** (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2370.py:L122)
- [ ] (P0) (HIGHEST / BLOCKER) **R2374 – config_manager Save konsolidieren** (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2370.py:L133)
- [ ] (P0) (HIGHEST / BLOCKER) **R2375 – Shims: config_loader.py / config_mgr.py** (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2370.py:L137)
- [ ] (P0) (HIGHEST / BLOCKER) **R2376 – Docking über Single Writer** (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2370.py:L141)
- [ ] (P0) (HIGHEST / BLOCKER) **R2377 – Monkeypatch/Altlogik Quarantäne** (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2370.py:L148)
- [ ] (P0) (HIGHEST / BLOCKER) **R2378 – Restore Reihenfolge finalisieren** (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2370.py:L152)
- [ ] (P0) (HIGHEST / BLOCKER) **R2379 – Regression-Testplan** (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2370.py:L156)
- [ ] (P1) TODO: \n- File: `{pipeline}`\n- Backup: `{backup}`\n", _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/_Archiv/Runner_Staging_2025-12-25/R2598.py:L59)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L24)
- [ ] (P1) NOTE: Did not match expected 'run: uvx ruff ...' lines. Please verify ci.yml manually.", _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2580.py:L109)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L25)
- [ ] (P1) TODO: ][HIGH] Runner-Cleanup – Archivierung unbenutzter Runner _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/_Pipeline/Pipeline_R2016_RunnerCleanup_20251208_154653.txt:L1)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L27)
- [ ] (P1) (P1) ... (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/ARCHITECTURE.md:L176)
- [ ] (P1) TODO: -Pipeline: eigener GUI-Tab MasterRules (Viewer + Open/Refresh). (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Pipeline_Notes.md:L29)
- [ ] (P1) TODO: (Pipeline), sondern bekommen einen eigenen Tab.` (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L19929)
- [ ] (P1) TODO: -Pipeline: eigener GUI-Tab MasterRules (Viewer + Open/Refresh).\n"` (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L19950)
- [ ] (P1) TODO: ) Pipeline-Eintrag: Tracebacks wieder ins Log (HIGH)` (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L19967)
- [ ] (P1) TODO: in der Pipeline-Datei.` (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L7958)
- [ ] (P1) TODO: in docs/Master/Pipeline_Notes.md eintragen:` (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L8944)
- [ ] (P1) TODO: (Pipeline), sondern bekommen einen eigenen Tab. (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2143.py:L2)
- [ ] (P1) TODO: -Pipeline: eigener GUI-Tab MasterRules (Viewer + Open/Refresh).\n" (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2143.py:L250)
- [ ] (P1) TODO: ) Pipeline-Eintrag: Tracebacks wieder ins Log (HIGH) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2144.py:L9)
- [ ] (P1) NOTE: for Docking incident and doc links (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2397.py:L2)
- [ ] (P1) `docs/Architecture_ProjectTab.md` – **Datenquellen/Contract** (nur lesen: PIPELINE, Reports, SmokeTest) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2521.py:L76)
- [ ] (P2) **Incremental Refactor Plan**: Schrittfolge ohne Vollrewrite (1 Modul pro Runner, jeweils compile+smoke) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2519.py:L94)
- [ ] (P3) TODO: (reports/ordner konsolidieren) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2596_20251225_111324.md:L4)
- [ ] (P3) TODO: `: `False` (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2655_20251225_200722.md:L84)
- [ ] (P3) TODO: (reports/ordner konsolidieren)\n" _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/_Archiv/Runner_Staging_2025-12-25/R2596.py:L93)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L28)
- [ ] (P3) NOTE: readline can block if no output; so we guard by checking rc or waiting small. _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/_Archiv/Runner_Staging_2025-12-25/R2609.py:L70)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L29)
- [ ] (P3) NOTE: ") _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/modules/ui_lists.py:L7)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L30)
- [ ] (P3) NOTE: btn_apply pack line not found (maybe already adjusted).") _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2448.py:L138)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L31)
- [ ] (P3) NOTE: btn_scan pack line not found (maybe already adjusted).") _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2448.py:L148)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L32)
- [ ] (P3) NOTE: `{pub}` not found.\n", _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2555.py:L26)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L33)
- [ ] (P3) NOTE: that these were fixed via runner) _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2576.cmd:L9)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L34)
- [ ] (P3) NOTE: {'patched' if c4 else 'no-op'}") _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2576.py:L184)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L35)
- [ ] (P3) NOTE: {'patched' if c3 else 'no-op'}") _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2577.py:L174)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L36)
- [ ] (P3) NOTE: = ( _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2638.py:L203)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L37)
- [ ] (P3) NOTE: + "\n") _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2638.py:L212)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L38)
- [ ] (P3) NOTE: (policy visibility) _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2638.py:L231)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L39)
- [ ] (P3) TODO: ", _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2655.py:L129)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L40)
- [ ] (P3) TODO: /FIXME in code) _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2658.cmd:L5)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L41)
- [ ] (P3) TODO: markers _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2658.py:L107)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L42)
- [ ] (P3) TODO: |FIXME|HACK|NOTE)\b[:]?\s*(?P<text>.*)$', re.IGNORECASE) _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2658.py:L26)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L43)
- [ ] (P3) TODO: /FIXME/HACK/NOTE markers in *.py/*.cmd/*.bat/*.ps1/*.yml/*.toml _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2658.py:L8)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L44)
- [ ] (P3) TODO: /FIXME Marker). Bitte bei Bedarf konsolidieren.\n\n") _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2659.py:L108)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L45)
- [ ] (P3) TODO: Flag/Policy). (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Architecture_DnD_FileOut.md:L21)
- [ ] (P3) NOTE: `[Docking]` intentionally excluded from updates (preserved by ini_writer default). (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2382_SingleWriter_Delegation_20251219_101450.md:L7)
- [ ] (P3) NOTE: ] {n}")` (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L11590)
- [ ] (P3) TODO: implement logic here` (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L15280)
- [ ] (P3) NOTE: ` (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L19697)
- [ ] (P3) TODO: list: add a high-priority item about tracebacks in log.` (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L19969)
- [ ] (P3) NOTE: = "Runner-Logs MUESSEN in debug_output.txt landen"` (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L21653)
- [ ] (P3) NOTE: Wir ersetzen NUR run_runner_with_popup bis EOF. Helpers bleiben unberührt.` (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L22290)
- [ ] (P3) TODO: ` (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L7989)
- [ ] (P3) TODO: bereits vorhanden – uebersprungen.\n")` (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L8918)
- [ ] (P3) TODO: hinzugefuegt.\n")` (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L8921)
- [ ] (P3) NOTE: patched restore_from_ini loop (open flag + geometry preferred) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2395_Docking_RestoreOpenGeo_20251219_223827.md:L14)
- [ ] (P3) NOTE: Root tools_keep.txt exists but is obsolete. Canonical file is registry/tools_keep.txt (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2416_RegistryAndDocsFix_20251221_105138.md:L9)
- [ ] (P3) NOTE: This runner made **no changes**. It only reports. (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2450_UI_ToolbarState_20251221_215319.md:L208)
- [ ] (P3) HACK: für on_sort (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R1301_IntakeV1_Install.py:L353)
- [ ] (P3) TODO: actual UI factory if separate exists\n" (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R1305_IntakeHardFix.py:L70)
- [ ] (P3) NOTE: str) -> None: (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2137.py:L31)
- [ ] (P3) NOTE: }\n" (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2137.py:L37)
- [ ] (P3) TODO: list: add a high-priority item about tracebacks in log. (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2144.py:L118)
- [ ] (P3) NOTE: later in report (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2183.py:L118)
- [ ] (P3) NOTE: = "Runner-Logs MUESSEN in debug_output.txt landen" (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2239.py:L124)
- [ ] (P3) NOTE: not in mr: (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2239.py:L125)
- [ ] (P3) NOTE: Wir ersetzen NUR run_runner_with_popup bis EOF. Helpers bleiben unberührt. (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2284.py:L52)
- [ ] (P3) (TOP/HIGH) Phase 2: Restore-Orchestrierung (pro Fenster-Key) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2375.py:L66)
- [ ] (P3) (HIGH) Migration: Remaining Writers -> SingleWriter (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2375.py:L79)
- [ ] (P3) (MED) Defactoring / Archivierung (nach erfolgreicher Umstellung) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2375.py:L83)
- [ ] (P3) NOTE: `[Docking]` intentionally excluded from updates (preserved by ini_writer default).", (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2382.py:L204)
- [ ] (P3) NOTE: If file has multiple Toplevel creations, we patch the one inside build_runner_products_tab only. (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2393.py:L58)
- [ ] (P3) NOTE: = _patch_restore_from_ini(src) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2395.py:L165)
- [ ] (P3) NOTE: {note}") (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2395.py:L169)
- [ ] (P3) NOTE: Root tools_keep.txt exists but is obsolete. " (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2416.py:L125)
- [ ] (P3) NOTE: target did not exist before restore", (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2432.py:L67)
- [ ] (P3) NOTE: This runner made **no changes**. It only reports.\n") (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2450.py:L185)
- [ ] (P3) NOTE: ", "- Dieser Report ist Grundlage für den minimalen Patch-Runner (R2463)."] (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2462.py:L123)
- [ ] (P3) NOTE: exists (minimal) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2470.py:L70)
- [ ] (P3) NOTE: = patch_guard_parent(code1) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/Runner_1132_FixGuardParent.py:L183)
- [ ] (P3) NOTE: .strip()) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/Runner_1132_FixGuardParent.py:L193)
- [ ] (P3) NOTE: ] {n}") (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/Runner_1137_IntakeLoadFix.py:L247)
- [ ] (P3) TODO: (optional): hier später Reflow/Anordnung implementieren. (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/Runner_1171m_IntakeToolbarReflowFix.py:L47)
- [ ] (P3) TODO: implement logic here (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/Runner_943_NewRunner.py:L49)
- [ ] (P3) **Define Actions Registry (Docs)**: Liste der erlaubten Actions + Labels (Copy Path/File/Text, Open, Folder, Restore gated) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2519.py:L90)
- [ ] (P3) **Define Gating Rules (Docs)**: wann ist Restore sichtbar? wann ist File-Copy erlaubt? (Backup/Archiv-Only, Busy-State) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2519.py:L91)
- [ ] (P3) **Central Helpers Plan (Docs)**: gemeinsame Helper-Funktionen (clipboard, file-copy-paste, restore-safe) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2519.py:L92)
- [ ] (P3) **Per-Tab Audit**: Artefakte (Tree/Preview), Intake, Runner Products etc. – Abweichungen dokumentieren (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2519.py:L93)
- [ ] (P3) **Regression Checklist**: Rechtsklick links/rechts, Selection behavior, busy-state, messageboxes (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2519.py:L95)
- [ ] (P3) `docs/Architecture_ProjectTab.md` – **Definition + Non-Goals** (keine Buttons, keine neue Logik) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2521.py:L75)
- [ ] (P3) `docs/Architecture_ProjectTab.md` – **Minimaler Anzeige-Contract/Wireframe** (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2521.py:L77)
- [ ] (P3) TODO: markers (now also in .md) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2661.py:L218)
- [ ] (P3) TODO: /FIXME/HACK/NOTE lines ALSO in Markdown (.md) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2661.py:L9)

<!-- SHRIMPDEV_PIPELINE_IMPORTED_TASKS_END -->


> **Hinweis:** Der Pipeline-Tab in ShrimpDev zeigt nur **Tasks** (z. B. `- [ ] …`).
> Policies/Regeln bleiben weiter oben im Dokument, aber ohne Tasks bleibt die GUI-Liste leer.

- [ ] (P1) CI: Reports wieder als GitHub Actions Artefakte anzeigen (Runner R2656)
- [ ] (P1) ShrimpDev: Artefakte-Tab prüfen/reaktivieren, falls Anzeige fehlt
- [ ] (P2) LearningJournal Auto-Write: Diagnose + Guard (nach CI stabil)
- [x] (P0) CI Syntax-Gate scoped + YAML valid (R2653/R2654)

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

