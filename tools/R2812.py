import sys
from pathlib import Path
from datetime import datetime

RID="R2812"

def ts(): return datetime.now().strftime("%Y%m%d_%H%M%S")

STANDARD_SECTION = f"""
## Popup-Standard (Single Source of Truth)

**Regel (verbindlich):**
- **UI darf niemals Popups öffnen.** (keine `_r1851_show_popup` Aufrufe in `ui_*.py`)
- **Popups werden ausschließlich in `modules/logic_actions.py` erzeugt.**
- Purge ist fest standardisiert:
  - **Purge Scan → Runner `R2218`**
  - **Purge Apply → Runner `R2224`**
  - Nach Run wird das **neueste Report-Artefakt** aus `Reports/` geladen und im Popup angezeigt.
- **Bridge-MD als Anzeigequelle ist verboten.** MD ist Doku, nicht UI-Content.

**Konsequenz / Anti-Pattern:**
- Mehrere Trigger-Pfade (Toolbar + Logic) sind unzulässig und führen zu Doppel-Popups.
- `.cmd` darf Fail niemals als OK ausgeben (Exitcode muss durchgereicht werden).
""".strip("\n") + "\n"

def write_report(root: Path, content: str) -> Path:
    d = root/"Reports"
    d.mkdir(parents=True, exist_ok=True)
    rp = d/f"Report_{RID}_{ts()}.md"
    rp.write_text(content, encoding="utf-8")
    return rp

def main():
    root = Path(sys.argv[1]).resolve()
    docs = root/"docs"
    docs.mkdir(exist_ok=True)

    # Try to find existing MasterRules doc
    candidates = [
        docs/"MasterRules.md",
        docs/"MASTER_RULES.md",
        docs/"MasterRules_ShrimpDev.md",
        root/"MasterRules.md",
        root/"MASTER_RULES.md",
    ]
    target = None
    for c in candidates:
        if c.exists():
            target = c
            break

    created = False
    if target is None:
        target = docs/"MasterRules_PopupStandard.md"
        created = True

    txt = ""
    if target.exists():
        txt = target.read_text(encoding="utf-8", errors="replace")

    if "## Popup-Standard (Single Source of Truth)" not in txt:
        if txt and not txt.endswith("\n"):
            txt += "\n"
        txt += "\n" + STANDARD_SECTION
        target.write_text(txt, encoding="utf-8")
        action = "appended"
    else:
        action = "already present (no change)"

    rp = write_report(root, f"# {RID} Docs-only\n\nTarget: `{target}`\n\nAction: {action}\nCreatedNewDoc: {created}\n")
    print(f"[{RID}] OK: {rp}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
