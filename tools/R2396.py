# R2396 - Docs update:
# - docs/Architecture_ShrimpDev.md (append/update section)
# - docs/Docking_Architecture.md (create/overwrite with canonical content block)
# - docs/Incidents/Docking_R2379-R2395.md (create)
# - Write report
#
# Safe: backups, minimal edits where possible, no triple quotes.

from __future__ import annotations
from pathlib import Path
from datetime import datetime
import hashlib
import re

RID = "R2396"
ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
INC = DOCS / "Incidents"
ARCH = DOCS / "Architecture_ShrimpDev.md"
DOCK = DOCS / "Docking_Architecture.md"
POST = INC / "Docking_R2379-R2395.md"


def ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()


def backup(p: Path) -> Path:
    bak = ROOT / "_Archiv" / f"{p.name}.{RID}_{stamp()}.bak"
    bak.parent.mkdir(parents=True, exist_ok=True)
    bak.write_bytes(p.read_bytes())
    return bak


def write_text(p: Path, content: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def ensure_architecture_section(arch_path: Path, report: list[str]) -> None:
    # Create file if missing
    if not arch_path.exists():
        base = []
        base.append("# ShrimpDev – Architektur")
        base.append("")
        base.append("Dieses Dokument beschreibt die Architektur von ShrimpDev.")
        base.append("")
        write_text(arch_path, "\n".join(base) + "\n")
        report.append(f"- created: {arch_path}")

    before = arch_path.read_text(encoding="utf-8", errors="replace")
    bak = backup(arch_path)
    report.append(f"- backup: {bak}")

    header = "## Docking & Window Lifecycle"
    block = []
    block.append(header)
    block.append("")
    block.append("### Verantwortung (Ownership)")
    block.append("- `modules/module_docking.py` ist der alleinige Owner für Dock/Undock-Fenster (Read-Only Viewer).")
    block.append("- Tab-Builder (`ui_pipeline_tab`, `ui_runner_products_tab`, `ui_log_tab`) bauen Inhalte in ein Parent-Widget, erzeugen aber keine eigenen Fenster.")
    block.append("")
    block.append("### Persistenz-Quelle")
    block.append("- `ShrimpDev.ini` ist die Single Source of Truth für `[Docking]`.")
    block.append("- Relevante Keys pro Fenster: `<key>.open`, `<key>.docked`, `<key>.geometry`, `<key>.ts`.")
    block.append("")
    block.append("### Restore-Reihenfolge (verbindlich)")
    block.append("1. INI laden")
    block.append("2. `open/docked` auswerten: restore nur wenn `open=1` und `docked=0`")
    block.append("3. Geometry bevorzugen: `<key>.geometry` (Format `WxH+X+Y`)")
    block.append("4. Fallback nur wenn nötig: legacy `w/h/x/y` verwenden, wenn `geometry` fehlt")
    block.append("5. Offscreen-Schutz: ist die Geometry offscreen, dann erst fallback/center")
    block.append("")
    block.append("### Verbotene Muster (Regression-Guards)")
    block.append("- Kein Zentrieren nach erfolgreichem Restore (Center ist nur Offscreen-/No-Geo-Fallback).")
    block.append("- Keine Fenstererzeugung (`tk.Toplevel`) in Tab-Buildern.")
    block.append("")

    new_block = "\n".join(block)

    if header in before:
        # Replace section until next ## header or EOF
        pattern = re.compile(r"(?s)^## Docking & Window Lifecycle.*?(?=^## |\Z)", re.MULTILINE)
        after = pattern.sub(new_block + "\n", before)
        write_text(arch_path, after)
        report.append("- architecture: section replaced")
    else:
        after = before.rstrip() + "\n\n" + new_block + "\n"
        write_text(arch_path, after)
        report.append("- architecture: section appended")


def write_docking_doc(dock_path: Path, report: list[str]) -> None:
    if dock_path.exists():
        bak = backup(dock_path)
        report.append(f"- backup: {bak}")

    lines = []
    lines.append("# Docking – Architektur & Persistenz")
    lines.append("")
    lines.append("Dieses Dokument beschreibt das Docking/Undocking der Read-Only Viewer (Pipeline, Log, Artefakte).")
    lines.append("")
    lines.append("## Begriffe")
    lines.append("- **Docked**: Tab im Notebook (kein Extra-Fenster).")
    lines.append("- **Undocked**: eigenes Toplevel-Fenster, verwaltet durch `module_docking.py`.")
    lines.append("")
    lines.append("## Ownership")
    lines.append("- Window-Lifecycle (erzeugen, schließen, persistieren, restoren) liegt ausschließlich in:")
    lines.append("  - `modules/module_docking.py`")
    lines.append("- Tab-Builder erzeugen Inhalte im Parent-Widget, aber keine Fenster.")
    lines.append("")
    lines.append("## Persistenz in ShrimpDev.ini")
    lines.append("Section: `[Docking]`")
    lines.append("")
    lines.append("Pro Key (z. B. `pipeline`, `log`, `runner_products`, `main`):")
    lines.append("- `<key>.open`   : `1` wenn undocked Fenster beim letzten Persist offen war")
    lines.append("- `<key>.docked` : `1` wenn docked (Tab), `0` wenn undocked")
    lines.append("- `<key>.geometry`: `WxH+X+Y`")
    lines.append("- `<key>.ts`     : Timestamp der letzten Persist")
    lines.append("")
    lines.append("## Restore-Regeln (verbindlich)")
    lines.append("1) Restore nur wenn `open=1` und `docked=0`")
    lines.append("2) Geometry bevorzugen: `<key>.geometry`")
    lines.append("3) Fallback: legacy `w/h/x/y`, falls `geometry` fehlt")
    lines.append("4) Offscreen-Guard: Offscreen Geometry wird verworfen; dann erst center/fallback")
    lines.append("")
    lines.append("## Anti-Pattern (nicht zulässig)")
    lines.append("- Nach Restore pauschal zentrieren (führt zu ständigem Zentrieren trotz gespeicherter Geo).")
    lines.append("- Tab-Builder bauen eigene `tk.Toplevel`-Fenster (führt zu doppeltem Window-Management).")
    lines.append("- Restore ignoriert `<key>.open` (öffnet geschlossene Fenster wieder).")
    lines.append("")
    write_text(dock_path, "\n".join(lines) + "\n")
    report.append("- docking doc: written")


def write_incident(post_path: Path, report: list[str]) -> None:
    post_path.parent.mkdir(parents=True, exist_ok=True)
    if post_path.exists():
        bak = backup(post_path)
        report.append(f"- backup: {bak}")

    lines = []
    lines.append("# Incident: Docking Restore Regression (R2379–R2395)")
    lines.append("")
    lines.append("- Date: 2025-12-19")
    lines.append("- Scope: Read-Only Viewer Docking (Pipeline/Log/Artefakte) + Main window geometry")
    lines.append("")
    lines.append("## Symptome")
    lines.append("- Nach Restart kamen Pipeline/Log/Artefakte wieder hoch, auch wenn vorher geschlossen.")
    lines.append("- Fenster wurden zentriert (statt gespeicherter Position).")
    lines.append("- Main-Fenster driftete leicht bei jedem Restart.")
    lines.append("")
    lines.append("## Root Cause")
    lines.append("- Restore-Pfad berücksichtigte `Docking.<key>.open` nicht strikt.")
    lines.append("- Restore verwendete bevorzugt legacy `w/h/x/y` oder erzeugte `restore_geo=None` → Center-Fallback.")
    lines.append("")
    lines.append("## Fix (R2395)")
    lines.append("- `restore_from_ini()` respektiert `open=1` und `docked=0`.")
    lines.append("- `<key>.geometry` (`WxH+X+Y`) wird priorisiert.")
    lines.append("- Fallback auf `w/h/x/y` nur wenn `geometry` fehlt.")
    lines.append("- Offscreen-Guard verhindert Restore außerhalb des sichtbaren Bereichs.")
    lines.append("")
    lines.append("## Verifikation")
    lines.append("- Geschlossene Fenster bleiben geschlossen nach Restart.")
    lines.append("- Offene Fenster kommen mit gespeicherter Geometry zurück (kein erzwungenes Centering).")
    lines.append("")
    write_text(post_path, "\n".join(lines) + "\n")
    report.append("- incident doc: written")


def main() -> int:
    rep = []
    rep.append(f"# Report {RID} – Docs Update (Docking)")
    rep.append("")
    rep.append(f"- Timestamp: {ts()}")
    rep.append(f"- Root: `{ROOT}`")
    rep.append("")

    DOCS.mkdir(parents=True, exist_ok=True)
    INC.mkdir(parents=True, exist_ok=True)

    ensure_architecture_section(ARCH, rep)
    write_docking_doc(DOCK, rep)
    write_incident(POST, rep)

    # hashes
    for p in (ARCH, DOCK, POST):
        if p.exists():
            rep.append(f"- sha256 {p}: `{sha256(p)}`")

    rp = DOCS / f"Report_{RID}_DocsUpdate_{stamp()}.md"
    write_text(rp, "\n".join(rep) + "\n")
    print(f"[{RID}] OK: Report {rp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
