# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from datetime import datetime
from typing import List, Optional
import subprocess


RUNNER_ID = "R2832"


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


def read_reg(repo: Path, name: str) -> Optional[Path]:
    fp = repo / "registry" / name
    if not fp.exists():
        return None
    txt = fp.read_text(encoding="utf-8", errors="replace").strip()
    if not txt:
        return None
    return Path(txt)


def run(cmd: List[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        shell=False,
    )


def main() -> int:
    repo = repo_root()
    report: List[str] = []

    report.append(f"# {RUNNER_ID} Init Public Repo")
    report.append(f"- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")

    pub = read_reg(repo, "public_export_root.txt")
    if pub is None:
        report.append("ERROR: public_export_root.txt missing")
        write_report(repo, report)
        return 11

    report.append(f"- Public path: `{pub}`")
    ensure_dir(pub)

    git_dir = pub / ".git"
    if git_dir.exists():
        report.append("- Public repo already initialized (.git exists)")
        write_report(repo, report)
        print(f"[{RUNNER_ID}] OK (already initialized)")
        return 0

    # git init
    report.append("## git init")
    cp = run(["git", "init"], cwd=pub)
    report.append(f"- returncode: {cp.returncode}")
    if cp.stdout:
        report.append("### stdout")
        report.append(cp.stdout.strip())
    if cp.stderr:
        report.append("### stderr")
        report.append(cp.stderr.strip())

    if cp.returncode != 0:
        write_report(repo, report)
        return 11

    report.append("")
    report.append("SUCCESS: Public repo initialized")
    rp = write_report(repo, report)
    print(f"[{RUNNER_ID}] OK -> {rp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
