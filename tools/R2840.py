# -*- coding: utf-8 -*-
from pathlib import Path
from datetime import datetime
import shutil

RUNNER_ID = "R2840"

def now():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def repo_root():
    return Path(__file__).resolve().parent.parent

def main():
    repo = repo_root()
    mr = repo / "MasterRules.md"
    if not mr.exists():
        print("MasterRules.md not found")
        return 11

    arch = repo / "_Archiv"
    arch.mkdir(exist_ok=True)
    bak = arch / f"MasterRules.md.{RUNNER_ID}_{now()}.bak"
    shutil.copy2(mr, bak)

    txt = mr.read_text(encoding="utf-8", errors="replace")

    block = """
## 🔁 Patch- & Rollback-Pflicht (verbindlich)

- Jeder PATCH-Runner **muss** vor Änderungen ein Backup erstellen.
- Schlägt ein Patch fehl (Syntax, Compile, Runtime), **ist automatisch ein Rollback auszuführen**.
- Ein fehlerhafter Zustand darf **niemals** im Arbeitsstand verbleiben.

## 🔘 UI-Regel: Push-Buttons

Push-Buttons dürfen **nur aktiv** sein, wenn **alle** Bedingungen erfüllt sind:
- gültiger Repo-Root (private/public)
- zugehöriger Wrapper existiert physisch:
  - Private Push → `tools/R2691.cmd`
  - Public Push → `tools/R2692.cmd`

Fehlt ein Wrapper, **muss** der Button deaktiviert sein.

## 🧹 Purge-Regel: Kritische Runner

- Kritische Runner sind über `registry/runner_whitelist.txt` zu schützen.
- Der Schutz ist **stem-basiert** (`R####`) und unabhängig von `.cmd` / `.py`.
- Purge darf **keinen** Whitelist-Runner archivieren.
"""

    if "Patch- & Rollback-Pflicht" not in txt:
        txt += "\n\n" + block.strip() + "\n"
        mr.write_text(txt, encoding="utf-8")

    rep = repo / "Reports" / f"Report_{RUNNER_ID}_{now()}.md"
    rep.parent.mkdir(exist_ok=True)
    rep.write_text(f"# {RUNNER_ID}\n\nMasterRules aktualisiert.\nBackup: {bak}\n")

    print(f"[{RUNNER_ID}] OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
