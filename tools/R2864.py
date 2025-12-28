# -*- coding: utf-8 -*-
"""
R2864 – SAFE PATCH
Fix UnboundLocalError in modules/ui_toolbar.py caused by R2863 insertion:
- Replace service_frame usage with frame_toolbar_right as robust parent.
- Only touches the R2863-marked block.
- Backup + report.
"""

from __future__ import annotations
import shutil
from datetime import datetime
from pathlib import Path
from typing import List

RUNNER_ID = "R2864"
EXIT_FAIL = 11

MARKER_START = "# R2863: Public export sync button"
MARKER_END = "btn_export_public.pack(side='right', padx=(6, 0))"


def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def backup(repo: Path, target: Path) -> Path:
    arch = repo / "_Archiv"
    ensure_dir(arch)
    bak = arch / f"{target.name}.{RUNNER_ID}_{now_stamp()}.bak"
    shutil.copy2(target, bak)
    return bak


def write_report(repo: Path, lines: List[str]) -> Path:
    rp = repo / "Reports"
    ensure_dir(rp)
    out = rp / f"Report_{RUNNER_ID}_{now_stamp()}.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8", errors="replace")
    return out


def main(root_arg: str) -> int:
    repo = Path(root_arg).resolve()
    report: List[str] = []
    report.append(f"# {RUNNER_ID} SAFE PATCH: Fix Export Public button parent")
    report.append(f"- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"- Root: `{repo}`")
    report.append("")

    p = repo / "modules" / "ui_toolbar.py"
    if not p.exists():
        report.append(f"ERROR: missing `{p}`")
        rp = write_report(repo, report)
        print(f"[{RUNNER_ID}] FAIL -> {rp}")
        return EXIT_FAIL

    txt = p.read_text(encoding="utf-8", errors="replace")

    sidx = txt.find(MARKER_START)
    eidx = txt.find(MARKER_END)
    if sidx == -1 or eidx == -1 or eidx < sidx:
        report.append("ERROR: R2863 block markers not found (cannot safely patch).")
        rp = write_report(repo, report)
        print(f"[{RUNNER_ID}] FAIL -> {rp}")
        return EXIT_FAIL

    # extend end to include line end
    eidx = txt.find("\n", eidx)
    if eidx == -1:
        eidx = len(txt)

    block = txt[sidx:eidx]
    if "Frame(service_frame)" not in block:
        report.append("- OK: No 'Frame(service_frame)' in R2863 block (already fixed?)")
        rp = write_report(repo, report)
        print(f"[{RUNNER_ID}] OK -> {rp}")
        return 0

    bak = backup(repo, p)
    report.append(f"- Backup: `{bak}`")

    fixed_block = block.replace("Frame(service_frame)", "Frame(frame_toolbar_right)")
    new_txt = txt[:sidx] + fixed_block + txt[eidx:]

    p.write_text(new_txt, encoding="utf-8", errors="replace")
    report.append("- OK: Replaced service_frame -> frame_toolbar_right in R2863 block")

    rp = write_report(repo, report)
    print(f"[{RUNNER_ID}] OK -> {rp}")
    return 0


if __name__ == "__main__":
    import sys
    root = sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).resolve().parents[1])
    raise SystemExit(main(root))
