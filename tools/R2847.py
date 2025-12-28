# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from datetime import datetime
from typing import List
import shutil


RUNNER_ID = "R2847"


def now() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def write_report(repo: Path, lines: List[str]) -> Path:
    rp = repo / "Reports"
    ensure_dir(rp)
    out = rp / f"Report_{RUNNER_ID}_{now()}.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8", errors="replace")
    return out


def backup(repo: Path, target: Path) -> Path:
    arch = repo / "_Archiv"
    ensure_dir(arch)
    bak = arch / f"{target.name}.{RUNNER_ID}_{now()}.bak"
    shutil.copy2(target, bak)
    return bak


def main() -> int:
    repo = repo_root()
    report: List[str] = []
    report.append(f"# {RUNNER_ID} PATCH: Update docs/Master/Pipeline_Notes.md")
    report.append(f"- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")

    pipe = repo / "docs" / "Master" / "Pipeline_Notes.md"
    if not pipe.exists():
        report.append(f"ERROR: target not found: `{pipe}`")
        rp = write_report(repo, report)
        print(f"[{RUNNER_ID}] FAIL -> {rp}")
        return 11

    bak = backup(repo, pipe)
    report.append(f"- Target: `{pipe}`")
    report.append(f"- Backup: `{bak}`")
    report.append("")

    txt = pipe.read_text(encoding="utf-8", errors="replace")

    marker = "Repo-Roots, Push-Buttons & Purge-Stabilisierung – DONE"
    if marker in txt:
        report.append("OK: Entry already present (no change).")
        rp = write_report(repo, report)
        print(f"[{RUNNER_ID}] OK -> {rp}")
        return 0

    entry = (
        "\n\n"
        f"## ✅ Repo-Roots, Push-Buttons & Purge-Stabilisierung – DONE ({datetime.now().strftime('%Y-%m-%d')})\n\n"
        "**Diagnose:**\n"
        "- R2834 (AST Locator)\n"
        "- R2836 (Runtime Trace)\n"
        "- R2838 (Whitelist Analyse)\n\n"
        "**Fixes:**\n"
        "- R2837 – Push-Buttons nur bei vorhandenen Wrappern aktiv\n"
        "- R2839 – Whitelist-Hardening (stem + cmd/py + tools\\… Varianten)\n\n"
        "**Ergebnis:**\n"
        "- Push-Buttons konsistent (Repo-root + Wrapper gating)\n"
        "- Wrapper werden nicht mehr purged (Whitelist robust)\n"
        "- Purge Scan zeigt KEEP/ARCHIVE korrekt\n"
        "\n"
    )

    pipe.write_text(txt.rstrip() + entry, encoding="utf-8", errors="replace")
    report.append("SUCCESS: Pipeline note appended.")
    rp = write_report(repo, report)
    print(f"[{RUNNER_ID}] OK -> {rp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
