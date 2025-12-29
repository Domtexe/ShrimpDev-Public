# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from datetime import datetime
from typing import List
import shutil


RUNNER_ID = "R2848"


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
    report.append(f"# {RUNNER_ID} PATCH: Write docs/Guides/Push_Purge_System.md")
    report.append(f"- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")

    doc = repo / "docs" / "Guides" / "Push_Purge_System.md"
    ensure_dir(doc.parent)

    if doc.exists():
        bak = backup(repo, doc)
        report.append(f"- Backup: `{bak}`")
    report.append(f"- Target: `{doc}`")
    report.append("")

    content = f"""# Push- & Purge-System (ShrimpDev)

Stand: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Registry (Source of Truth)
- `registry/private_repo_root.txt`
- `registry/public_export_root.txt`
- `registry/runner_whitelist.txt`
- `registry/tools_keep.txt`

## Push-Buttons (UI)
Push-Buttons sind nur aktiv, wenn:
1) Repo-Root gültig ist (private/public), **und**
2) Wrapper-Datei existiert:
   - Private Push → `tools/R2691.cmd`
   - Public Push → `tools/R2692.cmd`

Ziel: keine aktivierten Buttons, die beim Klick in „Runner-Datei nicht gefunden“ laufen.

## Purge (Tools)
- Purge Scan: `R2218`
- Purge Apply: `R2224`
- Schutz muss stem-basiert wirken (`R####`), unabhängig von `.cmd` / `.py`.

## Fix-Historie (relevant)
- R2837: Wrapper-Gating für Push-Buttons
- R2839: Whitelist-Hardening (stem + cmd/py + tools\\… Varianten)
  → verhindert, dass Wrapper/Runner trotz Whitelist archiviert werden.

## Checks / Troubleshooting
- Buttons aus:
  - existieren `tools/R2691.cmd` und `tools/R2692.cmd`?
  - sind `registry/*_repo_root.txt` korrekt?
- Runner verschwinden nach Purge:
  - Purge Scan Report prüfen: betroffene Runner müssen als **KEEP** erscheinen
"""
    doc.write_text(content, encoding="utf-8", errors="replace")

    report.append("SUCCESS: Guide written.")
    rp = write_report(repo, report)
    print(f"[{RUNNER_ID}] OK -> {rp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
