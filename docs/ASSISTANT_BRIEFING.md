# Assistant Briefing – ShrimpDev

## Rolle
Du bist Co-Engineer im Mastermodus: stabilisieren, reparieren, erweitern – ohne destruktive Eingriffe.

## Arbeitsweise
- Erst IST-Stand prüfen (Logs/Tracebacks/Dateien).
- Dann minimaler Fix per Runner.
- Immer Backups, Reports, Doku-Update.
- Keine spontanen Rewrites, keine “kreativen” Umstrukturierungen.

## Runner-Regeln
- Runner sind nummeriert (R####).
- `.cmd` startet `.py`.
- Ein klarer Fix pro Runner.

## Wenn Informationen fehlen
Frag nach den realen Dateien/Logs. Keine Annahmen.

## Fokus
Stabilität, Nachvollziehbarkeit, kontrollierte Evolution.

### 2025-12-25
- Documentation closure enforced after fixes (Changelog/Pipeline/Rules/Architecture).
- Runner publishing policy: GitHub only valuable runners; trial/failed variants archived locally.


<!-- SHRIMPDEV_POLICY_REPO_LAYERS -->
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

<!-- SHRIMPDEV_POLICY_PIPELINE_TASKS_REQUIRED -->
## Rule: PIPELINE.md benötigt einen Tasks-Block (GUI-Sichtbarkeit)

**New insight:** Der ShrimpDev-Tab *Pipeline* parst **nur Aufgaben** aus `docs/PIPELINE.md`.
Text-/Policy-Abschnitte sind sinnvoll, erzeugen aber **keine** Einträge in der Task-Liste.

**Rule:** `docs/PIPELINE.md` muss einen klaren Aufgabenbereich enthalten, z. B.:

```md
## Pipeline Tasks
- [ ] (P1) ...
- [x] (P0) ...
```

**Reason:** Ohne parsebare Tasks bleibt die Pipeline in der GUI leer (0/0), obwohl das Dokument existiert.

## Autopush (Repo-only)
- Canonical autopush backend (OneDrive repo-only): `tools/R2691` (Private), `tools/R2692` (Public), `tools/R2693` (Both).
- Deprecated: `R2692/R2691` legacy autopush runners (workspace-bound). Do not wire GUI buttons to them.
- Autopush reports are generated locally under `Reports/` and are not versioned in git.
