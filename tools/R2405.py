from __future__ import annotations

from pathlib import Path
from datetime import datetime
import hashlib

RID = "R2405"
ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
PIPE = DOCS / "PIPELINE.md"
ARCHIV = ROOT / "_Archiv"

def ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def sha256_bytes(b: bytes) -> str:
    h = hashlib.sha256(); h.update(b); return h.hexdigest()

def backup(path: Path) -> Path:
    ARCHIV.mkdir(parents=True, exist_ok=True)
    bak = ARCHIV / f"{path.name}.{RID}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak"
    bak.write_bytes(path.read_bytes())
    return bak

def normalize(s: str) -> str:
    return " ".join(s.lower().strip().split())

def contains_task(lines: list[str], needle: str) -> bool:
    n = normalize(needle)
    for ln in lines:
        if n in normalize(ln):
            return True
    return False

def ensure_section(lines: list[str], header: str) -> tuple[list[str], int]:
    """
    Sichert eine Section '## <header>' am Ende und gibt Insert-Index zurück
    (direkt nach der Header-Zeile).
    """
    hdr = f"## {header}"
    for i, ln in enumerate(lines):
        if ln.strip() == hdr:
            # insert after header (skip possible blank line)
            j = i + 1
            while j < len(lines) and lines[j].strip() == "":
                j += 1
            return lines, j

    if lines and lines[-1].strip() != "":
        lines.append("")
    lines.append(hdr)
    lines.append("")
    return lines, len(lines)

def insert_tasks(lines: list[str], section: str, tasks: list[str]) -> tuple[list[str], list[str]]:
    lines, idx = ensure_section(lines, section)
    added = []
    for t in tasks:
        if not contains_task(lines, t):
            lines.insert(idx, f"- [ ] {t}")
            idx += 1
            added.append(t)
    # ensure blank line after inserted block for readability
    if added:
        if idx < len(lines) and lines[idx].strip() != "":
            lines.insert(idx, "")
    return lines, added

def main() -> int:
    report_lines = []
    report_lines.append(f"# Report {RID} – Pipeline Update (Auto)")
    report_lines.append("")
    report_lines.append(f"- Timestamp: {ts()}")
    report_lines.append(f"- Root: `{ROOT}`")
    report_lines.append(f"- Target: `{PIPE}`")
    report_lines.append("")

    if not PIPE.exists():
        DOCS.mkdir(parents=True, exist_ok=True)
        PIPE.write_text("# PIPELINE\n\n", encoding="utf-8")

    raw = PIPE.read_bytes()
    before_sha = sha256_bytes(raw)
    text = raw.decode("utf-8", errors="replace")
    lines = text.splitlines()

    bak = backup(PIPE)

    # ---- Aufgaben, die wir sicher offen/ablesbar haben (außer Pipeline selbst) ----
    # 1) Artefakte: Button "Quelle kopieren" (Dateiinhalt in Clipboard, nicht Pfad)
    artefakte_tasks = [
        "Artefakte/Popup „intern anzeigen“: Button „Quelle kopieren“ (Datei-INHALT in Zwischenablage, nicht Pfad).",
    ]

    # 2) INI SingleWriter: Abschluss-Verify
    ini_tasks = [
        "SingleWriter: Finaler Audit – keine direkten ShrimpDev.ini Overwrites mehr (config_loader/config_mgr/ui_toolbar etc.).",
        "SingleWriter: optional Guard-Runner bauen, der direkte INI-Writes in Zukunft als Pipeline-Warnung meldet.",
    ]

    # 3) Docking/Geometry Drift: final fix based on R2404 GeometrySetters
    docking_tasks = [
        "Docking/Geometry: Drift & Centering final fix (R2404 auswerten, dann minimaler Patch nur am echten Post-Restore Setter).",
        "Docking/Geometry: kurzer Smoke-Test-Runner (Start/Restart, Fensterpositionen vergleichen, Report).",
    ]

    # 4) Doku/Architektur
    docs_tasks = [
        "Doku/Architektur: Docking-stabil + SingleWriter-Delegation (R2402/R2403) sauber dokumentieren (Architektur + Troubleshooting).",
        "Doku: Report-Index/Changelog-Eintrag für DockingStable Snapshot (R2398) + relevante Reports verlinken.",
    ]

    added_total = []

    lines, a1 = insert_tasks(lines, "GUI / Artefakte", artefakte_tasks); added_total += a1
    lines, a2 = insert_tasks(lines, "Config / INI / SingleWriter", ini_tasks); added_total += a2
    lines, a3 = insert_tasks(lines, "Docking / Fenster / Geometry", docking_tasks); added_total += a3
    lines, a4 = insert_tasks(lines, "Docs / Architektur", docs_tasks); added_total += a4

    new_text = "\n".join(lines) + "\n"
    PIPE.write_text(new_text, encoding="utf-8")

    after_sha = sha256_bytes(PIPE.read_bytes())

    report_lines.append(f"- backup: `{bak}`")
    report_lines.append(f"- sha256 before: `{before_sha}`")
    report_lines.append(f"- sha256 after: `{after_sha}`")
    report_lines.append("")
    report_lines.append("## Added tasks")
    if added_total:
        for t in added_total:
            report_lines.append(f"- {t}")
    else:
        report_lines.append("- (none) – all tasks already present")

    out = DOCS / f"Report_{RID}_PipelineUpdate_{stamp()}.md"
    out.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    print(f"[{RID}] OK: Pipeline updated: {PIPE} | Report {out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
