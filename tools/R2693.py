from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path

RID = "R2693"


def stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def run(cmd: list[str], cwd: Path) -> tuple[int, str]:
    cp = subprocess.run(cmd, cwd=str(cwd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return cp.returncode, cp.stdout


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    a = ap.parse_args()

    root = Path(a.root).resolve()
    reports = root / "Reports"
    reports.mkdir(parents=True, exist_ok=True)
    rep = reports / f"Report_{RID}_{stamp()}.md"

    lines: list[str] = []
    lines.append(f"[{RID}] PUSH BOTH (repo-only)")
    lines.append(f"Time: {datetime.now().isoformat(timespec='seconds')}")
    lines.append(f"Root: {root}")
    lines.append("")

    # Step 1: Private
    lines.append("--- Step 1/2: Private (R2691.py) ---")
    rc1, out1 = run([sys.executable, str(root / "tools" / "R2691.py"), "--root", str(root)], cwd=root)
    lines.append(out1.rstrip())
    lines.append(f"Exitcode: {rc1}")
    lines.append("")
    if rc1 != 0:
        lines.append("STOP: Private failed; skipping public.")
        rep.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
        print(f"[{RID}] ERROR: Report: {rep}")
        return rc1

    # Step 2: Public
    lines.append("--- Step 2/2: Public (R2692.py) ---")
    rc2, out2 = run([sys.executable, str(root / "tools" / "R2692.py"), "--root", str(root)], cwd=root)
    lines.append(out2.rstrip())
    lines.append(f"Exitcode: {rc2}")

    rep.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    if rc2 == 0:
        print(f"[{RID}] OK: Report: {rep}")
        return 0
    print(f"[{RID}] ERROR: Report: {rep}")
    return rc2


if __name__ == "__main__":
    raise SystemExit(main())
