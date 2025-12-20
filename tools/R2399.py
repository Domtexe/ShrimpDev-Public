# R2399 - Patch docs/PIPELINE.md:
# Adds non-urgent "Open Notes" items (NOT Docking) in a sensible section.
# Safe: backup, minimal edits, no triple-quotes.

from __future__ import annotations
from pathlib import Path
from datetime import datetime
import hashlib

RID = "R2399"
ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
PIPE = DOCS / "PIPELINE.md"

def stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def sha256(p: Path) -> str:
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()

def backup(p: Path) -> Path:
    bak = ROOT / "_Archiv" / f"{p.name}.{RID}_{stamp()}.bak"
    bak.parent.mkdir(parents=True, exist_ok=True)
    bak.write_bytes(p.read_bytes())
    return bak

def write(p: Path, s: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding="utf-8")

def ensure_pipeline_exists() -> None:
    if PIPE.exists():
        return
    base = []
    base.append("# PIPELINE")
    base.append("")
    base.append("## Backlog")
    base.append("")
    base.append("## In Progress")
    base.append("")
    base.append("## Done")
    base.append("")
    write(PIPE, "\n".join(base) + "\n")

def insert_under_section(txt: str, section_header: str, insert_block: str) -> tuple[str, bool]:
    # Inserts insert_block right after section header line (and a following blank line if present)
    if section_header not in txt:
        return txt, False
    parts = txt.split(section_header, 1)
    head = parts[0] + section_header
    tail = parts[1]
    # Ensure exactly one blank line after header
    if tail.startswith("\r\n"):
        tail = tail[2:]
    if tail.startswith("\n"):
        tail = tail[1:]
    if not head.endswith("\n"):
        head += "\n"
    # Insert with one blank line
    new_txt = head + "\n" + insert_block.rstrip() + "\n\n" + tail.lstrip()
    return new_txt, True

def main() -> int:
    rep = []
    rep.append(f"# Report {RID} – Pipeline Open Notes")
    rep.append("")
    rep.append(f"- Timestamp: {ts()}")
    rep.append(f"- Root: `{ROOT}`")
    rep.append("")

    ensure_pipeline_exists()
    bak = backup(PIPE)
    rep.append(f"- backup: `{bak}`")

    txt = PIPE.read_text(encoding="utf-8", errors="replace")

    header = "### Offene Notizen (nicht dringend, aber merken)"
    items = []
    items.append(header)
    items.append("- INI-SingleWriter Konsolidierung ist noch nicht final: `config_loader.save()`/`config_mgr`/vereinzelte `cfg.write()`-Pfade bei Gelegenheit zentralisieren (Ziel: ein Write-Pfad).")
    items.append("- Restart-Pfad ist sensibel (mehrere Persist-Hooks): zukünftige Änderungen nur mit READ-ONLY-Scan + klarer Verifikation, damit kein Regression-Centering/State-Leak entsteht.")
    items.append("- `module_docking.py` ist stabil, aber historisch komplex: Refactoring nur bewusst (Snapshot + Tests/Verifikation), kein „nebenbei“.")
    block = "\n".join(items)

    changed = False

    if header not in txt:
        # Prefer Backlog (non-urgent)
        if "## Backlog" in txt:
            txt2, ok = insert_under_section(txt, "## Backlog", block)
            if ok:
                txt = txt2
                changed = True
                rep.append("- inserted under: Backlog")
        else:
            # Append backlog section at end
            txt = txt.rstrip() + "\n\n## Backlog\n\n" + block + "\n"
            changed = True
            rep.append("- appended Backlog section + block")
    else:
        rep.append("- already present: no-op")

    if changed:
        write(PIPE, txt if txt.endswith("\n") else txt + "\n")

    rep.append(f"- changed: {changed}")
    rep.append(f"- sha256 docs/PIPELINE.md: `{sha256(PIPE)}`")

    rp = DOCS / f"Report_{RID}_Pipeline_OpenNotes_{stamp()}.md"
    write(rp, "\n".join(rep) + "\n")
    print(f"[{RID}] OK: Report {rp}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
