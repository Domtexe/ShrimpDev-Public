# Development Rules (Mastermodus)

## Unverhandelbar
1) **Keine Voll-Rewrites** ohne explizite Zustimmung.
2) **Ein Problem pro Runner** (klar, testbar, rückbaubar).
3) **Backups vor Änderungen** (Datei-Backups nach `_Archiv/`).
4) **Logs/Reports Pflicht** (`_Reports/`).
5) **Doku mitpflegen** (Architektur/Regeln/Notes).
6) **Keine Platzhalter-/Dummy-Dateien** als “fertig”.
7) **Runner-Standard** bleibt: `.cmd` + `.py`, nummeriert (R####).

## Stil
- Minimal-invasiv
- Robust (Fehlerbehandlung)
- Nachvollziehbar (klare Ausgabe)

## Registry & Runner Rules
- Systemische Regeln liegen **ausschließlich** unter `registry/`.
- Whitelists sind **append-only**.
- Public-Export erfolgt **nur** über Whitelist-Runner (z. B. R2692).
- Purge respektiert ausschließlich `registry/tools_keep.txt`.

## CI & Ruff – Scope (Runtime-only)

**Ziel:** CI soll Stabilität erzwingen, ohne Legacy-/Learning-Artefakte (Runner/Tools) zu blockieren.

### Hard Rules (verbindlich)
**MR-CI-001 — CI Scope = Runtime-Code**
- **IN:** `modules/`, `main_gui.py` (weitere Entrypoints nur nach expliziter Entscheidung)
- **OUT:** `tools/` (Runner/Legacy/Learning), `_Exports/` (Artefakte), `Reports/` (lokal)

**MR-CI-002 — Tools/Runner dürfen CI nicht blockieren**
- Der Format-/Style-Zustand historischer Runner ist **scheißegal** (Learning only).
- CI prüft Tools nicht. Punkt.

**MR-CI-003 — CI rot: Reihenfolge**
1) **Scope prüfen** (prüft CI aus Versehen `tools/` / Artefakte?)  
2) erst dann Code anfassen  
3) pro Fix: **Diagnose → minimaler Patch → Compile → Smoke**

**MR-CI-004 — Format ist kein Quality-Gate während Migration**
- Während aktiver Umstellung/Migration gilt: **kein `ruff format --check` als CI-Gate**.
- `ruff format` darf lokal/gezielt genutzt werden, aber **darf keine CI-Endlosschleifen erzeugen**.
- Nach “Format-Freeze” (Repo stabil): Format-Check kann optional wieder als Gate aktiviert werden.

**MR-IGN-001 — Reports sind lokal**
- `Reports/` bleibt `.gitignore`-lokal; Runner dürfen nie erwarten, dass Reports committet werden.

### CI Implementation (GitHub Actions)
**Migration / WIP (empfohlen):**
- `uvx ruff check modules main_gui.py`

**Nach Format-Freeze (optional):**
- `uvx ruff format --check modules main_gui.py`
- `uvx ruff check modules main_gui.py`

### Incident-Anker (Lessons Learned)
- Ruff/CI-Loop (R256x): Ursache = falscher Scope + Format-Check als Gate während WIP.
- Konsequenz = Runtime-only CI + Format-Gate erst nach Freeze.



## CI / Ruff – Regeln

**Grundsatz:** CI ist Gate für *Core-Code* und *neuen/aktiv gepflegten Code* – nicht für Legacy-/Archiv-Module.

Regeln:
1. **Legacy-Module dürfen CI nicht blockieren.** Wenn Legacy-Dateien Ruff-Fehler haben, werden sie per `--exclude` aus dem CI-Lint/Format-Gate genommen.
2. **TechDebt wird dokumentiert, nicht weg-gehackt.** Für jedes excluded Legacy-Modul kommt ein Pipeline-TechDebt-Eintrag mit Fix-Strategie.
3. **Neue Änderungen bleiben clean.** Alles, was aktiv entwickelt wird (Core, neue Features, refactor-teile), muss Ruff bestehen.
4. **Keine Massen-Reformat-Aktionen ohne Plan.** Formatierungen nur zielgerichtet und mit sauberem Commit, sonst erzeugt es Diff-Chaos.

## Runner publishing policy
- GitHub contains only valuable runners: fix-runners that resulted in merged commits and decisive READ-ONLY diagnosis runners.
- Trial/failed/variant runners are archived locally under `_Archiv/Runner_Staging_YYYY-MM-DD/`.

---
### CI / Ruff Legacy-Zonen (20251225_174811)
- Marker: `R2638_RUFF_LEGACY_ZONES`
- Policy: UI/Tools/LJ gelten als Legacy-Zonen und blockieren CI nicht mit Stil-/Modernisierungsregeln.
- Umsetzung: `pyproject.toml` per-file-ignores für `modules/ui_*.py`, `modules/tools/*.py`, `modules/module_learningjournal.py`.
- Ziel: CI prüft Stabilität (Syntax/echte Fehler), nicht Legacy-Style.
---



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
