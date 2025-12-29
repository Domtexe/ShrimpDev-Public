import sys
from pathlib import Path
from datetime import datetime

RID = "R2824"

def ts():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def write_report(root: Path, text: str) -> Path:
    reports = root / "Reports"
    reports.mkdir(exist_ok=True)
    rp = reports / f"Report_{RID}_{ts()}.md"
    rp.write_text(text, encoding="utf-8")
    return rp

def backup_file(p: Path) -> Path:
    bak = p.with_suffix(p.suffix + f".{RID}_{ts()}.bak")
    bak.write_text(p.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
    return bak

PIPE_ITEM_ID = "P3-Workspace-Deaktivieren-RepoRoots-Explizit"

PIPE_BLOCK = f"""
---

## {PIPE_ITEM_ID}

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
""".lstrip("\n")

def main():
    root = Path(sys.argv[1]).resolve()
    pipeline = root / "docs" / "PIPELINE.md"

    notes = []
    notes.append(f"# {RID} – PIPELINE update\n\n")
    notes.append(f"Target: `{pipeline}`\n\n")

    if not pipeline.exists():
        rp = write_report(root, "".join(notes) + "**FAIL**: docs/PIPELINE.md not found.\n")
        print(f"[{RID}] FAIL: {rp}")
        return 11

    content = pipeline.read_text(encoding="utf-8", errors="replace")

    # Dup-guard
    if PIPE_ITEM_ID in content:
        rp = write_report(root, "".join(notes) + f"**OK**: Entry already present: `{PIPE_ITEM_ID}` (no changes).\n")
        print(f"[{RID}] OK: Report: {rp}")
        return 0

    bak = backup_file(pipeline)
    notes.append(f"- Backup: `{bak.name}`\n")

    # Insert strategy:
    # Prefer inserting near a "Backlog"/"TODO"/"P3" area if found; otherwise append at end.
    insert_at = None
    for marker in ("## Backlog", "## TODO", "## ToDo", "## Tasks", "## P3", "# Backlog", "# TODO"):
        idx = content.lower().find(marker.lower())
        if idx != -1:
            # insert before the marker header so it stays visible at top of that section
            insert_at = idx
            notes.append(f"- Inserted before marker: `{marker}`\n")
            break

    if insert_at is None:
        new_content = content.rstrip() + "\n\n" + PIPE_BLOCK + "\n"
        notes.append("- Appended to end of file (no marker found)\n")
    else:
        new_content = content[:insert_at].rstrip() + "\n\n" + PIPE_BLOCK + "\n\n" + content[insert_at:].lstrip()

    pipeline.write_text(new_content, encoding="utf-8")

    rp = write_report(root, "".join(notes) + "\n**RESULT: OK**\n")
    print(f"[{RID}] OK: Report: {rp}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
