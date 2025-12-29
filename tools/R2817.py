import sys
from pathlib import Path
from datetime import datetime

RID = "R2817"

def ts():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

SECTION = """
## UI Popups – Single Source of Truth (verbindlich)

**Regel: UI erzeugt niemals Popups.**
- Kein `*_show_popup` / kein Popup-Wrapper in `ui_*.py`.
- UI darf nur Aktionen auslösen (Callbacks), aber keine Ausgabefenster bauen.

**Popups werden ausschließlich in `modules/logic_actions.py` erzeugt.**
- Zentraler Mechanismus: `_r1851_run_tools_runner(...)` + `_r1851_show_popup(...)`.

### Purge Standard (verbindlich)
- Purge Scan: Runner `R2218`
- Purge Apply: Runner `R2224`
- Popup-Inhalt kommt aus `Reports\\R2218_*.txt` bzw. `Reports\\R2224_*.txt` (neuestes mtime).
- Markdown-Bridge-Dateien sind **keine** Anzeigequelle.

### Signatur-Regel (nicht raten!)
`_r1851_run_tools_runner(app, runner_id, label)`  
- `label` ist positional Pflichtparameter.
- Keine erfundenen kwargs wie `title=` oder `subtitle=` ohne echte Signaturprüfung.

### Runner-Auslieferungsregel
- Vor Auslieferung eines Fix-Runners: **Compile-Gate** (`py_compile`) auf alle geänderten Python-Dateien.
- Keine „OK trotz FAIL“ in `.cmd`: Exitcode muss korrekt durchgereicht werden.

### Patch-Disziplin (kritische Module)
- Kein Regex-basiertes Ersetzen ganzer Funktionsblöcke in kritischen Dateien (z. B. `logic_tools.py`, `ui_toolbar.py`) ohne strukturierte Parser/Bounds.
- Minimal-invasive Änderungen + Backups + Rollback bei Compile-Fail.
""".strip() + "\n"

def write_report(root: Path, content: str) -> Path:
    d = root / "Reports"
    d.mkdir(parents=True, exist_ok=True)
    rp = d / f"Report_{RID}_{ts()}.md"
    rp.write_text(content, encoding="utf-8")
    return rp

def main():
    root = Path(sys.argv[1]).resolve()
    docs = root / "docs"
    docs.mkdir(exist_ok=True)

    # Prefer existing MasterRules file if present, else create a dedicated doc.
    candidates = [
        docs / "MasterRules.md",
        docs / "MASTER_RULES.md",
        docs / "MasterRules_ShrimpDev.md",
        root / "MasterRules.md",
        root / "MASTER_RULES.md",
    ]

    target = None
    for c in candidates:
        if c.exists():
            target = c
            break
    if target is None:
        target = docs / "MasterRules_Popups_Standard.md"

    txt = ""
    if target.exists():
        txt = target.read_text(encoding="utf-8", errors="replace")
    if "## UI Popups – Single Source of Truth (verbindlich)" not in txt:
        if txt and not txt.endswith("\n"):
            txt += "\n"
        txt += "\n" + SECTION
        target.write_text(txt, encoding="utf-8")
        action = "appended"
    else:
        action = "already present (no change)"

    rp = write_report(
        root,
        f"# {RID} Docs-only\n\nTarget: `{target}`\n\nAction: {action}\n\n---\n\n{SECTION}"
    )
    print(f"[{RID}] OK: {rp}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
