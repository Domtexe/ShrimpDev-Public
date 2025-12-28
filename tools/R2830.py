# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from datetime import datetime
from typing import List, Tuple


RUNNER_ID = "R2830"


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


def _snip(lines: List[str], center: int, radius: int = 3) -> List[Tuple[int, str]]:
    a = max(0, center - radius - 1)
    b = min(len(lines), center + radius)
    out = []
    for i in range(a, b):
        out.append((i + 1, lines[i].rstrip("\n")))
    return out


def main() -> int:
    repo = repo_root()
    ui = repo / "modules" / "ui_toolbar.py"

    report: List[str] = []
    report.append(f"# {RUNNER_ID} READ-ONLY: Locate _resolve_repo_path and workspace usage")
    report.append(f"- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"- Root: `{repo}`")
    report.append("")

    if not ui.exists():
        report.append("ERROR: modules/ui_toolbar.py not found")
        write_report(repo, report)
        return 11

    lines = ui.read_text(encoding="utf-8", errors="replace").splitlines()

    needles = [
        "def _resolve_repo_path",
        "private_repo_root.txt",
        "public_export_root.txt",
        "workspace",
        "os.getcwd",
        "cwd",
    ]

    hits = []
    for idx, line in enumerate(lines, start=1):
        for n in needles:
            if n in line:
                hits.append((idx, n))

    report.append("## Hits (line -> needle)")
    report.append("")
    if not hits:
        report.append("- No hits found (unexpected)")
    else:
        for (lineno, needle) in hits:
            report.append(f"- L{lineno}: `{needle}`")

    report.append("")
    report.append("## Context: def _resolve_repo_path")
    report.append("")

    ctx_found = False
    for (lineno, needle) in hits:
        if needle == "def _resolve_repo_path":
            ctx_found = True
            report.append(f"### Around L{lineno}")
            report.append("")
            for (ln, txt) in _snip(lines, lineno, radius=10):
                report.append(f"- L{ln}: {txt}")
            report.append("")

    if not ctx_found:
        report.append("- Not found. That explains R2829 failing: function name/signature differs.")

    report.append("")
    report.append("## Next Step")
    report.append("")
    report.append("- Use the exact signature/body found above to build a safe PATCH runner (single block replace).")
    report.append("- No assumptions, no blind replace.")
    report.append("")

    rp = write_report(repo, report)
    print(f"[{RUNNER_ID}] OK -> {rp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
