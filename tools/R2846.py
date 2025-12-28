# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from datetime import datetime
from typing import List
import shutil


RUNNER_ID = "R2846"


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
    report.append(f"# {RUNNER_ID} PATCH: Update docs/Master/MasterRules.md")
    report.append(f"- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"- Root: `{repo}`")
    report.append("")

    mr = repo / "docs" / "Master" / "MasterRules.md"
    if not mr.exists():
        report.append(f"ERROR: target not found: `{mr}`")
        rp = write_report(repo, report)
        print(f"[{RUNNER_ID}] FAIL -> {rp}")
        return 11

    bak = backup(repo, mr)
    report.append(f"- Target: `{mr}`")
    report.append(f"- Backup: `{bak}`")
    report.append("")

    txt = mr.read_text(encoding="utf-8", errors="replace")

    title = "## 🔁 Patch- & Rollback-Pflicht (verbindlich)"
    if title in txt:
        report.append("OK: Section already present (no change).")
        rp = write_report(repo, report)
        print(f"[{RUNNER_ID}] OK -> {rp}")
        return 0

    block = (
        "\n\n"
        "## 🔁 Patch- & Rollback-Pflicht (verbindlich)\n\n"
        "- Jeder PATCH-Runner **muss** vor Änderungen ein Backup erstellen.\n"
        "- Schlägt ein Patch fehl (Syntax, Compile, Runtime), **ist automatisch ein Rollback auszuführen**.\n"
        "- Ein fehlerhafter Zustand darf **niemals** im Arbeitsstand verbleiben.\n\n"
        "## 🔘 UI-Regel: Push-Buttons\n\n"
        "Push-Buttons dürfen **nur aktiv** sein, wenn **alle** Bedingungen erfüllt sind:\n"
        "- gültiger Repo-Root (private/public)\n"
        "- zugehöriger Wrapper existiert physisch:\n"
        "  - Private Push → `tools/R2691.cmd`\n"
        "  - Public Push → `tools/R2692.cmd`\n\n"
        "Fehlt ein Wrapper, **muss** der Button deaktiviert sein.\n\n"
        "## 🧹 Purge-Regel: Kritische Runner\n\n"
        "- Kritische Runner sind über `registry/runner_whitelist.txt` zu schützen.\n"
        "- Der Schutz ist **stem-basiert** (`R####`) und unabhängig von `.cmd` / `.py`.\n"
        "- Purge darf **keinen** Whitelist-Runner archivieren.\n"
        "\n"
    )

    mr.write_text(txt.rstrip() + block, encoding="utf-8", errors="replace")
    report.append("SUCCESS: Rules appended.")
    rp = write_report(repo, report)
    print(f"[{RUNNER_ID}] OK -> {rp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
