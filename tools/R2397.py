# R2397 - Patch docs/PIPELINE.md:
# - Add resolved note for Docking incident and doc links
# - Add backlog item: Artefakte popup "Quelle kopieren" (file content)
# Safe: backup, minimal append if no anchor found.

from __future__ import annotations
from pathlib import Path
from datetime import datetime
import hashlib

RID = "R2397"
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

def main() -> int:
    rep = []
    rep.append(f"# Report {RID} – Pipeline Sync")
    rep.append("")
    rep.append(f"- Timestamp: {ts()}")
    rep.append(f"- Root: `{ROOT}`")
    rep.append("")

    if not PIPE.exists():
        # create minimal pipeline
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
        rep.append("- created docs/PIPELINE.md")

    bak = backup(PIPE)
    txt = PIPE.read_text(encoding="utf-8", errors="replace")
    rep.append(f"- backup: `{bak}`")

    done_block = []
    done_block.append("### Docking Restore Bug – resolved (R2395)")
    done_block.append("- Fix: `modules/module_docking.py` restore respects `open/docked` + prefers `<key>.geometry`.")
    done_block.append("- Docs: `docs/Docking_Architecture.md`")
    done_block.append("- Incident: `docs/Incidents/Docking_R2379-R2395.md`")
    done_block.append("")

    backlog_item = []
    backlog_item.append("- Artefakte: Popup \"intern anzeigen\" → Button \"Quelle kopieren\" (kopiert Dateiinhalt, nicht Pfad).")
    backlog_item.append("")

    if "### Docking Restore Bug – resolved (R2395)" not in txt:
        if "## Done" in txt:
            parts = txt.split("## Done", 1)
            txt = parts[0] + "## Done\n\n" + "\n".join(done_block) + parts[1].lstrip()
            rep.append("- inserted into Done")
        else:
            txt = txt.rstrip() + "\n\n## Done\n\n" + "\n".join(done_block)
            rep.append("- appended Done section")

    if "Quelle kopieren" not in txt:
        if "## Backlog" in txt:
            parts = txt.split("## Backlog", 1)
            txt = parts[0] + "## Backlog\n\n" + "\n".join(backlog_item) + parts[1].lstrip()
            rep.append("- inserted into Backlog")
        else:
            txt = txt.rstrip() + "\n\n## Backlog\n\n" + "\n".join(backlog_item)
            rep.append("- appended Backlog section")

    write(PIPE, txt if txt.endswith("\n") else txt + "\n")

    rep.append(f"- sha256 docs/PIPELINE.md: `{sha256(PIPE)}`")
    rp = DOCS / f"Report_{RID}_PipelineSync_{stamp()}.md"
    write(rp, "\n".join(rep) + "\n")
    print(f"[{RID}] OK: Report {rp}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
