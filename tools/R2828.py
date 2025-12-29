# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from datetime import datetime
from typing import List, Optional


RUNNER_ID = "R2828"


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


def read_reg_path(repo: Path, name: str) -> Optional[Path]:
    fp = repo / "registry" / name
    if not fp.exists():
        return None
    txt = fp.read_text(encoding="utf-8", errors="replace").strip().strip('"')
    if not txt:
        return None
    return Path(txt)


def check_repo(p: Optional[Path]) -> List[str]:
    if p is None:
        return ["- Path: (missing in registry)"]
    lines = [f"- Path: `{p}`"]
    lines.append(f"- Exists: **{p.exists()}**")
    git_dir = p / ".git"
    lines.append(f"- Has .git: **{git_dir.exists()}**")
    return lines


def main() -> int:
    repo = repo_root()
    report: List[str] = []
    report.append(f"# {RUNNER_ID} READ-ONLY: Repo Roots Check")
    report.append(f"- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"- Root: `{repo}`")
    report.append("")

    priv = read_reg_path(repo, "private_repo_root.txt")
    pub = read_reg_path(repo, "public_export_root.txt")

    report.append("## Private Root (registry/private_repo_root.txt)")
    report.append("")
    report += check_repo(priv)
    report.append("")

    report.append("## Public Root (registry/public_export_root.txt)")
    report.append("")
    report += check_repo(pub)
    report.append("")

    report.append("## Interpretation")
    report.append("")
    report.append("- If Private exists but Has .git = False: registry points to wrong folder.")
    report.append("- If Public exists but Has .git = False: public folder is not a git repo (needs clone/init).")
    report.append("- If registry files are missing: UI resolution likely returns empty -> buttons disabled.")
    report.append("")

    rp = write_report(repo, report)
    print(f"[{RUNNER_ID}] OK -> {rp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
