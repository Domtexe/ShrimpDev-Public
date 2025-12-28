# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from datetime import datetime
from typing import List
import shutil

RUNNER_ID = "R2852"

def now() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)

def backup(repo: Path, target: Path) -> Path:
    arch = repo / "_Archiv"
    ensure_dir(arch)
    bak = arch / f"{target.name}.{RUNNER_ID}_{now()}.bak"
    shutil.copy2(target, bak)
    return bak

def write_report(repo: Path, lines: List[str]) -> Path:
    rp = repo / "Reports"
    ensure_dir(rp)
    out = rp / f"Report_{RUNNER_ID}_{now()}.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8", errors="replace")
    return out

def main() -> int:
    repo = Path(__file__).resolve().parent.parent
    pipe = repo / "docs" / "Master" / "Pipeline_Notes.md"
    lines: List[str] = []
    lines.append(f"# {RUNNER_ID} PATCH: Pipeline_Notes finalize (CI + stability)")
    lines.append(f"- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")

    if not pipe.exists():
        lines.append(f"ERROR: `{pipe}` not found")
        rp = write_report(repo, lines)
        print(f"[{RUNNER_ID}] FAIL -> {rp}")
        return 11

    bak = backup(repo, pipe)
    txt = pipe.read_text(encoding="utf-8", errors="replace")

    marker = "CI repariert & gehärtet (R2850/R2851)"
    if marker in txt:
        lines.append("OK: Marker already present (no change).")
        rp = write_report(repo, lines)
        print(f"[{RUNNER_ID}] OK -> {rp}")
        return 0

    entry = (
        "\n\n"
        f"### ✅ Stabilitäts-Update ({datetime.now().strftime('%Y-%m-%d')})\n"
        f"- CI repariert & gehärtet (R2850/R2851)\n"
        f"- Push-Buttons konsistent (Wrapper-Gating R2837)\n"
        f"- Purge schützt Wrapper zuverlässig (Whitelist-Hardening R2839)\n"
    )

    pipe.write_text(txt.rstrip() + entry, encoding="utf-8", errors="replace")
    lines.append(f"OK: `{pipe}` updated (backup: `{bak}`)")
    rp = write_report(repo, lines)
    print(f"[{RUNNER_ID}] OK -> {rp}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
