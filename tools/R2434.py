import shutil
from datetime import datetime
from pathlib import Path

RID = "R2434"


def ts() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def now_human() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n")


def write(p: Path, s: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding="utf-8", newline="\n")


def backup(p: Path, archiv: Path) -> Path | None:
    if not p.exists():
        return None
    archiv.mkdir(parents=True, exist_ok=True)
    b = archiv / f"{p.name}.{RID}_{ts()}.bak"
    shutil.copy2(p, b)
    return b


def append_keep(root: Path, archiv: Path, report: list[str]) -> None:
    keep = root / "registry" / "tools_keep.txt"
    if not keep.exists():
        report.append("INFO: registry/tools_keep.txt not found (skip).")
        return
    txt = read(keep)
    items = [ln.strip() for ln in txt.splitlines() if ln.strip() and not ln.strip().startswith("#")]
    if "R2434" in items:
        report.append("NO-OP: R2434 already in tools_keep.txt")
        return
    bk = backup(keep, archiv)
    write(keep, txt.rstrip() + "\nR2434\n")
    report.append(f"OK: appended R2434 to tools_keep.txt (backup={bk})")


def insert_under_heading(txt: str, heading: str, block: str) -> tuple[str, bool]:
    idx = txt.find(heading)
    if idx < 0:
        return txt, False
    head_end = txt.find("\n", idx)
    if head_end < 0:
        head_end = len(txt) - 1
    insert_at = head_end + 1
    return txt[:insert_at] + block + txt[insert_at:], True


def main() -> int:
    tools_dir = Path(__file__).resolve().parent
    root = tools_dir.parent
    docs = root / "docs"
    archiv = root / "_Archiv"
    pipe = docs / "PIPELINE.md"

    report = [
        f"[{RID}] PIPELINE: GitHub update urgency indicator (P1)",
        f"Time: {now_human()}",
        f"Root: {root}",
        f"Pipeline: {pipe}",
        "",
    ]

    if not pipe.exists():
        rp = docs / f"Report_{RID}_Pipeline_{ts()}.md"
        write(rp, "\n".join(report + ["ERROR: docs/PIPELINE.md not found"]) + "\n")
        print(f"[{RID}] ERROR: Report {rp}")
        return 2

    txt = read(pipe)

    # dedupe
    dedupe_key = "GitHub-Update-Indikator"
    if dedupe_key in txt or "update urgency indicator" in txt.lower():
        rp = docs / f"Report_{RID}_Pipeline_{ts()}.md"
        write(rp, "\n".join(report + ["NO-OP: entry already present"]) + "\n")
        print(f"[{RID}] OK (NO-OP): Report {rp}")
        return 0

    block = (
        "\n"
        "- [ ] (P1) GitHub-Update-Indikator an Push-Buttons (Private/Public)\n"
        "  - Visual: kleiner Wimpel/Badge/Punkt am Button; sehr schwach rosa -> zunehmend rot je nach Dringlichkeit\n"
        "  - Dringlichkeit (Heuristik): Zeit seit letztem Push ODER Anzahl unpushed Commits (oder kombiniert)\n"
        "  - Datenquelle: git log origin/main..HEAD (unpushed count) + Zeitstempel aus letztem Push-Report/Registry\n"
        "  - Polling: UI after()-Loop (30–60s), respektiert Busy-Flag (pausiert während Runner läuft)\n"
        "  - Reset: nach erfolgreichem Push zurück auf „frisch“\n"
        "  - Architektur: READ-ONLY Status -> registry/push_status.json; UI rendert nur (keine Git-Logik im UI)\n"
    )

    b = backup(pipe, archiv)

    # Prefer to place under a relevant section; fall back gracefully.
    placed = False
    for heading in ["## Intake", "## Git", "## GitHub", "## Automatisierung", "## Tooling"]:
        txt2, ok = insert_under_heading(txt, heading, block)
        if ok:
            txt = txt2
            placed = True
            report.append(f"OK: inserted under {heading}")
            break

    if not placed:
        # fallback: append near top (after first H1 if present)
        m = txt.find("\n")
        insert_at = m + 1 if m >= 0 else 0
        txt = txt[:insert_at] + block + txt[insert_at:]
        report.append("OK: inserted near top (no matching heading found)")

    write(pipe, txt)

    # keep list
    append_keep(root, archiv, report)

    rp = docs / f"Report_{RID}_Pipeline_{ts()}.md"
    write(rp, "\n".join(report + [f"Backup: {b}"]) + "\n")
    print(f"[{RID}] OK: Report {rp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
